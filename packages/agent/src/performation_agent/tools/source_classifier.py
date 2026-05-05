from __future__ import annotations

from urllib.parse import urlparse

from performation_agent.state import SearchResult
from performation_domain import ConfidenceLabel


PUBLIC_REVIEW_DOMAINS = (
  "blog.naver.com",
  "m.blog.naver.com",
  "tistory.com",
  "velog.io",
  "brunch.co.kr",
)
PUBLIC_REVIEW_HINTS = (
  "blog",
  "review",
  "tistory",
  "후기",
  "리뷰",
  "방문기",
)
OFFICIAL_DOMAINS = (
  "ksponco.or.kr",
  "bluesquare.kr",
  "yes24livehall.com",
  "yes24.com",
  "interpark.com",
  "ticketlink.co.kr",
  "mcst.go.kr",
  "culture.go.kr",
)
OFFICIAL_HINTS = (
  "official",
  "공식",
  "공지",
  "예매처",
  "ticket",
  "kspo",
  "blue square",
  "yes24 live hall",
)
LATEST_CHECK_HINTS = (
  "입장 시간",
  "입장시간",
  "입장 위치",
  "입장위치",
  "물품보관",
  "보관소",
  "락커",
  "locker",
  "주차",
  "운영 여부",
  "운영여부",
  "스탠딩",
)


def classify_search_result(result: SearchResult) -> tuple[ConfidenceLabel, str]:
  haystack = _combined_text(result)
  hostname = urlparse(result["url"]).hostname or ""

  if _matches_domain(hostname, PUBLIC_REVIEW_DOMAINS) or _contains_any(haystack, PUBLIC_REVIEW_HINTS):
    return (
      ConfidenceLabel.PUBLIC_REVIEW_REFERENCE,
      "블로그/후기 성격의 공개 정보이므로 참고용으로 분류합니다.",
    )
  if _contains_any(haystack, LATEST_CHECK_HINTS):
    return (
      ConfidenceLabel.LATEST_OFFICIAL_CHECK_REQUIRED,
      "공연별로 바뀔 수 있는 정보라 최신 공식 확인이 필요합니다.",
    )
  if _matches_domain(hostname, OFFICIAL_DOMAINS) or _contains_any(haystack, OFFICIAL_HINTS):
    return (
      ConfidenceLabel.OFFICIAL_CONFIRMED,
      "공식 홈페이지, 예매처, 공공정보 성격의 출처입니다.",
    )
  return (
    ConfidenceLabel.UNCERTAIN,
    "출처 성격을 안정적으로 판단하기 어려워 불확실로 분류합니다.",
  )


def _combined_text(result: SearchResult) -> str:
  return " ".join(
    (
      result["title"],
      result["url"],
      result["snippet"],
    )
  ).casefold()


def _contains_any(text: str, hints: tuple[str, ...]) -> bool:
  return any(hint.casefold() in text for hint in hints)


def _matches_domain(hostname: str, domains: tuple[str, ...]) -> bool:
  normalized_hostname = hostname.casefold()
  return any(
    normalized_hostname == domain or normalized_hostname.endswith(f".{domain}")
    for domain in domains
  )
