import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app, lifespan

@pytest.fixture(scope="function")
async def test_client():
    async with lifespan(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client
