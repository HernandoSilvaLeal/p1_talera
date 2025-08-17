from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from app.domain import errors
from app.domain.entities import can_transition
from app.domain.models import OrderIn, OrderOut, OrderStatus
from app.infra.mongo import db
from app.utils.idempotency import get_existing_order_id, record_idempotency


def _doc_to_order_out(doc: dict) -> OrderOut:
    return OrderOut(
        id=doc["_id"],
        status=doc["status"],
        amount=Decimal(str(doc["amount"])),
        currency=doc["currency"],
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
        version=doc["version"],
    )


async def get_order(order_id: str) -> OrderOut | None:
    doc = await db().get_collection("orders").find_one({"_id": order_id})
    return _doc_to_order_out(doc) if doc else None


async def create_order(payload: OrderIn, idempotency_key: str | None) -> OrderOut:
    # Idempotency: short path if already created
    if idempotency_key:
        existing_id = await get_existing_order_id(idempotency_key)
        if existing_id:
            existing = await get_order(existing_id)
            if existing:
                return existing

    amount = sum(Decimal(str(it.price)) * it.qty for it in payload.items)
    now = datetime.utcnow()
    order_id = str(uuid.uuid4())

    doc = {
        "_id": order_id,
        "status": "CREATED",
        "amount": str(amount),  # store as string to avoid float issues
        "currency": payload.currency,
        "customer_id": payload.customer_id,
        "items": [i.model_dump() for i in payload.items],
        "created_at": now,
        "updated_at": now,
        "version": 1,
    }
    await db().get_collection("orders").insert_one(doc)

    if idempotency_key:
        await record_idempotency(idempotency_key, order_id)

    return _doc_to_order_out(doc)


async def update_status(order_id: str, new_status: OrderStatus, expected_version: int) -> OrderOut:
    orders = db().get_collection("orders")
    current = await orders.find_one({"_id": order_id})
    if not current:
        raise errors.NotFound("order not found")

    src = current["status"]
    if not can_transition(src, new_status):
        raise errors.InvalidTransition(f"cannot transition {src} -> {new_status}")

    # optimistic locking using version
    res = await orders.update_one(
        {"_id": order_id, "version": expected_version},
        {
            "$set": {
                "status": new_status,
                "updated_at": datetime.utcnow(),
            },
            "$inc": {"version": 1},
        },
    )
    if res.matched_count == 0:
        raise errors.Conflict("version mismatch")

    updated = await orders.find_one({"_id": order_id})
    return _doc_to_order_out(updated)
