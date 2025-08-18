# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock

from app.main import app, lifespan

@pytest.fixture(scope="function")
async def test_client():
    # Evita efectos reales de BD durante los tests
    with patch("app.infra.mongo.connect_to_mongo", new=AsyncMock()), \
         patch("app.infra.mongo.close_mongo_connection", new=AsyncMock()), \
         patch("app.infra.mongo.ensure_indexes", new=AsyncMock()), \
         patch("app.infra.mongo.db") as mock_db:

        # Comportamiento saludable por defecto para /health
        mock_db.return_value.command = AsyncMock(return_value={"ok": 1})

        # Arranca y apaga la app correctamente durante el test
        async with lifespan(app):
            async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test"
            ) as client:
                yield client
