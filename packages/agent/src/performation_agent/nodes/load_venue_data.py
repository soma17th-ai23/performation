from __future__ import annotations

from performation_agent.state import GuideState
from performation_venue_data import get_default_repository


def load_venue_data(state: GuideState) -> GuideState:
  repository = get_default_repository()
  venue = repository.find_by_query(state["query"])

  if venue is None:
    input_type = "unsupported_or_ambiguous"
  elif state.get("detail_keywords"):
    input_type = "venue_with_detail_question"
  else:
    input_type = "venue_name"

  return {
    **state,
    "venue": venue,
    "input_type": input_type,
  }

