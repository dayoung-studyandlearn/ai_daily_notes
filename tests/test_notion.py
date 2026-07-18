from datetime import date

from ai_daily_notes.models import CodeExample, Concept, DailyNote, NewsItem, Quiz, Term
from ai_daily_notes.publishers.notion import _build_blocks


def _make_sample_note() -> DailyNote:
    return DailyNote(
        note_date=date(2026, 7, 18),
        news=(NewsItem("샘플 뉴스", "https://example.com", "요약"),),
        concept=Concept("샘플 개념", "설명"),
        term=Term("샘플 용어", "정의"),
        code_example=CodeExample("설명", "python", "print(1)"),
        tip="팁",
        quiz=Quiz("질문", "답"),
        tomorrow_topics=("주제1", "주제2"),
    )


def test_build_blocks_includes_code_block_with_correct_language():
    note = _make_sample_note()
    blocks = _build_blocks(note)

    code_blocks = [b for b in blocks if b["type"] == "code"]
    assert len(code_blocks) == 1
    assert code_blocks[0]["code"]["language"] == "python"
    assert code_blocks[0]["code"]["rich_text"][0]["text"]["content"] == "print(1)"


def test_build_blocks_includes_a_bullet_per_tomorrow_topic():
    note = _make_sample_note()
    blocks = _build_blocks(note)

    bullet_texts = [
        b["bulleted_list_item"]["rich_text"][0]["text"]["content"]
        for b in blocks
        if b["type"] == "bulleted_list_item"
    ]
    assert "주제1" in bullet_texts
    assert "주제2" in bullet_texts
