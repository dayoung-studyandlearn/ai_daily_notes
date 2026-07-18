from anthropic import Anthropic

from ai_daily_notes.config import get_anthropic_api_key
from ai_daily_notes.models import NewsItem

_MODEL = "claude-sonnet-5"

_SUBMIT_TRANSLATIONS_TOOL = {
    "name": "submit_translations",
    "description": "뉴스 제목과 요약을 한국어로 번역해서 제출한다.",
    "input_schema": {
        "type": "object",
        "properties": {
            "translations": {
                "type": "array",
                "description": "입력받은 뉴스와 같은 순서, 같은 개수로 번역 결과를 담는다",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "한국어로 번역된 제목"},
                        "summary": {"type": "string", "description": "한국어로 번역된 요약"},
                    },
                    "required": ["title", "summary"],
                },
            },
        },
        "required": ["translations"],
    },
}


def _build_translation_prompt(items: tuple[NewsItem, ...]) -> str:
    numbered = "\n\n".join(
        f"{i}. 제목: {item.title}\n요약: {item.summary}"
        for i, item in enumerate(items, start=1)
    )
    return (
        f"다음 AI 뉴스 {len(items)}개의 제목과 요약을 자연스러운 한국어로 번역해줘. "
        "영어를 모르는 사람이 읽을 거라, 직역보다는 뜻이 잘 통하게 번역해줘. "
        "번역 순서는 원문 순서와 똑같이 유지해줘.\n\n" + numbered
    )


def _apply_translations(items: tuple[NewsItem, ...], translations: list[dict]) -> tuple[NewsItem, ...]:
    if len(translations) != len(items):
        raise ValueError(
            f"번역 결과 개수({len(translations)})가 원본 뉴스 개수({len(items)})와 다릅니다."
        )

    return tuple(
        NewsItem(title=t["title"], url=item.url, summary=t["summary"])
        for item, t in zip(items, translations)
    )


def translate_news(items: tuple[NewsItem, ...]) -> tuple[NewsItem, ...]:
    if not items:
        return items

    client = Anthropic(api_key=get_anthropic_api_key())

    response = client.messages.create(
        model=_MODEL,
        max_tokens=2048,
        tools=[_SUBMIT_TRANSLATIONS_TOOL],
        tool_choice={"type": "tool", "name": "submit_translations"},
        messages=[{"role": "user", "content": _build_translation_prompt(items)}],
    )

    tool_use_block = next(block for block in response.content if block.type == "tool_use")
    return _apply_translations(items, tool_use_block.input["translations"])
