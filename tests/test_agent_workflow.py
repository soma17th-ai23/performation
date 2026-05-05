from performation_agent import generate_visit_guide


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

