import logging
import sys

import structlog
from structlog.contextvars import merge_contextvars

def configure_logging(level: str = "INFO") -> None:
    """
    Configure structured logging using structlog.
    """
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.getLevelName(level.upper()),
    )

    structlog.configure(
        processors=[
            merge_contextvars,  # Adds context variables to the log record
            structlog.stdlib.add_log_level, # Adds the log level
            structlog.processors.TimeStamper(fmt="iso", utc=True), # ISO UTC timestamp
            structlog.processors.JSONRenderer(), # Renders the log as JSON
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Silenciar logs de uvicorn y otros que no sean de la app
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)