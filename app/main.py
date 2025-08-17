import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

from app.config import settings
from app.domain import errors as domain_errors
from app.infra import metrics
from app.infra.logging import configure_logging
from app.infra.mongo import close_db_connection, connect_to_db, ensure_indexes
from app.routes.metrics import router as metrics_router
from app.routes.orders import router as orders_router
from app.utils.request_context import ensure_request_id

configure_logging(level=settings.log_level)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events, like DB connections."""
    logger.info("Application startup...")
    await connect_to_db()
    try:
        await ensure_indexes()
    except Exception as e:
        logger.warning("Could not ensure indexes on startup: %s", e)
    yield
    logger.info("Closing DB connection...")
    await close_db_connection()
    logger.info("Application shutdown.")


async def observe_request_latency(request: Request, call_next):
    """
    Middleware to observe request latency and expose it as a Prometheus metric.
    """
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time

    path_template = request.scope.get("route").path if request.scope.get("route") else request.url.path

    metrics.request_latency_seconds.labels(
        method=request.method, path=path_template, status_code=response.status_code
    ).observe(duration)

    return response

# Define the servers for OpenAPI documentation. This helps Swagger UI know where to send requests.
servers = [
    {"url": "http://127.0.0.1:8000", "description": "Local Development Server"}
]

app = FastAPI(
    title="Order Processing Service",
    version="1.0.0",
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    servers=servers,
)

# Exception Handlers
@app.exception_handler(domain_errors.NotFound)
async def not_found_exception_handler(request: Request, exc: domain_errors.NotFound):
    return ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})

@app.exception_handler(domain_errors.Conflict)
async def conflict_exception_handler(request: Request, exc: domain_errors.Conflict):
    return ORJSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})

@app.exception_handler(domain_errors.InvalidTransition)
async def invalid_transition_exception_handler(request: Request, exc: domain_errors.InvalidTransition):
    return ORJSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": str(exc)})

# Middleware & Routers
app.middleware("http")(observe_request_latency)
app.middleware("http")(ensure_request_id)
app.include_router(orders_router)
app.include_router(metrics_router)

@app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK)
async def health():
    return {"status": "ok", "service": settings.service_name}
