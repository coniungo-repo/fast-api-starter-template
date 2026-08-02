from abc import ABC, abstractmethod
from uuid import UUID

from src.modules.users.domain.entities import CreateUserData, UpdateUserData
from src.modules.users.domain.models import User


class UserRepository(ABC):
    """
    User persistence contract.
    """

    @abstractmethod
    async def get_by_public_id(
        self,
        public_id: UUID,
    ) -> User | None: ...

    @abstractmethod
    async def get_by_auth_id(
        self,
        auth_id: str,
    ) -> User | None: ...

    @abstractmethod
    async def get_by_email(
        self,
        email: str,
    ) -> User | None: ...

    @abstractmethod
    async def create(
        self,
        data: CreateUserData,
    ) -> User: ...

    @abstractmethod
    async def update_auth_id(
        self,
        user: User,
        auth_id: str,
    ) -> User:
        """
        Link a SuperTokens account to an existing guest user.
        """
        ...

    @abstractmethod
    async def update(
        self,
        user: User,
        data: UpdateUserData,
    ) -> User: ...
