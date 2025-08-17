from fastapi import APIRouter, Header, HTTPException, Response, status
from typing import Optional

from app.domain import errors as domain_errors
from app.domain.models import OrderIn, OrderOut, StatusUpdate
from app.services.orders_service import create_order, get_order, update_status

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED, name="create_order_endpoint")
async def create_order_endpoint(payload: OrderIn, response: Response, idempotency_key: Optional[str] = Header(default=None, alias="Idempotency-Key")):
    try:
        order = await create_order(payload, idempotency_key)
    except domain_errors.Conflict as e:
        # This can happen in a race condition if the idempotency key is being created by another request.
        # The client should retry.
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    response.headers["Location"] = f"/orders/{order.id}"
    return order

@router.get("/{order_id}", response_model=OrderOut, name="get_order_endpoint")
async def get_order_endpoint(order_id: str):
    return await get_order(order_id)

@router.patch("/{order_id}", response_model=OrderOut, name="update_status_endpoint")
async def update_status_endpoint(order_id: str, payload: StatusUpdate, if_match: Optional[str] = Header(default=None, alias="If-Match")):
    if not if_match:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="If-Match header (version) is required")
    try:
        expected_version = int(if_match)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="If-Match must be an integer version") from e

    return await update_status(order_id, payload, expected_version)
