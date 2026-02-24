"""Wave 226: Handoff Protocol v1 Router — Manages task handoffs between teams during close. Tracks handoff initiation, acceptance, evidence attachment, and sign-off. Ensures no task falls between cracks.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w226_handoff_protocol import service

router = APIRouter(tags=["Handoff Protocol v1"])

@router.get("/api/handoff-protocol")
async def api_handoff_protocol_w226_list_handoffs(limit: int = 100):
    """List handoffs"""
    items = service.list_handoffs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/handoff-protocol", status_code=201)
async def api_handoff_protocol_w226_initiate_handoff(request: Request):
    """Initiate handoff"""
    data = await request.json()
    item = service.initiate_handoff(data)
    return item

@router.get("/api/handoff-protocol/report")
async def api_handoff_protocol_w226_handoff_report(limit: int = 100):
    """Get handoff protocol report"""
    items = service.handoff_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/handoff-protocol/{handoff_id}")
async def api_handoff_protocol_w226_get_handoff(handoff_id: str):
    """Get handoff details"""
    item = service.get_handoff(handoff_id)
    if not item:
        raise HTTPException(status_code=404, detail="handoff_protocol not found")
    return item

@router.post("/api/handoff-protocol/{handoff_id}/accept")
async def api_handoff_protocol_w226_accept_handoff(handoff_id: str, request: Request):
    """Accept handoff"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.accept_handoff(handoff_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="handoff_protocol not found")
    return item

@router.post("/api/handoff-protocol/{handoff_id}/signoff")
async def api_handoff_protocol_w226_sign_off(handoff_id: str, request: Request):
    """Sign off on handoff"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.sign_off(handoff_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="handoff_protocol not found")
    return item
