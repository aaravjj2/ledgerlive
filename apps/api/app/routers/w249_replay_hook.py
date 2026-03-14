"""Wave 249: Replay Hook v1 Router — Every executed plan auto-creates a replay artifact store snapshot. Replay is available from Race Control with full deterministic reproduction.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w249_replay_hook import service

router = APIRouter(tags=["Replay Hook v1"])

@router.get("/api/replay-hook")
async def api_replay_hook_w249_list_hooks(limit: int = 100):
    """List replay hooks"""
    items = service.list_hooks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/replay-hook", status_code=201)
async def api_replay_hook_w249_create_hook(request: Request):
    """Create replay hook snapshot"""
    data = await request.json()
    item = service.create_hook(data)
    return item

@router.get("/api/replay-hook/report")
async def api_replay_hook_w249_hook_report(limit: int = 100):
    """Get replay hook report"""
    items = service.hook_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/replay-hook/{hook_id}")
async def api_replay_hook_w249_get_hook(hook_id: str):
    """Get replay hook details"""
    item = service.get_hook(hook_id)
    if not item:
        raise HTTPException(status_code=404, detail="replay_hook not found")
    return item

@router.post("/api/replay-hook/{hook_id}/trigger")
async def api_replay_hook_w249_trigger_replay(hook_id: str, request: Request):
    """Trigger replay from snapshot"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.trigger_replay(hook_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="replay_hook not found")
    return item

@router.post("/api/replay-hook/{hook_id}/verify")
async def api_replay_hook_w249_verify_reproduction(hook_id: str, request: Request):
    """Verify reproduction fidelity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_reproduction(hook_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="replay_hook not found")
    return item
