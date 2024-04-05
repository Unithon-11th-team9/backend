from fastapi import Cookie, Depends, Request

from app import dto
from app.base.auth import decode_token
from app.exceptions import NotFoundError, PermissionError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user import UserRepository
from app.services.user import UserService


def session(request: Request) -> AsyncSession:
    return request.state.session


def user_repo(session: AsyncSession = Depends(session)) -> UserRepository:
    return UserRepository(session)


def user_service(user_repo: UserRepository = Depends(user_repo)) -> UserService:
    return UserService(user_repo)


async def current_user(
    user_repo: UserRepository = Depends(user_repo),
    access_token: str = Cookie(default=None),
    refresh_token: str = Cookie(default=None),
) -> dto.UserProfile:
    if access_token or refresh_token:
        try:
            result = decode_token(access_token)
        except Exception:
            try:
                result = decode_token(refresh_token)
            except Exception:
                raise PermissionError(
                    f"{access_token=}, {refresh_token=} 토큰이 유효하지 않습니다."
                )

        user_id = result.get("user_id", None)
        user = await user_repo.get(user_id=user_id)
        if not user:
            raise NotFoundError(f"{user_id} 유저가 존재하지 않습니다.")
        return user.profile

    else:
        raise PermissionError(
            f"{access_token=}, {refresh_token=} 토큰이 유효하지 않습니다."
        )
