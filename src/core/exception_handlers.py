import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.common.responses import ErrorResponse

from .exceptions import AppException

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Registers global exception handlers to standardize all API error outputs."""

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request, exc: AppException
    ) -> JSONResponse:
        """Catches custom domain-driven application exceptions."""
        error_payload = ErrorResponse(
            message=exc.message,
            details=getattr(exc, "details", None),
        ).model_dump()

        return JSONResponse(
            status_code=exc.status_code,
            content=error_payload,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Overrides FastAPI's default 422 error format to match our schema structure."""
        formatted_errors = []
        for error in exc.errors():
            formatted_errors.append(
                {
                    "field": " -> ".join(
                        str(loc) for loc in error["loc"] if loc != "body"
                    ),
                    "issue": error["msg"],
                    "type": error["type"],
                }
            )

        error_payload = ErrorResponse(
            message="The request payload failed structural validation checks.",
            details=formatted_errors,
        ).model_dump()

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_payload,
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Fallback handler for unhandled code errors, database drops, or runtime crashes."""
        logger.error("Unhandled exception encountered: %s", exc, exc_info=True)

        error_payload = ErrorResponse(
            message="An unexpected system error occurred. Please try again later.",
            details=None,
        ).model_dump()

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_payload,
        )
