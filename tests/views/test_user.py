from unittest import mock
import orjson
from pytest_mock import MockerFixture
from app.base.provider import KakaoAuthProvider
from httpx import AsyncClient


async def test_kakao_social_login_and_fetch_profile_via_cookies(
    client: AsyncClient, mocker: MockerFixture
) -> None:
    """카카오 소셜 로그인과 쿠키를 통한 내 정보 조회 테스트"""
    # given
    mocker.patch.object(KakaoAuthProvider, "get_user_info", return_value={"uid": "1"})
    data = orjson.dumps({"token": "fake token"})

    # when: 카카오 소셜 로그인
    res = await client.post(
        "/v1/social-login/kakao",
        data=data,
    )

    # then
    assert res.status_code == 200
    assert (
        len(res.cookies) == 2
    )  # 참고. 쿠키에 도메인을 추가하면 테스트에서는 쿠키를 받지 못함
    assert res.json() == {
        "id": 1,
        "name": None,
        "email": None,
        "profile_image_url": None,
        "created_at": mock.ANY,
        "updated_at": mock.ANY,
    }

    # when: 쿠키를 통한 내 정보 조회
    res = await client.get(
        "/v1/users/me",
        cookies=dict(res.cookies),
    )

    # then
    assert res.status_code == 200
    assert res.json() == {
        "id": 1,
        "name": None,
        "email": None,
        "profile_image_url": None,
        "created_at": mock.ANY,
        "updated_at": mock.ANY,
    }
