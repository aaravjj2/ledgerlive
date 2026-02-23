"""Wave 88: Consolidation Regression Budgets Router — Regression budgets for consolidation outputs ensuring stable results.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w088_consol_regression import service

router = APIRouter(tags=["Consolidation Regression Budgets"])

@router.get("/api/consol-regression")
async def api_consol_regression_w88_list_budgets(limit: int = 100):
    """List regression budgets"""
    items = service.list_budgets(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/consol-regression", status_code=201)
async def api_consol_regression_w88_set_budget(request: Request):
    """Set regression budget"""
    data = await request.json()
    item = service.set_budget(data)
    return item

@router.get("/api/consol-regression/report")
async def api_consol_regression_w88_budget_report(limit: int = 100):
    """Get regression report"""
    items = service.budget_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/consol-regression/{budget_id}")
async def api_consol_regression_w88_get_budget(budget_id: str):
    """Get budget details"""
    item = service.get_budget(budget_id)
    if not item:
        raise HTTPException(status_code=404, detail="consol_regression not found")
    return item

@router.post("/api/consol-regression/{budget_id}/measure")
async def api_consol_regression_w88_measure(budget_id: str, request: Request):
    """Measure against budget"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.measure(budget_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="consol_regression not found")
    return item
