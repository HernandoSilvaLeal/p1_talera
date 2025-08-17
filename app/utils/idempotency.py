from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Awaitable, Callable, Optional, TypedDict

from app.infra.mongo import db

class CachedResult(TypedDict, total=False):
    result: dict
    status_code: int
    headers: dict

async def get_cached_result(key: Optional[str]) -> Optional[CachedResult]:
    if not key:
        return None
    doc = await db()["idempotency"].find_one({"key": key})
    if not doc:
        return None
    return {
        "result": doc.get("result", {}),
        "status_code": doc.get("status_code", 200),
        "headers": doc.get("headers", {}),
    }

async def save_result(key: str, result: dict, status_code: int, headers: dict | None = None, ttl_seconds: int = 86400) -> None:
    expires = datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)
    await db()["idempotency"].update_one(
        {"key": key},
        {"$set": {"result": result, "status_code": status_code, "headers": headers or {}, "expires_at": expires}},
        upsert=True,
    )
