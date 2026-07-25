from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.domain.models import User
from src.modules.users.domain.repository import UserRepository


class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, session: AsyncSession) -> None:

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

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))

        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        """Saves a new user instance entity inside the active session lifecycle context."""
        self.session.add(user)
        await self.session.flush()
        return user

    async def update(self, user: User) -> User:
        """Merges modifications on an existing trackable model entity state instance."""
        updated_user = await self.session.merge(user)
        await self.session.flush()
        return updated_user
