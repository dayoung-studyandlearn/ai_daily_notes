import requests

from ai_daily_notes.config import get_discord_webhook_url
from ai_daily_notes.models import DailyNote

_TEASER_LENGTH = 300


def _teaser(text: str, limit: int = _TEASER_LENGTH) -> str:
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def _format_links(github_url: str, notion_url: str | None) -> str:
    links = [f"[GitHub]({github_url})"]
    if notion_url:
        links.append(f"[Notion]({notion_url})")
    return " · ".join(links)


def _build_payload(note: DailyNote, github_url: str, notion_url: str | None = None) -> dict:
    return {
        "embeds": [
            {
                "title": f"오늘의 AI 노트: {note.concept.title}",
                "description": _teaser(note.concept.explanation),
                "url": notion_url or github_url,
                "color": 0x5865F2,  # Discord 브랜드 색
                "fields": [
                    {"name": "오늘의 용어", "value": note.term.word, "inline": True},
                    {"name": "오늘의 퀴즈", "value": _teaser(note.quiz.question, 150)},
                    {"name": "링크", "value": _format_links(github_url, notion_url)},
                ],
            }
        ]
    }


def notify_note(note: DailyNote, github_url: str, notion_url: str | None = None) -> None:
    webhook_url = get_discord_webhook_url()
    payload = _build_payload(note, github_url, notion_url)

    response = requests.post(webhook_url, json=payload, timeout=10)
    response.raise_for_status()
