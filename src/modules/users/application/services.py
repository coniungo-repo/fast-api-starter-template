from uuid import UUID

from src.core.exceptions import ConflictError
from src.modules.users.application.schemas import UserCreate
from src.modules.users.domain.entities import CreateUserData
from src.modules.users.domain.exceptions import UserNotFoundError
from src.modules.users.domain.models import User
from src.modules.users.domain.repository import UserRepository


class UserService:
    """
    Handles user business logic.
    """

    def __init__(
        self,
        repository: UserRepository,
    ) -> None:
        self._repository = repository

    async def get_by_auth_id(
        self,
        auth_id: str,
    ) -> User:

        user = await self._repository.get_by_auth_id(auth_id)

        if user is None:
            raise UserNotFoundError()

        return user

    async def get_by_public_id(
        self,
        public_id: UUID,
    ) -> User:
        user = await self._repository.get_by_public_id(
            public_id,
        )
        if user is None:
            raise UserNotFoundError()

        return user

    async def create(
        self,
        auth_id: str,
        data: UserCreate,
    ) -> User:

        existing = await self._repository.get_by_email(data.email)

        if existing:
            raise ConflictError(message="An account with this email already exists.")

        user_data = CreateUserData(
            auth_id=auth_id,
            email=data.email,
            phone=data.phone,
            full_name=data.full_name,
            profile_image=(
                data.profile_image.model_dump(mode="json")
                if data.profile_image
                else None
            ),
        )

        return await self._repository.create(user_data)
