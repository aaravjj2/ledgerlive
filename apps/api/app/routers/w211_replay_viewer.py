"""Wave 211: Replay Viewer UI v1 Router — UI page Replay: timeline of steps, tool trace rows linked to dossiers, evidence span viewer. Fully data-testid instrumented.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w211_replay_viewer import service

router = APIRouter(tags=["Replay Viewer UI v1"])

@router.get("/api/replay-viewer")
async def api_replay_viewer_w211_list_viewers(limit: int = 100):
    """List replay viewer states"""
    items = service.list_viewers(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/replay-viewer", status_code=201)
async def api_replay_viewer_w211_create_viewer(request: Request):
    """Create replay viewer session"""
    data = await request.json()
    item = service.create_viewer(data)
    return item

@router.get("/api/replay-viewer/report")
async def api_replay_viewer_w211_viewer_report(limit: int = 100):
    """Get replay viewer report"""
    items = service.viewer_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/replay-viewer/{viewer_id}")
async def api_replay_viewer_w211_get_viewer(viewer_id: str):
    """Get viewer state"""
    item = service.get_viewer(viewer_id)
    if not item:
        raise HTTPException(status_code=404, detail="replay_viewer not found")
    return item

@router.post("/api/replay-viewer/{viewer_id}/dossier")
async def api_replay_viewer_w211_open_dossier(viewer_id: str, request: Request):
    """Open linked dossier"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.open_dossier(viewer_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="replay_viewer not found")
    return item

@router.post("/api/replay-viewer/{viewer_id}/highlight")
async def api_replay_viewer_w211_highlight_evidence(viewer_id: str, request: Request):
    """Highlight evidence span"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.highlight_evidence(viewer_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="replay_viewer not found")
    return item

@router.post("/api/replay-viewer/{viewer_id}/step")
async def api_replay_viewer_w211_step_forward(viewer_id: str, request: Request):
    """Step forward in timeline"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.step_forward(viewer_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="replay_viewer not found")
    return item
