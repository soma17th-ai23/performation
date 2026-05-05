import json

import httpx

from performation_agent.tools.guide_draft import build_deterministic_guide_draft
from performation_agent.tools.llm import (
  DEFAULT_GEMINI_MODEL,
  GEMINI_GENERATE_CONTENT_URL,
  GeminiGuideDraftProvider,
  build_guide_draft_provider_from_env,
  build_guide_prompt,
  generate_guide_draft_with_fallback,
)


FALLBACK_DRAFT = {
  "summary": ["fallback summary"],
  "checklist": ["fallback checklist"],
  "transit_and_entry_tips": ["fallback tip"],
  "official_check_required": ["fallback official check"],
}


def test_build_guide_draft_provider_requires_gemini_key(monkeypatch) -> None:
  monkeypatch.delenv("GEMINI_API_KEY", raising=False)

  assert build_guide_draft_provider_from_env({}) is None


def test_build_guide_draft_provider_uses_gemini_env() -> None:
  provider = build_guide_draft_provider_from_env(
    {
      "PERFORMATION_LLM_PROVIDER": "gemini",
      "PERFORMATION_LLM_MODEL": "gemini-test",
      "GEMINI_API_KEY": "gemini-key",
    }
  )

  assert isinstance(provider, GeminiGuideDraftProvider)


def test_gemini_provider_normalizes_structured_response() -> None:
  def handler(request: httpx.Request) -> httpx.Response:
    assert str(request.url) == GEMINI_GENERATE_CONTENT_URL.format(model=DEFAULT_GEMINI_MODEL)
    assert request.headers["x-goog-api-key"] == "gemini-test-key"
    body = json.loads(request.content)
    assert body["generationConfig"]["responseMimeType"] == "application/json"
    assert body["generationConfig"]["responseSchema"]["type"] == "OBJECT"
    assert "공연 관람 준비 가이드" in body["contents"][0]["parts"][0]["text"]
    return httpx.Response(
      200,
      json={
        "candidates": [
          {
            "content": {
              "parts": [
                {
                  "text": json.dumps(
                    {
                      "summary": ["AI 요약"],
                      "checklist": ["AI 체크리스트"],
                      "transit_and_entry_tips": ["AI 교통 팁"],
                      "official_check_required": ["AI 공식 확인"],
                    },
                    ensure_ascii=False,
                  )
                }
              ]
            }
          }
        ]
      },
    )

  with httpx.Client(transport=httpx.MockTransport(handler)) as client:
    provider = GeminiGuideDraftProvider("gemini-test-key", client=client)
    draft = provider.generate("공연 관람 준비 가이드")

  assert draft == {
    "summary": ["AI 요약"],
    "checklist": ["AI 체크리스트"],
    "transit_and_entry_tips": ["AI 교통 팁"],
    "official_check_required": ["AI 공식 확인"],
  }


def test_generate_guide_draft_uses_provider_output() -> None:
  class FakeProvider:
    def generate(self, prompt: str):
      assert "fallback summary" in prompt
      return {
        "summary": ["AI 요약"],
        "checklist": ["AI 체크리스트"],
        "transit_and_entry_tips": ["AI 팁"],
        "official_check_required": ["AI 공식 확인"],
      }

  draft, llm_used = generate_guide_draft_with_fallback(
    {"query": "KSPO DOME 준비물", "input_type": "venue_with_detail_question"},
    FALLBACK_DRAFT,
    provider=FakeProvider(),
  )

  assert llm_used is True
  assert draft["summary"] == ["AI 요약"]
  assert draft["checklist"] == ["AI 체크리스트"]


def test_generate_guide_draft_keeps_fallback_on_provider_error() -> None:
  class FailingProvider:
    def generate(self, prompt: str):
      raise httpx.TimeoutException("timeout")

  draft, llm_used = generate_guide_draft_with_fallback(
    {"query": "KSPO DOME 준비물"},
    FALLBACK_DRAFT,
    provider=FailingProvider(),
  )

  assert llm_used is False
  assert draft == FALLBACK_DRAFT


def test_build_guide_prompt_includes_sources_but_not_secrets() -> None:
  prompt = build_guide_prompt(
    {
      "query": "KSPO DOME 준비물",
      "input_type": "venue_with_detail_question",
      "classified_sources": [],
    },
    FALLBACK_DRAFT,
  )

  assert "GEMINI_API_KEY" not in prompt
  assert "KSPO DOME 준비물" in prompt
  assert "fallback summary" in prompt


def test_deterministic_draft_reflects_search_availability() -> None:
  draft = build_deterministic_guide_draft(
    {
      "query": "KSPO DOME 준비물",
      "search_results": [
        {
          "title": "검색 결과",
          "url": "https://example.com",
          "snippet": "검색 결과 내용",
          "query": "KSPO DOME 준비물",
        }
      ],
    }
  )

  assert "MVP" in draft["summary"][0]
