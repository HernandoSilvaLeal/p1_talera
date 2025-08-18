import pytest
from httpx import AsyncClient

from app.infra.mongo import db
from app.main import app

pytestmark = pytest.mark.anyio


async def test_create_and_get_order(test_client: AsyncClient):
    body = {
        "customer_id": "c1",
        "currency": "USD",
        "items": [{"sku": "A", "qty": 2, "price": "10.00"}],
    }
    r1 = await test_client.post("/orders", json=body, headers={"Idempotency-Key": "K1"})
    assert r1.status_code == 201  # Check for successful creation
    order = r1.json()
    assert order["status"] == "CREATED"
    assert order["amount"] == "20.00"

    # idempotent retry
    r2 = await test_client.post("/orders", json=body, headers={"Idempotency-Key": "K1"})
    assert r2.status_code == 201  # Check for successful idempotent retry
    assert r2.json()["id"] == order["id"]

    # GET
    r3 = await test_client.get(f"/orders/{order['id']}")
    assert r3.status_code == 200  # Check for successful retrieval
    assert r3.json()["id"] == order["id"]


async def test_patch_with_optimistic_locking_and_transitions(test_client: AsyncClient):
    body = {
        "customer_id": "c2",
        "currency": "USD",
        "items": [{"sku": "B", "qty": 1, "price": "5.50"}],
    }
    r = await test_client.post("/orders", json=body)
    oid = r.json()["id"]
    ver = r.json()["version"]  # expect 1

    # valid transition: CREATED -> PAID
    r1 = await test_client.patch(
        f"/orders/{oid}", json={"status": "PAID"}, headers={"If-Match": str(ver)}
    )
    assert r1.status_code == 200
    assert r1.json()["status"] == "PAID"
    new_ver = r1.json()["version"]

    # invalid transition: PAID -> CREATED
    r2 = await test_client.patch(
        f"/orders/{oid}", json={"status": "CREATED"}, headers={"If-Match": str(new_ver)}
    )
    assert r2.status_code == 422

    # conflict: wrong If-Match
    r3 = await test_client.patch(
        f"/orders/{oid}", json={"status": "FULFILLED"}, headers={"If-Match": "999"}
    )
    assert r3.status_code == 409