from anthropic import Anthropic

from ai_daily_notes.config import get_anthropic_api_key
from ai_daily_notes.models import Concept

_MODEL = "claude-sonnet-5"

_SUBMIT_CONCEPT_TOOL = {
    "name": "submit_concept",
    "description": "오늘의 AI 개념 설명을 제출한다.",
    "input_schema": {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "개념 이름"},
            "explanation": {
                "type": "string",
                "description": "AI 입문자도 이해할 수 있는 3~5문장 설명",
            },
        },
        "required": ["title", "explanation"],
    },
}


def generate_concept(topic: str) -> Concept:
    client = Anthropic(api_key=get_anthropic_api_key())

    response = client.messages.create(
        model=_MODEL,
        max_tokens=1024,
        tools=[_SUBMIT_CONCEPT_TOOL],
        tool_choice={"type": "tool", "name": "submit_concept"},
        messages=[
            {
                "role": "user",
                "content": (
                    f"AI를 공부하는 사람을 위해 '{topic}'과 관련된 오늘의 개념을 "
                    "하나 골라 설명해줘. 전문 용어를 남발하지 말고, 입문자가 "
                    "이해할 수 있는 눈높이로 써줘."
                ),
            }
        ],
    )

    tool_use_block = next(block for block in response.content if block.type == "tool_use")
    return Concept(**tool_use_block.input)
