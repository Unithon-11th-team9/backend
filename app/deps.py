from fastapi import Cookie

from app.base.auth import decode_token
from app.exceptions import NotFoundError, PermissionError


async def current_user(
    access_token: str = Cookie(default=None),
    refresh_token: str = Cookie(default=None),
) -> int:
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
        if not user_id:
            raise NotFoundError(f"{user_id} 유저가 존재하지 않습니다.")
        return user_id  # TODO: 유저 객체 반환하도록 변경 예정

    else:
        raise PermissionError(
            f"{access_token=}, {refresh_token=} 토큰이 유효하지 않습니다."
        )
