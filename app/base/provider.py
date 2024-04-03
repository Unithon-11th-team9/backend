from typing import TypedDict
from app.exceptions import ValidationError
import requests


class ProviderUserInfo(TypedDict):
    uid: str


class KakaoAuthProvider:
    def __init__(self, token: str) -> None:
        self._token = token

    def get_user_info(self) -> ProviderUserInfo:
        res = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {self._token}"},
        )
        if res.status_code != 200:
            try:
                message = res.json()["msg"]
            except KeyError:
                message = f"Something went wrong while getting user information\
                    {res.status_code}"
            raise ValidationError(message)

        data = res.json()
        user_info = ProviderUserInfo(uid=str(data["id"]))
        return user_info
