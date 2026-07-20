import argparse
from datetime import date

from ai_daily_notes.assembler import assemble_note
from ai_daily_notes.collectors.rss import fetch_news
from ai_daily_notes.config import (
    get_discord_webhook_url,
    get_notion_api_key,
    get_notion_database_id,
)
from ai_daily_notes.generators.news_translator import translate_news
from ai_daily_notes.publishers.discord import notify_note
from ai_daily_notes.publishers.notion import publish_note
from ai_daily_notes.topics import peek_upcoming, pop_next_topic
from ai_daily_notes.writer import note_path_for, save_note

DEFAULT_FEED_URL = "https://www.artificialintelligence-news.com/feed/"
GITHUB_REPO_URL = "https://github.com/dayoung-studyandlearn/ai_daily_notes"


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
    news = translate_news(news)
    note = assemble_note(
        topic=topic,
        tomorrow_topics=tuple(args.tomorrow) or peek_upcoming(2) or ("topics.txt에 새 주제를 추가해주세요",),
        news=news,
        note_date=target_date,
    )
    path = save_note(note, overwrite=args.force)
    print(f"오늘의 노트를 저장했습니다: {path}")

    github_url = f"{GITHUB_REPO_URL}/blob/main/notes/{target_date.isoformat()}.md"
    notion_url = None

    if get_notion_api_key() and get_notion_database_id():
        notion_url = publish_note(note)
        print(f"Notion에도 등록했습니다: {notion_url}")
    else:
        print(
            "Notion 연동이 설정되어 있지 않아 건너뜁니다. "
            "(.env에 NOTION_API_KEY, NOTION_DATABASE_ID를 추가하면 활성화됩니다)"
        )

    if get_discord_webhook_url():
        notify_note(note, github_url, notion_url=notion_url)
        print("Discord에도 알림을 보냈습니다.")
    else:
        print(
            "Discord 연동이 설정되어 있지 않아 건너뜁니다. "
            "(.env에 DISCORD_WEBHOOK_URL을 추가하면 활성화됩니다)"
        )


if __name__ == "__main__":
    main()
