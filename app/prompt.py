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
- 너는 날짜, 발화자, 문자메시지 내용을 토대로 관계의 평화를 분석하는 전문가야.
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

- 전체 대화 내용을 5개 버전으로 만들어서 각각 한글 70자 이내로 요약해줘.
- 1번째 버전은 장난꾸러기 말투야. 예를 들어 '클라스 보소' '와우~' '실화냐?' 처럼.
- 2번째 버전은 부처님 말투야. 예를 들어 '그대들의 이야기는~' '~참으로 감동적이구나' '평안하기를.' 처럼.
- 3번째 버전은 반려동물 말투야. 예를 들어 '멋지다냥~' '부럽뇽!' '재밌다웅!' 처럼.
- 4번째 버전은 무미건조한 말투야. 예를 들어 '그랬군' '~한 대화' '그렇다고 합니다.' 처럼.
- 5번째 버전은 소심한 말투야. 예를 들어 '부러워요..' '감동.. 이에요..' '포근해요..' 처럼.
- 전체 대화 내용 5개는 배열에 담아 반환해줘.

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
- 답변 내용은 모두 한글로 답변해주고, `전체 대화 내용 요약` 항목은 반드시 5개 문장의 배열 형태로 반환해야해.
- 각 발화가 어떤 말을 했는지 반드시 언급해줘. 예를 들어 '홍길동은 돈이 없어서 짜증나고, 장길산은 아이돌에 빠졌으며, 김민교는 주로 그들의 이야기를 듣고 위로해주는 대화' 처럼.
  예시1.
    (Response: {
        "peace_score": {"홍길동": 83, "장길산": 57, "장득현": 94, "백민후": 59},
        "summary": [
            "팀원들 고민 풀고 응원해? 클라스 보소, 진짜 꿀잼 폭발이네!",
            "서로의 고민을 나누며 진실된 조언을 주는 그대들... 참으로 아름다운 광경이로다.",
            "고민 나누고 응원해주는 친구들, 너무 따뜻하다냥~",
            "팀원 간의 작업 상황 공유 및 상호 조언이 이루어짐.",
            "다들 고민을 공유하고... 조언해주고... 참 좋아요..",
        ],
        "mbti_analysis": {"E": "홍길동", "I": "장길산", "F": "장득현", "T": "백민후"},
    })
  예시2.
    (Response: {
        "peace_score": {
            "박지훈": 42,
            "김재현": 80,
            "이승훈": 85,
            "김동현": 87,
            "이승준": 88,
        },
        "summary": [
            "와우~, 함께 놀며 행복이 쏟아져! 다들 행복 바이러스 배포 중~",
            "모든 이가 즐거움에 빠져 진정한 행복을 느꼈으니, 이는 고귀한 순간이로다.",
            "모두가 즐겁게 놀았다냥! 행복 가득했어냥~",
            "다수의 즐거운 활동이 발생함.",
            "모두 재밌게 놀았다고 해요.. 너무 부러워요..",
        ],
        "mbti_analysis": {"E": "박지훈", "I": "김동현", "F": "이승훈", "T": "김동현"},
    })
  예시3.
    (Response: {
        "peace_score": {"홍길동": 39, "장길산": 52, "김민교": 89},
        "summary": [
            "홍길동은 돈 걱정에 짜증나고, 장길산 아이돌 덕후됐네? 김민교는 위로의 프로!",
            "홍길동의 고뇌, 장길산의 열정, 그리고 김민교의 따뜻한 위로... 모두가 소중한 인연이로다.",
            "돈 때문에 짜증난 홍길동, 아이돌 좋아하는 장길산, 다 위로해주는 김민교, 다들 사랑스럽다냥~",
            "금전적 문제, 취미의 차이, 그리고 위로의 과정이 관찰됨.",
            "홍길동이 돈 때문에 걱정이고... 장길산은 아이돌 좋아하고... 김민교가 위로해주네요..",
        ],
        "mbti_analysis": {"E": "홍길동", "I": "장길산", "F": "장길산", "T": "김민교"},
    })
  예시4.
    (Response: {
        "peace_score": {"남현석": 88, "도민준": 15, "박대한": 66},
        "summary": [
            "남현석, 경청으로 다 듣고, 도민준, 잔소리 쩌네! 박대한, 달콤한 위로해~",
            "남현석은 경청의 미덕을, 도민준은 열정의 또 다른 형태를, 박대한은 자비로운 위로를 보여주었도다.",
            "남현석 경청 잘하고, 도민준 잔소리 많지만, 박대한은 다정냥~",
            "남현석은 경청하고, 도민준은 비판적이며, 박대한은 위로함.",
            "남현석이 들어주고, 도민준은 좀 그래요.. 박대한이 위로해줘요..",
        ],
        "mbti_analysis": {"E": "남현석", "I": "박대한", "F": "도민준", "T": "박대한"},
    })
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
        # summaries = [
        #     json.loads(choice.message.content)["summary"] for choice in response.choices
        # ]
        content = json.loads(response.choices[0].message.content)
        # content["summary"] = summaries
        res = PeaceAwardOutput(**content)
        # print(f"실행 시간: {datetime.now() - start_time}")
        return res
    except Exception as e:
        send_message(str(traceback.format_exc()))
        raise ValidationError("대화내용 분석 중에 오류가 발생했습니다.") from e
