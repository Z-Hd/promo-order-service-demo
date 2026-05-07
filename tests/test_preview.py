from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_preview_order_with_valid_coupon() -> None:
    response = client.post(
        "/orders/preview",
        json={
            "items": [{"sku": "A100", "price": 100, "quantity": 2}],
            "coupon": {"type": "percent", "value": 10},
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "subtotal": 200.0,
        "discount": 20.0,
        "payable_amount": 180.0,
        "average_unit_price": 100.0,
        "item_count": 2,
    }


def test_preview_order_empty_items_should_not_crash() -> None:
    response = client.post(
        "/orders/preview",
        json={
            "items": [],
            "coupon": {"type": "percent", "value": 10},
        },
    )

    assert response.status_code == 200


def test_preview_order_without_coupon_should_not_crash() -> None:
    response = client.post(
        "/orders/preview",
        json={
            "items": [{"sku": "A100", "price": 100, "quantity": 1}],
            "coupon": None,
        },
    )

    assert response.status_code == 200
