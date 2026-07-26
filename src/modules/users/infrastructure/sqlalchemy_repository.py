from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.domain.entities import CreateUserData
from src.modules.users.domain.models import User
from src.modules.users.domain.repository import UserRepository


class SQLAlchemyUserRepository(UserRepository):

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
            profile_image=(data.profile_image),
        )

        self.session.add(user)

        await self.session.flush()

        return user
