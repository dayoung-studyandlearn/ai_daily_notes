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
