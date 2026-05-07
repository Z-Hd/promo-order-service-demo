from __future__ import annotations

from app.models.schemas import OrderItem, OrderPreviewRequest


def _compute_subtotal(items: list[OrderItem]) -> tuple[float, int]:
    subtotal = sum(item.price * item.quantity for item in items)
    total_quantity = sum(item.quantity for item in items)
    return subtotal, total_quantity


def preview_order_pricing(payload: OrderPreviewRequest) -> dict:
    subtotal, total_quantity = _compute_subtotal(payload.items)

    # Bug 1: when items is empty, this triggers ZeroDivisionError.
    average_unit_price = subtotal / total_quantity if total_quantity > 0 else 0.0

    discount = 0.0
    # Apply discount only if coupon exists and order has non-zero items
    if payload.coupon is not None and total_quantity > 0:
        coupon_type = payload.coupon.type
        coupon_value = payload.coupon.value
        if coupon_type == "percent":
            discount = subtotal * (coupon_value / 100)
        elif coupon_type == "fixed":
            discount = coupon_value

    payable_amount = subtotal - discount
    return {
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "payable_amount": round(payable_amount, 2),
        "average_unit_price": round(average_unit_price, 2),
        "item_count": total_quantity,
    }
