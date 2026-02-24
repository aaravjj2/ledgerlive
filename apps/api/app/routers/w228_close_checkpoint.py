"""Wave 228: Close Checkpoint Manager v1 Router — Defines and evaluates checkpoints (gates) in the close process. Each checkpoint has pass/fail criteria, evidence requirements, and approval rules.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w228_close_checkpoint import service

router = APIRouter(tags=["Close Checkpoint Manager v1"])

@router.get("/api/close-checkpoint")
async def api_close_checkpoint_w228_list_checkpoints(limit: int = 100):
    """List close checkpoints"""
    items = service.list_checkpoints(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/close-checkpoint", status_code=201)
async def api_close_checkpoint_w228_create_checkpoint(request: Request):
    """Create close checkpoint"""
    data = await request.json()
    item = service.create_checkpoint(data)
    return item

@router.get("/api/close-checkpoint/report")
async def api_close_checkpoint_w228_checkpoint_report(limit: int = 100):
    """Get checkpoint report"""
    items = service.checkpoint_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/close-checkpoint/{checkpoint_id}")
async def api_close_checkpoint_w228_get_checkpoint(checkpoint_id: str):
    """Get checkpoint details"""
    item = service.get_checkpoint(checkpoint_id)
    if not item:
        raise HTTPException(status_code=404, detail="close_checkpoint not found")
    return item

@router.post("/api/close-checkpoint/{checkpoint_id}/approve")
async def api_close_checkpoint_w228_approve_checkpoint(checkpoint_id: str, request: Request):
    """Approve checkpoint"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_checkpoint(checkpoint_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_checkpoint not found")
    return item

@router.post("/api/close-checkpoint/{checkpoint_id}/evaluate")
async def api_close_checkpoint_w228_evaluate_gate(checkpoint_id: str, request: Request):
    """Evaluate checkpoint gate"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.evaluate_gate(checkpoint_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_checkpoint not found")
    return item

@router.post("/api/close-checkpoint/{checkpoint_id}/evidence")
async def api_close_checkpoint_w228_submit_evidence(checkpoint_id: str, request: Request):
    """Submit checkpoint evidence"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.submit_evidence(checkpoint_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_checkpoint not found")
    return item
