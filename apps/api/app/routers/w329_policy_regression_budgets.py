"""Wave 329: Policy Regression Budgets v1 Router — Fail if deny explainability coverage or detection coverage regresses.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w329_policy_regression_budgets import service

router = APIRouter(tags=["Policy Regression Budgets v1"])

@router.get("/api/policy-regression-budgets")
async def api_policy_regression_budgets_w329_list_budgets(limit: int = 100):
    """List regression budgets"""
    items = service.list_budgets(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/policy-regression-budgets", status_code=201)
async def api_policy_regression_budgets_w329_create_budget(request: Request):
    """Create regression budget"""
    data = await request.json()
    item = service.create_budget(data)
    return item

@router.get("/api/policy-regression-budgets/report")
async def api_policy_regression_budgets_w329_budget_report(limit: int = 100):
    """Get regression budget report"""
    items = service.budget_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/policy-regression-budgets/{budget_id}")
async def api_policy_regression_budgets_w329_get_budget(budget_id: str):
    """Get budget details"""
    item = service.get_budget(budget_id)
    if not item:
        raise HTTPException(status_code=404, detail="policy_regression_budgets not found")
    return item

@router.post("/api/policy-regression-budgets/{budget_id}/evaluate")
async def api_policy_regression_budgets_w329_evaluate_regression(budget_id: str, request: Request):
    """Evaluate regression"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.evaluate_regression(budget_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="policy_regression_budgets not found")
    return item

@router.post("/api/policy-regression-budgets/{budget_id}/reset")
async def api_policy_regression_budgets_w329_reset_baseline(budget_id: str, request: Request):
    """Reset baseline"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reset_baseline(budget_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="policy_regression_budgets not found")
    return item
