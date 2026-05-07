from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from performation_agent import generate_visit_guide
from performation_domain import GuideRequest, GuideResponse


app = FastAPI(
  title="Performation API",
  description="Backend API that owns Performation agent workflow execution.",
  version="0.1.0",
)

_origins = os.getenv("PERFORMATION_CORS_ORIGINS", "*")
app.add_middleware(
  CORSMiddleware,
  allow_origins=_origins.split(",") if _origins != "*" else ["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
  return {"status": "ok"}


@app.post("/guides", response_model=GuideResponse)
@app.post("/analyze", response_model=GuideResponse)
def create_guide(request: GuideRequest) -> GuideResponse:
  return generate_visit_guide(request.query)
