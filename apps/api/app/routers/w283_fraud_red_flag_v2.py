"""Wave 283: Fraud Red Flag Engine v2 Router — Vendor spoofing, duplicates, and outlier detection with dossier linking and approval gates for risky actions.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w283_fraud_red_flag_v2 import service

router = APIRouter(tags=["Fraud Red Flag Engine v2"])

@router.get("/api/fraud-red-flag-v2")
async def api_fraud_red_flag_v2_w283_list_flags(limit: int = 100):
    """List fraud red flags"""
    items = service.list_flags(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/fraud-red-flag-v2", status_code=201)
async def api_fraud_red_flag_v2_w283_create_flag(request: Request):
    """Create fraud red flag"""
    data = await request.json()
    item = service.create_flag(data)
    return item

@router.get("/api/fraud-red-flag-v2/report")
async def api_fraud_red_flag_v2_w283_flag_report(limit: int = 100):
    """Get fraud red flag report"""
    items = service.flag_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/fraud-red-flag-v2/{flag_id}")
async def api_fraud_red_flag_v2_w283_get_flag(flag_id: str):
    """Get red flag details"""
    item = service.get_flag(flag_id)
    if not item:
        raise HTTPException(status_code=404, detail="fraud_red_flag_v2 not found")
    return item

@router.post("/api/fraud-red-flag-v2/{flag_id}/approve")
async def api_fraud_red_flag_v2_w283_approve_action(flag_id: str, request: Request):
    """Approve risky action"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_action(flag_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="fraud_red_flag_v2 not found")
    return item

@router.post("/api/fraud-red-flag-v2/{flag_id}/assess")
async def api_fraud_red_flag_v2_w283_assess_risk(flag_id: str, request: Request):
    """Assess fraud risk"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.assess_risk(flag_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="fraud_red_flag_v2 not found")
    return item

@router.post("/api/fraud-red-flag-v2/{flag_id}/dossier")
async def api_fraud_red_flag_v2_w283_link_dossier(flag_id: str, request: Request):
    """Link to dossier"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.link_dossier(flag_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="fraud_red_flag_v2 not found")
    return item
