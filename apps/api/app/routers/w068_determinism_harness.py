"""Wave 68: Determinism Harness Router — E2E run-twice-compare tool: fails if any output mismatch between runs.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w068_determinism_harness import service

router = APIRouter(tags=["Determinism Harness"])

@router.get("/api/determinism-harness")
async def api_determinism_harness_w68_list_runs(limit: int = 100):
    """List determinism harness runs"""
    items = service.list_runs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/determinism-harness", status_code=201)
async def api_determinism_harness_w68_start_run(request: Request):
    """Start determinism comparison run"""
    data = await request.json()
    item = service.start_run(data)
    return item

@router.get("/api/determinism-harness/diffs")
async def api_determinism_harness_w68_diffs_detail(limit: int = 100):
    """Get diff details"""
    items = service.diffs_detail(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/determinism-harness/report")
async def api_determinism_harness_w68_report(limit: int = 100):
    """Get determinism report"""
    items = service.report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/determinism-harness/{harness_id}")
async def api_determinism_harness_w68_get_run(harness_id: str):
    """Get harness run details"""
    item = service.get_run(harness_id)
    if not item:
        raise HTTPException(status_code=404, detail="determinism_harness not found")
    return item

@router.post("/api/determinism-harness/{harness_id}/compare")
async def api_determinism_harness_w68_compare(harness_id: str, request: Request):
    """Compare two runs"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.compare(harness_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="determinism_harness not found")
    return item
