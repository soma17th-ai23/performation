from __future__ import annotations

from functools import lru_cache
from typing import TypedDict

from langgraph.graph import END, StateGraph

from performation_domain import GuideResponse, VenueInfo
from performation_venue_data import get_default_repository


DETAIL_KEYWORDS = ("준비물", "스탠딩", "입장", "물품보관", "교통", "주차", "동선")


class GuideState(TypedDict, total=False):
  query: str
  venue: VenueInfo | None
  response: GuideResponse


def generate_visit_guide(query: str) -> GuideResponse:
  state = build_workflow_graph().invoke({"query": query})
  return state["response"]


@lru_cache(maxsize=1)
def build_workflow_graph():
  graph = StateGraph(GuideState)
  graph.add_node("match_venue", match_venue_node)
  graph.add_node("compose_guide", compose_guide_node)
  graph.set_entry_point("match_venue")
  graph.add_edge("match_venue", "compose_guide")
  graph.add_edge("compose_guide", END)
  return graph.compile()


def match_venue_node(state: GuideState) -> GuideState:
  repository = get_default_repository()
  query = state["query"]
  venue = repository.find_by_query(query)
  return {**state, "venue": venue}


def compose_guide_node(state: GuideState) -> GuideState:
  query = state["query"]
  venue = state.get("venue")
  input_type = classify_input(query, venue_found=venue is not None)

  if venue is None:
    return {
      **state,
      "response": GuideResponse(
        input=query,
        input_type=input_type,
        venue=None,
        summary=[
          "현재 MVP는 KSPO DOME, Blue Square, YES24 Live Hall 중심으로 지원합니다.",
          "공연장명, 공연 날짜, 아티스트명 또는 예매처 링크를 추가하면 더 정확히 확인할 수 있습니다.",
        ],
        checklist=["공식 예매처 또는 공연 공지에서 공연장 정보를 먼저 확인하기"],
        transit_and_entry_tips=[],
        official_check_required=["공연장명", "공연 날짜", "아티스트명", "예매처 공지"],
        sources=[],
        confidence_notes=["지원 범위 밖이거나 입력이 모호하여 로컬 공연장 데이터와 매칭하지 못했습니다."],
        fallback_used=True,
      ),
    }

  return {
    **state,
    "response": GuideResponse(
      input=query,
      input_type=input_type,
      venue=venue,
      summary=[
        f"{venue.name} 방문 전에는 입장 위치, 도착 시간, 물품보관 운영 여부를 공연별 공지로 다시 확인해야 합니다.",
        "현재 스캐폴드에서는 공개 웹 검색 provider가 연결되지 않아 로컬 공연장 데이터 기반으로 안내합니다.",
      ],
      checklist=build_default_checklist(),
      transit_and_entry_tips=[
        *venue.transit_notes,
        *venue.entry_notes,
        *venue.locker_notes,
      ],
      official_check_required=venue.event_check_items,
      sources=venue.sources,
      confidence_notes=[
        "공식 또는 안정적인 공연장 기본 정보와 공연별 변동 가능성이 큰 정보를 분리했습니다.",
        "검색 API 미설정 상태에서는 공개 후기나 최신 공지 검색 결과를 사용하지 않습니다.",
      ],
      fallback_used=True,
    ),
  }


def classify_input(query: str, venue_found: bool) -> str:
  if not venue_found:
    return "unsupported_or_ambiguous"
  if any(keyword in query for keyword in DETAIL_KEYWORDS):
    return "venue_with_detail_question"
  return "venue_name"


def build_default_checklist() -> list[str]:
  return [
    "모바일 티켓 또는 예매 내역 확인",
    "신분증 필요 여부 확인",
    "보조배터리 준비",
    "공연장 도착 추천 시간 확인",
    "물품보관 운영 여부 확인",
    "공연 종료 후 교통 혼잡 가능성 확인",
    "공식 공지에서 최종 변동 사항 확인",
  ]
