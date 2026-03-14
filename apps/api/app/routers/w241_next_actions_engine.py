"""Wave 241: Next Actions Engine v1 Router — Generates prioritized next steps from DAG, blockers, SLA, and incidents. Output is deterministic and dossier-linked with evidence references.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w241_next_actions_engine import service

router = APIRouter(tags=["Next Actions Engine v1"])

@router.get("/api/next-actions")
async def api_next_actions_engine_w241_list_actions(limit: int = 100):
    """List prioritized next actions"""
    items = service.list_actions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/next-actions", status_code=201)
async def api_next_actions_engine_w241_generate_actions(request: Request):
    """Generate next actions from DAG state"""
    data = await request.json()
    item = service.generate_actions(data)
    return item

@router.get("/api/next-actions/report")
async def api_next_actions_engine_w241_actions_report(limit: int = 100):
    """Get next actions report"""
    items = service.actions_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/next-actions/{action_id}")
async def api_next_actions_engine_w241_get_action(action_id: str):
    """Get action details"""
    item = service.get_action(action_id)
    if not item:
        raise HTTPException(status_code=404, detail="next_actions_engine not found")
    return item

@router.post("/api/next-actions/{action_id}/dismiss")
async def api_next_actions_engine_w241_dismiss_action(action_id: str, request: Request):
    """Dismiss action"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.dismiss_action(action_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="next_actions_engine not found")
    return item

@router.post("/api/next-actions/{action_id}/link-dossier")
async def api_next_actions_engine_w241_link_dossier(action_id: str, request: Request):
    """Link dossier to action"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.link_dossier(action_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="next_actions_engine not found")
    return item

@router.post("/api/next-actions/{action_id}/reprioritize")
async def api_next_actions_engine_w241_reprioritize(action_id: str, request: Request):
    """Reprioritize action"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reprioritize(action_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="next_actions_engine not found")
    return item
