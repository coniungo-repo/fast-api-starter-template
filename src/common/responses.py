from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """Standardized wrapper for all successful API responses."""

    success: bool = Field(
        default=True, description="Indicates if the operation was successful."
    )
    message: str = Field(
        default="Operation completed successfully.",
        description="Human-readable response message.",
    )
    data: T | None = Field(default=None, description="The actual response payload.")


class ErrorResponse(BaseModel):
    """Standardized wrapper for all failed API responses."""

    success: bool = Field(
        default=False, description="Indicates if the operation failed."
    )
    message: str = Field(..., description="Human-readable error explanation.")
    details: dict | list | None = Field(
        default=None, description="Granular error data or validation fields."
    )
