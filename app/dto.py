from pydantic import BaseModel, Field


class PeaceAwardOutput(BaseModel):
    peace_score: dict[str, int] = Field(
        description="평화 점수",
        examples=[{"보민": 85, "김은찬": 87, "조유나": 88, "최은지": 90, "한아름": 92}],
    )
    summary: list[str] = Field(
        description="전체 대화 내용 요약",
        examples=[
            [
                "다들 친하게.. 이야기하고.. 좋은 분위기예요..",
                "치킨 나눠먹고, 평화 점수 올리기 놀이? 진짜 웃김ㅋㅋ",
                "서로의 존재에 감사함을 나누며 평화와 기쁨을 전파하는 모습이로구나.",
                "치킨 나눠 먹고, 평화 점수 올리기 놀이하다냥~ 귀엽다냥!",
                "치킨 나눔, 평화 점수 올리기 놀이 등 긍정적인 상호작용 발생.",
            ]
        ],
    )
    mbti_analysis: dict[str, str] = Field(
        description="각 발화자의 mbti 분석",
        examples=[{"E": "한아름", "F": "조유나", "I": "김은찬", "T": "보민"}],
    )


class AnalysisStatistics(BaseModel):
    total_char_count: int = Field(
        description="분석된 문자열의 총 개수",
        examples=[588273],
    )
    total_result_count: int = Field(
        description="분석된 결과의 총 개수",
        examples=[82],
    )
