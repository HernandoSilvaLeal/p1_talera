import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch
from app.main import app, lifespan

@pytest_asyncio.fixture
async def test_client():
    # Aislamos infra real durante los tests
    with patch("app.main.connect_to_mongo"), \
         patch("app.main.ensure_indexes"), \
         patch("app.main.close_mongo_connection"):
        async with lifespan(app):
            async with AsyncClient(
                transport=ASGITransport(app=app, lifespan="on"),
                base_url="http://test",
            ) as client:
                yield client
