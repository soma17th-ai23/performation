from __future__ import annotations

from performation_agent.state import ClassifiedSource, GuideState, SearchResult
from performation_domain import ConfidenceLabel, Source


OFFICIAL_SOURCE_HINTS = (
  "official",
  "공지",
  "공식",
  "interpark",
  "ticketlink",
  "yes24",
  "kspo",
  "bluesquare",
)
PUBLIC_REVIEW_HINTS = (
  "blog",
  "tistory",
  "후기",
  "리뷰",
)


def classify_sources(state: GuideState) -> GuideState:
  classified_sources: list[ClassifiedSource] = []
  venue = state.get("venue")

  if venue:
    classified_sources.extend(
      {"source": source, "reason": "로컬 공연장 fallback 데이터에 포함된 공식 또는 안정 정보입니다."}
      for source in venue.sources
    )

  for result in state.get("search_results", []):
    classified_sources.append(
      {
        "source": Source(
          title=result["title"],
          url=result["url"],
          source_type=_classify_search_result(result),
          used_for=[result["query"]],
        ),
        "reason": "공개 웹 검색 결과에서 수집된 출처입니다.",
      }
    )

  return {
    "classified_sources": classified_sources,
    "sources": [item["source"] for item in classified_sources],
  }


def _classify_search_result(result: SearchResult) -> ConfidenceLabel:
  haystack = " ".join((result["title"], result["url"], result["snippet"])).casefold()
  if any(hint in haystack for hint in PUBLIC_REVIEW_HINTS):
    return ConfidenceLabel.PUBLIC_REVIEW_REFERENCE
  if any(hint in haystack for hint in OFFICIAL_SOURCE_HINTS):
    return ConfidenceLabel.OFFICIAL_CONFIRMED
  return ConfidenceLabel.UNCERTAIN
