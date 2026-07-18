"""
2026-07-18 노트에서 배운 두 가지를 직접 코드로 만져봅니다.
- LLM: "다음 단어를 확률로 예측해서 이어 붙인다"
- API: "메뉴판(정해진 규칙)으로 주문하고 답을 받는다"

API 키 없이, 인터넷 연결 없이 그냥 실행하면 됩니다.
"""

import random


# ── 실습 1: LLM 흉내내기 ────────────────────────────────
#
# 진짜 LLM은 수억~수천억 개의 글을 보고 이 확률표를 스스로 학습합니다.
# 여기서는 그 원리만 아주 작게 흉내내기 위해, 확률표를 직접 손으로 적어봤습니다.
# "오늘"이라는 단어 다음에 어떤 단어가 나올 확률이 높은지를 정해둔 것입니다.

NEXT_WORD_PROBABILITIES = {
    "오늘": [("날씨가", 0.5), ("저녁에", 0.3), ("아침에", 0.2)],
    "날씨가": [("좋다", 0.6), ("춥다", 0.2), ("덥다", 0.2)],
    "저녁에": [("치킨을", 0.4), ("공부를", 0.4), ("운동을", 0.2)],
}


def predict_next_word(word: str) -> str:
    """word 다음에 올 단어를, 확률에 따라 하나 골라서 돌려줍니다."""
    candidates = NEXT_WORD_PROBABILITIES.get(word)
    if candidates is None:
        return "(더 이상 아는 단어가 없어요)"

    words, weights = zip(*candidates)
    return random.choices(words, weights=weights, k=1)[0]


def generate_sentence(start_word: str, steps: int = 3) -> str:
    """시작 단어부터 predict_next_word를 반복 호출해서 문장을 이어붙입니다."""
    sentence = [start_word]
    current = start_word
    for _ in range(steps):
        next_word = predict_next_word(current)
        if next_word.startswith("("):
            break
        sentence.append(next_word)
        current = next_word
    return " ".join(sentence)


# ── 실습 2: API 흉내내기 ────────────────────────────────
#
# 노트에서 설명한 "손님 - 메뉴판 - 웨이터 - 주방" 비유를 그대로 코드로 옮겨봤습니다.
# 진짜 Claude API도 이 구조와 똑같습니다: 정해진 형식(menu)으로 요청을 보내면,
# 정해진 형식으로 답이 돌아옵니다.

MENU = {
    "인사": "안녕하세요! 무엇을 도와드릴까요?",
    "날씨": "오늘 날씨는 맑음입니다.",
}


def call_api(request_type: str) -> str:
    """진짜 API 호출을 흉내낸 함수. request_type(주문)을 받아서 정해진 답을 돌려줍니다."""
    if request_type not in MENU:
        return "메뉴에 없는 주문입니다. (실제 API였다면 에러가 났을 거예요)"
    return MENU[request_type]


if __name__ == "__main__":
    print("=== 실습 1: LLM 흉내내기 ===")
    for _ in range(3):
        print(generate_sentence("오늘"))

    print()
    print("=== 실습 2: API 흉내내기 ===")
    print(call_api("인사"))
    print(call_api("날씨"))
    print(call_api("없는메뉴"))
