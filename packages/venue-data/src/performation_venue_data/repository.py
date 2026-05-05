from __future__ import annotations

import json
from pathlib import Path

from performation_domain import VenueInfo


DATA_PATH = Path(__file__).resolve().parent / "data" / "venues.json"


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
    normalized = query.casefold()
    for venue in self._venues:
      candidates = [venue.name, *venue.aliases]
      if any(candidate.casefold() in normalized for candidate in candidates):
        return venue
    return None


def get_default_repository() -> VenueRepository:
  return VenueRepository.from_json()

