from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl


class ProfileImageSchema(BaseModel):
    """Validates external media metadata blocks."""

    id: str = Field(
        ...,
        description="The asset identifier tracking index from the cloud host provider.",
    )
    url: HttpUrl = Field(
        ...,
        description="The direct secure public endpoint URL layout pointing to the file.",
    )


class UserBase(BaseModel):
    """Shared baseline schema ensuring structural alignment across child modules."""

    email: EmailStr = Field(
        ..., description="The unique, verified primary email address context."
    )
    phone: str = Field(
        ...,
        min_length=8,
        max_length=16,
        examples=["+2348012345678"],
        description="The unique contact phone string formatted strictly following E.164 rules.",
    )
    full_name: str | None = Field(default=None, min_length=2, max_length=100)


class UserCreate(UserBase):
    """Strict data validation rule contract for processing registration payloads via SuperTokens setup."""

    auth_id: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="The matching SuperTokens userId.",
    )


class CurrentUserResponse(UserBase):
    """Secure serialization payload model regulating public endpoint responses."""

    model_config = ConfigDict(from_attributes=True)

    public_id: UUID = Field(
        ..., description="The immutable public tracking structural token identifier."
    )
    auth_id: str = Field(
        ..., description="The SuperTokens external user account tracker."
    )
    profile_image: ProfileImageSchema | None = Field(default=None)
    is_active: bool = Field(default=True)
    created_at: datetime
    updated_at: datetime


class UserResponse(UserBase):
    """Secure serialization payload model regulating public endpoint responses."""

    model_config = ConfigDict(from_attributes=True)

    public_id: UUID = Field(
        ..., description="The immutable public tracking structural token identifier."
    )
    auth_id: str = Field(
        ..., description="The SuperTokens external user account tracker."
    )
    profile_image: ProfileImageSchema | None = Field(default=None)
    is_active: bool = Field(default=True)
    is_deleted: bool = Field(default=False)
    created_at: datetime
    updated_at: datetime
