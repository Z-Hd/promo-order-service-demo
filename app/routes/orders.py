from __future__ import annotations

from fastapi import APIRouter

from app.models.schemas import OrderPreviewRequest
from app.services.pricing import preview_order_pricing


router = APIRouter()


@router.post("/orders/preview")
def preview_order(payload: OrderPreviewRequest) -> dict:
    return preview_order_pricing(payload)
