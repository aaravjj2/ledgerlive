"""Wave 109: Compliance Regression Budgets Router — Regression budgets for compliance coverage metrics.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w109_compliance_regression import service

router = APIRouter(tags=["Compliance Regression Budgets"])

@router.get("/api/compliance-regression")
async def api_compliance_regression_w109_list_budgets(limit: int = 100):
    """List compliance regression budgets"""
    items = service.list_budgets(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/compliance-regression", status_code=201)
async def api_compliance_regression_w109_set_budget(request: Request):
    """Set regression budget"""
    data = await request.json()
    item = service.set_budget(data)
    return item

@router.get("/api/compliance-regression/report")
async def api_compliance_regression_w109_regression_report(limit: int = 100):
    """Get regression report"""
    items = service.regression_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/compliance-regression/{budget_id}")
async def api_compliance_regression_w109_get_budget(budget_id: str):
    """Get budget details"""
    item = service.get_budget(budget_id)
    if not item:
        raise HTTPException(status_code=404, detail="compliance_regression not found")
    return item

@router.post("/api/compliance-regression/{budget_id}/measure")
async def api_compliance_regression_w109_measure(budget_id: str, request: Request):
    """Measure compliance coverage"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.measure(budget_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="compliance_regression not found")
    return item
