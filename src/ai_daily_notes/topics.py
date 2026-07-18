from pathlib import Path

TOPICS_FILE = Path(__file__).resolve().parent.parent.parent / "topics.txt"


def _read_lines() -> list[str]:
    if not TOPICS_FILE.exists():
        return []
    lines = TOPICS_FILE.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip()]


def pop_next_topic() -> str | None:
    """topics.txt 맨 위 줄을 오늘의 주제로 꺼내고, 파일에서는 지운다."""
    topics = _read_lines()
    if not topics:
        return None

    today_topic, *rest = topics
    remaining_text = "\n".join(rest) + ("\n" if rest else "")
    TOPICS_FILE.write_text(remaining_text, encoding="utf-8")
    return today_topic


def peek_upcoming(count: int = 2) -> tuple[str, ...]:
    """다음 학습 주제 몇 개를 미리 살펴본다 (파일은 건드리지 않는다)."""
    return tuple(_read_lines()[:count])
