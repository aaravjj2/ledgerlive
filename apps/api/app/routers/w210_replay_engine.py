"""Wave 210: Replay Engine v1 Router — Replay close run from artifacts: re-run recon, triage, approvals simulation in sandbox. Output replay_report with step hashes. Deterministic replay.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w210_replay_engine import service

router = APIRouter(tags=["Replay Engine v1"])

@router.get("/api/replay-engine")
async def api_replay_engine_w210_list_replays(limit: int = 100):
    """List replay runs"""
    items = service.list_replays(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/replay-engine", status_code=201)
async def api_replay_engine_w210_start_replay(request: Request):
    """Start replay from artifacts"""
    data = await request.json()
    item = service.start_replay(data)
    return item

@router.get("/api/replay-engine/report")
async def api_replay_engine_w210_replay_report(limit: int = 100):
    """Get replay engine report"""
    items = service.replay_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/replay-engine/{replay_id}")
async def api_replay_engine_w210_get_replay(replay_id: str):
    """Get replay details"""
    item = service.get_replay(replay_id)
    if not item:
        raise HTTPException(status_code=404, detail="replay_engine not found")
    return item

@router.post("/api/replay-engine/{replay_id}/advance")
async def api_replay_engine_w210_advance_step(replay_id: str, request: Request):
    """Advance replay step"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.advance_step(replay_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="replay_engine not found")
    return item

@router.post("/api/replay-engine/{replay_id}/verify")
async def api_replay_engine_w210_verify_replay(replay_id: str, request: Request):
    """Verify replay hashes match original"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_replay(replay_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="replay_engine not found")
    return item
