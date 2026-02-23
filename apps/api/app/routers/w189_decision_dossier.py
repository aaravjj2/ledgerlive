"""Wave 189: Decision Dossier Model API Router — Decision dossier entity for exception resolutions and approvals: evidence spans, recon scoring, ML confidence, approvals chain, export verification.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w189_decision_dossier import service

router = APIRouter(tags=["Decision Dossier Model API"])

@router.get("/api/decision-dossiers")
async def api_decision_dossier_w189_list_dossiers(limit: int = 100):
    """List decision dossiers"""
    items = service.list_dossiers(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/decision-dossiers", status_code=201)
async def api_decision_dossier_w189_create_dossier(request: Request):
    """Create decision dossier"""
    data = await request.json()
    item = service.create_dossier(data)
    return item

@router.get("/api/decision-dossiers/report")
async def api_decision_dossier_w189_dossier_report(limit: int = 100):
    """Get dossier report"""
    items = service.dossier_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/decision-dossiers/{dossier_id}")
async def api_decision_dossier_w189_get_dossier(dossier_id: str):
    """Get dossier details"""
    item = service.get_dossier(dossier_id)
    if not item:
        raise HTTPException(status_code=404, detail="decision_dossier not found")
    return item

@router.post("/api/decision-dossiers/{dossier_id}/approval")
async def api_decision_dossier_w189_add_approval(dossier_id: str, request: Request):
    """Add approval to chain"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_approval(dossier_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="decision_dossier not found")
    return item

@router.post("/api/decision-dossiers/{dossier_id}/evidence")
async def api_decision_dossier_w189_add_evidence(dossier_id: str, request: Request):
    """Add evidence span"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_evidence(dossier_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="decision_dossier not found")
    return item

@router.post("/api/decision-dossiers/{dossier_id}/verify")
async def api_decision_dossier_w189_verify_dossier(dossier_id: str, request: Request):
    """Verify dossier completeness"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_dossier(dossier_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="decision_dossier not found")
    return item
