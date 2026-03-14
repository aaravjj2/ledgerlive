"""Wave 299: Performance Regression Budgets v1 Router — Fail if key flows exceed thresholds. Stable reports with deterministic timing measurement.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w299_perf_regression import service

router = APIRouter(tags=["Performance Regression Budgets v1"])

@router.get("/api/perf-regression")
async def api_perf_regression_w299_list_perf_regs(limit: int = 100):
    """List performance regressions"""
    items = service.list_perf_regs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/perf-regression", status_code=201)
async def api_perf_regression_w299_create_perf_reg(request: Request):
    """Create performance regression check"""
    data = await request.json()
    item = service.create_perf_reg(data)
    return item

@router.get("/api/perf-regression/report")
async def api_perf_regression_w299_perf_reg_report(limit: int = 100):
    """Get performance regression report"""
    items = service.perf_reg_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/perf-regression/{perf_reg_id}")
async def api_perf_regression_w299_get_perf_reg(perf_reg_id: str):
    """Get regression details"""
    item = service.get_perf_reg(perf_reg_id)
    if not item:
        raise HTTPException(status_code=404, detail="perf_regression not found")
    return item

@router.post("/api/perf-regression/{perf_reg_id}/measure")
async def api_perf_regression_w299_run_measurement(perf_reg_id: str, request: Request):
    """Run performance measurement"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.run_measurement(perf_reg_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="perf_regression not found")
    return item

@router.post("/api/perf-regression/{perf_reg_id}/threshold")
async def api_perf_regression_w299_check_threshold(perf_reg_id: str, request: Request):
    """Check against threshold"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_threshold(perf_reg_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="perf_regression not found")
    return item
