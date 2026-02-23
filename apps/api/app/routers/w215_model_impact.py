"""Wave 215: Model Impact Dashboard v1 Router — Compare review queue volume reduction, false match reduction, calibration error improvement. Computed on fixture-eval runs deterministically.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w215_model_impact import service

router = APIRouter(tags=["Model Impact Dashboard v1"])

@router.get("/api/model-impact")
async def api_model_impact_w215_list_impacts(limit: int = 100):
    """List model impact evaluations"""
    items = service.list_impacts(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/model-impact", status_code=201)
async def api_model_impact_w215_compute_impact(request: Request):
    """Compute model impact metrics"""
    data = await request.json()
    item = service.compute_impact(data)
    return item

@router.get("/api/model-impact/report")
async def api_model_impact_w215_impact_report(limit: int = 100):
    """Get model impact report"""
    items = service.impact_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/model-impact/{impact_id}")
async def api_model_impact_w215_get_impact(impact_id: str):
    """Get impact details"""
    item = service.get_impact(impact_id)
    if not item:
        raise HTTPException(status_code=404, detail="model_impact not found")
    return item

@router.post("/api/model-impact/{impact_id}/compare")
async def api_model_impact_w215_compare_baseline(impact_id: str, request: Request):
    """Compare baseline vs model metrics"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.compare_baseline(impact_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="model_impact not found")
    return item

@router.post("/api/model-impact/{impact_id}/verify")
async def api_model_impact_w215_verify_metrics(impact_id: str, request: Request):
    """Verify metrics determinism"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_metrics(impact_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="model_impact not found")
    return item
