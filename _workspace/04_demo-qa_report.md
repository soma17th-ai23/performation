# Demo QA Report

## Commands

- `python3 scripts/validate_harness.py` - pass
- `uv run --python 3.11 pytest` - pass, 52 passed
- `git diff --check` - pass
- `.env` loaded in-process + `generate_visit_guide("워터밤")` - pass
- `.env` loaded in-process + FastAPI `TestClient` smoke for `/health` and `/guides` - pass

## Scenarios

| ID | Input | Result | Notes |
| --- | --- | --- | --- |
| S12 | `워터밤` | `event_candidates` | 실제 Tavily 검색 기준 후보 6개 반환, Gradio markdown에 `## 공연 후보` 표시 |
| S1/S10 | `KSPO DOME 콘서트 준비물` | `concert_with_venue_hint` | backend API에서 KSPO DOME venue guide 반환 |
| broad event | `랩비트 공연` | `event_candidates` | backend API에서 후보 4개 반환 |
| broad event | `랩비트 페스티벌` | `event_candidates` | backend API에서 후보 5개 반환, 장소명 과추출 보정 확인 |

## Risks

- 라이브 검색 결과는 Tavily 색인 상태에 따라 후보 개수와 세부 후보명이 달라질 수 있습니다.
