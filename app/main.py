import asyncio
import logging
import time
import uuid
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from pymongo.errors import PyMongoError

from app.config import settings
from app.domain import errors as domain_errors
from app.infra.logging import configure_logging
from app.infra.mongo import close_mongo_connection, connect_to_mongo, ensure_indexes, db
from app.routes.metrics import router as metrics_router
from app.routes.orders import router as orders_router
from app.routes import health as health_router
from app.utils import request_context

# 1. Configurar el logging ESTRUCTURADO lo antes posible
configure_logging(level=settings.log_level)
log = structlog.get_logger("bootstrap")
log.info("app_booting", service_name=settings.service_name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("lifespan.startup.begin")
    await connect_to_mongo()
    try:
        await ensure_indexes()
    except Exception as e:
        log.warning("lifespan.startup.ensure_indexes.failed", error=str(e))
    log.info("Application startup complete")
    yield
    log.info("lifespan.shutdown.begin")
    await close_mongo_connection()
    log.info("lifespan.shutdown.end")


async def logging_middleware(request: Request, call_next):
    request_context.clear_context()

    # Extraer o generar Request ID
    request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
    request_context.set_request_id(request_id)

    # Extraer otros IDs relevantes de la ruta
    if "order_id" in request.path_params:
        request_context.set_order_id(request.path_params["order_id"])

    structlog.contextvars.bind_contextvars(
        request_id=request_context.get_request_id(),
    )
    request_log = structlog.get_logger("api.request")

    start_time = time.perf_counter()
    request_log.info("request_started", method=request.method, path=request.url.path)

    response = await call_next(request)
    response.headers["X-Request-Id"] = request_id
    status_code = response.status_code

    duration = time.perf_counter() - start_time
    request_log.info(
        "request_finished",
        status_code=status_code,
        duration_ms=round(duration * 1000, 2),
    )
    request_context.clear_context()
    return response


app = FastAPI(
    title="Order Processing Service",
    version="1.0.0",
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

# Middleware & Routers
app.middleware("http")(logging_middleware)
app.include_router(orders_router)
app.include_router(metrics_router)


# --- Health Endpoints ---

@app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK)
async def health():
    """Health check: confirma que la app puede conectar con sus dependencias (Mongo)."""
    try:
        # Usar un timeout bajo para no bloquear el event loop por mucho tiempo
        await asyncio.wait_for(
            db().command("ping"),
            timeout=2.0
        )
        return {"status": "ok", "mongo": "ok"}
    except Exception:
        log.warning("health.check.failed", dependency="mongo")
        return ORJSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "degraded", "mongo": "error"}
        )


# --- Exception Handlers ---

@app.exception_handler(PyMongoError)
async def mongo_exception_handler(request: Request, exc: PyMongoError):
    log.error("mongo.error", error=str(exc), exc_info=True)
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected database error occurred"}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Log detallado de errores de validación
    log.warning("api.validation.error", errors=exc.errors())
    return ORJSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()}
    )

@app.exception_handler(domain_errors.NotFound)
async def not_found_exception_handler(request: Request, exc: domain_errors.NotFound):
    return ORJSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})

@app.exception_handler(domain_errors.Conflict)
async def conflict_exception_handler(request: Request, exc: domain_errors.Conflict):
    return ORJSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})

@app.exception_handler(domain_errors.InvalidTransition)
async def invalid_transition_exception_handler(request: Request, exc: domain_errors.InvalidTransition):
    return ORJSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": str(exc)})
