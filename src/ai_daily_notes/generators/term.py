from anthropic import Anthropic

from ai_daily_notes.config import get_anthropic_api_key
from ai_daily_notes.generators import BEGINNER_AUDIENCE
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
                "description": "완전 초보자도 이해할 수 있는 2~3문장 정의. 전문 용어는 풀어서 설명",
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
                    f"{BEGINNER_AUDIENCE} 이런 사람을 위해 '{topic}'과 관련된 "
                    "오늘의 용어를 하나 골라 정의해줘."
                ),
            }
        ],
    )

    tool_use_block = next(block for block in response.content if block.type == "tool_use")
    return Term(**tool_use_block.input)
