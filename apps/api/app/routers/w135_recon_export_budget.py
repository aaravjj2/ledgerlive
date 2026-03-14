"""Wave 135: Recon/Export Regression Budgets Router — Strict regression budgets for reconciliation and export output stability.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w135_recon_export_budget import service

router = APIRouter(tags=["Recon/Export Regression Budgets"])

@router.get("/api/recon-export-budgets")
async def api_recon_export_budget_w135_list_budgets(limit: int = 100):
    """List recon/export budgets"""
    items = service.list_budgets(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/recon-export-budgets", status_code=201)
async def api_recon_export_budget_w135_set_budget(request: Request):
    """Set regression budget"""
    data = await request.json()
    item = service.set_budget(data)
    return item

@router.get("/api/recon-export-budgets/report")
async def api_recon_export_budget_w135_budget_report(limit: int = 100):
    """Get budget report"""
    items = service.budget_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/recon-export-budgets/{budget_id}")
async def api_recon_export_budget_w135_get_budget(budget_id: str):
    """Get budget details"""
    item = service.get_budget(budget_id)
    if not item:
        raise HTTPException(status_code=404, detail="recon_export_budget not found")
    return item

@router.post("/api/recon-export-budgets/{budget_id}/measure")
async def api_recon_export_budget_w135_measure(budget_id: str, request: Request):
    """Measure output stability"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.measure(budget_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="recon_export_budget not found")
    return item
