"""Agent Loop Router — Perceive → Decide → Act autonomous close agent.

Exposes the agent's autonomous loop as REST endpoints:
  POST /api/agent/cycle       → run one full perceive→decide→act cycle
  GET  /api/agent/cycles      → recent cycle history
  GET  /api/agent/cycle/{id}  → specific cycle detail
  GET  /api/agent/perceive    → read-only perception of current state

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["Agent Loop"])


@router.post("/api/agent/cycle", status_code=201)
async def run_agent_cycle():
    """Run one full perceive→decide→act cycle.

    The agent:
    1. PERCEIVES current state from all live services
    2. DECIDES which actions to take (auto-resolve, escalate, advance)
    3. ACTS by executing those actions against the live stores
    4. Posts results to Airia webhook

    Returns the complete decision trace for auditability.
    """
    from app.services.agent_loop import run_cycle
    return run_cycle()


@router.get("/api/agent/cycles")
async def list_agent_cycles(limit: int = 20):
    """Return recent agent cycle history."""
    from app.services.agent_loop import get_cycle_log
    cycles = get_cycle_log(limit)
    return {
        "cycles": cycles,
        "total": len(cycles),
    }


@router.get("/api/agent/cycle/{cycle_id}")
async def get_agent_cycle(cycle_id: str):
    """Get a specific agent cycle by ID."""
    from app.services.agent_loop import get_cycle
    cycle = get_cycle(cycle_id)
    if not cycle:
        raise HTTPException(status_code=404, detail=f"Cycle {cycle_id} not found")
    return cycle


@router.get("/api/agent/perceive")
async def agent_perceive():
    """Read-only perception of current system state.

    This is the PERCEIVE phase only — no actions are taken.
    Useful for dashboards and monitoring.
    """
    from app.services.agent_loop import perceive
    return perceive()
