"""Wave 326: Tool Scope Diffing v1 Router — Show scope changes over time; approvals required for expanding scopes; audited.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w326_tool_scope_diffing import service

router = APIRouter(tags=["Tool Scope Diffing v1"])

@router.get("/api/tool-scope-diffing")
async def api_tool_scope_diffing_w326_list_diffs(limit: int = 100):
    """List scope diffs"""
    items = service.list_diffs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/tool-scope-diffing", status_code=201)
async def api_tool_scope_diffing_w326_create_diff(request: Request):
    """Create scope diff"""
    data = await request.json()
    item = service.create_diff(data)
    return item

@router.get("/api/tool-scope-diffing/report")
async def api_tool_scope_diffing_w326_diff_report(limit: int = 100):
    """Get scope diffing report"""
    items = service.diff_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/tool-scope-diffing/{diff_id}")
async def api_tool_scope_diffing_w326_get_diff(diff_id: str):
    """Get diff details"""
    item = service.get_diff(diff_id)
    if not item:
        raise HTTPException(status_code=404, detail="tool_scope_diffing not found")
    return item

@router.post("/api/tool-scope-diffing/{diff_id}/approve")
async def api_tool_scope_diffing_w326_approve_expansion(diff_id: str, request: Request):
    """Approve scope expansion"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_expansion(diff_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="tool_scope_diffing not found")
    return item

@router.post("/api/tool-scope-diffing/{diff_id}/reject")
async def api_tool_scope_diffing_w326_reject_expansion(diff_id: str, request: Request):
    """Reject scope expansion"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reject_expansion(diff_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="tool_scope_diffing not found")
    return item
