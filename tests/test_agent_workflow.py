import importlib

from performation_agent import generate_visit_guide
from performation_agent.nodes.build_search_queries import build_search_queries
from performation_agent.nodes.classify_sources import classify_sources
from performation_agent.workflow import NODE_SEQUENCE
from performation_domain import ConfidenceLabel, VenueInfo


def test_workflow_has_expected_node_sequence() -> None:
  assert NODE_SEQUENCE == (
    "analyze_input",
    "load_venue_data",
    "build_search_queries",
    "search_public_web",
    "classify_sources",
    "summarize_information",
    "assign_confidence",
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


def test_search_queries_preserve_detail_and_localized_input() -> None:
  result = build_search_queries(
    {
      "query": "예스24라이브홀 스탠딩",
      "venue": VenueInfo(name="YES24 Live Hall"),
    }
  )

  queries = [item["query"] for item in result["search_queries"]]
  assert all("YES24 Live Hall" in query for query in queries)
  assert all("예스24라이브홀 스탠딩" in query for query in queries)


def test_classify_sources_assigns_confidence_after_search() -> None:
  result = classify_sources(
    {
      "search_results": [
        {
          "title": "공연장 관람 후기",
          "url": "https://example.tistory.com/kspo-review",
          "snippet": "공연장 방문 후기와 준비물 팁",
          "query": "KSPO DOME 준비물 팁",
        }
      ]
    }
  )

  source = result["sources"][0]
  assert source.source_type == ConfidenceLabel.PUBLIC_REVIEW_REFERENCE


def test_classify_sources_marks_latest_check_items() -> None:
  result = classify_sources(
    {
      "search_results": [
        {
          "title": "공연 당일 입장 시간 안내",
          "url": "https://example.com/entry-notice",
          "snippet": "입장 시간과 물품보관 운영 여부는 공연별 공지를 확인하세요.",
          "query": "KSPO DOME 입장 시간 물품보관",
        }
      ]
    }
  )

  source = result["sources"][0]
  classified_source = result["classified_sources"][0]
  assert source.source_type == ConfidenceLabel.LATEST_OFFICIAL_CHECK_REQUIRED
  assert "최신 공식 확인" in classified_source["reason"]


def test_summarize_information_accepts_llm_draft(monkeypatch) -> None:
  def fake_generate_guide_draft_with_fallback(state, fallback_draft):
    return (
      {
        "summary": ["AI 요약"],
        "checklist": ["AI 체크리스트"],
        "transit_and_entry_tips": ["AI 팁"],
        "official_check_required": ["AI 공식 확인"],
      },
      True,
    )

  summarize_module = importlib.import_module("performation_agent.nodes.summarize_information")
  monkeypatch.setattr(summarize_module, "generate_guide_draft_with_fallback", fake_generate_guide_draft_with_fallback)

  result = summarize_module.summarize_information({"query": "KSPO DOME 준비물"})

  assert result["summary"] == ["AI 요약"]
  assert result["checklist"] == ["AI 체크리스트"]
  assert result["llm_used"] is True
