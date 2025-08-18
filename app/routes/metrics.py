from fastapi import APIRouter

router = APIRouter()

# Placeholder for metrics endpoint
@router.get("/metrics")
async def metrics():
    return {}