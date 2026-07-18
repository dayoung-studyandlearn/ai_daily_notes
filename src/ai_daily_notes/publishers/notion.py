from notion_client import Client

from ai_daily_notes.config import get_notion_api_key, get_notion_database_id
from ai_daily_notes.models import DailyNote


def _rich_text(content: str) -> list[dict]:
    return [{"type": "text", "text": {"content": content}}]


def _heading(content: str) -> dict:
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": _rich_text(content)},
    }


def _paragraph(content: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": _rich_text(content)},
    }


def _bulleted_item(content: str) -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": _rich_text(content)},
    }


def _code_block(content: str, language: str) -> dict:
    return {
        "object": "block",
        "type": "code",
        "code": {"rich_text": _rich_text(content), "language": language},
    }


def _build_blocks(note: DailyNote) -> list[dict]:
    blocks = [_heading("오늘의 AI 뉴스")]
    for item in note.news:
        blocks.append(_bulleted_item(f"{item.title} — {item.summary}"))

    blocks += [
        _heading(f"오늘의 개념: {note.concept.title}"),
        _paragraph(note.concept.explanation),
        _heading(f"오늘의 용어: {note.term.word}"),
        _paragraph(note.term.definition),
        _heading("예제 코드"),
        _code_block(note.code_example.code, note.code_example.language),
        _paragraph(note.code_example.description),
        _heading("실무 팁"),
        _paragraph(note.tip),
        _heading("오늘의 퀴즈"),
        _paragraph(f"Q. {note.quiz.question}"),
        _paragraph(f"A. {note.quiz.answer}"),
        _heading("내일 공부할 내용"),
    ]
    blocks += [_bulleted_item(topic) for topic in note.tomorrow_topics]
    return blocks


def _find_data_source(client: Client, database_id: str) -> tuple[str, str]:
    """데이터베이스 안의 data source ID와, 그 안에서 title 타입인 속성 이름을 찾는다.

    Notion은 데이터베이스 하나가 여러 data source를 가질 수 있는 구조로 바뀌었고,
    제목 속성 이름도 계정 언어 설정에 따라 "Name"이 아닐 수 있다 (예: "이름").
    그래서 하드코딩하지 않고, 매번 실제 구조를 물어봐서 알아낸다.
    """
    database = client.databases.retrieve(database_id)
    data_source_id = database["data_sources"][0]["id"]

    data_source = client.data_sources.retrieve(data_source_id)
    title_property = next(
        name for name, prop in data_source["properties"].items() if prop["type"] == "title"
    )
    return data_source_id, title_property


def publish_note(note: DailyNote) -> str:
    client = Client(auth=get_notion_api_key())
    data_source_id, title_property = _find_data_source(client, get_notion_database_id())

    page = client.pages.create(
        parent={"type": "data_source_id", "data_source_id": data_source_id},
        properties={
            title_property: {
                "title": _rich_text(f"{note.note_date.isoformat()} AI Daily Note")
            }
        },
        children=_build_blocks(note),
    )
    return page["url"]
