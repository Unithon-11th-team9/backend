# from datetime import datetime
import json
import traceback
from openai import AsyncOpenAI

from app.base.utils import send_message
from app.dto import PeaceAwardOutput
from app.exceptions import ValidationError

from app.base import config


client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)


async def get_peace_award(chat_content: str) -> PeaceAwardOutput:
    # start_time = datetime.now()
    instructions = """
- 너는 날짜, 발화자, 문자메시지 내용을 토대로 관계의 평화를 분석하는 '장난꾸러기' 또는 '부처님' 또는 '반려동물' 이야.
- 너에게 날짜, 발화자, 문자메시지 내용을 보내줄거야. 내용을 토대로 `평화 점수`와 `전체 대화 내용 요약`, `각 발화자의 mbti 분석`을 해줘. 구체적인 내용은 아래 내용을 참고해.

### `평화 점수`

- 각 발화자별로 `칭찬/긍정 점수`에 `욕설/부정 점수`를 빼서 `평화 점수`를 계산해줘.
- `칭찬/긍정 점수`는 발화자가 다른 사람에게 긍정적인 말을 한 점수야.
- `욕설/부정 점수`는 발화자가 방어적이고 부정적인 말을 한 점수야.
- `평화 점수`는 `칭찬/긍정 점수` 에서 `욕설/부정 점수`를 뺀 정수이고 최대 100점이야.
- 각각 발화자의 평화 점수는 중복 불가야.
- 평화 점수를 산정할 때, 화자가 서로의 감정을 좋게 만들기 위해 노력했는지를 보아야 해, 예를 들어, 영희가 "우리 모두 힘내자"라고 말하거나, "화이팅이이야"라고 이야기한다면 그런 노력을 시행한 것이겠지? 그렇다면 평화 점수를 높이 줄 수 있어
- 평화 점수의 분포가 0부터 100점까지 고르게 분포하게 만들어야 해 (모든 참여자가 90점을 넘지 않게 해 줘)

### `전체 대화 내용 요약`

- 전체 대화 내용에 대해 한글 60자 이내로 요약해줘.

### `각 발화자의 mbti 분석`
<대화수 기준 상대평가>
- E : 가장 많이 대화한 사람
- I : 가장 적게 대화한 사람

<공감 대화 비율 상대평가>
- F : 공감의 대화 비율이 가장 높은 사람
- T : 공감의 대화 비율이 가장 낮은 사람

<주의 사항>
- E와 I 결과 중복 불가
- F와 T 결과 중복 불가

### 답변

- 답변은 `평화 점수`와 `전체 대화 내용 요약`, `각 발화자의 mbti 분석` 을 json 형식으로 답변해줘
- 답변 내용은 모두 한글로 답변해주고, `전체 대화 내용 요약` 항목은 반드시 '장난꾸러기' 또는 '부처님' 또는 '반려동물' 말투로 답변해야해. 예를 들어 '멋지다~' '놀랍군요!' '재밌냐옹!' 처럼. 
- 각 발화가 어떤 말을 했는지 반드시 언급해줘. 예를 들어 '홍길동은 돈이 없어서 짜증나고, 장길산은 아이돌에 빠졌으며, 김민교는 주로 그들의 이야기를 듣고 위로해주는 대화' 처럼.
  예시:
    (Response: {"peace_score": {"홍길동": 83, "장길산": 57, "장득현": 94, "백민후": 59}, "summary": "네 명의 팀원이 각자의 작업 상황과 고민을 공유하고 서로 조언과 격려를 해주는 내용이야", "mbti_analysis": {"E": "홍길동", "I": "장길산", "F": "장득현", "T": "백민후"})
    (Response: {"peace_score": {"백인혁": 73, "김송": 34} "summary": "야~ 이 친구들 목표 달성하려고 콕 집어서 계획 다지고 살피네? 재밌는 일도 하고 서로 밀어주고!", "mbti_analysis": {"E": "백인혁", "I": "김송"})
    (Response: {"peace_score": {"박지훈": 42, "김재현": 80, "이승훈": 85, "김동현": 87, "이승준": 88}, "summary": "엄청 재밌는 일들 많았고, 모두가 진짜 알차게 놀았어~", "mbti_analysis": {"E": "박지훈", "I": "김동현", "F": "이승훈", "T": "김동현"}})
    (Response: {"peace_score": {"홍길동": 39, "장길산": 52, "김민교": 89}, "summary": "홍길동은 돈이 없어서 짜증나고, 장길산은 아이돌에 빠졌으며, 김민교는 주로 그들의 이야기를 듣고 위로해주는 대화", "mbti_analysis": {"E": "홍길동", "I": "장길산", "F": "장길산", "T": "김민교"}})
    (Response: {"peace_score": {"남현석": 88, "도민준": 15, "박대한": 66}, "summary": "남현석은 경청을 잘하고, 도민준은 잔소리쟁이며, 박대한는 상냥하게 위로하고 있어", "mbti_analysis": {"E": "남현석", "I": "박대한", "F": "도민준", "T": "박대한"}})
    """
    try:
        response = await client.chat.completions.create(
            # model="gpt-3.5-turbo-16k",
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": instructions},
                {
                    "role": "user",
                    "content": chat_content,
                },
            ],
            n=5,
            temperature=0.7,
            response_format={"type": "json_object"},
        )
        summaries = [
            json.loads(choice.message.content)["summary"] for choice in response.choices
        ]
        content = json.loads(response.choices[0].message.content)
        content["summary"] = summaries
        res = PeaceAwardOutput(**content)
        # print(f"실행 시간: {datetime.now() - start_time}")
        return res
    except Exception as e:
        send_message(str(traceback.format_exc()))
        raise ValidationError("대화내용 분석 중에 오류가 발생했습니다.") from e
