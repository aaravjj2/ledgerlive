"""Wave 229: Race Control State Machine v1 Router — Finite state machine governing close lifecycle: NOT_STARTED -> IN_PROGRESS -> REVIEW -> APPROVED -> CLOSED. Transition guards enforce prerequisites.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w229_rc_state_machine import service

router = APIRouter(tags=["Race Control State Machine v1"])

@router.get("/api/rc-state-machine")
async def api_rc_state_machine_w229_list_machines(limit: int = 100):
    """List state machines"""
    items = service.list_machines(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/rc-state-machine", status_code=201)
async def api_rc_state_machine_w229_create_machine(request: Request):
    """Create state machine"""
    data = await request.json()
    item = service.create_machine(data)
    return item

@router.get("/api/rc-state-machine/report")
async def api_rc_state_machine_w229_machine_report(limit: int = 100):
    """Get state machine report"""
    items = service.machine_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/rc-state-machine/{machine_id}")
async def api_rc_state_machine_w229_get_machine(machine_id: str):
    """Get state machine details"""
    item = service.get_machine(machine_id)
    if not item:
        raise HTTPException(status_code=404, detail="rc_state_machine not found")
    return item

@router.post("/api/rc-state-machine/{machine_id}/lock")
async def api_rc_state_machine_w229_lock_state(machine_id: str, request: Request):
    """Lock state machine"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.lock_state(machine_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_state_machine not found")
    return item

@router.post("/api/rc-state-machine/{machine_id}/transition")
async def api_rc_state_machine_w229_transition(machine_id: str, request: Request):
    """Perform state transition"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.transition(machine_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_state_machine not found")
    return item
