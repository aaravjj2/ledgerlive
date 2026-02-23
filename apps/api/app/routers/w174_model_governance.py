"""Wave 174: Model Governance Lite Router — Model registry, dataset registry, drift snapshot in eval reports. Drift report artifacts with stable ordering and hashes.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w174_model_governance import service

router = APIRouter(tags=["Model Governance Lite"])

@router.get("/api/model-governance")
async def api_model_governance_w174_list_governance(limit: int = 100):
    """List governance records"""
    items = service.list_governance(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/model-governance", status_code=201)
async def api_model_governance_w174_create_eval(request: Request):
    """Create governance evaluation"""
    data = await request.json()
    item = service.create_eval(data)
    return item

@router.get("/api/model-governance/report")
async def api_model_governance_w174_governance_report(limit: int = 100):
    """Get governance report"""
    items = service.governance_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/model-governance/{governance_id}")
async def api_model_governance_w174_get_governance(governance_id: str):
    """Get governance record"""
    item = service.get_governance(governance_id)
    if not item:
        raise HTTPException(status_code=404, detail="model_governance not found")
    return item

@router.post("/api/model-governance/{governance_id}/drift")
async def api_model_governance_w174_compute_drift(governance_id: str, request: Request):
    """Compute drift snapshot"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.compute_drift(governance_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="model_governance not found")
    return item

@router.post("/api/model-governance/{governance_id}/verify")
async def api_model_governance_w174_verify_stability(governance_id: str, request: Request):
    """Verify snapshot stability"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_stability(governance_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="model_governance not found")
    return item
