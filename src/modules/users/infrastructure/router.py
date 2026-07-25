from fastapi import APIRouter, Depends, status

from src.modules.users.application.schemas import UserCreate, UserResponse
from src.modules.users.application.services import UserService
from src.modules.users.dependencies import get_user_service

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
    service: UserService = Depends(get_user_service),
):

    return await service.create(payload)
