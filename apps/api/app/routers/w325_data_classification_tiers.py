"""Wave 325: Data Classification Tiers v1 Router — Tag documents/fields with classification tiers; show tier in UI; enforce policy by tier.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w325_data_classification_tiers import service

router = APIRouter(tags=["Data Classification Tiers v1"])

@router.get("/api/data-classification-tiers")
async def api_data_classification_tiers_w325_list_classifications(limit: int = 100):
    """List classifications"""
    items = service.list_classifications(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/data-classification-tiers", status_code=201)
async def api_data_classification_tiers_w325_create_classification(request: Request):
    """Classify a document/field"""
    data = await request.json()
    item = service.create_classification(data)
    return item

@router.get("/api/data-classification-tiers/report")
async def api_data_classification_tiers_w325_classification_report(limit: int = 100):
    """Get classification report"""
    items = service.classification_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/data-classification-tiers/{classification_id}")
async def api_data_classification_tiers_w325_get_classification(classification_id: str):
    """Get classification details"""
    item = service.get_classification(classification_id)
    if not item:
        raise HTTPException(status_code=404, detail="data_classification_tiers not found")
    return item

@router.post("/api/data-classification-tiers/{classification_id}/enforce")
async def api_data_classification_tiers_w325_enforce_policy(classification_id: str, request: Request):
    """Enforce tier policy"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.enforce_policy(classification_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="data_classification_tiers not found")
    return item

@router.post("/api/data-classification-tiers/{classification_id}/reclassify")
async def api_data_classification_tiers_w325_reclassify(classification_id: str, request: Request):
    """Reclassify tier"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reclassify(classification_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="data_classification_tiers not found")
    return item
