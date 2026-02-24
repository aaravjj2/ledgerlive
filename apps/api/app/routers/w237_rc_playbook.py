"""Wave 237: RC Playbook Engine v1 Router — Executable playbooks for common close scenarios: month-end, quarter-end, year-end. Each playbook defines ordered steps, decision points, and rollback procedures.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w237_rc_playbook import service

router = APIRouter(tags=["RC Playbook Engine v1"])

@router.get("/api/rc-playbook")
async def api_rc_playbook_w237_list_playbooks(limit: int = 100):
    """List playbooks"""
    items = service.list_playbooks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/rc-playbook", status_code=201)
async def api_rc_playbook_w237_create_playbook(request: Request):
    """Create playbook"""
    data = await request.json()
    item = service.create_playbook(data)
    return item

@router.get("/api/rc-playbook/report")
async def api_rc_playbook_w237_playbook_report(limit: int = 100):
    """Get playbook engine report"""
    items = service.playbook_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/rc-playbook/{playbook_id}")
async def api_rc_playbook_w237_get_playbook(playbook_id: str):
    """Get playbook details"""
    item = service.get_playbook(playbook_id)
    if not item:
        raise HTTPException(status_code=404, detail="rc_playbook not found")
    return item

@router.post("/api/rc-playbook/{playbook_id}/advance")
async def api_rc_playbook_w237_advance_step(playbook_id: str, request: Request):
    """Advance playbook step"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.advance_step(playbook_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_playbook not found")
    return item

@router.post("/api/rc-playbook/{playbook_id}/rollback")
async def api_rc_playbook_w237_rollback_step(playbook_id: str, request: Request):
    """Rollback playbook step"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.rollback_step(playbook_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_playbook not found")
    return item
