import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import IndexModel, ASCENDING

from app.config import settings

logger = logging.getLogger(__name__)

_client: Optional[AsyncIOMotorClient] = None


async def connect_to_db():
    """Initializes the database connection."""
    global _client
    if _client:
        return
    logger.info("Connecting to MongoDB at %s...", settings.mongo_uri)
    _client = AsyncIOMotorClient(settings.mongo_uri)
    logger.info("MongoDB connection successful.")


async def close_db_connection():
    """Closes the database connection."""
    global _client
    if _client:
        logger.info("Closing MongoDB connection...")
        _client.close()
        _client = None
        logger.info("MongoDB connection closed.")


def db() -> AsyncIOMotorDatabase:
    """Returns the database instance. Must be called after connect_to_db."""
    if not _client:
        raise RuntimeError("Database not connected. Call connect_to_db during application startup.")
    # Motor automatically uses the database specified in the MONGO_URL
    return _client.get_default_database()


async def ensure_indexes():
    """Ensures that the required MongoDB indexes are created."""
    logger.info("Ensuring database indexes exist...")
    database = db()

    # Idempotency collection indexes
    idempotency_indexes = [
        IndexModel([("key", ASCENDING)], name="idempotency_key_unique", unique=True),
        IndexModel([("expires_at", ASCENDING)], name="idempotency_ttl", expireAfterSeconds=0),
    ]
    await database["idempotency"].create_indexes(idempotency_indexes)
    logger.info("Indexes for 'idempotency' collection ensured.")

    # Orders collection indexes
    orders_indexes = [IndexModel([("customer_id", ASCENDING)], name="orders_customer_id")]
    await database["orders"].create_indexes(orders_indexes)
    logger.info("Indexes for 'orders' collection ensured.")