import json
import os
import traceback
from openai import OpenAI

from app.base.utils import send_message
from app.dto import PeaceAwardOutput
from app.exceptions import ValidationError

from app.base import config


client = OpenAI(api_key=config.OPENAI_API_KEY)


def get_peace_award(chat_content: str) -> PeaceAwardOutput:
    instructions = """
- 너는 날짜, 발화자, 문자메시지 내용을 토대로 관계의 평화를 분석하는 장난꾸러기야.
- 너에게 날짜, 발화자, 문자메시지 내용을 보내줄거야. 내용을 토대로 `평화 점수`와 `전체 대화 내용 요약`, `각 발화자의 mbti 분석`을 해줘. 구체적인 내용은 아래 내용을 참고해.

### `평화 점수`

- 각 발화자별로 `칭찬/긍정 점수`에 `욕설/부정 점수`를 빼서 `평화 점수`를 계산해줘.
- `칭찬/긍정 점수`는 발화자가 다른 사람에게 긍정적인 말을 한 점수야.
- `욕설/부정 점수`는 발화자가 방어적이고 부정적인 말을 한 점수야.
- `평화 점수`는 정수이고 최대 100점이야.
- 각각 발화자의 평화 점수는 중복 불가야.
- 평화 점수를 산정할 때, 화자가 서로의 감정을 좋게 만들기 위해 노력했는지를 보아야 해, 예를 들어, 영희가 "우리 모두 힘내자"라고 말하거나, "화이팅이이야"라고 이야기한다면 그런 노력을 시행한 것이겠지?
그렇다면 평화 점수를 높이 줄 수 있어
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
- 답변 내용은 모두 한글로 답변해주고, `전체 대화 내용 요약` 항목은 반드시 반말의 장난꾸러기 말투로 답변해야해. 예를 들어 '멋지다~' '놀라운데?' '재밌다.' 처럼.
  예시:
    (Response: {"peace_score": {"홍길동": 83, "장길산": 57, "장득현": 94, "백민후": 59}, "summary": "네 명의 팀원이 각자의 작업 상황과 고민을 공유하고 서로 조언과 격려를 해주는 내용이야", "mbti_analysis": {"E": "홍길동", "I": "장길산", "F": "장득현", "T": "백민후"})
    (Response: {"peace_score": {"백인혁": 73, "김송": 34} "summary": "야~ 이 친구들 목표 달성하려고 콕 집어서 계획 다지고 살피네? 재밌는 일도 하고 서로 밀어주고!", "mbti_analysis": {"E": "백인혁", "I": "김송"})
    """
    try:
        # chat_content = get_chat_content() # 테스트용 코드입니다.
        response = client.chat.completions.create(
            # model="gpt-3.5-turbo-16k",
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": instructions},
                {
                    "role": "user",
                    "content": chat_content[-15000:],
                },  # TODO: 15000자 이상은 분리 필요
            ],
            n=5,
            response_format={"type": "json_object"},
        )
        summaries = [
            json.loads(choice.message.content)["summary"]
            for choice in response.choices[1:]
        ]
        content = json.loads(response.choices[0].message.content)
        content["summary"] = summaries
        return PeaceAwardOutput(**content)
    except Exception:
        send_message(str(traceback.format_exc()))
        raise ValidationError("대화내용 분석 중에 오류가 발생했습니다.")


# 아래는 테스트용 코드입니다.
# def get_chat_content():
#     with open("secrets/sample/sample001.csv", mode="r", encoding="utf-8") as f:
#         reader = csv.reader(f, quoting=csv.QUOTE_ALL)
#         data = list(reader)
#     chat_content = "\n".join([" ".join(row) for row in data])
#     return chat_content[-15000:]

#     with open(f"sample/sample002.txt", mode="r", encoding="utf-8") as f:
#         chat_content = f.read()
#     return chat_content


# if __name__ == "__main__":
#     a = main()
#     print(a)
