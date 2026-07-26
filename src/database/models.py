from src.database.base import Base
from src.database.mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin


class BaseDBModel(
    UUIDMixin,
    TimestampMixin,
    SoftDeleteMixin,
    Base,
):
    """
    Base model inherited by all application models.

    Includes:
        - public_id
        - created_at
        - updated_at
        - is_deleted
        - deleted_at
    """

    __abstract__ = True
