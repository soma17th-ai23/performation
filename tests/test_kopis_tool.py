from datetime import date

import httpx

from performation_agent.tools.kopis import (
  KOPIS_PERFORMANCE_LIST_URL,
  KOPIS_PERFORMANCE_PAGE_URL,
  KopisPerformanceProvider,
  build_kopis_provider_from_env,
  search_kopis_with_fallback,
)


def test_search_kopis_with_fallback_returns_empty_without_key(monkeypatch) -> None:
  monkeypatch.delenv("KOPIS_API_KEY", raising=False)

  assert search_kopis_with_fallback("EK 콘서트") == []


def test_build_kopis_provider_from_env_uses_api_key() -> None:
  provider = build_kopis_provider_from_env(
    {
      "KOPIS_API_KEY": "kopis-key",
      "PERFORMATION_KOPIS_LOOKAHEAD_DAYS": "31",
      "PERFORMATION_KOPIS_ROWS": "5",
    }
  )

  assert isinstance(provider, KopisPerformanceProvider)


def test_kopis_provider_normalizes_performance_list_xml() -> None:
  def handler(request: httpx.Request) -> httpx.Response:
    assert str(request.url).startswith(KOPIS_PERFORMANCE_LIST_URL)
    assert request.url.params["service"] == "kopis-test"
    assert request.url.params["shprfnm"] == "EK"
    assert request.url.params["stdate"] == "20260501"
    assert request.url.params["eddate"] == "20260531"
    assert request.url.params["rows"] == "2"
    return httpx.Response(
      200,
      text="""
      <dbs>
        <db>
          <mt20id>PF999999</mt20id>
          <prfnm>EK 3rd Concert : You Good?</prfnm>
          <prfpdfrom>2026.05.10</prfpdfrom>
          <prfpdto>2026.05.10</prfpdto>
          <fcltynm>예스24라이브홀</fcltynm>
          <area>서울특별시</area>
          <genrenm>대중음악</genrenm>
          <prfstate>공연예정</prfstate>
        </db>
      </dbs>
      """,
    )

  with httpx.Client(transport=httpx.MockTransport(handler)) as client:
    provider = KopisPerformanceProvider(
      "kopis-test",
      client=client,
      start_date=date(2026, 5, 1),
      lookahead_days=30,
      rows=2,
    )
    results = provider.search_performances("EK 콘서트")

  assert results == [
    {
      "title": "EK 3rd Concert : You Good? - KOPIS 공연 공식 데이터",
      "url": KOPIS_PERFORMANCE_PAGE_URL.format(performance_id="PF999999"),
      "snippet": (
        "공식 KOPIS 공연 데이터. 공연명 EK 3rd Concert : You Good?. 공연기간 2026년 5월 10일. "
        "공연장소 예스24라이브홀. 지역 서울특별시. 장르 대중음악. 공연상태 공연예정."
      ),
      "query": "EK 콘서트 KOPIS 공식 정보 일정 장소",
    }
  ]


def test_search_kopis_with_fallback_handles_provider_errors() -> None:
  class FailingProvider:
    def search_performances(self, query: str):
      raise httpx.TimeoutException("timeout")

  assert search_kopis_with_fallback("워터밤", provider=FailingProvider()) == []
