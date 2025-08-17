import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, ORJSONResponse

from app.config import settings
from app.infra.logging import configure_logging
from app.routes.orders import router as orders_router
from app.utils.idempotency import ensure_indexes
from app.utils.request_context import ensure_request_id

configure_logging(level=settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager for application startup and shutdown events."""
    logger.info("Application startup...")
    yield
    logger.info("Application shutdown.")


app = FastAPI(
    title="Order Processing Service",
    version="1.0.0",
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

app.middleware("http")(ensure_request_id)
app.include_router(orders_router)

@app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK)
async def health():
    return {"status": "ok", "service": settings.service_name}
