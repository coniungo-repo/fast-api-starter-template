from dataclasses import dataclass


@dataclass(slots=True)
class CreateUserData:
    """
    Domain data required to create a user.
    """

    auth_id: str

    email: str

    phone: str

    full_name: str

    profile_image: dict | None = None
