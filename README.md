# AI Daily Notes

매일 하나의 Markdown 노트를 자동으로 생성하는 개인 AI 학습 비서입니다.
단순 요약기가 아니라, 꾸준히 AI를 공부하고 실무 감각을 기르기 위한 도구를 목표로 합니다.

## 왜 만드나요

- 매일 AI 개념 / 용어 / 예제 코드 / 실무 팁 / 퀴즈를 담은 노트를 자동 생성
- 코드를 읽으며 성장할 수 있도록, 실무에서 쓰는 프로젝트 구조를 그대로 따라감
- 처음부터 다 만들지 않고, 설계 → 구현 → 리뷰 → 리팩토링을 반복하며 단계적으로 성장

## 프로젝트 구조

```
src/ai_daily_notes/
├── models.py         # 노트를 구성하는 데이터 구조
├── collectors/        # 재료 수집 (RSS 뉴스)
├── generators/         # Claude API로 콘텐츠 생성 (개념/용어/예제코드/팁/퀴즈)
├── publishers/          # 선택적 배포 채널 (Notion 등, 없으면 건너뜀)
├── assembler.py         # 조각들을 하나의 노트로 조립
├── writer.py             # Markdown 파일로 저장 (덮어쓰기 방지 내장)
├── topics.py             # topics.txt에서 오늘의 주제를 하나씩 꺼내옴
└── main.py               # ai-daily-notes 콘솔 명령어 진입점

topics.txt               # 앞으로 다룰 학습 주제 목록 (한 줄에 하나씩, 직접 관리)
notes/                    # 매일 생성되는 노트 (git으로 추적됨)
practice/                 # 배운 내용을 직접 코드로 연습하는 공간 (git으로 추적)
.github/workflows/        # 매일 아침 자동 실행하는 GitHub Actions 설정
```

## 실행 방법

```bash
# topics.txt 맨 위 줄을 오늘의 주제로 자동 사용
ai-daily-notes

# 주제를 직접 지정하고 싶을 때
ai-daily-notes "주제명" --tomorrow "다음 주제"
```

Notion에도 등록하려면 `.env`에 `NOTION_API_KEY`, `NOTION_DATABASE_ID`를 채워주세요 (둘 다 선택 사항이며, 없으면 자동으로 건너뜁니다).

## 현재 진행 상황

- [x] 프로젝트 뼈대 세팅
- [x] 노트 데이터 모델 정의
- [x] Markdown 조립 및 저장 (덮어쓰기 방지 포함)
- [x] 테스트 코드
- [x] 실습 공간(practice/) 마련
- [x] Claude API로 콘텐츠 생성
- [x] 뉴스 수집(RSS) 연동
- [x] 자동화(GitHub Actions) — 매일 한국 시간 오전 7시 자동 실행
- [x] Notion 저장 연동 (선택 사항)
