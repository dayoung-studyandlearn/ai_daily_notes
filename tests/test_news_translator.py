import pytest

from ai_daily_notes.generators.news_translator import _apply_translations
from ai_daily_notes.models import NewsItem


def test_apply_translations_keeps_original_url_and_swaps_text():
    items = (
        NewsItem("English title", "https://example.com/1", "English summary"),
    )
    translations = [{"title": "한글 제목", "summary": "한글 요약"}]

    result = _apply_translations(items, translations)

    assert result[0].title == "한글 제목"
    assert result[0].summary == "한글 요약"
    assert result[0].url == "https://example.com/1"


def test_apply_translations_raises_on_count_mismatch():
    items = (
        NewsItem("A", "https://example.com/1", "a"),
        NewsItem("B", "https://example.com/2", "b"),
    )
    translations = [{"title": "번역A", "summary": "요약A"}]  # 1개뿐 -> 원본은 2개

    with pytest.raises(ValueError):
        _apply_translations(items, translations)
