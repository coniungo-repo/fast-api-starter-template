from http import HTTPStatus


class AppException(Exception):
    """Base exception class for all custom application errors."""

    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    default_message: str = "An unexpected error occurred."

    def __init__(
        self, message: str | None = None, details: dict | list | None = None
    ) -> None:
        self.message = message or self.default_message
        self.details = details
        super().__init__(self.message)


class NotFoundError(AppException):
    """Raised when a requested resource does not exist."""

    status_code = HTTPStatus.NOT_FOUND
    default_message = "Resource not found."


class ValidationError(AppException):
    """Raised when request payloads fail business or structural validation."""

    status_code = HTTPStatus.BAD_REQUEST
    default_message = "Validation failed."


class UnauthorizedError(AppException):
    """Raised when authentication credentials are missing or invalid."""

    status_code = HTTPStatus.UNAUTHORIZED
    default_message = "Could not validate credentials."


class ForbiddenError(AppException):
    """Raised when an authenticated user lacks permissions for an action."""

    status_code = HTTPStatus.FORBIDDEN
    default_message = "Permission denied."
