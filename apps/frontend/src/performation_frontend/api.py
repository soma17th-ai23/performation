from __future__ import annotations

import os

import httpx
from performation_domain import ErrorResponse, GuideRequest, GuideResponse

API_URL = os.getenv("PERFORMATION_API_URL", "http://127.0.0.1:8000").rstrip("/")


class PerformationAPIError(Exception):
    """API 호출 중 발생한 기본 예외"""

    pass


def get_guide(query: str) -> GuideResponse:
    """백엔드 API를 호출하여 가이드 데이터를 가져옵니다."""
    try:
        request_data = GuideRequest(query=query)
    except ValueError as exc:
        raise PerformationAPIError(f"유효하지 않은 입력입니다: {exc}")

    try:
        response = httpx.post(
            f"{API_URL}/guides",
            json=request_data.model_dump(),
            timeout=30.0,
        )

        if response.status_code != 200:
            try:
                error_data = ErrorResponse.model_validate(response.json())
                raise PerformationAPIError(
                    f"API 오류: {error_data.error_message} ({error_data.detail or ''})"
                )
            except Exception:
                response.raise_for_status()

        return GuideResponse.model_validate(response.json())
    except httpx.HTTPError as exc:
        raise PerformationAPIError(f"백엔드 API 호출에 실패했습니다: {exc}") from exc
    except Exception as exc:
        raise PerformationAPIError(
            f"데이터 처리 중 오류가 발생했습니다: {exc}"
        ) from exc
