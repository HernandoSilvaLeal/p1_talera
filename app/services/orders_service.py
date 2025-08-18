from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from bson import ObjectId, errors

from app.domain import errors as domain_errors
from app.domain.models import OrderIn, OrderOut, StatusUpdate
from app.infra import metrics
from app.infra.mongo import db
from app.utils import idempotency as idem

ALLOWED_TRANSITIONS = {
    "CREATED": {"PAID", "CANCELLED"},
    "PAID": {"FULFILLED", "CANCELLED"},
    "FULFILLED": set(),
    "CANCELLED": set(),
}

# TODO: Migrar a BSON Decimal128 en producción (Decimal -> Decimal128 al persistir; Decimal128 -> str/Decimal al leer).
def _persistable_doc_from_payload(payload: OrderIn) -> dict:
    """Mongo-safe: Decimal -> str en items[].price y amount; timestamps en UTC; version inicial."""
    now = datetime.now(timezone.utc)
    items = []
    amount = Decimal("0")
    for it in payload.items:
        price = it.price if isinstance(it.price, Decimal) else Decimal(str(it.price))
        items.append({"sku": it.sku, "qty": it.qty, "price": str(price)})
        amount += price * it.qty
    return {
        "customer_id": payload.customer_id,
        "currency": payload.currency,
        "items": items,
        "status": "CREATED",
        "version": 1,
        "amount": str(amount),
        "created_at": now,
        "updated_at": now,
    }

def _order_out_from_doc(doc: dict) -> OrderOut:
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    # Convert amount and item prices back to Decimal
    if "amount" in doc:
        doc["amount"] = Decimal(doc["amount"])
    for item in doc.get("items", []):
        if "price" in item:
            item["price"] = Decimal(item["price"])
    return OrderOut.model_validate(doc)

async def create_order(payload: OrderIn, idempotency_key: Optional[str]) -> OrderOut:
    # Idempotencia: si existe, devolvemos lo guardado
    cached = await idem.get_cached_result(idempotency_key)
    if cached:
        # Reconstruimos OrderOut desde el resultado cacheado
        return OrderOut.model_validate(cached["result"])

    document = _persistable_doc_from_payload(payload)
    res = await db()["orders"].insert_one(document)
    created = await db()["orders"].find_one({"_id": res.inserted_id})

    # Increment metric for created orders
    metrics.orders_created_total.inc()

    order = _order_out_from_doc(created)
    
    if idempotency_key:
        # Status code and headers are handled by the route/exception handler layer
        await idem.save_result(idempotency_key, result=order.model_dump(), status_code=201)
    return order

async def get_order(order_id: str) -> OrderOut:
    try:
        oid = ObjectId(order_id)
    except errors.InvalidId as e:
        raise domain_errors.NotFound("order not found") from e

    doc = await db()["orders"].find_one({"_id": oid})
    if not doc:
        raise domain_errors.NotFound("order not found")
    return _order_out_from_doc(doc)

async def update_status(order_id: str, payload: StatusUpdate, expected_version: int) -> OrderOut:
    try:
        oid = ObjectId(order_id)
    except errors.InvalidId as e:
        raise domain_errors.NotFound("order not found") from e

    current = await db()["orders"].find_one({"_id": oid})
    if not current:
        raise domain_errors.NotFound("order not found")

    cur_status: str = current["status"]
    new_status: str = payload.status

    # Regla de dominio (simplificada): validar transición
    allowed = ALLOWED_TRANSITIONS.get(cur_status, set())
    if new_status not in allowed:
        raise domain_errors.InvalidTransition(f"invalid transition from {cur_status} to {new_status}")

    # Control optimista de concurrencia por versión
    result = await db()["orders"].find_one_and_update(
        {"_id": oid, "version": expected_version},
        {"$set": {"status": new_status, "updated_at": datetime.now(timezone.utc)}, "$inc": {"version": 1}},
        return_document=True, # type: ignore
    )
    if not result:
        # No coincidió la versión
        raise domain_errors.Conflict("version mismatch")

    # Increment metric for state transitions
    metrics.state_transitions_total.labels(from_status=cur_status, to_status=new_status).inc()

    return _order_out_from_doc(result)
