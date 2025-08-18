# tests/test_health.py
import pytest
from unittest.mock import patch, AsyncMock
from pymongo.errors import ConnectionFailure

@pytest.mark.asyncio
async def test_health_check_ok(test_client):
    resp = await test_client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "mongo": "ok"}

@pytest.mark.asyncio
async def test_health_check_mongo_error(test_client):
    # Forzamos que falle el ping a Mongo para este test
    with patch("app.infra.mongo.db") as mock_db:
        mock_db.return_value.command = AsyncMock(side_effect=ConnectionFailure("fail"))
        resp = await test_client.get("/health")
        assert resp.status_code == 503
        assert resp.json() == {"status": "degraded", "mongo": "error"}
