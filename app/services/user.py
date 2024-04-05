from app import dto
from app.base.provider import ProviderUserInfo
from app.exceptions import NotFoundError
from app.orm import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def get_or_create_user(
        self, provider: str, provider_data: ProviderUserInfo
    ) -> dto.UserProfile:
        """기존 유저를 가져오거나 없다면 생성합니다."""
        user = await self._user_repo.get(uid=provider_data["uid"])
        if user:
            return user.profile
        else:
            user = await self._user_repo.create(
                User(
                    uid=provider_data["uid"],
                    provider=provider,
                    name=provider_data.get("name"),
                    email=provider_data.get("email"),
                    profile_image_url=provider_data.get("profile_image_url"),
                )
            )
            return user.profile

    async def get(self, user_id: int) -> dto.UserProfile:
        """유저를 조회합니다."""
        user = await self._user_repo.get(user_id=user_id)
        if user is None:
            raise NotFoundError("유저가 존재하지 않습니다.")
        return user.profile

    async def fetch(self, offset: int, limit: int) -> list[dto.UserProfile]:
        """복수 유저를 조회합니다."""
        users = await self._user_repo.fetch(offset=offset, limit=limit)
        return [user.profile for user in users]

    async def update(self, user_id: int) -> dto.UserProfile:
        """유저 정보를 수정합니다."""
        user = await self._user_repo.get(user_id=user_id)
        if user is None:
            raise NotFoundError("유저가 존재하지 않습니다.")

        # TODO: 기획에 따라 유저 정보 수정
        # Example: user.name = "변경할 이름"
        await self._user_repo.save(user)
        return user.profile

    async def delete(self, user_id: int) -> None:
        """유저를 삭제합니다."""
        await self._user_repo.delete(user_id)
