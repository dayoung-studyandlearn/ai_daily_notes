import html
import re

import feedparser

from ai_daily_notes.models import NewsItem

_HTML_TAG = re.compile(r"<[^>]+>")


def _strip_html(text: str) -> str:
    """RSS 요약에 섞여 오는 HTML 태그를 제거하고 순수 텍스트만 남긴다."""
    return html.unescape(_HTML_TAG.sub("", text)).strip()


def fetch_news(feed_url: str, limit: int = 3) -> tuple[NewsItem, ...]:
    feed = feedparser.parse(feed_url)

    news_items = []
    for entry in feed.entries[:limit]:
        news_items.append(
            NewsItem(
                title=entry.get("title", "(제목 없음)"),
                url=entry.get("link", ""),
                summary=_strip_html(entry.get("summary", "")),
            )
        )
    return tuple(news_items)
