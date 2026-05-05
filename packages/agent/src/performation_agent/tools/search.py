from __future__ import annotations

from performation_agent.state import SearchQuery, SearchResult


def search_with_fallback(search_queries: list[SearchQuery]) -> list[SearchResult]:
  # Real Tavily/Brave Search integration belongs to a later issue.
  # Returning an empty list keeps the workflow deterministic and exercises local-data fallback.
  return []

