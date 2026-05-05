from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from performation_domain import VenueInfo


DATA_PATH = Path(__file__).resolve().parent / "data" / "venues.json"


@dataclass(frozen=True)
class VenueMatch:
  venue: VenueInfo
  alias: str


class VenueRepository:
  def __init__(self, venues: list[VenueInfo]) -> None:
    self._venues = venues

  @classmethod
  def from_json(cls, path: Path = DATA_PATH) -> "VenueRepository":
    payload = json.loads(path.read_text(encoding="utf-8"))
    return cls([VenueInfo.model_validate(item) for item in payload["venues"]])

  def list_venues(self) -> list[VenueInfo]:
    return list(self._venues)

  def find_by_query(self, query: str) -> VenueInfo | None:
    match = self.find_match_by_query(query)
    return match.venue if match is not None else None

  def find_match_by_query(self, query: str) -> VenueMatch | None:
    matches = self.find_matches_by_query(query)
    matched_venue_names = {match.venue.name for match in matches}
    if len(matched_venue_names) != 1:
      return None
    return matches[0]

  def find_matches_by_query(self, query: str) -> list[VenueMatch]:
    normalized = _normalize_for_match(query)
    matches: list[VenueMatch] = []
    for venue in self._venues:
      candidates = [venue.name, *venue.aliases]
      for candidate in candidates:
        normalized_candidate = _normalize_for_match(candidate)
        if normalized_candidate and normalized_candidate in normalized:
          matches.append(VenueMatch(venue=venue, alias=candidate))
          break
    return sorted(matches, key=lambda match: len(_normalize_for_match(match.alias)), reverse=True)


@lru_cache(maxsize=1)
def get_default_repository() -> VenueRepository:
  return VenueRepository.from_json()


def _normalize_for_match(value: str) -> str:
  return re.sub(r"[\W_]+", "", value.casefold())
