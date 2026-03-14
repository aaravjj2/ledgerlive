"""Wave 336: One Cockpit v1 Router — Race Control as default home route with minimal cognitive load polish.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w336_one_cockpit import service

router = APIRouter(tags=["One Cockpit v1"])

@router.get("/api/one-cockpit")
async def api_one_cockpit_w336_list_cockpits(limit: int = 100):
    """List cockpit configs"""
    items = service.list_cockpits(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/one-cockpit", status_code=201)
async def api_one_cockpit_w336_create_cockpit(request: Request):
    """Create cockpit config"""
    data = await request.json()
    item = service.create_cockpit(data)
    return item

@router.get("/api/one-cockpit/report")
async def api_one_cockpit_w336_cockpit_report(limit: int = 100):
    """Get cockpit config report"""
    items = service.cockpit_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/one-cockpit/{cockpit_id}")
async def api_one_cockpit_w336_get_cockpit(cockpit_id: str):
    """Get cockpit details"""
    item = service.get_cockpit(cockpit_id)
    if not item:
        raise HTTPException(status_code=404, detail="one_cockpit not found")
    return item

@router.post("/api/one-cockpit/{cockpit_id}/customize")
async def api_one_cockpit_w336_customize_layout(cockpit_id: str, request: Request):
    """Customize layout"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.customize_layout(cockpit_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="one_cockpit not found")
    return item

@router.post("/api/one-cockpit/{cockpit_id}/set-default")
async def api_one_cockpit_w336_set_default(cockpit_id: str, request: Request):
    """Set as default home"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.set_default(cockpit_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="one_cockpit not found")
    return item
