from __future__ import annotations

import re

from performation_agent.state import GuideState, SearchResult
from performation_domain import ConfidenceLabel, EventCandidate, Source


CONCERT_INTENTS = {"concert_or_event_name", "concert_detail_question"}
REGION_PATTERN = re.compile(
  r"(서울|인천|부산|대구|대전|광주|울산|수원|고양|성남|과천|춘천|강릉|청주|천안|전주|여수|창원|제주)"
)
DATE_PATTERN = re.compile(r"(20\d{2}(?:년)?(?:\s*[0-9]{1,2}월)?|[0-9]{1,2}월\s*[0-9]{1,2}일|[0-9]{1,2}월)")
VENUE_PATTERN = re.compile(r"(?:장소|venue|공연장)[:：]?\s*([가-힣A-Za-z0-9][가-힣A-Za-z0-9\s&+\-]{1,40})", re.IGNORECASE)


def infer_event_candidates(state: GuideState) -> GuideState:
  if state.get("venue") is not None:
    return {}
  if state.get("input_intent") not in CONCERT_INTENTS:
    return {}
  if not state.get("search_results"):
    return {}

  candidates_by_key: dict[tuple[str, str, str], EventCandidate] = {}
  for result in state.get("search_results", []):
    candidate = _candidate_from_result(state["query"], result)
    if candidate is None:
      continue
    key = (candidate.name.casefold(), candidate.region, candidate.date_text)
    existing = candidates_by_key.get(key)
    if existing is None:
      candidates_by_key[key] = candidate
    else:
      existing.sources.extend(candidate.sources)

  candidates = list(candidates_by_key.values())
  if len(candidates) < 2:
    return {}

  return {
    "input_type": "event_candidates",
    "event_candidates": candidates[:6],
  }


def _candidate_from_result(query: str, result: SearchResult) -> EventCandidate | None:
  evidence_text = " ".join((result["title"], result["snippet"]))
  region = _first_match(REGION_PATTERN, evidence_text)
  if not region:
    return None

  name = _candidate_name(query, region, evidence_text)
  date_text = _first_match(DATE_PATTERN, evidence_text)
  venue_name = _venue_name(result["title"], result["snippet"])
  source = Source(
    title=result["title"],
    url=result["url"],
    source_type=_candidate_confidence(result),
    used_for=[result["query"]],
  )
  return EventCandidate(
    name=name,
    region=region,
    date_text=date_text,
    venue_name=venue_name,
    confidence_label=source.source_type,
    sources=[source],
  )


def _candidate_name(query: str, region: str, evidence_text: str) -> str:
  base_name = query.strip()
  for suffix in ("공연", "콘서트", "페스티벌", "일정", "장소"):
    base_name = base_name.replace(suffix, "")
  base_name = base_name.strip() or query.strip()
  if region in base_name:
    return base_name
  return f"{base_name} {region}".strip()


def _venue_name(*evidence_fields: str) -> str:
  for evidence_text in evidence_fields:
    match = VENUE_PATTERN.search(evidence_text)
    if match:
      return match.group(1).strip(" .,/|")
  return ""


def _candidate_confidence(result: SearchResult) -> ConfidenceLabel:
  text = " ".join((result["title"], result["url"], result["snippet"])).casefold()
  if any(term in text for term in ("공식", "official", "ticket", "예매", "공지")):
    return ConfidenceLabel.LATEST_OFFICIAL_CHECK_REQUIRED
  if any(term in text for term in ("blog", "후기", "리뷰", "tistory")):
    return ConfidenceLabel.PUBLIC_REVIEW_REFERENCE
  return ConfidenceLabel.UNCERTAIN


def _first_match(pattern: re.Pattern[str], text: str) -> str:
  match = pattern.search(text)
  return match.group(1).strip() if match else ""
