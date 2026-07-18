import os

from dotenv import load_dotenv

load_dotenv()


def get_anthropic_api_key() -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY가 설정되어 있지 않습니다. "
            ".env.example을 복사해 .env 파일을 만들고 키를 채워주세요."
        )
    return api_key


def get_notion_api_key() -> str | None:
    """Notion은 선택적 연동이라, 없으면 에러 대신 None을 돌려준다."""
    return os.environ.get("NOTION_API_KEY") or None


def get_notion_database_id() -> str | None:
    return os.environ.get("NOTION_DATABASE_ID") or None


def get_discord_webhook_url() -> str | None:
    """Discord 알림도 선택적 연동이라, 없으면 에러 대신 None을 돌려준다."""
    return os.environ.get("DISCORD_WEBHOOK_URL") or None
