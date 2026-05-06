# Delivery Summary

## Issue

- #16 `[agent] 공연 후보 다중 추론 및 선택 요청 응답 지원`

## Changes

- Added `event_candidates` to the shared response contract.
- Added `infer_event_candidates` to produce regional/date options for broad event inputs.
- Added `event_candidates` input type and S12 scenario.
- Updated the Gradio renderer to show candidate options when present.
- Kept user-facing wording focused on selection and official confirmation, without exposing local-data internals.

## Validation

- `python3 scripts/validate_harness.py`
- `uv run --python 3.11 pytest`
- Manual smoke:
  - `워터밤` + Seoul/Incheon search results -> `event_candidates`
