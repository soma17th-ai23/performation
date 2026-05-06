from __future__ import annotations

from performation_agent.state import GuideState, SearchQuery


QUERY_PURPOSES = (
  ("공식 정보", "official"),
  ("일정 장소", "event_candidates"),
  ("입장 정보", "entry"),
  ("교통 정보", "transit"),
  ("물품보관", "locker"),
  ("준비물 팁", "preparation"),
)


def build_search_queries(state: GuideState) -> GuideState:
  base_query = _build_base_query(state)
  queries: list[SearchQuery] = [
    {"query": f"{base_query} {query_suffix}", "purpose": purpose}
    for query_suffix, purpose in QUERY_PURPOSES
  ]

  return {"search_queries": queries}


def _build_base_query(state: GuideState) -> str:
  venue = state.get("venue")
  original_query = state["query"]
  if venue is None:
    return original_query

  query_parts = [venue.name]
  if original_query.casefold() != venue.name.casefold():
    query_parts.append(original_query)

  return " ".join(query_parts)
