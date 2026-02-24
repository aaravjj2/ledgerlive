"""Wave 245: Race Control Why v1 Router — Every next action has a one-click dossier/reason DAG/evidence view. Consistent across surfaces with deterministic rendering.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w245_rc_why_dossier import service

router = APIRouter(tags=["Race Control Why v1"])

@router.get("/api/rc-why")
async def api_rc_why_dossier_w245_list_whys(limit: int = 100):
    """List why dossiers"""
    items = service.list_whys(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/rc-why", status_code=201)
async def api_rc_why_dossier_w245_generate_why(request: Request):
    """Generate why dossier for action"""
    data = await request.json()
    item = service.generate_why(data)
    return item

@router.get("/api/rc-why/report")
async def api_rc_why_dossier_w245_why_report(limit: int = 100):
    """Get why dossier report"""
    items = service.why_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/rc-why/{why_id}")
async def api_rc_why_dossier_w245_get_why(why_id: str):
    """Get why dossier details"""
    item = service.get_why(why_id)
    if not item:
        raise HTTPException(status_code=404, detail="rc_why_dossier not found")
    return item

@router.post("/api/rc-why/{why_id}/expand")
async def api_rc_why_dossier_w245_expand_reason(why_id: str, request: Request):
    """Expand reason DAG node"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.expand_reason(why_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_why_dossier not found")
    return item

@router.post("/api/rc-why/{why_id}/verify-consistency")
async def api_rc_why_dossier_w245_verify_consistency(why_id: str, request: Request):
    """Verify cross-surface consistency"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_consistency(why_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_why_dossier not found")
    return item
