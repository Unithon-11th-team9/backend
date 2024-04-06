from typing import Any
import httpx
from supabase_py_async import create_client
from supabase_py_async.lib.client_options import ClientOptions

from app.base.config import SUPABASE_KEY, SUPABASE_URL

SUPABASE_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}


async def save_to_result(result: dict[str, Any], char_count: int) -> None:
    """분석 결과를 저장합니다."""
    data = {
        "analysis_result": result,
        "analysis_char_count": char_count,
    }
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{SUPABASE_URL}/rest/v1/peace_award_result",
            headers=SUPABASE_HEADERS,
            json=data,
        )


async def fetch_analysis_statistics() -> dict[str, Any]:
    """
    total_char_count: 'analysis_char_count' 컬럼의 총합
    total_result_count: 'analysis_result' 컬럼의 총 개수
    """
    client = await create_client(
        SUPABASE_URL,
        SUPABASE_KEY,
        options=ClientOptions(postgrest_client_timeout=10, storage_client_timeout=10),
    )
    response = (
        await client.table("peace_award_result")
        .select("analysis_char_count", "analysis_result")
        .execute()
    )
    data = response.data
    return {
        "total_char_count": sum(row["analysis_char_count"] for row in data),
        "total_result_count": len(data),
    }
