from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl, field_validator


class ProfileImageSchema(BaseModel):
    """External media metadata."""

    id: str = Field(
        ...,
        description="Cloud storage asset identifier.",
    )

    url: HttpUrl = Field(
        ...,
        description="Public secure URL of the image.",
    )


class UserBase(BaseModel):
    """Shared user fields."""

    email: EmailStr = Field(
        ...,
        description="Primary user email address.",
    )

    phone: str = Field(
        ...,
        min_length=8,
        max_length=16,
        examples=["+447911123456"],
        description="Customer contact phone number in E.164 format.",
    )

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Customer full name.",
    )

    @field_validator("email")
    @classmethod
    def normalise_email(
        cls,
        value: str,
    ) -> str:
        return value.strip().lower()


class UserCreate(UserBase):
    """
    Data required when creating a user profile.

    auth_id is injected internally from SuperTokens.
    """

    profile_image: ProfileImageSchema | None = None


class UserUpdate(BaseModel):
    """
    Fields a customer can update.
    """

    phone: str = Field(
        ...,
        min_length=8,
        max_length=16,
    )

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    profile_image: ProfileImageSchema | None = None


class UserResponse(UserBase):
    """Public user response."""

    model_config = ConfigDict(
        from_attributes=True,
    )

    public_id: UUID

    profile_image: ProfileImageSchema | None = None

    is_active: bool

    created_at: datetime

    updated_at: datetime


class AdminUserResponse(UserResponse):
    """Internal/admin response."""

    is_deleted: bool
