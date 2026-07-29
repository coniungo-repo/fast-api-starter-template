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
    """Fields shared by all user representations."""

    email: EmailStr = Field(
        ...,
        description="Primary user email address.",
    )

    @field_validator("email")
    @classmethod
    def normalise_email(cls, value: str) -> str:
        return value.strip().lower()


class GuestUserCreate(UserBase):
    """
    User creation from guest checkout.

    Guest checkout collects customer details before authentication exists.
    """

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Customer full name.",
    )

    phone: str = Field(
        ...,
        min_length=8,
        max_length=16,
        examples=["+447911123456"],
        description="Customer phone number in E.164 format.",
    )

    profile_image: ProfileImageSchema | None = None


class UserCreate(UserBase):
    """
    User creation after successful SuperTokens authentication.

    auth_id is injected internally from SuperTokens.
    Additional customer details can be collected later.
    """

    profile_image: ProfileImageSchema | None = None


class UserUpdate(BaseModel):
    """
    Customer profile update fields.
    """

    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
        description="Customer full name.",
    )

    phone: str | None = Field(
        default=None,
        min_length=8,
        max_length=16,
        examples=["+447911123456"],
        description="Customer phone number in E.164 format.",
    )

    profile_image: ProfileImageSchema | None = None


class UserResponse(UserBase):
    """
    Public user representation.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    public_id: UUID

    full_name: str | None = None

    phone: str | None = None

    profile_image: ProfileImageSchema | None = None

    is_active: bool

    created_at: datetime

    updated_at: datetime


class AdminUserResponse(UserResponse):
    """
    Internal/admin user representation.
    """

    is_deleted: bool
