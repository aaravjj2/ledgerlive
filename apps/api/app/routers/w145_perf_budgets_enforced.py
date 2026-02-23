"""Wave 145: Performance Budgets Enforced Router — Enforced performance budgets with automated regression detection.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w145_perf_budgets_enforced import service

router = APIRouter(tags=["Performance Budgets Enforced"])

@router.get("/api/perf-budgets-enforced")
async def api_perf_budgets_enforced_w145_list_budgets(limit: int = 100):
    """List enforced perf budgets"""
    items = service.list_budgets(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/perf-budgets-enforced", status_code=201)
async def api_perf_budgets_enforced_w145_set_budget(request: Request):
    """Set enforced perf budget"""
    data = await request.json()
    item = service.set_budget(data)
    return item

@router.get("/api/perf-budgets-enforced/report")
async def api_perf_budgets_enforced_w145_enforcement_report(limit: int = 100):
    """Get enforcement report"""
    items = service.enforcement_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/perf-budgets-enforced/{budget_id}")
async def api_perf_budgets_enforced_w145_get_budget(budget_id: str):
    """Get budget details"""
    item = service.get_budget(budget_id)
    if not item:
        raise HTTPException(status_code=404, detail="perf_budgets_enforced not found")
    return item

@router.post("/api/perf-budgets-enforced/{budget_id}/enforce")
async def api_perf_budgets_enforced_w145_enforce(budget_id: str, request: Request):
    """Enforce budget gate"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.enforce(budget_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="perf_budgets_enforced not found")
    return item

@router.post("/api/perf-budgets-enforced/{budget_id}/measure")
async def api_perf_budgets_enforced_w145_measure(budget_id: str, request: Request):
    """Measure performance"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.measure(budget_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="perf_budgets_enforced not found")
    return item
