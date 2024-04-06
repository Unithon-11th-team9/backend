import requests

from app.base.config import DISCORD_WEBHOOK_URL


def send_message(msg: str) -> None:
    """메시지를 디스코드로 보낸다."""
    message = {"content": msg}
    requests.post(DISCORD_WEBHOOK_URL, data=message)
