from __future__ import annotations

from performation_agent.state import GuideState


def summarize_information(state: GuideState) -> GuideState:
  venue = state.get("venue")

  if venue is None:
    return {
      "summary": [
        "현재 MVP는 KSPO DOME, Blue Square, YES24 Live Hall 중심으로 지원합니다.",
        "공연장명, 공연 날짜, 아티스트명 또는 예매처 링크를 추가하면 더 정확히 확인할 수 있습니다.",
      ],
      "transit_and_entry_tips": [],
      "official_check_required": ["공연장명", "공연 날짜", "아티스트명", "예매처 공지"],
    }

  return {
    "summary": [
      f"{venue.name} 방문 전에는 입장 위치, 도착 시간, 물품보관 운영 여부를 공연별 공지로 다시 확인해야 합니다.",
      "현재 단계에서는 실제 검색 provider가 연결되지 않아 로컬 공연장 데이터 기반으로 안내합니다.",
    ],
    "transit_and_entry_tips": [
      *venue.transit_notes,
      *venue.entry_notes,
      *venue.locker_notes,
    ],
    "official_check_required": venue.event_check_items,
  }
