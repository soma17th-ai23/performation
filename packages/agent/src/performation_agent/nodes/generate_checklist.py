from __future__ import annotations

from performation_agent.state import GuideState


DEFAULT_CHECKLIST = [
  "모바일 티켓 또는 예매 내역 확인",
  "신분증 필요 여부 확인",
  "보조배터리 준비",
  "공연장 도착 추천 시간 확인",
  "물품보관 운영 여부 확인",
  "공연 종료 후 교통 혼잡 가능성 확인",
  "공식 공지에서 최종 변동 사항 확인",
]


def generate_checklist(state: GuideState) -> GuideState:
  if state.get("venue") is None:
    checklist = ["공식 예매처 또는 공연 공지에서 공연장 정보를 먼저 확인하기"]
  else:
    checklist = DEFAULT_CHECKLIST

  return {"checklist": checklist}
