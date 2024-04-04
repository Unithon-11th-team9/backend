from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from app import deps, dto
from app.services.user import UserService

router = APIRouter()


# @router.get(
#     "/users/me",
#     status_code=HTTP_200_OK,
#     response_model=dto.UserProfile,
# )
# async def get_user(
#     current_user: dto.UserProfile = Depends(deps.current_user),
#     user_service: UserService = Depends(deps.user_service),
# ) -> dto.UserProfile:
#     """내 정보를 조회합니다."""
#     user_profile = await user_service.get(current_user.id)
#     return user_profile


@router.get(
    "/users",
    status_code=HTTP_200_OK,
    response_model=list[dto.UserProfile],
)
async def fetch_users(
    user_service: UserService = Depends(deps.user_service),
    offset: int = 0,
    limit: int = 100,
) -> list[dto.UserProfile]:
    """복수 유저를 조회합니다."""
    user_profiles = await user_service.fetch(offset=offset, limit=limit)
    return user_profiles


# @router.post(
#     "/users/{user_id}",
#     status_code=HTTP_200_OK,
#     response_model=dto.UserProfile,
# )
# async def update_user(
#     user_id: int,
#     current_user: dto.UserProfile = Depends(deps.current_user),
#     user_service: UserService = Depends(deps.user_service),
# ) -> dto.UserProfile:
#     """내 정보를 수정합니다."""
#     if user_id == current_user.id:
#         raise ValidationError("본인만 수정할 수 있습니다.")
#     user_profile = await user_service.update(user_id)
#     return user_profile


# @router.delete(
#     "/users/{user_id}",
#     status_code=HTTP_204_NO_CONTENT,
# )
# async def delete_user(
#     user_id: int,
#     current_user: dto.UserProfile = Depends(deps.current_user),
#     user_service: UserService = Depends(deps.user_service),
# ) -> None:
#     """내 정보를 삭제합니다."""
#     if current_user.id != user_id:
#         raise ValidationError("본인만 탈퇴할 수 있습니다.")
#     await user_service.delete(user_id)
