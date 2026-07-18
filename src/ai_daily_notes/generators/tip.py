from anthropic import Anthropic

from ai_daily_notes.config import get_anthropic_api_key
from ai_daily_notes.generators import BEGINNER_AUDIENCE

_MODEL = "claude-sonnet-5"

_SUBMIT_TIP_TOOL = {
    "name": "submit_tip",
    "description": "오늘의 실무 팁을 제출한다.",
    "input_schema": {
        "type": "object",
        "properties": {
            "tip": {
                "type": "string",
                "description": "AI/개발 실무에서 바로 써먹을 수 있는 구체적인 팁, 1~2문장",
            },
        },
        "required": ["tip"],
    },
}


def generate_tip(topic: str) -> str:
    client = Anthropic(api_key=get_anthropic_api_key())

    response = client.messages.create(
        model=_MODEL,
        max_tokens=1024,
        tools=[_SUBMIT_TIP_TOOL],
        tool_choice={"type": "tool", "name": "submit_tip"},
        messages=[
            {
                "role": "user",
                "content": (
                    f"{BEGINNER_AUDIENCE} 이런 사람을 위해 '{topic}'과 관련해서 "
                    "실제로 도움이 될 팁을 하나 알려줘. 막연한 조언 말고, "
                    "바로 적용해볼 수 있을 만큼 구체적으로."
                ),
            }
        ],
    )

    tool_use_block = next(block for block in response.content if block.type == "tool_use")
    return tool_use_block.input["tip"]
