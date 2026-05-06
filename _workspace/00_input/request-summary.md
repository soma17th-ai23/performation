# Request Summary

## Issue

- GitHub issue: #26 `[agent] 공개 SNS 공식 공지 출처 처리 추가`

## Scope

- Add public-search query coverage for official SNS notices.
- Treat official SNS notice links as `latest_official_check_required` confirmation channels.
- Keep generic SNS posts uncertain and fan/review SNS posts as `public_review_reference`.
- Preserve the project boundary: no direct SNS login crawling or page scraping.
- Preserve frontend -> backend -> agent dependency boundary.

## Validation Plan

- `python3 scripts/validate_harness.py`
- `uv run --python 3.11 pytest`
