"""Wave 165: Live Session Simulator Router — Deterministic agent session replay runner: streams transcript events, triggers tool calls, streams verifier outcomes and tool trace updates.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w165_session_sim import service

router = APIRouter(tags=["Live Session Simulator"])

@router.get("/api/session-sim")
async def api_session_sim_w165_list_sessions(limit: int = 100):
    """List simulator sessions"""
    items = service.list_sessions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/session-sim", status_code=201)
async def api_session_sim_w165_start_session(request: Request):
    """Start a simulator session"""
    data = await request.json()
    item = service.start_session(data)
    return item

@router.get("/api/session-sim/report")
async def api_session_sim_w165_session_report(limit: int = 100):
    """Get session simulation report"""
    items = service.session_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/session-sim/{session_id}")
async def api_session_sim_w165_get_session(session_id: str):
    """Get session details"""
    item = service.get_session(session_id)
    if not item:
        raise HTTPException(status_code=404, detail="session_sim not found")
    return item

@router.post("/api/session-sim/{session_id}/advance")
async def api_session_sim_w165_advance_session(session_id: str, request: Request):
    """Advance session step"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.advance_session(session_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="session_sim not found")
    return item

@router.post("/api/session-sim/{session_id}/complete")
async def api_session_sim_w165_complete_session(session_id: str, request: Request):
    """Complete session"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.complete_session(session_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="session_sim not found")
    return item

@router.get("/api/session-sim/{session_id}/transcript")
async def api_session_sim_w165_session_transcript(session_id: str):
    """Get session transcript"""
    item = service.session_transcript(session_id)
    if not item:
        raise HTTPException(status_code=404, detail="session_sim not found")
    return item
