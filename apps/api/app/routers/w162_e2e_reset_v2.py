"""Wave 162: E2E Reset Seed State v2 Router — Snapshot-based canonical scenario: POST reset restores DB+storage, POST seed loads canonical close scenario, GET state returns stable IDs.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w162_e2e_reset_v2 import service

router = APIRouter(tags=["E2E Reset Seed State v2"])

@router.get("/api/ops/e2e-snapshots")
async def api_e2e_reset_v2_w162_list_snapshots(limit: int = 100):
    """List E2E snapshots"""
    items = service.list_snapshots(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/ops/e2e-snapshots/reset", status_code=201)
async def api_e2e_reset_v2_w162_create_reset(request: Request):
    """Reset DB and storage to clean snapshot"""
    data = await request.json()
    item = service.create_reset(data)
    return item

@router.post("/api/ops/e2e-snapshots/seed", status_code=201)
async def api_e2e_reset_v2_w162_create_seed(request: Request):
    """Seed canonical multi-entity close scenario"""
    data = await request.json()
    item = service.create_seed(data)
    return item

@router.get("/api/ops/e2e-snapshots/state")
async def api_e2e_reset_v2_w162_get_state(limit: int = 100):
    """Get current state with stable IDs"""
    items = service.get_state(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/ops/e2e-snapshots/{snapshot_id}")
async def api_e2e_reset_v2_w162_get_snapshot(snapshot_id: str):
    """Get snapshot details"""
    item = service.get_snapshot(snapshot_id)
    if not item:
        raise HTTPException(status_code=404, detail="e2e_reset_v2 not found")
    return item

@router.post("/api/ops/e2e-snapshots/{snapshot_id}/verify")
async def api_e2e_reset_v2_w162_verify_state(snapshot_id: str, request: Request):
    """Verify state hash consistency"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_state(snapshot_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="e2e_reset_v2 not found")
    return item
