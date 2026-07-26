from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.modules.users.application.schemas import UserCreate, UserResponse, UserUpdate
from src.modules.users.application.services import UserService
from src.modules.users.dependencies import get_current_auth_id, get_user_service

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    payload: UserCreate,
    auth_id: str = Depends(get_current_auth_id),
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """
    Create customer profile after SuperTokens authentication.
    """

    user = await service.create(
        auth_id=auth_id,
        data=payload,
    )

    return UserResponse.model_validate(user)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_current_user(
    auth_id: str = Depends(get_current_auth_id),
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """
    Retrieve the currently authenticated customer profile.
    """

    user = await service.get_by_auth_id(
        auth_id=auth_id,
    )

    return UserResponse.model_validate(user)


@router.get(
    "/{public_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    public_id: UUID,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """
    Retrieve a user by public identifier.
    """

    user = await service.get_by_public_id(
        public_id=public_id,
    )

    return UserResponse.model_validate(user)
