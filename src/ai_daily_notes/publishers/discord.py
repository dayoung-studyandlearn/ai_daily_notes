import requests

from ai_daily_notes.config import get_discord_webhook_url
from ai_daily_notes.models import DailyNote

_TEASER_LENGTH = 300


def _teaser(text: str, limit: int = _TEASER_LENGTH) -> str:
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def _build_payload(note: DailyNote, note_url: str) -> dict:
    return {
        "embeds": [
            {
                "title": f"오늘의 AI 노트: {note.concept.title}",
                "description": _teaser(note.concept.explanation),
                "url": note_url,
                "color": 0x5865F2,  # Discord 브랜드 색
                "fields": [
                    {"name": "오늘의 용어", "value": note.term.word, "inline": True},
                    {"name": "오늘의 퀴즈", "value": _teaser(note.quiz.question, 150)},
                ],
            }
        ]
    }


def notify_note(note: DailyNote, note_url: str) -> None:
    webhook_url = get_discord_webhook_url()
    payload = _build_payload(note, note_url)

    response = requests.post(webhook_url, json=payload, timeout=10)
    response.raise_for_status()
