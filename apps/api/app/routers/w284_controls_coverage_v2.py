"""Wave 284: Controls Coverage v2 Router — Quantifies coverage for close period. Gaps become blockers with SLA enforcement and deterministic scoring.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w284_controls_coverage_v2 import service

router = APIRouter(tags=["Controls Coverage v2"])

@router.get("/api/controls-coverage-v2")
async def api_controls_coverage_v2_w284_list_coverages(limit: int = 100):
    """List controls coverage"""
    items = service.list_coverages(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/controls-coverage-v2", status_code=201)
async def api_controls_coverage_v2_w284_create_coverage(request: Request):
    """Create controls coverage evaluation"""
    data = await request.json()
    item = service.create_coverage(data)
    return item

@router.get("/api/controls-coverage-v2/report")
async def api_controls_coverage_v2_w284_coverage_report(limit: int = 100):
    """Get controls coverage report"""
    items = service.coverage_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/controls-coverage-v2/{coverage_id}")
async def api_controls_coverage_v2_w284_get_coverage(coverage_id: str):
    """Get coverage details"""
    item = service.get_coverage(coverage_id)
    if not item:
        raise HTTPException(status_code=404, detail="controls_coverage_v2 not found")
    return item

@router.post("/api/controls-coverage-v2/{coverage_id}/blockers")
async def api_controls_coverage_v2_w284_create_blockers(coverage_id: str, request: Request):
    """Create gap blockers"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.create_blockers(coverage_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="controls_coverage_v2 not found")
    return item

@router.post("/api/controls-coverage-v2/{coverage_id}/gaps")
async def api_controls_coverage_v2_w284_identify_gaps(coverage_id: str, request: Request):
    """Identify control gaps"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.identify_gaps(coverage_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="controls_coverage_v2 not found")
    return item
