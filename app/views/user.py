from typing import Literal
from fastapi import APIRouter, Body, Depends, Response
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from app import deps, dto
from app.base.auth import login
from app.base.provider import KakaoAuthProvider
from app.exceptions import ValidationError
from app.services.user import UserService

router = APIRouter()


@router.post(
    "/social-login/{provider}",
    status_code=HTTP_200_OK,
    response_model=dto.UserProfile,
)
async def social_login(
    response: Response,
    provider: Literal["kakao"],
    token: str = Body(embed=True),
    user_service: UserService = Depends(deps.user_service),
) -> dto.UserProfile:
    """소셜 로그인을 합니다."""
    if provider == "kakao":
        kakao_provider = KakaoAuthProvider(token)
        user_info = kakao_provider.get_user_info()
    else:
        raise ValidationError(f"지원하지 않는 소셜 플랫폼입니다. '{provider}'")
    user = await user_service.get_or_create_user(provider, user_info)
    login(response, user.id)
    return user


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
