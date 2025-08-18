import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch
from mongomock_motor import AsyncMongoMockClient
from app.main import app, lifespan

@pytest_asyncio.fixture
async def test_client():
    # DB en memoria para orders + idempotency
    fake_client = AsyncMongoMockClient()
    fake_db = fake_client["testdb"]

    # Mock de la función db() para que devuelva la base de datos en memoria
    with patch("app.services.orders_service.db", return_value=fake_db), \
         patch("app.utils.idempotency.db", return_value=fake_db):
        async with lifespan(app):
            async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
            ) as client:
                yield client