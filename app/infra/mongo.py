from __future__ import annotations

import os
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/orders")

async def connect_to_mongo() -> None:
    """Create global Motor client/db if not already created."""
    global _client, _db
    if _client is not None and _db is not None:
        return
    _client = AsyncIOMotorClient(MONGO_URI, uuidRepresentation="standard")
    # Si la URI trae DB por defecto úsala; si no, 'orders'
    default_db = _client.get_default_database()  # puede ser None
    db_name = (default_db.name if default_db.name else "orders")
    _db = _client[db_name]

def db() -> AsyncIOMotorDatabase:
    """Return the initialized database handle."""
    assert _db is not None, "Mongo not initialized. Call connect_to_mongo() first."
    return _db

async def close_mongo_connection() -> None:
    """Close and clear the global client/db."""
    global _client, _db
    if _client is not None:
        _client.close()
    _client = None
    _db = None

async def ensure_indexes() -> None:
    """Create minimal indexes for the service collections."""
    database = db()
    await database["orders"].create_index("customer_id")
    await database["orders"].create_index("status")
    await database["idempotency"].create_index("key", unique=True)
    # TTL para resultados de idempotencia si manejamos expiración
    await database["idempotency"].create_index("expires_at", expireAfterSeconds=0)