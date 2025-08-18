import pytest
from unittest.mock import AsyncMock, patch
from pymongo.errors import ConnectionFailure

@pytest.mark.asyncio
async def test_health_check_ok(test_client):
    with patch("app.main.db") as mock_db_func:
        fake_db = AsyncMock()
        fake_db.command = AsyncMock(return_value={"ok": 1})
        mock_db_func.return_value = fake_db

        resp = await test_client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok", "mongo": "ok"}

@pytest.mark.asyncio
async def test_health_check_mongo_error(test_client):
    with patch("app.main.db") as mock_db_func:
        fake_db = AsyncMock()
        fake_db.command = AsyncMock(side_effect=ConnectionFailure("fail"))
        mock_db_func.return_value = fake_db

        resp = await test_client.get("/health")
        assert resp.status_code == 503
        assert resp.json() == {"status": "degraded", "mongo": "error"}
