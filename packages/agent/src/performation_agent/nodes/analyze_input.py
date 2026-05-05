from __future__ import annotations

from performation_agent.state import GuideState


DETAIL_KEYWORDS = ("준비물", "스탠딩", "입장", "물품보관", "교통", "주차", "동선")


def analyze_input(state: GuideState) -> GuideState:
  query = state["query"].strip()
  detail_keywords = [keyword for keyword in DETAIL_KEYWORDS if keyword in query]

  return {
    **state,
    "query": query,
    "normalized_query": query.casefold(),
    "input_type": "detail_question" if detail_keywords else "venue_or_concert_name",
    "detail_keywords": detail_keywords,
  }

