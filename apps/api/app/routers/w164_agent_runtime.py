"""Wave 164: Agent Runtime v1 Router — Verifier-first propose/verify/execute runtime producing ProposedAction objects with invariant checks before execution.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w164_agent_runtime import service

router = APIRouter(tags=["Agent Runtime v1"])

@router.get("/api/agent-runtime/actions")
async def api_agent_runtime_w164_list_actions(limit: int = 100):
    """List proposed actions"""
    items = service.list_actions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/agent-runtime/actions", status_code=201)
async def api_agent_runtime_w164_propose_action(request: Request):
    """Propose a new action"""
    data = await request.json()
    item = service.propose_action(data)
    return item

@router.get("/api/agent-runtime/audit")
async def api_agent_runtime_w164_action_audit(limit: int = 100):
    """Get agent runtime audit log"""
    items = service.action_audit(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/agent-runtime/actions/{action_id}")
async def api_agent_runtime_w164_get_action(action_id: str):
    """Get action details"""
    item = service.get_action(action_id)
    if not item:
        raise HTTPException(status_code=404, detail="agent_runtime not found")
    return item

@router.post("/api/agent-runtime/actions/{action_id}/approve")
async def api_agent_runtime_w164_approve_action(action_id: str, request: Request):
    """Approve action"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_action(action_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="agent_runtime not found")
    return item

@router.post("/api/agent-runtime/actions/{action_id}/execute")
async def api_agent_runtime_w164_execute_action(action_id: str, request: Request):
    """Execute verified action"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.execute_action(action_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="agent_runtime not found")
    return item

@router.post("/api/agent-runtime/actions/{action_id}/reject")
async def api_agent_runtime_w164_reject_action(action_id: str, request: Request):
    """Reject action"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reject_action(action_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="agent_runtime not found")
    return item

@router.post("/api/agent-runtime/actions/{action_id}/verify")
async def api_agent_runtime_w164_verify_action(action_id: str, request: Request):
    """Run verifier on action"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_action(action_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="agent_runtime not found")
    return item
