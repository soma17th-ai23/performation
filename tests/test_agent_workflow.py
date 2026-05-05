from performation_agent import generate_visit_guide
from performation_agent.workflow import NODE_SEQUENCE


def test_workflow_has_expected_node_sequence() -> None:
  assert NODE_SEQUENCE == (
    "analyze_input",
    "load_venue_data",
    "build_search_queries",
    "search_public_web",
    "classify_sources",
    "summarize_information",
    "assign_confidence",
    "generate_checklist",
    "format_response",
  )


def test_supported_venue_returns_fallback_guide() -> None:
  guide = generate_visit_guide("KSPO DOME 콘서트 준비물")

  assert guide.input_type == "venue_with_detail_question"
  assert guide.venue is not None
  assert guide.venue.name == "KSPO DOME"
  assert guide.fallback_used is True
  assert guide.sources
  assert "물품보관 운영 여부 확인" in guide.checklist


def test_unsupported_venue_is_clear_about_mvp_scope() -> None:
  guide = generate_visit_guide("처음 보는 소극장")

  assert guide.input_type == "unsupported_or_ambiguous"
  assert guide.venue is None
  assert guide.fallback_used is True
  assert any("MVP" in item for item in guide.summary)


def test_supported_venue_examples_keep_existing_fallback_behavior() -> None:
  examples = [
    ("KSPO DOME 콘서트 준비물", "KSPO DOME"),
    ("블루스퀘어", "Blue Square"),
    ("예스24라이브홀 스탠딩", "YES24 Live Hall"),
  ]

  for query, venue_name in examples:
    guide = generate_visit_guide(query)
    assert guide.venue is not None
    assert guide.venue.name == venue_name
    assert guide.fallback_used is True
    assert guide.checklist
