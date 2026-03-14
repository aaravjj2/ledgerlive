"""Wave 282: Tie-Out Engine v2 Router — Configurable tie-out rules with variance incident creation and evidence linking. Deterministic variance calculation.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w282_tie_out_engine_v2 import service

router = APIRouter(tags=["Tie-Out Engine v2"])

@router.get("/api/tie-out-engine-v2")
async def api_tie_out_engine_v2_w282_list_tie_outs(limit: int = 100):
    """List tie-out evaluations"""
    items = service.list_tie_outs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/tie-out-engine-v2", status_code=201)
async def api_tie_out_engine_v2_w282_create_tie_out(request: Request):
    """Create tie-out evaluation"""
    data = await request.json()
    item = service.create_tie_out(data)
    return item

@router.get("/api/tie-out-engine-v2/report")
async def api_tie_out_engine_v2_w282_tie_out_report(limit: int = 100):
    """Get tie-out engine report"""
    items = service.tie_out_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/tie-out-engine-v2/{tie_out_id}")
async def api_tie_out_engine_v2_w282_get_tie_out(tie_out_id: str):
    """Get tie-out details"""
    item = service.get_tie_out(tie_out_id)
    if not item:
        raise HTTPException(status_code=404, detail="tie_out_engine_v2 not found")
    return item

@router.post("/api/tie-out-engine-v2/{tie_out_id}/evaluate")
async def api_tie_out_engine_v2_w282_evaluate_variance(tie_out_id: str, request: Request):
    """Evaluate variance"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.evaluate_variance(tie_out_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="tie_out_engine_v2 not found")
    return item

@router.post("/api/tie-out-engine-v2/{tie_out_id}/incident")
async def api_tie_out_engine_v2_w282_create_incident_from_variance(tie_out_id: str, request: Request):
    """Create incident from variance"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.create_incident_from_variance(tie_out_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="tie_out_engine_v2 not found")
    return item
