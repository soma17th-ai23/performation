from __future__ import annotations

import logging
import time
from collections.abc import Callable
from functools import lru_cache

from langgraph.graph import END, StateGraph

from performation_agent.nodes import (
  analyze_input,
  assign_confidence,
  build_search_queries,
  classify_sources,
  extract_event_info,
  format_response,
  infer_event_candidates,
  infer_venue_from_search,
  load_venue_data,
  search_kopis_official,
  search_public_web,
  summarize_information,
)
from performation_agent.state import GuideState
from performation_domain import GuideResponse


logger = logging.getLogger("performation.agent.workflow")

NODE_SEQUENCE = (
  "analyze_input",
  "load_venue_data",
  "build_search_queries",
  "search_public_web",
  "search_kopis_official",
  "infer_venue_from_search",
  "infer_event_candidates",
  "extract_event_info",
  "classify_sources",
  "summarize_information",
  "assign_confidence",
  "format_response",
)


def generate_visit_guide(query: str) -> GuideResponse:
  state = build_workflow_graph().invoke({"query": query})
  return state["response"]


@lru_cache(maxsize=1)
def build_workflow_graph():
  graph = StateGraph(GuideState)
  graph.add_node("analyze_input", _logged_node("analyze_input", analyze_input))
  graph.add_node("load_venue_data", _logged_node("load_venue_data", load_venue_data))
  graph.add_node("build_search_queries", _logged_node("build_search_queries", build_search_queries))
  graph.add_node("search_public_web", _logged_node("search_public_web", search_public_web))
  graph.add_node("search_kopis_official", _logged_node("search_kopis_official", search_kopis_official))
  graph.add_node("infer_venue_from_search", _logged_node("infer_venue_from_search", infer_venue_from_search))
  graph.add_node("infer_event_candidates", _logged_node("infer_event_candidates", infer_event_candidates))
  graph.add_node("extract_event_info", _logged_node("extract_event_info", extract_event_info))
  graph.add_node("classify_sources", _logged_node("classify_sources", classify_sources))
  graph.add_node("summarize_information", _logged_node("summarize_information", summarize_information))
  graph.add_node("assign_confidence", _logged_node("assign_confidence", assign_confidence))
  graph.add_node("format_response", _logged_node("format_response", format_response))

  graph.set_entry_point("analyze_input")
  for current_node, next_node in zip(NODE_SEQUENCE, NODE_SEQUENCE[1:]):
    graph.add_edge(current_node, next_node)
  graph.add_edge("format_response", END)

  return graph.compile()


def _logged_node(
  node_name: str,
  node: Callable[[GuideState], GuideState],
) -> Callable[[GuideState], GuideState]:
  def wrapped(state: GuideState) -> GuideState:
    logger.info("워크플로우 노드 시작: node=%s %s", node_name, _state_log_summary(state))
    started = time.monotonic()
    try:
      update = node(state)
    except Exception:
      elapsed = time.monotonic() - started
      logger.exception("워크플로우 노드 실패: node=%s elapsed=%.2fs", node_name, elapsed)
      raise

    elapsed = time.monotonic() - started
    merged_state = {**state, **update}
    logger.info(
      "워크플로우 노드 완료: node=%s elapsed=%.2fs %s",
      node_name,
      elapsed,
      _state_log_summary(merged_state),
    )
    return update

  return wrapped


def _state_log_summary(state: GuideState) -> str:
  venue = state.get("venue")
  event_info = state.get("event_info")
  response = state.get("response")
  return (
    "input_type=%s venue=%s search_queries=%d search_results=%d "
    "event_info=%s event_candidates=%d sources=%d fallback_used=%s llm_used=%s response_ready=%s"
  ) % (
    state.get("input_type", "pending"),
    venue.name if venue else "none",
    len(state.get("search_queries", [])),
    len(state.get("search_results", [])),
    bool(event_info),
    len(state.get("event_candidates", [])),
    len(state.get("sources", [])),
    state.get("fallback_used", False),
    state.get("llm_used", False),
    bool(response),
  )
