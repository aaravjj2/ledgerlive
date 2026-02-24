"""Wave 276: Channel Reliability Harness v1 Router — Seeded failures including timeouts, retries, and partial delivery with deterministic recovery scenarios.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w276_channel_reliability import service

router = APIRouter(tags=["Channel Reliability Harness v1"])

@router.get("/api/channel-reliability")
async def api_channel_reliability_w276_list_harnesses(limit: int = 100):
    """List reliability harnesses"""
    items = service.list_harnesses(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/channel-reliability", status_code=201)
async def api_channel_reliability_w276_create_harness(request: Request):
    """Create reliability harness"""
    data = await request.json()
    item = service.create_harness(data)
    return item

@router.get("/api/channel-reliability/report")
async def api_channel_reliability_w276_reliability_report(limit: int = 100):
    """Get reliability harness report"""
    items = service.reliability_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/channel-reliability/{harness_id}")
async def api_channel_reliability_w276_get_harness(harness_id: str):
    """Get harness details"""
    item = service.get_harness(harness_id)
    if not item:
        raise HTTPException(status_code=404, detail="channel_reliability not found")
    return item

@router.post("/api/channel-reliability/{harness_id}/inject")
async def api_channel_reliability_w276_inject_failure(harness_id: str, request: Request):
    """Inject seeded failure"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.inject_failure(harness_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="channel_reliability not found")
    return item

@router.post("/api/channel-reliability/{harness_id}/recover")
async def api_channel_reliability_w276_test_recovery(harness_id: str, request: Request):
    """Test recovery strategy"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.test_recovery(harness_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="channel_reliability not found")
    return item
