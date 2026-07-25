from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

from src.common.schemas.error import ValidationErrorDetail
from src.common.schemas.pagination import PaginationMetadata

T = TypeVar("T")


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    details: list[ValidationErrorDetail] | dict[str, Any] | None = None


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Operation completed successfully."
    data: T | None = None


class PaginatedSuccessResponse(BaseModel, Generic[T]):
    """Standardized wrapper structure for list blocks or filtered data arrays."""

    success: bool = True
    message: str = "Records retrieved successfully."
    pagination: PaginationMetadata
    data: list[T] = Field(default=[], description="The list slice payload array.")
