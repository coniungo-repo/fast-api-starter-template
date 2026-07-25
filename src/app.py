from fastapi import FastAPI

from src.common.utils.enums import Environment
from src.core.config import settings
from src.core.exception_handlers import register_exception_handlers
from src.core.logging import LogLevel, configure_logging


def create_app() -> FastAPI:
    """Application factory that configurartion"""
    configure_logging(LogLevel.INFO)

    entry = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        docs_url=None if settings.APP_ENV == Environment.PRODUCTION else "/docs",
        redoc_url=None if settings.APP_ENV == Environment.PRODUCTION else "/redoc",
        openapi_url=(
            None if settings.APP_ENV == Environment.PRODUCTION else "/openapi.json"
        ),
    )

    register_exception_handlers(entry)

    return entry


app = create_app()
