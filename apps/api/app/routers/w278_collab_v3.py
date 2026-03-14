"""Wave 278: Collaboration v3 Router — Mentions, watchers across channels with activity feed tied to Race Control lanes. Deterministic feed ordering.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w278_collab_v3 import service

router = APIRouter(tags=["Collaboration v3"])

@router.get("/api/collab-v3")
async def api_collab_v3_w278_list_collabs(limit: int = 100):
    """List collaborations"""
    items = service.list_collabs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/collab-v3", status_code=201)
async def api_collab_v3_w278_create_collab(request: Request):
    """Create collaboration entry"""
    data = await request.json()
    item = service.create_collab(data)
    return item

@router.get("/api/collab-v3/report")
async def api_collab_v3_w278_collab_report(limit: int = 100):
    """Get collaboration report"""
    items = service.collab_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/collab-v3/{collab_id}")
async def api_collab_v3_w278_get_collab(collab_id: str):
    """Get collaboration details"""
    item = service.get_collab(collab_id)
    if not item:
        raise HTTPException(status_code=404, detail="collab_v3 not found")
    return item

@router.post("/api/collab-v3/{collab_id}/feed")
async def api_collab_v3_w278_get_feed(collab_id: str, request: Request):
    """Get activity feed"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.get_feed(collab_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="collab_v3 not found")
    return item

@router.post("/api/collab-v3/{collab_id}/mention")
async def api_collab_v3_w278_add_mention(collab_id: str, request: Request):
    """Add mention"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_mention(collab_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="collab_v3 not found")
    return item

@router.post("/api/collab-v3/{collab_id}/watcher")
async def api_collab_v3_w278_add_watcher(collab_id: str, request: Request):
    """Add watcher"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_watcher(collab_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="collab_v3 not found")
    return item
