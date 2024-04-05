from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from app import deps, dto
from app.services.user import UserService

router = APIRouter()


@router.get(
    "/users/me",
    status_code=HTTP_200_OK,
    response_model=dto.UserProfile,
)
async def get_user(
    current_user: dto.UserProfile = Depends(deps.current_user),
    user_service: UserService = Depends(deps.user_service),
) -> dto.UserProfile:
    """내 정보를 조회합니다."""
    user_profile = await user_service.get(current_user.id)
    return user_profile


@router.post(
    "/users",
    status_code=HTTP_200_OK,
    response_model=dto.UserProfile,
)
async def update_user(
    current_user: dto.UserProfile = Depends(deps.current_user),
    user_service: UserService = Depends(deps.user_service),
) -> dto.UserProfile:
    """내 정보를 수정합니다."""
    user_profile = await user_service.update(current_user.id)
    return user_profile


@router.delete(
    "/users",
    status_code=HTTP_204_NO_CONTENT,
)
async def delete_user(
    current_user: dto.UserProfile = Depends(deps.current_user),
    user_service: UserService = Depends(deps.user_service),
) -> None:
    """내 정보를 삭제합니다."""
    await user_service.delete(current_user.id)
