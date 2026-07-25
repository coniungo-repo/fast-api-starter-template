from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ValidationErrorDetail(BaseModel):
    field: str
    issue: str
    type: str
