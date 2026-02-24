"""Wave 288: ML Impact v4 Router — Live comparison baseline vs model with drift alerts becoming incidents. Performance budgets enforced with deterministic evaluation.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w288_ml_impact_v4 import service

router = APIRouter(tags=["ML Impact v4"])

@router.get("/api/ml-impact-v4")
async def api_ml_impact_v4_w288_list_impacts(limit: int = 100):
    """List ML impact evaluations"""
    items = service.list_impacts(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/ml-impact-v4", status_code=201)
async def api_ml_impact_v4_w288_create_impact(request: Request):
    """Create ML impact evaluation"""
    data = await request.json()
    item = service.create_impact(data)
    return item

@router.get("/api/ml-impact-v4/report")
async def api_ml_impact_v4_w288_impact_report(limit: int = 100):
    """Get ML impact report"""
    items = service.impact_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/ml-impact-v4/{impact_id}")
async def api_ml_impact_v4_w288_get_impact(impact_id: str):
    """Get impact details"""
    item = service.get_impact(impact_id)
    if not item:
        raise HTTPException(status_code=404, detail="ml_impact_v4 not found")
    return item

@router.post("/api/ml-impact-v4/{impact_id}/compare")
async def api_ml_impact_v4_w288_compare_models(impact_id: str, request: Request):
    """Compare baseline vs model"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.compare_models(impact_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ml_impact_v4 not found")
    return item

@router.post("/api/ml-impact-v4/{impact_id}/drift")
async def api_ml_impact_v4_w288_detect_drift(impact_id: str, request: Request):
    """Detect model drift"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.detect_drift(impact_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ml_impact_v4 not found")
    return item

@router.post("/api/ml-impact-v4/{impact_id}/incident")
async def api_ml_impact_v4_w288_create_drift_incident(impact_id: str, request: Request):
    """Create drift incident"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.create_drift_incident(impact_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="ml_impact_v4 not found")
    return item
