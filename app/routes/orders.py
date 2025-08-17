from fastapi import APIRouter, Header, HTTPException, Response, status

from app.domain import errors
from app.domain.models import OrderIn, OrderOut, StatusUpdate
from app.services.orders_service import create_order, get_order, update_status

router = APIRouter(prefix="/orders", tags=["orders"])

IDEMPOTENCY_HEADER = "Idempotency-Key"
IF_MATCH_HEADER = "If-Match"


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order_endpoint(
    payload: OrderIn,
    response: Response,
    idempotency_key: str | None = Header(default=None, alias=IDEMPOTENCY_HEADER),
):
    try:
        order = await create_order(payload, idempotency_key)
        response.headers["Location"] = f"/orders/{order.id}"
        return order
    except Exception as e:
        # B904: Chaining the exception preserves the full stack trace for better debugging.
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.get("/{order_id}", response_model=OrderOut)
async def get_order_endpoint(order_id: str):
    order = await get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    return order


@router.patch("/{order_id}", response_model=OrderOut)
async def update_status_endpoint(
    order_id: str,
    payload: StatusUpdate,
    if_match: str | None = Header(default=None, alias=IF_MATCH_HEADER),
):
    if not if_match:
        raise HTTPException(status_code=400, detail="If-Match header (version) is required")
    try:
        version = int(if_match)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="If-Match must be an integer version") from e

    try:
        updated = await update_status(order_id, payload.status, version)
        return updated
    except errors.NotFound as e:
        raise HTTPException(status_code=404, detail="order not found") from e
    except errors.InvalidTransition as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    except errors.Conflict as e:
        raise HTTPException(status_code=409, detail="version mismatch") from e
