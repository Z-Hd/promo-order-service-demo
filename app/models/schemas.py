from __future__ import annotations

from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    sku: str
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)


class Coupon(BaseModel):
    type: str
    value: float


class OrderPreviewRequest(BaseModel):
    items: list[OrderItem]
    coupon: Coupon | None = None
