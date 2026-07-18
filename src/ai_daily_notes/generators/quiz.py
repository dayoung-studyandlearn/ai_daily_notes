from anthropic import Anthropic

from ai_daily_notes.config import get_anthropic_api_key
from ai_daily_notes.generators import BEGINNER_AUDIENCE
from ai_daily_notes.models import Quiz

_MODEL = "claude-sonnet-5"

_SUBMIT_QUIZ_TOOL = {
    "name": "submit_quiz",
    "description": "오늘의 퀴즈 질문과 답을 제출한다.",
    "input_schema": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "오늘 배운 개념을 이해했는지 확인하는 질문",
            },
            "answer": {
                "type": "string",
                "description": "질문에 대한 명확한 답, 2~3문장",
            },
        },
        "required": ["question", "answer"],
    },
}


def generate_quiz(topic: str) -> Quiz:
    client = Anthropic(api_key=get_anthropic_api_key())

    response = client.messages.create(
        model=_MODEL,
        max_tokens=1024,
        tools=[_SUBMIT_QUIZ_TOOL],
        tool_choice={"type": "tool", "name": "submit_quiz"},
        messages=[
            {
                "role": "user",
                "content": (
                    f"{BEGINNER_AUDIENCE} 이런 사람이 '{topic}'을 제대로 이해했는지 "
                    "확인할 수 있는 퀴즈 질문과 답을 하나 만들어줘. 암기보다는 "
                    "개념 이해를 확인하는 질문으로, 답도 완전 초보자가 이해할 수 있게 써줘."
                ),
            }
        ],
    )

    tool_use_block = next(block for block in response.content if block.type == "tool_use")
    return Quiz(**tool_use_block.input)
