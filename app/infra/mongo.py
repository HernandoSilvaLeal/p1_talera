from __future__ import annotations

import os
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

_client: Optional[AsyncIOMotorClient] = None

def get_client() -> AsyncIOMotorClient:
    global _client
    if not _client:
        uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/orders")
        _client = AsyncIOMotorClient(uri)
    return _client

def db() -> AsyncIOMotorDatabase:
    # If MONGO_URI includes the DB name (…/orders), get_default_database() works.
    # Otherwise, default to 'orders'.
    client = get_client()
    return client.get_default_database() or client["orders"]

async def ensure_indexes() -> None:
    database = db()
    orders = database["orders"]
    idemp = database["idempotency"]

    # Orders: by created_at (optional), and unique compound (optional)
    await orders.create_index("created_at")
    await orders.create_index([("version", 1)])

    # Idempotency: unique key + TTL by expires_at
    await idemp.create_index("key", unique=True)
    # 24h TTL. Mongo requiere un índice TTL sobre un campo tipo fecha.
    await idemp.create_index("expires_at", expireAfterSeconds=0)
