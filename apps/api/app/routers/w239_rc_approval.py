"""Wave 239: RC Approval Chain v1 Router — Multi-level approval chain for close sign-off. Supports sequential and parallel approvals, delegation, expiry, and audit trail of all approval decisions.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w239_rc_approval import service

router = APIRouter(tags=["RC Approval Chain v1"])

@router.get("/api/rc-approval")
async def api_rc_approval_w239_list_approvals(limit: int = 100):
    """List approval chains"""
    items = service.list_approvals(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/rc-approval", status_code=201)
async def api_rc_approval_w239_create_approval(request: Request):
    """Create approval chain"""
    data = await request.json()
    item = service.create_approval(data)
    return item

@router.get("/api/rc-approval/report")
async def api_rc_approval_w239_approval_report(limit: int = 100):
    """Get approval chain report"""
    items = service.approval_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/rc-approval/{approval_id}")
async def api_rc_approval_w239_get_approval(approval_id: str):
    """Get approval chain details"""
    item = service.get_approval(approval_id)
    if not item:
        raise HTTPException(status_code=404, detail="rc_approval not found")
    return item

@router.post("/api/rc-approval/{approval_id}/approve")
async def api_rc_approval_w239_approve_level(approval_id: str, request: Request):
    """Approve current level"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_level(approval_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_approval not found")
    return item

@router.post("/api/rc-approval/{approval_id}/delegate")
async def api_rc_approval_w239_delegate_approval(approval_id: str, request: Request):
    """Delegate approval"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.delegate_approval(approval_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_approval not found")
    return item

@router.post("/api/rc-approval/{approval_id}/reject")
async def api_rc_approval_w239_reject_level(approval_id: str, request: Request):
    """Reject current level"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reject_level(approval_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_approval not found")
    return item
