from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from supertokens_python import get_all_cors_headers
from supertokens_python.framework.fastapi import get_middleware

from common.utils.enums import Environment
from core.config import settings
from core.exception_handlers import register_exception_handlers
from core.logging import configure_logging
from src.api.router import api_router
from src.integrations.supertokens.config import configure_auth


def create_app() -> FastAPI:
    """Application factory that initializes and configures the FastAPI instance."""
    configure_logging(level_name=settings.LOG_LEVEL)

    is_production = settings.APP_ENV == Environment.PRODUCTION

    configure_auth()

    entry = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        docs_url=None if is_production else "/docs",
        redoc_url=None if is_production else "/redoc",
        openapi_url=None if is_production else "/openapi.json",
    )

    entry.add_middleware(get_middleware())

    entry.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL],
        allow_credentials=True,
        allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["Content-Type"] + get_all_cors_headers(),
    )

    register_exception_handlers(entry)

    entry.include_router(api_router)

    return entry


app = create_app()
