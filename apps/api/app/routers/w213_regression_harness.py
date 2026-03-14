"""Wave 213: Replay Regression Harness v1 Router — Replays N canonical runs and compares tool plan hash, binder hash, dossier hashes. Fails on drift unless baseline update approved.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w213_regression_harness import service

router = APIRouter(tags=["Replay Regression Harness v1"])

@router.get("/api/regression-harness")
async def api_regression_harness_w213_list_harnesses(limit: int = 100):
    """List regression harness runs"""
    items = service.list_harnesses(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/regression-harness", status_code=201)
async def api_regression_harness_w213_run_harness(request: Request):
    """Run regression harness"""
    data = await request.json()
    item = service.run_harness(data)
    return item

@router.get("/api/regression-harness/report")
async def api_regression_harness_w213_harness_report(limit: int = 100):
    """Get regression harness report"""
    items = service.harness_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/regression-harness/{harness_id}")
async def api_regression_harness_w213_get_harness(harness_id: str):
    """Get harness run details"""
    item = service.get_harness(harness_id)
    if not item:
        raise HTTPException(status_code=404, detail="regression_harness not found")
    return item

@router.post("/api/regression-harness/{harness_id}/approve")
async def api_regression_harness_w213_approve_baseline(harness_id: str, request: Request):
    """Approve baseline update"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_baseline(harness_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="regression_harness not found")
    return item

@router.post("/api/regression-harness/{harness_id}/drift")
async def api_regression_harness_w213_detect_drift(harness_id: str, request: Request):
    """Detect drift in canonical runs"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.detect_drift(harness_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="regression_harness not found")
    return item
