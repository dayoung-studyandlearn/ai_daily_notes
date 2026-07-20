from datetime import date

from ai_daily_notes.models import CodeExample, Concept, DailyNote, NewsItem, Quiz, Term
from ai_daily_notes.publishers.discord import _build_payload, _format_links, _teaser


def _make_sample_note() -> DailyNote:
    return DailyNote(
        note_date=date(2026, 7, 18),
        news=(NewsItem("샘플 뉴스", "https://example.com", "요약"),),
        concept=Concept("샘플 개념", "설명"),
        term=Term("샘플 용어", "정의"),
        code_example=CodeExample("설명", "python", "print(1)"),
        tip="팁",
        quiz=Quiz("샘플 질문", "샘플 답"),
        tomorrow_topics=("주제1",),
    )


def test_build_payload_includes_concept_title_and_note_url():
    note = _make_sample_note()
    payload = _build_payload(note, "https://example.com/note")

    embed = payload["embeds"][0]
    assert "샘플 개념" in embed["title"]
    assert embed["url"] == "https://example.com/note"


def test_build_payload_prefers_notion_url_when_given():
    note = _make_sample_note()
    payload = _build_payload(
        note, "https://example.com/github", notion_url="https://example.com/notion"
    )

    embed = payload["embeds"][0]
    assert embed["url"] == "https://example.com/notion"

    links_field = next(f for f in embed["fields"] if f["name"] == "링크")
    assert "https://example.com/github" in links_field["value"]
    assert "https://example.com/notion" in links_field["value"]


def test_format_links_omits_notion_when_not_given():
    links = _format_links("https://example.com/github", None)
    assert "github" in links.lower()
    assert "notion" not in links.lower()


def test_teaser_truncates_long_text_and_leaves_short_text_alone():
    short_text = "짧은 문장"
    assert _teaser(short_text, limit=100) == short_text

    long_text = "가" * 400
    truncated = _teaser(long_text, limit=300)
    assert len(truncated) == 303  # 300자 + "..."
    assert truncated.endswith("...")
