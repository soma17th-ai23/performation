from __future__ import annotations

from performation_agent.state import GuideState
from performation_agent.tools.guide_draft import build_deterministic_guide_draft


def generate_checklist(state: GuideState) -> GuideState:
  if "checklist" in state:
    return {}
  return {"checklist": build_deterministic_guide_draft(state)["checklist"]}
