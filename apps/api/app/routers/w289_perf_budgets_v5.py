"""Wave 289: Performance Budgets v5 Router — 100x fixtures for Race Control, search, and replay with stable pagination enforcement. Deterministic timing verification.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w289_perf_budgets_v5 import service

router = APIRouter(tags=["Performance Budgets v5"])

@router.get("/api/perf-budgets-v5")
async def api_perf_budgets_v5_w289_list_budgets(limit: int = 100):
    """List performance budgets"""
    items = service.list_budgets(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/perf-budgets-v5", status_code=201)
async def api_perf_budgets_v5_w289_create_budget(request: Request):
    """Create performance budget test"""
    data = await request.json()
    item = service.create_budget(data)
    return item

@router.get("/api/perf-budgets-v5/report")
async def api_perf_budgets_v5_w289_budget_report(limit: int = 100):
    """Get performance budget report"""
    items = service.budget_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/perf-budgets-v5/{budget_id}")
async def api_perf_budgets_v5_w289_get_budget(budget_id: str):
    """Get budget details"""
    item = service.get_budget(budget_id)
    if not item:
        raise HTTPException(status_code=404, detail="perf_budgets_v5 not found")
    return item

@router.post("/api/perf-budgets-v5/{budget_id}/benchmark")
async def api_perf_budgets_v5_w289_run_benchmark(budget_id: str, request: Request):
    """Run performance benchmark"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_benchmark(budget_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="perf_budgets_v5 not found")
    return item

@router.post("/api/perf-budgets-v5/{budget_id}/pagination")
async def api_perf_budgets_v5_w289_check_pagination(budget_id: str, request: Request):
    """Check pagination stability"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_pagination(budget_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="perf_budgets_v5 not found")
    return item
