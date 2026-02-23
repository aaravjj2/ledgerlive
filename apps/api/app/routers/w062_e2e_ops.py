"""Wave 62: E2E Ops Endpoints Router — Reset/seed/state endpoints for deterministic E2E test orchestration across all flows.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w062_e2e_ops import service

router = APIRouter(tags=["E2E Ops Endpoints"])

@router.get("/api/e2e-ops")
async def api_e2e_ops_w62_list_ops(limit: int = 100):
    """List E2E operations"""
    items = service.list_ops(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/e2e-ops/reset", status_code=201)
async def api_e2e_ops_w62_reset_all(request: Request):
    """Reset all services to clean state"""
    data = await request.json()
    item = service.reset_all(data)
    return item

@router.post("/api/e2e-ops/seed", status_code=201)
async def api_e2e_ops_w62_seed_fixtures(request: Request):
    """Seed deterministic fixtures"""
    data = await request.json()
    item = service.seed_fixtures(data)
    return item

@router.get("/api/e2e-ops/state")
async def api_e2e_ops_w62_get_state(limit: int = 100):
    """Get current state snapshot"""
    items = service.get_state(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/e2e-ops/{op_id}")
async def api_e2e_ops_w62_get_op(op_id: str):
    """Get operation details"""
    item = service.get_op(op_id)
    if not item:
        raise HTTPException(status_code=404, detail="e2e_ops not found")
    return item

@router.post("/api/e2e-ops/{op_id}/verify")
async def api_e2e_ops_w62_verify_state(op_id: str, request: Request):
    """Verify state consistency"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_state(op_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="e2e_ops not found")
    return item
