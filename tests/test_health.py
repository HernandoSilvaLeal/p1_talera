import pytest
from httpx import AsyncClient
from unittest.mock import patch

from app.main import app

@pytest.mark.asyncio
async def test_health_check_ok(test_client: AsyncClient):
    response = await test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "mongo": "ok"}

@pytest.mark.asyncio
async def test_health_check_mongo_error():
    with patch("app.infra.mongo.connect_to_mongo") as mock_connect:
        mock_connect.side_effect = Exception("Connection failed")
        from app.main import lifespan
        from httpx import ASGITransport
        async with lifespan(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.get("/health")
                assert response.status_code == 503
                assert response.json() == {"status": "degraded", "mongo": "error"}
