from __future__ import annotations

from performation_agent.state import GuideDraft, GuideState


DEFAULT_CHECKLIST = [
  "모바일 티켓 또는 예매 내역 확인",
  "신분증 필요 여부 확인",
  "보조배터리 준비",
  "공연장 도착 추천 시간 확인",
  "물품보관 운영 여부 확인",
  "공연 종료 후 교통 혼잡 가능성 확인",
  "공식 공지에서 최종 변동 사항 확인",
]


def build_deterministic_guide_draft(state: GuideState) -> GuideDraft:
  venue = state.get("venue")

  if venue is None:
    return {
      "summary": [
        "현재 MVP는 KSPO DOME, Blue Square, YES24 Live Hall 중심으로 지원합니다.",
        "공연장명, 공연 날짜, 아티스트명 또는 예매처 링크를 추가하면 더 정확히 확인할 수 있습니다.",
      ],
      "checklist": ["공식 예매처 또는 공연 공지에서 공연장 정보를 먼저 확인하기"],
      "transit_and_entry_tips": [],
      "official_check_required": ["공연장명", "공연 날짜", "아티스트명", "예매처 공지"],
    }

  search_summary = (
    "공개 웹 검색 결과와 로컬 공연장 데이터를 함께 참고했습니다."
    if state.get("search_results")
    else "검색 결과가 없거나 검색 provider가 꺼져 있어 로컬 공연장 데이터 기반으로 안내합니다."
  )
  return {
    "summary": [
      f"{venue.name} 방문 전에는 입장 위치, 도착 시간, 물품보관 운영 여부를 공연별 공지로 다시 확인해야 합니다.",
      search_summary,
    ],
    "checklist": DEFAULT_CHECKLIST,
    "transit_and_entry_tips": [
      *venue.transit_notes,
      *venue.entry_notes,
      *venue.locker_notes,
    ],
    "official_check_required": venue.event_check_items,
  }
