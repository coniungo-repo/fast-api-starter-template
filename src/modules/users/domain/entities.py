from dataclasses import dataclass


@dataclass(slots=True)
class CreateUserData:
    """
    Domain data required to create a user.
    """

    email: str

    phone: str | None = None

    full_name: str | None = None

    profile_image: dict | None = None

    auth_id: str | None = None


@dataclass
class UpdateUserData:
    full_name: str | None = None
    phone: str | None = None
    profile_image: dict | None = None
