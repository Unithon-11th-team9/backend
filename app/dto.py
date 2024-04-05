import datetime
from pydantic import BaseModel, Field

from app.base.utils import tz_now


class UserProfile(BaseModel):
    id: int = Field(description="유저 아이디", examples=[1])
    name: str = Field(description="이름", examples=["홍길동"])
    email: str = Field(description="이메일", examples=["user@email.com"])
    profile_image_url: str = Field(
        description="프로필 이미지 URL",
        examples=["https://www.google.com"],
        default=None,
    )
    created_at: datetime.datetime = Field(description="생성일시", examples=[tz_now()])
    updated_at: datetime.datetime = Field(description="변경일시", examples=[tz_now()])
