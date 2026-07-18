from anthropic import Anthropic

from ai_daily_notes.config import get_anthropic_api_key
from ai_daily_notes.generators import BEGINNER_AUDIENCE
from ai_daily_notes.models import CodeExample

_MODEL = "claude-sonnet-5"

_SUBMIT_CODE_EXAMPLE_TOOL = {
    "name": "submit_code_example",
    "description": "오늘의 예제 코드를 제출한다.",
    "input_schema": {
        "type": "object",
        "properties": {
            "description": {
                "type": "string",
                "description": "이 코드가 무엇을 보여주는지 2~3문장 설명",
            },
            "language": {"type": "string", "description": "코드 언어 (예: python)"},
            "code": {"type": "string", "description": "짧고 실행 가능한 예제 코드"},
        },
        "required": ["description", "language", "code"],
    },
}


def generate_code_example(topic: str) -> CodeExample:
    client = Anthropic(api_key=get_anthropic_api_key())

    response = client.messages.create(
        model=_MODEL,
        max_tokens=1024,
        tools=[_SUBMIT_CODE_EXAMPLE_TOOL],
        tool_choice={"type": "tool", "name": "submit_code_example"},
        messages=[
            {
                "role": "user",
                "content": (
                    f"{BEGINNER_AUDIENCE} 이런 사람을 위해 '{topic}'과 관련된 아주 짧은 "
                    "파이썬 예제 코드를 하나 만들어줘. 20줄을 넘지 않게, 한 줄씩 무엇을 "
                    "하는지 주석으로 설명해줘. 파이썬 문법 자체가 낯설 수 있다는 것도 감안해줘."
                ),
            }
        ],
    )

    tool_use_block = next(block for block in response.content if block.type == "tool_use")
    return CodeExample(**tool_use_block.input)
