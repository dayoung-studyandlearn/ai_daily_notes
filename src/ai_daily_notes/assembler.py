from datetime import date

from ai_daily_notes.generators.code_example import generate_code_example
from ai_daily_notes.generators.concept import generate_concept
from ai_daily_notes.generators.quiz import generate_quiz
from ai_daily_notes.generators.term import generate_term
from ai_daily_notes.generators.tip import generate_tip
from ai_daily_notes.models import DailyNote, NewsItem


def assemble_note(
    topic: str,
    tomorrow_topics: tuple[str, ...],
    news: tuple[NewsItem, ...] = (),
    note_date: date | None = None,
) -> DailyNote:
    return DailyNote(
        note_date=note_date or date.today(),
        news=news,
        concept=generate_concept(topic),
        term=generate_term(topic),
        code_example=generate_code_example(topic),
        tip=generate_tip(topic),
        quiz=generate_quiz(topic),
        tomorrow_topics=tomorrow_topics,
    )
