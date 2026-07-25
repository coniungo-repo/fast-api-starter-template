from typing import TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationMetadata(BaseModel):
    """Metadata detailing list state positions."""

    total_records: int = Field(
        ..., description="Total records matching criteria in database."
    )
    limit: int = Field(
        ..., description="Number of maximum records requested per batch page."
    )
    offset: int = Field(..., description="Starting record marker point used.")
    has_next: bool = Field(..., description="Flag indicating if more records follow.")
    has_previous: bool = Field(
        ..., description="Flag indicating if matching records precede."
    )
