"""Wave 148: Batch Workflow Performance Router — Batch workflow performance tests with timing budgets.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w148_batch_workflow_perf import service

router = APIRouter(tags=["Batch Workflow Performance"])

@router.get("/api/batch-workflow-perf")
async def api_batch_workflow_perf_w148_list_benchmarks(limit: int = 100):
    """List batch workflow benchmarks"""
    items = service.list_benchmarks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/batch-workflow-perf", status_code=201)
async def api_batch_workflow_perf_w148_run_benchmark(request: Request):
    """Run batch workflow benchmark"""
    data = await request.json()
    item = service.run_benchmark(data)
    return item

@router.get("/api/batch-workflow-perf/report")
async def api_batch_workflow_perf_w148_perf_report(limit: int = 100):
    """Get batch workflow perf report"""
    items = service.perf_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/batch-workflow-perf/{perf_id}")
async def api_batch_workflow_perf_w148_get_benchmark(perf_id: str):
    """Get benchmark details"""
    item = service.get_benchmark(perf_id)
    if not item:
        raise HTTPException(status_code=404, detail="batch_workflow_perf not found")
    return item

@router.post("/api/batch-workflow-perf/{perf_id}/budget")
async def api_batch_workflow_perf_w148_set_budget(perf_id: str, request: Request):
    """Set performance budget"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.set_budget(perf_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="batch_workflow_perf not found")
    return item
