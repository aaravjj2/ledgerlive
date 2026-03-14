"""Wave 216: Drift Monitoring Budgets Enforced Router — Drift snapshot per release: dataset hash, model hash, metrics. Budget enforcement fails if key metrics regress beyond thresholds.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w216_drift_budgets import service

router = APIRouter(tags=["Drift Monitoring Budgets Enforced"])

@router.get("/api/drift-budgets")
async def api_drift_budgets_w216_list_budgets(limit: int = 100):
    """List drift budget evaluations"""
    items = service.list_budgets(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/drift-budgets", status_code=201)
async def api_drift_budgets_w216_evaluate_budget(request: Request):
    """Evaluate drift budget"""
    data = await request.json()
    item = service.evaluate_budget(data)
    return item

@router.get("/api/drift-budgets/report")
async def api_drift_budgets_w216_budget_report(limit: int = 100):
    """Get drift budget report"""
    items = service.budget_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/drift-budgets/{budget_id}")
async def api_drift_budgets_w216_get_budget(budget_id: str):
    """Get budget details"""
    item = service.get_budget(budget_id)
    if not item:
        raise HTTPException(status_code=404, detail="drift_budgets not found")
    return item

@router.post("/api/drift-budgets/{budget_id}/enforce")
async def api_drift_budgets_w216_enforce_threshold(budget_id: str, request: Request):
    """Enforce budget thresholds"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.enforce_threshold(budget_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="drift_budgets not found")
    return item

@router.post("/api/drift-budgets/{budget_id}/regression")
async def api_drift_budgets_w216_check_regression(budget_id: str, request: Request):
    """Check for metric regression"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_regression(budget_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="drift_budgets not found")
    return item
