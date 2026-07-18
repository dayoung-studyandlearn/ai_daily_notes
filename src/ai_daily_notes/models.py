from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class NewsItem:
    title: str
    url: str
    summary: str


@dataclass(frozen=True)
class Concept:
    title: str
    explanation: str


@dataclass(frozen=True)
class Term:
    word: str
    definition: str


@dataclass(frozen=True)
class CodeExample:
    description: str
    language: str
    code: str


@dataclass(frozen=True)
class Quiz:
    question: str
    answer: str


@dataclass(frozen=True)
class DailyNote:
    """하루치 학습 노트 전체를 묶는 최상위 데이터 구조 (aggregate root)."""

    note_date: date
    news: tuple[NewsItem, ...]
    concept: Concept
    term: Term
    code_example: CodeExample
    tip: str
    quiz: Quiz
    tomorrow_topics: tuple[str, ...]
