from collections.abc import Sequence
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import User
from app.base.utils import tz_now


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(
        self,
        *,
        user_id: int | None = None,
        uid: str | None = None,
    ) -> User | None:
        query = sa.select(User).where(
            sa.and_(
                User.id == user_id if user_id else sa.true(),
                User.uid == uid if uid else sa.true(),
                User.deleted_at.is_(None),
            )
        )
        res = await self._session.execute(query)
        return res.scalar_one_or_none()

    async def fetch(self, *, offset: int, limit: int) -> Sequence[User]:
        query = (
            sa.select(User).where(User.deleted_at.is_(None)).offset(offset).limit(limit)
        )
        res = await self._session.execute(query)
        return res.scalars().all()

    async def save(self, user: User) -> None:
        await self._session.flush()

    async def create(self, user: User) -> User:
        self._session.add(user)
        await self._session.flush()
        return user

    async def delete(self, user_id: int) -> None:
        query = sa.update(User).where(User.id == user_id).values(deleted_at=tz_now())
        await self._session.execute(query)
