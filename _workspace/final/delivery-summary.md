# Delivery Summary

## Issue

- #22 `[backend] /analyze 호환 엔드포인트와 입력 검증 추가`

## Changes

- Kept `POST /guides` as the canonical guide generation endpoint.
- Added `POST /analyze` as a compatibility alias with the same `GuideResponse` contract.
- Normalized `GuideRequest.query` before agent execution and reject blank or whitespace-only values.
- Added backend API tests for the alias, trimming behavior, and blank input rejection.
- Documented the backend API contract in `README.md`.

## Validation

- `python3 scripts/validate_harness.py`
- `uv run --python 3.11 pytest`
- Manual smoke:
  - `/guides` and `/analyze` both return 200 with trimmed `input`
  - `/guides` and `/analyze` both return 422 for whitespace-only `query`
