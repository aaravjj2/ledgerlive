"""Wave 146: Export Time Budgets Router — Export time budgets and stable resource usage reporting.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w146_export_budget import service

router = APIRouter(tags=["Export Time Budgets"])

@router.get("/api/export-budgets")
async def api_export_budget_w146_list_budgets(limit: int = 100):
    """List export time budgets"""
    items = service.list_budgets(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/export-budgets", status_code=201)
async def api_export_budget_w146_set_budget(request: Request):
    """Set export time budget"""
    data = await request.json()
    item = service.set_budget(data)
    return item

@router.get("/api/export-budgets/report")
async def api_export_budget_w146_resource_report(limit: int = 100):
    """Get resource usage report"""
    items = service.resource_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/export-budgets/{budget_id}")
async def api_export_budget_w146_get_budget(budget_id: str):
    """Get budget details"""
    item = service.get_budget(budget_id)
    if not item:
        raise HTTPException(status_code=404, detail="export_budget not found")
    return item

@router.post("/api/export-budgets/{budget_id}/measure")
async def api_export_budget_w146_measure(budget_id: str, request: Request):
    """Measure export timing"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.measure(budget_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="export_budget not found")
    return item
