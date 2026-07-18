from anthropic import Anthropic

from ai_daily_notes.config import get_anthropic_api_key
from ai_daily_notes.models import Term

_MODEL = "claude-sonnet-5"

_SUBMIT_TERM_TOOL = {
    "name": "submit_term",
    "description": "오늘의 AI 용어와 정의를 제출한다.",
    "input_schema": {
        "type": "object",
        "properties": {
            "word": {"type": "string", "description": "용어 (한글, 필요시 영문 병기)"},
            "definition": {
                "type": "string",
                "description": "AI 입문자도 이해할 수 있는 2~3문장 정의",
            },
        },
        "required": ["word", "definition"],
    },
}


def generate_term(topic: str) -> Term:
    client = Anthropic(api_key=get_anthropic_api_key())

    response = client.messages.create(
        model=_MODEL,
        max_tokens=1024,
        tools=[_SUBMIT_TERM_TOOL],
        tool_choice={"type": "tool", "name": "submit_term"},
        messages=[
            {
                "role": "user",
                "content": (
                    f"AI를 공부하는 사람을 위해 '{topic}'과 관련된 오늘의 용어를 "
                    "하나 골라 정의해줘. 전문 용어를 쓸 때도 쉬운 말로 풀어서 설명해줘."
                ),
            }
        ],
    )

    tool_use_block = next(block for block in response.content if block.type == "tool_use")
    return Term(**tool_use_block.input)
