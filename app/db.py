from datetime import datetime
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


async def create_result(result: dict[str, Any], char_count: int) -> int:
    """분석 결과를 생성합니다."""
    id = int(datetime.now().timestamp() * 1000)
    data = {
        "id": id,
        "analysis_result": result,
        "analysis_char_count": char_count,
    }
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{SUPABASE_URL}/rest/v1/peace_award_result",
            headers=SUPABASE_HEADERS,
            json=data,
        )
    return id


async def get_result(peace_award_id: int) -> dict[str, Any]:
    """분석 결과를 조회합니다."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/peace_award_result?id=eq.{peace_award_id}",
            headers=SUPABASE_HEADERS,
        )
    return response.json()[0]["analysis_result"]


async def fetch_analysis_statistics() -> dict[str, Any]:
    """
    현재까지의 분석 통계를 응답합니다.
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
        # 4월 7일 오전 10시 이후 데이터만 조회(제품 공개 이후 데이터)
        .gt("created_at", "2024-04-07 01:00:00.00000+00")
        .execute()
    )
    data = response.data
    return {
        "total_char_count": sum(row["analysis_char_count"] for row in data),
        "total_result_count": len(data),
    }
