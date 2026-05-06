from __future__ import annotations

from performation_agent.state import GuideState
from performation_agent.tools.guide_draft import build_deterministic_guide_draft
from performation_agent.tools.llm import generate_guide_draft_with_fallback


def summarize_information(state: GuideState) -> GuideState:
  if state.get("event_candidates") and state.get("venue") is None:
    return {
      "summary": [
        "검색 결과에서 여러 공연 후보가 확인되었습니다.",
        "지역, 날짜 또는 후보명을 골라 다시 입력하면 해당 공연 기준으로 관람 준비 가이드를 생성할 수 있습니다.",
      ],
      "checklist": ["방문하려는 지역/날짜 후보 선택하기", "선택한 후보의 공식 공지와 예매처 정보 확인하기"],
      "transit_and_entry_tips": [],
      "official_check_required": ["공연 지역", "공연 날짜", "공연 장소", "입장 시간"],
      "llm_used": False,
    }

  fallback_draft = build_deterministic_guide_draft(state)
  draft, llm_used = generate_guide_draft_with_fallback(state, fallback_draft)
  return {
    "summary": draft["summary"],
    "checklist": draft["checklist"],
    "transit_and_entry_tips": draft["transit_and_entry_tips"],
    "official_check_required": draft["official_check_required"],
    "llm_used": llm_used,
  }
