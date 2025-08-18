import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch
from mongomock_motor import AsyncMongoMockClient
from app.main import app, lifespan

@pytest_asyncio.fixture
async def test_client():
    # DB en memoria para TODOS los tests (orders + idempotency)
    fake_client = AsyncMongoMockClient()
    fake_db = fake_client["testdb"]

    with patch("app.main.connect_to_mongo"), \
         patch("app.main.ensure_indexes"), \
         patch("app.main.close_mongo_connection"), \
         # MUY IMPORTANTE: patch a los módulos que llaman db()
         patch("app.services.orders_service.db", return_value=fake_db), \
         patch("app.utils.idempotency.db", return_value=fake_db):
        async with lifespan(app):
            async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
            ) as client:
                yield client
