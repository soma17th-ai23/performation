# Delivery Summary

## Issue

- #26 `[agent] 공개 SNS 공식 공지 출처 처리 추가`

## Changes

- Added `공식 SNS 공지` public-search query coverage.
- Added SNS source classification that distinguishes official notices, unverified posts, and fan/review posts.
- Allowed official SNS notice snippets to feed event candidate/event info extraction while keeping the confidence label at `latest_official_check_required`.
- Hardened live-search extraction after multi-concert smoke tests:
  - yearless broad event queries now drop past-only event candidates
  - yearless single-concert queries no longer surface past event dates as current event info
  - KINTEX address snippets no longer create a false `고양` regional WATERBOMB candidate
  - KINTEX venue names trim marketing copy such as `올해는 더 강력한...`
- Added `threads.com` to SNS-domain handling after live results surfaced Threads URLs.
- Documented the boundary: public search metadata/snippets only, no direct SNS login crawling.

## Validation

- `python3 scripts/validate_harness.py` - pass
- `uv run --python 3.11 pytest` - pass, 91 passed
- `git diff --check` - pass
- `tests/test_source_classifier.py` covers official SNS, unverified SNS, and fan/review SNS branches.
- `tests/test_agent_workflow.py` covers SNS query generation, candidate extraction without official overtrust, past-date filtering, and KINTEX address-region cleanup.
- PR review follow-up prevents lower-confidence SNS/review fields from filling higher-confidence event info.
- Live multi-concert smoke covered `랩비트 페스티벌`, `워터밤`, `EK 콘서트`, `아이유 콘서트 KSPO`, `데이식스 콘서트`, and `싸이 흠뻑쇼` with Tavily+Gemini configured.
