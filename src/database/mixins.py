from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column


class UUIDMixin:
    """
    Adds a public UUID identifier.

    Used for:
    - API responses
    - External references
    - Avoid exposing database IDs
    """

    public_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        unique=True,
        index=True,
        nullable=False,
        default=uuid4,
    )


class AuthMixin:
    """
    Stores external authentication identity.

    Authentication provider:
    SuperTokens

    This should match:
    SuperTokens userId
    """

    auth_id: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        index=True,
        nullable=False,
    )


class TimestampMixin:
    """
    Adds creation and update timestamps.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class SoftDeleteMixin:
    """
    Allows soft deletion instead of removing records.

    Useful for:
    - Users
    - Providers
    - Products
    - Services
    """

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class ActiveMixin:
    """
    Adds active/inactive status.

    Useful for:
    - Services
    - Products
    - Categories
    """

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
    )
