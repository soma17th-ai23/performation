import json

import httpx

from performation_agent.tools.search import (
  BRAVE_SEARCH_URL,
  TAVILY_SEARCH_URL,
  BraveSearchProvider,
  TavilySearchProvider,
  build_search_provider_from_env,
  search_with_fallback,
)


def test_search_with_fallback_returns_empty_without_provider(monkeypatch) -> None:
  monkeypatch.delenv("TAVILY_API_KEY", raising=False)
  monkeypatch.delenv("BRAVE_SEARCH_API_KEY", raising=False)

  results = search_with_fallback([{"query": "KSPO DOME 공식 정보", "purpose": "official"}])

  assert results == []


def test_build_search_provider_prefers_tavily_when_both_keys_exist() -> None:
  provider = build_search_provider_from_env(
    {
      "TAVILY_API_KEY": "tavily-key",
      "BRAVE_SEARCH_API_KEY": "brave-key",
    }
  )

  assert isinstance(provider, TavilySearchProvider)


def test_build_search_provider_honors_explicit_brave_provider() -> None:
  provider = build_search_provider_from_env(
    {
      "PERFORMATION_SEARCH_PROVIDER": "brave",
      "TAVILY_API_KEY": "tavily-key",
      "BRAVE_SEARCH_API_KEY": "brave-key",
    }
  )

  assert isinstance(provider, BraveSearchProvider)


def test_tavily_provider_normalizes_results() -> None:
  def handler(request: httpx.Request) -> httpx.Response:
    assert str(request.url) == TAVILY_SEARCH_URL
    assert request.headers["Authorization"] == "Bearer tvly-test"
    body = json.loads(request.content)
    assert body["query"] == "KSPO DOME 입장 정보"
    assert body["max_results"] == 2
    return httpx.Response(
      200,
      json={
        "results": [
          {
            "title": "KSPO DOME 공식 안내",
            "url": "https://example.com/kspo",
            "content": "입장 위치와 공지 확인 안내",
          }
        ]
      },
    )

  with httpx.Client(transport=httpx.MockTransport(handler)) as client:
    provider = TavilySearchProvider("tvly-test", client=client)
    results = provider.search({"query": "KSPO DOME 입장 정보", "purpose": "entry"}, max_results=2)

  assert results == [
    {
      "title": "KSPO DOME 공식 안내",
      "url": "https://example.com/kspo",
      "snippet": "입장 위치와 공지 확인 안내",
      "query": "KSPO DOME 입장 정보",
    }
  ]


def test_brave_provider_normalizes_results() -> None:
  def handler(request: httpx.Request) -> httpx.Response:
    assert str(request.url).startswith(BRAVE_SEARCH_URL)
    assert request.headers["X-Subscription-Token"] == "brave-test"
    assert request.url.params["q"] == "YES24 Live Hall 물품보관"
    assert request.url.params["count"] == "2"
    return httpx.Response(
      200,
      json={
        "web": {
          "results": [
            {
              "title": "YES24 Live Hall 방문 후기",
              "url": "https://example.com/yes24-review",
              "description": "물품보관 후기",
              "extra_snippets": ["스탠딩 입장 팁"],
            }
          ]
        }
      },
    )

  with httpx.Client(transport=httpx.MockTransport(handler)) as client:
    provider = BraveSearchProvider("brave-test", client=client)
    results = provider.search({"query": "YES24 Live Hall 물품보관", "purpose": "locker"}, max_results=2)

  assert results == [
    {
      "title": "YES24 Live Hall 방문 후기",
      "url": "https://example.com/yes24-review",
      "snippet": "물품보관 후기 스탠딩 입장 팁",
      "query": "YES24 Live Hall 물품보관",
    }
  ]


def test_tavily_provider_handles_null_results() -> None:
  def handler(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={"results": None})

  with httpx.Client(transport=httpx.MockTransport(handler)) as client:
    provider = TavilySearchProvider("tvly-test", client=client)
    results = provider.search({"query": "KSPO DOME 공식 정보", "purpose": "official"}, max_results=2)

  assert results == []


def test_brave_provider_handles_null_web_payload() -> None:
  def handler(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={"web": None})

  with httpx.Client(transport=httpx.MockTransport(handler)) as client:
    provider = BraveSearchProvider("brave-test", client=client)
    results = provider.search({"query": "블루스퀘어 교통 정보", "purpose": "transit"}, max_results=2)

  assert results == []


def test_search_with_fallback_dedupes_urls_and_keeps_fallback_on_error() -> None:
  class DuplicateProvider:
    def search(self, search_query, *, max_results):
      return [
        {
          "title": "첫 결과",
          "url": "https://example.com/same",
          "snippet": "첫 번째",
          "query": search_query["query"],
        },
        {
          "title": "중복 결과",
          "url": "https://example.com/same",
          "snippet": "두 번째",
          "query": search_query["query"],
        },
      ]

  class FailingProvider:
    def search(self, search_query, *, max_results):
      raise httpx.TimeoutException("timeout")

  query = {"query": "블루스퀘어 교통 정보", "purpose": "transit"}

  assert len(search_with_fallback([query], provider=DuplicateProvider())) == 1
  assert search_with_fallback([query], provider=FailingProvider()) == []
