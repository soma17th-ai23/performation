# Demo QA Report

## Commands

- `python3 scripts/validate_harness.py` - pass
- `uv run --python 3.11 pytest` - pass, 78 passed
- `git diff --check` - pass
- `.env` loaded in-process + `generate_visit_guide("워터밤")` - pass
- `.env` loaded in-process + FastAPI `TestClient` smoke for `/health` and `/guides` - pass
- KOPIS key injected through hidden stdin/env + `generate_visit_guide("EK 콘서트")` - pass
- KOPIS key injected through hidden stdin/env + `generate_visit_guide("워터밤")` - pass
- KOPIS canonical HTTPS endpoint smoke - pass
- KOPIS key injected through hidden stdin/env + alias-expanded `search_kopis_with_fallback("랩비트 페스티벌")` - pass, no current KOPIS result

## Scenarios

| ID | Input | Result | Notes |
| --- | --- | --- | --- |
| S12 | `워터밤` | `event_candidates` | 실제 Tavily 검색 기준 2026 서울/부산 후보 반환, 과거 회차 후보 제거 |
| KOPIS | `워터밤` | `event_candidates` | 실제 KOPIS 기준 서울/속초 후보 반환, 각 후보 `official_confirmed` |
| S1/S10 | `KSPO DOME 콘서트 준비물` | `concert_with_venue_hint` | backend API에서 KSPO DOME venue guide 반환 |
| broad event | `랩비트 공연` | `event_candidates` | backend API에서 후보 4개 반환 |
| broad event | `랩비트 페스티벌` | `event_candidates` | backend API에서 2026 서울/문화비축기지 후보 반환, 과거 회차 후보 제거 |
| single concert | `EK 콘서트` | `concert_with_inferred_venue` + `event_info` | backend API에서 YES24 Live Hall, `2026.05.10`, `18:00` 표시 |
| KOPIS | `EK 콘서트` | `concert_with_inferred_venue` + `event_info` | 실제 KOPIS 기준 YES24 Live Hall, `2026년 5월 10일`, `official_confirmed` |
| KOPIS alias | `랩비트 페스티벌` | no KOPIS result | `RAPBEAT`/`RAP BEAT` alias까지 검색했지만 현재 KOPIS 공식 목록 결과 없음 |

## Risks

- 라이브 검색 결과는 Tavily 색인 상태에 따라 후보 개수와 세부 후보명이 달라질 수 있습니다.
- KOPIS에 없는 공연명은 기존 public search/fallback 경로에 의존합니다.
