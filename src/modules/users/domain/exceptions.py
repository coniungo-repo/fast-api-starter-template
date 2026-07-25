from src.core.exceptions import NotFoundError


class UserNotFoundError(NotFoundError):

    def __init__(self, auth_id: str | None = None):
        message = (
            "User not found." if auth_id is None else f"User '{auth_id}' not found."
        )
        super().__init__(message)
