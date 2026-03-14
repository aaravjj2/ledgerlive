"""Wave 176: Reliability Harness v1 Router — Seeded chaos matrix for connector 429, partial OCR, job interruption, storage failure. Deterministic chaos report with resilience score.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w176_reliability_harness import service

router = APIRouter(tags=["Reliability Harness v1"])

@router.get("/api/reliability-harness")
async def api_reliability_harness_w176_list_harnesses(limit: int = 100):
    """List reliability harness runs"""
    items = service.list_harnesses(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/reliability-harness", status_code=201)
async def api_reliability_harness_w176_run_harness(request: Request):
    """Run reliability harness test"""
    data = await request.json()
    item = service.run_harness(data)
    return item

@router.get("/api/reliability-harness/report")
async def api_reliability_harness_w176_harness_report(limit: int = 100):
    """Get chaos report with resilience score"""
    items = service.harness_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/reliability-harness/{harness_id}")
async def api_reliability_harness_w176_get_harness(harness_id: str):
    """Get harness details"""
    item = service.get_harness(harness_id)
    if not item:
        raise HTTPException(status_code=404, detail="reliability_harness not found")
    return item

@router.post("/api/reliability-harness/{harness_id}/inject")
async def api_reliability_harness_w176_inject_failure(harness_id: str, request: Request):
    """Inject specific failure"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.inject_failure(harness_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="reliability_harness not found")
    return item

@router.post("/api/reliability-harness/{harness_id}/verify")
async def api_reliability_harness_w176_verify_determinism(harness_id: str, request: Request):
    """Verify report determinism"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_determinism(harness_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="reliability_harness not found")
    return item
