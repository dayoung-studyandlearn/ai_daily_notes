from datetime import date

from ai_daily_notes.models import CodeExample, Concept, DailyNote, NewsItem, Quiz, Term
from ai_daily_notes.writer import render_markdown


def _make_sample_note() -> DailyNote:
    return DailyNote(
        note_date=date(2026, 7, 18),
        news=(NewsItem("샘플 뉴스 제목", "https://example.com", "뉴스 요약"),),
        concept=Concept("샘플 개념", "개념 설명 내용"),
        term=Term("샘플 용어", "용어 정의"),
        code_example=CodeExample("코드 설명", "python", "print(1)"),
        tip="샘플 팁",
        quiz=Quiz("샘플 질문", "샘플 답"),
        tomorrow_topics=("내일 주제1", "내일 주제2"),
    )


def test_render_markdown_includes_every_section():
    note = _make_sample_note()
    markdown = render_markdown(note)

    assert "샘플 개념" in markdown
    assert "샘플 용어" in markdown
    assert "print(1)" in markdown
    assert "샘플 질문" in markdown
    assert "내일 주제1" in markdown
    assert "내일 주제2" in markdown


def test_render_markdown_starts_with_date_heading():
    note = _make_sample_note()
    markdown = render_markdown(note)

    assert markdown.startswith("# 2026-07-18")
