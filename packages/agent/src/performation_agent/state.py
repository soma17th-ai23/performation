from __future__ import annotations

from typing import TypedDict

from performation_domain import ConfidenceLabel, GuideResponse, Source, VenueInfo


class SearchQuery(TypedDict):
  query: str
  purpose: str


class SearchResult(TypedDict):
  title: str
  url: str
  snippet: str
  query: str
  source_type: ConfidenceLabel


class ClassifiedSource(TypedDict):
  source: Source
  reason: str


class GuideState(TypedDict, total=False):
  query: str
  normalized_query: str
  input_type: str
  detail_keywords: list[str]
  venue: VenueInfo | None
  search_queries: list[SearchQuery]
  search_results: list[SearchResult]
  classified_sources: list[ClassifiedSource]
  summary: list[str]
  checklist: list[str]
  transit_and_entry_tips: list[str]
  official_check_required: list[str]
  sources: list[Source]
  confidence_notes: list[str]
  fallback_used: bool
  response: GuideResponse

