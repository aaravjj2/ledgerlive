"""Race Weekend Router — Stage model endpoints for the Race Control timeline.

PROJECT_ID: LEDGERLIVE

Endpoints:
  GET /api/race-weekend/stages   → canonical 6-stage model with lap times + safety car state
"""
from __future__ import annotations

from fastapi import APIRouter

from app.services.race_weekend import get_race_weekend_stages

router = APIRouter(prefix="/api/race-weekend", tags=["race-weekend"])


@router.get("/stages")
async def race_weekend_stages() -> dict:
    """Return canonical race weekend stage model with metrics for the Race Control timeline."""
    return get_race_weekend_stages()
