from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from performation_agent import generate_visit_guide
from performation_domain import ErrorResponse, GuideRequest, GuideResponse


app = FastAPI(
  title="Performation API",
  description="Backend API that owns Performation agent workflow execution.",
  version="0.1.0",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
  first = exc.errors()[0]
  return JSONResponse(
    status_code=400,
    content=ErrorResponse(
      error_message="입력값이 올바르지 않습니다.",
      detail=first.get("msg"),
    ).model_dump(),
  )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
  return JSONResponse(
    status_code=500,
    content=ErrorResponse(
      error_message="요청을 처리하는 중 오류가 발생했습니다.",
      detail=str(exc) if str(exc) else None,
    ).model_dump(),
  )


@app.get("/health")
def health() -> dict[str, str]:
  return {"status": "ok"}


@app.post("/guides", response_model=GuideResponse)
@app.post("/analyze", response_model=GuideResponse)
def create_guide(request: GuideRequest) -> GuideResponse:
  return generate_visit_guide(request.query)
