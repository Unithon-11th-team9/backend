from pydantic import BaseModel, Field


class PeaceAwardOutput(BaseModel):
    peace_score: dict[str, int] = Field(
        description="평화 점수",
        examples=[
            {
                "샌디 박신영 언니 핏프티": 90,
                "한아름": 80,
                "임영선 핏프티": 95,
                "김소미 YAPP Server": 85,
                "박근보 YAPP iOS": 87,
                "배수연 네이버 마케팅": 88,
                "조기윤 YAPP Server": 84,
            }
        ],
    )
    summary: list[str] = Field(
        description="전체 대화 내용 요약",
        examples=[
            [
                "엄청 재밌는 일들 많았고, 모두가 진짜 알차게 놀았어~",
                "동료들이 서로 격려하고 축하해주는 훈훈한 분위기야~",
                "멤버들 서로 챙기며 일상 공유하고 격려해, 온통 화기애애해~",
                "일하면서 친분도 쌓고 정보도 공유하는 든든한 친구들 모임이구만!",
                "친구들이 서로 격려하고 응원해주는 훈훈한 분위기야~",
            ]
        ],
    )
    mbti_analysis: dict[str, str] = Field(
        description="각 발화자의 mbti 분석",
        examples=[
            {
                "E": "샌디 박신영 언니 핏프티",
                "I": "조기윤 YAPP Server",
                "F": "임영선 핏프티",
                "T": "박근보 YAPP iOS",
            }
        ],
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
