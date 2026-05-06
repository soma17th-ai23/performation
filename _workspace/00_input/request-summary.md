# Request Summary

## Issue

- GitHub issue: #16 `[agent] 공연 후보 다중 추론 및 선택 요청 응답 지원`

## Scope

- Add search-based event candidate options for broad concert/festival inputs.
- Return multiple regional/date candidates instead of forcing a single venue guide.
- Keep ticketing/payment/action execution out of scope.
- Preserve frontend -> backend -> agent dependency boundary.

## Validation Plan

- `python3 scripts/validate_harness.py`
- `uv run --python 3.11 pytest`
