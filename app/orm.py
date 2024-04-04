import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.base.db import TimestampBase
from app.dto import UserProfile


class User(TimestampBase):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    uid: Mapped[str] = mapped_column(sa.String(128), nullable=False, unique=True)
    provider: Mapped[str] = mapped_column(sa.String(128), nullable=False)
    name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    email: Mapped[str] = mapped_column(sa.Text, nullable=True, default=None)
    profile_image_url: Mapped[str] = mapped_column(
        sa.Text, nullable=True, server_default=None
    )

    @property
    def profile(self) -> UserProfile:
        return UserProfile(
            id=self.id,
            name=self.name,
            email=self.email,
            profile_image_url=self.profile_image_url,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
