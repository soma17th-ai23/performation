import importlib

from performation_agent import generate_visit_guide
from performation_agent.nodes.analyze_input import analyze_input
from performation_agent.nodes.assign_confidence import assign_confidence
from performation_agent.nodes.build_search_queries import build_search_queries
from performation_agent.nodes.classify_sources import classify_sources
from performation_agent.nodes.infer_event_candidates import infer_event_candidates
from performation_agent.nodes.infer_venue_from_search import infer_venue_from_search
from performation_agent.nodes.load_venue_data import load_venue_data
from performation_agent.nodes.summarize_information import summarize_information
from performation_agent.workflow import NODE_SEQUENCE
from performation_domain import ConfidenceLabel, VenueInfo


def test_workflow_has_expected_node_sequence() -> None:
  assert NODE_SEQUENCE == (
    "analyze_input",
    "load_venue_data",
    "build_search_queries",
    "search_public_web",
    "infer_venue_from_search",
    "infer_event_candidates",
    "classify_sources",
    "summarize_information",
    "assign_confidence",
    "format_response",
  )


def test_supported_venue_returns_fallback_guide() -> None:
  guide = generate_visit_guide("KSPO DOME 콘서트 준비물")

  assert guide.input_type == "concert_with_venue_hint"
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


def test_concert_query_with_venue_hint_infers_supported_venue() -> None:
  guide = generate_visit_guide("아이유 콘서트 KSPO")

  assert guide.input_type == "concert_with_venue_hint"
  assert guide.venue is not None
  assert guide.venue.name == "KSPO DOME"
  assert guide.fallback_used is True
  assert guide.checklist


def test_concert_detail_query_with_venue_hint_keeps_concert_input_type() -> None:
  guide = generate_visit_guide("아이유 콘서트 KSPO 스탠딩")

  assert guide.input_type == "concert_with_venue_hint"
  assert guide.venue is not None
  assert guide.venue.name == "KSPO DOME"


def test_venue_alias_with_live_word_stays_venue_name() -> None:
  guide = generate_visit_guide("예스24라이브홀")

  assert guide.input_type == "venue_name"
  assert guide.venue is not None
  assert guide.venue.name == "YES24 Live Hall"


def test_concert_query_without_venue_hint_stays_ambiguous() -> None:
  guide = generate_visit_guide("아이유 콘서트 티켓팅")

  assert guide.input_type == "unsupported_or_ambiguous"
  assert guide.venue is None
  assert any("공연장명" in item for item in guide.summary)


def test_infer_venue_from_search_sets_single_supported_venue() -> None:
  result = infer_venue_from_search(
    {
      "query": "아이유 콘서트",
      "input_intent": "concert_or_event_name",
      "input_type": "unsupported_or_ambiguous",
      "search_results": [
        {
          "title": "아이유 콘서트 KSPO DOME 공연 안내",
          "url": "https://example.com/iu-kspo",
          "snippet": "서울 KSPO DOME에서 열리는 공연 정보입니다.",
          "query": "아이유 콘서트 공식 정보",
        }
      ],
    }
  )

  assert result["input_type"] == "concert_with_inferred_venue"
  assert result["venue"].name == "KSPO DOME"
  assert result["matched_venue_alias"] == "KSPO DOME"
  assert result["venue_inference_source"] == "public_search"


def test_infer_venue_from_search_does_not_guess_multiple_supported_venues() -> None:
  result = infer_venue_from_search(
    {
      "query": "아이유 콘서트",
      "input_intent": "concert_or_event_name",
      "input_type": "unsupported_or_ambiguous",
      "search_results": [
        {
          "title": "아이유 콘서트 KSPO DOME",
          "url": "https://example.com/iu-kspo",
          "snippet": "KSPO DOME 공연 정보",
          "query": "아이유 콘서트 공식 정보",
        },
        {
          "title": "아이유 콘서트 Blue Square",
          "url": "https://example.com/iu-blue-square",
          "snippet": "Blue Square 공연 정보",
          "query": "아이유 콘서트 공식 정보",
        },
      ],
    }
  )

  assert result == {}


def test_infer_venue_from_search_ignores_url_only_matches() -> None:
  result = infer_venue_from_search(
    {
      "query": "랩비트 공연",
      "input_intent": "concert_or_event_name",
      "input_type": "unsupported_or_ambiguous",
      "search_results": [
        {
          "title": "랩비트 공연 정보",
          "url": "https://example.com/kspo-dome-archive",
          "snippet": "공연 일정과 티켓 안내를 확인하세요.",
          "query": "랩비트 공연 공식 정보",
        }
      ],
    }
  )

  assert result == {}


def test_infer_event_candidates_returns_multiple_regional_options() -> None:
  result = infer_event_candidates(
    {
      "query": "워터밤",
      "input_intent": "concert_or_event_name",
      "input_type": "unsupported_or_ambiguous",
      "search_results": [
        {
          "title": "워터밤 서울 2026 일정 장소: 서울월드컵경기장",
          "url": "https://example.com/waterbomb-seoul",
          "snippet": "공식 예매 공지에서 서울 공연 일정과 장소를 확인하세요.",
          "query": "워터밤 2026 일정 장소",
        },
        {
          "title": "워터밤 인천 2026 일정 장소: 송도",
          "url": "https://example.com/waterbomb-incheon",
          "snippet": "인천 공연 일정은 공식 공지 기준으로 확인이 필요합니다.",
          "query": "워터밤 2026 일정 장소",
        },
      ],
    }
  )

  candidates = result["event_candidates"]
  assert result["input_type"] == "event_candidates"
  assert [candidate.region for candidate in candidates] == ["서울", "인천"]
  assert candidates[0].name == "워터밤 서울"
  assert candidates[0].venue_name == "서울월드컵경기장"
  assert candidates[0].sources


def test_candidate_summary_asks_user_to_choose() -> None:
  state = {
    "query": "워터밤",
    "input_intent": "concert_or_event_name",
    "input_type": "unsupported_or_ambiguous",
    "search_results": [
      {
        "title": "워터밤 서울 2026 일정 장소: 서울월드컵경기장",
        "url": "https://example.com/waterbomb-seoul",
        "snippet": "서울 공연 공식 공지",
        "query": "워터밤 2026 일정 장소",
      },
      {
        "title": "워터밤 인천 2026 일정 장소: 송도",
        "url": "https://example.com/waterbomb-incheon",
        "snippet": "인천 공연 공식 공지",
        "query": "워터밤 2026 일정 장소",
      },
    ],
  }
  candidate_result = infer_event_candidates(state)
  summary_result = summarize_information({**state, **candidate_result})
  confidence_result = assign_confidence({**state, **candidate_result, **summary_result})

  assert candidate_result["input_type"] == "event_candidates"
  assert any("여러 공연 후보" in item for item in summary_result["summary"])
  assert any("후보" in item for item in confidence_result["confidence_notes"])


def test_input_analysis_marks_concert_like_queries() -> None:
  result = analyze_input({"query": "아이유 콘서트 KSPO"})

  assert result["input_intent"] == "concert_or_event_name"
  assert result["detail_keywords"] == []


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


def test_search_queries_use_inferred_venue_and_original_concert_query() -> None:
  analysis = analyze_input({"query": "아이유 콘서트 KSPO"})
  venue_state = load_venue_data(analysis)
  result = build_search_queries({**analysis, **venue_state})

  queries = [item["query"] for item in result["search_queries"]]
  assert venue_state["matched_venue_alias"] == "KSPO"
  assert all("KSPO DOME" in query for query in queries)
  assert all("아이유 콘서트 KSPO" in query for query in queries)


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
