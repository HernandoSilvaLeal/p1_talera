from fastapi import APIRouter
from pymongo.errors import PyMongoError
from app.infra.mongo import db  # si en main hiciste from ... import db, mantén coherencia

router = APIRouter()

@router.get("/health")
async def health():
    try:
        await db().command("ping")
        return {"status": "ok", "mongo": "ok"}
    except PyMongoError:
        return {"status": "degraded", "mongo": "error"}, 503
