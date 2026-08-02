from uuid import UUID

from src.core.exceptions import ConflictError
from src.modules.users.application.schemas import (
    GuestUserCreate,
    UserCreate,
    UserUpdate,
)
from src.modules.users.domain.entities import CreateUserData, UpdateUserData
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
        user = await self._repository.get_by_public_id(public_id)

        if user is None:
            raise UserNotFoundError()

        return user

    async def create_from_supertokens(
        self,
        auth_id: str,
        data: UserCreate,
    ) -> User:
        """
        Create or link a user after successful
        SuperTokens signup.

        SuperTokens provides:
        - auth_id
        - verified email
        """

        user = await self._repository.get_by_email(data.email)

        if user:
            if user.auth_id is None:
                return await self._repository.update_auth_id(
                    user=user,
                    auth_id=auth_id,
                )

            if user.auth_id == auth_id:
                return user

            raise ConflictError(message="An account with this email already exists.")

        return await self._repository.create(
            CreateUserData(
                email=data.email,
                auth_id=auth_id,
                profile_image=(
                    data.profile_image.model_dump(mode="json")
                    if data.profile_image
                    else None
                ),
            )
        )

    async def create_guest_user(
        self,
        data: GuestUserCreate,
    ) -> User:
        """
        Create or update a user from guest checkout.

        Guest users do not have auth_id.
        """

        user = await self._repository.get_by_email(data.email)

        if user:
            if user.auth_id is not None:
                return user

            return await self._repository.update(
                user=user,
                data=UpdateUserData(
                    full_name=data.full_name,
                    phone=data.phone,
                    profile_image=(
                        data.profile_image.model_dump(mode="json")
                        if data.profile_image
                        else None
                    ),
                ),
            )
        return await self._repository.create(
            CreateUserData(
                email=data.email,
                auth_id=None,
                full_name=data.full_name,
                phone=data.phone,
                profile_image=(
                    data.profile_image.model_dump(mode="json")
                    if data.profile_image
                    else None
                ),
            )
        )

    async def update_profile(
        self,
        public_id: UUID,
        data: UserUpdate,
    ) -> User:
        """
        Update authenticated customer profile.
        """

        user = await self._repository.get_by_public_id(public_id)

        if user is None:
            raise UserNotFoundError()

        return await self._repository.update(
            user=user,
            data=UpdateUserData(
                full_name=data.full_name,
                phone=data.phone,
                profile_image=(
                    data.profile_image.model_dump(mode="json")
                    if data.profile_image
                    else None
                ),
            ),
        )
