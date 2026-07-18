import argparse
from datetime import date

from ai_daily_notes.assembler import assemble_note
from ai_daily_notes.collectors.rss import fetch_news
from ai_daily_notes.topics import peek_upcoming, pop_next_topic
from ai_daily_notes.writer import note_path_for, save_note

DEFAULT_FEED_URL = "https://www.artificialintelligence-news.com/feed/"


def main() -> None:
    parser = argparse.ArgumentParser(description="오늘의 AI 학습 노트를 생성합니다.")
    parser.add_argument(
        "topic",
        nargs="?",
        default=None,
        help="오늘 다룰 AI 개념/용어 주제. 생략하면 topics.txt 맨 위 줄을 자동으로 씁니다.",
    )
    parser.add_argument(
        "--tomorrow",
        action="append",
        default=[],
        help="내일 공부할 주제 (여러 번 지정하면 여러 개가 들어갑니다)",
    )
    parser.add_argument(
        "--feed-url",
        default=DEFAULT_FEED_URL,
        help="뉴스를 가져올 RSS 주소",
    )
    parser.add_argument(
        "--date",
        type=date.fromisoformat,
        default=None,
        help="노트 날짜 (YYYY-MM-DD). 지정하지 않으면 오늘 날짜를 씁니다.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="같은 날짜의 노트가 이미 있어도 덮어씁니다.",
    )
    args = parser.parse_args()
    target_date = args.date or date.today()

    # API 호출(비용 발생)을 시작하기 전에, 먼저 파일이 이미 있는지부터 확인한다.
    existing_path = note_path_for(target_date)
    if existing_path.exists() and not args.force:
        raise SystemExit(
            f"{existing_path.name}가 이미 있습니다. "
            "--force 옵션을 추가하면 덮어쓸 수 있습니다."
        )

    # topic이 주어지지 않았을 때만 topics.txt에서 꺼낸다 (실패할 run에서 괜히 소비하지 않도록).
    topic = args.topic or pop_next_topic()
    if topic is None:
        raise SystemExit("topics.txt에 학습 주제가 없습니다. 한 줄씩 추가해주세요.")

    news = fetch_news(args.feed_url, limit=3)
    note = assemble_note(
        topic=topic,
        tomorrow_topics=tuple(args.tomorrow) or peek_upcoming(2) or ("topics.txt에 새 주제를 추가해주세요",),
        news=news,
        note_date=target_date,
    )
    path = save_note(note, overwrite=args.force)
    print(f"오늘의 노트를 저장했습니다: {path}")


if __name__ == "__main__":
    main()
