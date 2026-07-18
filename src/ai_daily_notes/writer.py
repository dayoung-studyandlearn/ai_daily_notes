from pathlib import Path

from ai_daily_notes.models import DailyNote

NOTES_DIR = Path(__file__).resolve().parent.parent.parent / "notes"


def render_markdown(note: DailyNote) -> str:
    lines = [
        f"# {note.note_date.isoformat()} AI Daily Note",
        "",
        "## 오늘의 AI 뉴스",
    ]
    for item in note.news:
        lines.append(f"- [{item.title}]({item.url}) — {item.summary}")

    lines += [
        "",
        f"## 오늘의 개념: {note.concept.title}",
        note.concept.explanation,
        "",
        f"## 오늘의 용어: {note.term.word}",
        note.term.definition,
        "",
        "## 예제 코드",
        f"```{note.code_example.language}",
        note.code_example.code,
        "```",
        note.code_example.description,
        "",
        "## 실무 팁",
        note.tip,
        "",
        "## 오늘의 퀴즈",
        f"Q. {note.quiz.question}",
        f"A. {note.quiz.answer}",
        "",
        "## 내일 공부할 내용",
    ]
    lines += [f"- {topic}" for topic in note.tomorrow_topics]

    return "\n".join(lines) + "\n"


def save_note(note: DailyNote) -> Path:
    NOTES_DIR.mkdir(exist_ok=True)
    path = NOTES_DIR / f"{note.note_date.isoformat()}.md"
    path.write_text(render_markdown(note), encoding="utf-8")
    return path
