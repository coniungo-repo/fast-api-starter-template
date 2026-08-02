from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.domain.entities import CreateUserData, UpdateUserData
from src.modules.users.domain.models import User
from src.modules.users.domain.repository import UserRepository


class SQLAlchemyUserRepository(UserRepository):
    """
    SQLAlchemy implementation of user persistence.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_by_public_id(
        self,
        public_id: UUID,
    ) -> User | None:

        result = await self.session.execute(
            select(User).where(User.public_id == public_id)
        )

        return result.scalar_one_or_none()

    async def get_by_auth_id(
        self,
        auth_id: str,
    ) -> User | None:

        result = await self.session.execute(select(User).where(User.auth_id == auth_id))

        return result.scalar_one_or_none()

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:

        result = await self.session.execute(select(User).where(User.email == email))

        return result.scalar_one_or_none()

    async def create(
        self,
        data: CreateUserData,
    ) -> User:

        user = User(
            auth_id=data.auth_id,
            email=data.email,
            phone=data.phone,
            full_name=data.full_name,
            profile_image=data.profile_image,
        )

        self.session.add(user)

        await self.session.flush()

        return user

    async def update_auth_id(
        self,
        user: User,
        auth_id: str,
    ) -> User:
        """
        Link an existing guest user to SuperTokens.
        """

        user.auth_id = auth_id

        await self.session.flush()

        return user

    async def update(
        self,
        user: User,
        data: UpdateUserData,
    ) -> User:
        """
        Update user profile fields.
        """

        if data.full_name is not None:
            user.full_name = data.full_name

        if data.phone is not None:
            user.phone = data.phone

        if data.profile_image is not None:
            user.profile_image = data.profile_image

        await self.session.flush()

        return user
