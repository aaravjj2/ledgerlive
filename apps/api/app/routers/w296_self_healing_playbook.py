"""Wave 296: Self-Healing Playbook v2 Router — Playbooks suggest recovery steps, require approvals, and are fully audited. Deterministic step sequencing.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w296_self_healing_playbook import service

router = APIRouter(tags=["Self-Healing Playbook v2"])

@router.get("/api/self-healing-playbook")
async def api_self_healing_playbook_w296_list_playbooks(limit: int = 100):
    """List self-healing playbooks"""
    items = service.list_playbooks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/self-healing-playbook", status_code=201)
async def api_self_healing_playbook_w296_create_playbook(request: Request):
    """Create self-healing playbook"""
    data = await request.json()
    item = service.create_playbook(data)
    return item

@router.get("/api/self-healing-playbook/report")
async def api_self_healing_playbook_w296_playbook_report(limit: int = 100):
    """Get self-healing playbook report"""
    items = service.playbook_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/self-healing-playbook/{playbook_id}")
async def api_self_healing_playbook_w296_get_playbook(playbook_id: str):
    """Get playbook details"""
    item = service.get_playbook(playbook_id)
    if not item:
        raise HTTPException(status_code=404, detail="self_healing_playbook not found")
    return item

@router.post("/api/self-healing-playbook/{playbook_id}/advance")
async def api_self_healing_playbook_w296_advance_step(playbook_id: str, request: Request):
    """Advance playbook step"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.advance_step(playbook_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="self_healing_playbook not found")
    return item

@router.post("/api/self-healing-playbook/{playbook_id}/approve")
async def api_self_healing_playbook_w296_approve_step(playbook_id: str, request: Request):
    """Approve recovery step"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_step(playbook_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="self_healing_playbook not found")
    return item

@router.post("/api/self-healing-playbook/{playbook_id}/complete")
async def api_self_healing_playbook_w296_complete_playbook(playbook_id: str, request: Request):
    """Complete playbook"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.complete_playbook(playbook_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="self_healing_playbook not found")
    return item
