from datetime import datetime
from zoneinfo import ZoneInfo

import requests

from app.base.config import DISCORD_WEBHOOK_URL


def tz_now(tz: str = "UTC") -> datetime:
    """타임존이 포함된 현재시간을 반환합니다.

    Args:
        tz: 타임존(기본값:UTC)

    Returns:
        타임존이 포함된 현재시간.
    """
    return datetime.now(tz=ZoneInfo(tz))


def datetime_to_msepoch(dt: datetime) -> int:
    """Aware Datetime객체를 Millisecond Epoch로 변환합니다.

    Args:
        dt: datetime객체

    Returns:
        millisecond epoch
    """
    if dt.tzinfo is None:
        raise ValueError("datetime has no timezone info")
    return int(dt.timestamp() * 1000)


def msepoch_to_datetime(ms: float, tz: str = "UTC") -> datetime:
    """Millisecond Epoch를 Aware Datetime객체로 변환합니다.

    Args:
        ms: millisecond epoch
        tz: 타임존(기본값:UTC)

    Returns:
        Aware Datetime객체
    """
    return datetime.fromtimestamp(ms / 1000, tz=ZoneInfo(tz))


def send_message(msg: str) -> None:
    """메시지를 디스코드로 보낸다."""
    message = {"content": msg}
    requests.post(DISCORD_WEBHOOK_URL, data=message)
