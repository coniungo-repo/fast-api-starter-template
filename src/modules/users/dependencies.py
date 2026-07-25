from fastapi import Depends

from src.database.session import DbSession
from src.modules.users.application.services import UserService
from src.modules.users.infrastructure.sqlalchemy_repository import (
    SQLAlchemyUserRepository,
)


def get_user_repository(
    db: DbSession,
):
    return SQLAlchemyUserRepository(db)


def get_user_service(
    repo=Depends(get_user_repository),
):
    return UserService(repo)
