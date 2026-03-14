"""Wave 242: Plan Preview v1 Router — Agent proposes a full run plan with sequence of actions and predicted artifacts/hashes. Zero side effects — preview only with deterministic output.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w242_plan_preview import service

router = APIRouter(tags=["Plan Preview v1"])

@router.get("/api/plan-preview")
async def api_plan_preview_w242_list_plans(limit: int = 100):
    """List plan previews"""
    items = service.list_plans(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/plan-preview", status_code=201)
async def api_plan_preview_w242_create_preview(request: Request):
    """Create plan preview"""
    data = await request.json()
    item = service.create_preview(data)
    return item

@router.get("/api/plan-preview/report")
async def api_plan_preview_w242_plan_report(limit: int = 100):
    """Get plan preview report"""
    items = service.plan_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/plan-preview/{plan_id}")
async def api_plan_preview_w242_get_plan(plan_id: str):
    """Get plan preview details"""
    item = service.get_plan(plan_id)
    if not item:
        raise HTTPException(status_code=404, detail="plan_preview not found")
    return item

@router.post("/api/plan-preview/{plan_id}/predict-hashes")
async def api_plan_preview_w242_predict_hashes(plan_id: str, request: Request):
    """Predict artifact hashes"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.predict_hashes(plan_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="plan_preview not found")
    return item

@router.post("/api/plan-preview/{plan_id}/validate")
async def api_plan_preview_w242_validate_plan(plan_id: str, request: Request):
    """Validate plan prerequisites"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_plan(plan_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="plan_preview not found")
    return item
