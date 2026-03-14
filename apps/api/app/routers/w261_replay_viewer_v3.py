"""Wave 261: Replay Viewer v3 Router — Diffing between original and replay artifacts. Jump-to-evidence and jump-to-policy-event navigation with deterministic rendering.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w261_replay_viewer_v3 import service

router = APIRouter(tags=["Replay Viewer v3"])

@router.get("/api/replay-viewer-v3")
async def api_replay_viewer_v3_w261_list_viewers(limit: int = 100):
    """List replay viewers"""
    items = service.list_viewers(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/replay-viewer-v3", status_code=201)
async def api_replay_viewer_v3_w261_create_viewer(request: Request):
    """Create replay viewer comparison"""
    data = await request.json()
    item = service.create_viewer(data)
    return item

@router.get("/api/replay-viewer-v3/report")
async def api_replay_viewer_v3_w261_viewer_report(limit: int = 100):
    """Get replay viewer report"""
    items = service.viewer_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/replay-viewer-v3/{viewer_id}")
async def api_replay_viewer_v3_w261_get_viewer(viewer_id: str):
    """Get viewer details"""
    item = service.get_viewer(viewer_id)
    if not item:
        raise HTTPException(status_code=404, detail="replay_viewer_v3 not found")
    return item

@router.post("/api/replay-viewer-v3/{viewer_id}/diff")
async def api_replay_viewer_v3_w261_compute_diff(viewer_id: str, request: Request):
    """Compute artifact diff"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.compute_diff(viewer_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="replay_viewer_v3 not found")
    return item

@router.post("/api/replay-viewer-v3/{viewer_id}/evidence")
async def api_replay_viewer_v3_w261_jump_to_evidence(viewer_id: str, request: Request):
    """Jump to evidence"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.jump_to_evidence(viewer_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="replay_viewer_v3 not found")
    return item
