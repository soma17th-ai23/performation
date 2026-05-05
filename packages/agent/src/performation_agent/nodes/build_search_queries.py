from __future__ import annotations

from performation_agent.state import GuideState, SearchQuery


QUERY_PURPOSES = (
  ("공식 정보", "official"),
  ("입장 정보", "entry"),
  ("교통 정보", "transit"),
  ("물품보관", "locker"),
  ("준비물 팁", "preparation"),
)


def build_search_queries(state: GuideState) -> GuideState:
  venue = state.get("venue")
  base_query = venue.name if venue else state["query"]
  queries: list[SearchQuery] = [
    {"query": f"{base_query} {query_suffix}", "purpose": purpose}
    for query_suffix, purpose in QUERY_PURPOSES
  ]

  return {"search_queries": queries}
