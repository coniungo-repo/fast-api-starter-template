from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import UnauthorizedError
from src.database.session import DbSession
from src.integrations.supertokens.dependencies import AuthSession
from src.modules.users.application.services import UserService
from src.modules.users.domain.repository import UserRepository
from src.modules.users.infrastructure.sqlalchemy_repository import (
    SQLAlchemyUserRepository,
)


def build_user_repository(
    db: AsyncSession,
) -> UserRepository:
    """
    Creates the user repository implementation.

    Used by both:
    - FastAPI dependency injection
    - background tasks / integrations
    """
    return SQLAlchemyUserRepository(db)


def build_user_service(
    db: AsyncSession,
) -> UserService:
    """
    Creates the user application service.

    Used by both:
    - FastAPI routes
    - SuperTokens callbacks
    """
    repository = build_user_repository(db)

    return UserService(
        repository=repository,
    )


def get_user_repository(
    db: DbSession,
) -> UserRepository:
    """
    FastAPI dependency provider for user repository.
    """
    return build_user_repository(db)


def get_user_service(
    db: DbSession,
) -> UserService:
    """
    FastAPI dependency provider for user service.
    """
    return build_user_service(db)


async def get_current_auth_id(
    session: AuthSession,
) -> str:
    """
    Extract authenticated SuperTokens user ID.
    """

    user_id = session.get_user_id()

    if not user_id:
        raise UnauthorizedError("Authentication required")

    return user_id
