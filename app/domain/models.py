from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Literal, List
from pydantic import BaseModel, Field, field_validator, field_serializer

OrderStatus = Literal["CREATED", "PAID", "FULFILLED", "CANCELLED"]

class OrderItem(BaseModel):
    sku: str
    qty: int = Field(gt=0)
    price: Decimal

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("price must be > 0")
        return v

class OrderIn(BaseModel):
    customer_id: str
    currency: str = "USD"
    items: List[OrderItem] = Field(min_length=1)

class OrderOut(BaseModel):
    id: str
    status: OrderStatus
    amount: Decimal
    currency: str
    created_at: datetime
    updated_at: datetime
    version: int

    # pydantic v2: serialize Decimal as string
    @field_serializer("amount")
    def _ser_amount(self, v: Decimal) -> str:
        return format(v, "f")

class StatusUpdate(BaseModel):
    status: OrderStatus