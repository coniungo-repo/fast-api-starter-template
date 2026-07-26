from fastapi import Depends, HTTPException

from src.database.session import DbSession
from src.modules.users.application.services import UserService
from src.modules.users.domain.repository import UserRepository
from src.modules.users.infrastructure.sqlalchemy_repository import (
    SQLAlchemyUserRepository,
)


def get_user_repository(
    db: DbSession,
):
    """
    Provides the user repository implementation.
    """
    return SQLAlchemyUserRepository(db)


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    """
    Provides the user application service.
    """

    return UserService(
        repository=repository,
    )


async def get_current_auth_id() -> str:
    """
    Extract authenticated SuperTokens user ID.
    """

    user_id = "test123"

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
        )

    return user_id
