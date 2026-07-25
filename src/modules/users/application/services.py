from src.core.exceptions import ConflictError
from src.modules.users.application.schemas import UserCreate
from src.modules.users.domain.exceptions import UserNotFoundError
from src.modules.users.domain.models import User
from src.modules.users.domain.repository import UserRepository


class UserService:
    """Handles business rules and validation logic for User entities."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def get_profile(self, auth_id: str) -> User:
        """Retrieves a user profile by their SuperTokens ID, failing fast if absent."""
        user = await self.repository.get_by_auth_id(auth_id)

        if user is None:
            raise UserNotFoundError()

        return user

    async def create(self, data: UserCreate) -> User:
        """Validates domain constraints and saves a new user into the database infrastructure."""
        normalized_email = data.email.lower().strip()

        existing_user = await self.repository.get_by_email(normalized_email)
        if existing_user:
            raise ConflictError(
                message="An account with this email address already exists."
            )

        user_attributes = data.model_dump()
        user_attributes["email"] = normalized_email

        new_user = await self.repository.create(User(**user_attributes))
        return new_user
