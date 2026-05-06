from __future__ import annotations

from fastapi import FastAPI

from performation_agent import generate_visit_guide
from performation_domain import GuideRequest, GuideResponse


app = FastAPI(
  title="Performation API",
  description="Backend API that owns Performation agent workflow execution.",
  version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
  return {"status": "ok"}


@app.post("/guides", response_model=GuideResponse)
def create_guide(request: GuideRequest) -> GuideResponse:
  return _run_guide_workflow(request)


@app.post("/analyze", response_model=GuideResponse)
def analyze_guide(request: GuideRequest) -> GuideResponse:
  return _run_guide_workflow(request)


def _run_guide_workflow(request: GuideRequest) -> GuideResponse:
  return generate_visit_guide(request.query)
