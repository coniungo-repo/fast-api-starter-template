from fastapi import FastAPI

from common.utils.enums import Environment
from core.config import settings
from core.exception_handlers import register_exception_handlers
from core.logging import configure_logging


def create_app() -> FastAPI:
    """Application factory that initializes and configures the FastAPI instance."""
    configure_logging(level_name=settings.LOG_LEVEL)

    is_production = settings.APP_ENV == Environment.PRODUCTION

    entry = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        docs_url=None if is_production else "/docs",
        redoc_url=None if is_production else "/redoc",
        openapi_url=None if is_production else "/openapi.json",
    )

    register_exception_handlers(entry)

    return entry


app = create_app()
