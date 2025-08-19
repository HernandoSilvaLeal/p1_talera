import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from app.main import app, lifespan

pytestmark = pytest.mark.asyncio

async def _client():
    async with lifespan(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            yield c

@pytest.fixture
async def ac():
    async for c in _client():
        yield c

async def test_404_not_found_shape(ac):
    r = await ac.get("/__nope__")
    assert r.status_code == status.HTTP_404_NOT_FOUND
    body = r.json()
    assert "error" in body and "message" in body["error"] and "request_id" in body["error"]

async def test_405_method_not_allowed_shape(ac):
    # /orders/{id} no permite POST
    r = await ac.post("/orders/some-id")
    assert r.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert "error" in r.json()

async def test_415_unsupported_media_type_shape(ac):
    # body con content-type no soportado (text/plain) en POST /orders
    r = await ac.post("/orders", content="raw-text", headers={"Content-Type": "text/plain"})
    assert r.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    assert "error" in r.json()

async def test_400_if_match_required(ac):
    # PATCH sin If-Match → 400 por guard mínimo
    r = await ac.patch("/orders/abc", json={"status": "PAID"})
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.json()["error"]["code"] == "bad_request"

async def test_422_invalid_transition_shape(ac, monkeypatch):
    # Forzar existencia de la orden y transición inválida si tus servicios lo permiten;
    # o simplemente validar shape cuando se devuelva 422 por validaciones de payload
    r = await ac.patch("/orders/abc", headers={"If-Match": "0"}, json={"status": "NOT_A_STATE"})
    assert r.status_code in (status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_400_BAD_REQUEST)
    assert "error" in r.json()