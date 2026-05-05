from __future__ import annotations

from performation_agent.state import GuideState
from performation_agent.tools.guide_draft import build_deterministic_guide_draft
from performation_agent.tools.llm import generate_guide_draft_with_fallback


def summarize_information(state: GuideState) -> GuideState:
  fallback_draft = build_deterministic_guide_draft(state)
  draft, llm_used = generate_guide_draft_with_fallback(state, fallback_draft)
  return {
    "summary": draft["summary"],
    "checklist": draft["checklist"],
    "transit_and_entry_tips": draft["transit_and_entry_tips"],
    "official_check_required": draft["official_check_required"],
    "llm_used": llm_used,
  }
