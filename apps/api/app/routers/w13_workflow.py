"""Wave 13: Workflow Engine Router — Configurable close workflow templates and execution.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w13_workflow import service

router = APIRouter(tags=["Workflow Engine"])

@router.get("/api/workflows")
async def api_list(limit: int = 100):
    """List workflows"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/workflows", status_code=201)
async def api_create(request: Request):
    """Create a workflow"""
    data = await request.json()
    item = service.create(data)
    return item

@router.get("/api/workflows/{workflow_id}")
async def api_get(workflow_id: str):
    """Get workflow details"""
    item = service.get(workflow_id)
    if not item:
        raise HTTPException(status_code=404, detail="workflow not found")
    return item

@router.post("/api/workflows/{workflow_id}/abort")
async def api_abort(workflow_id: str, request: Request):
    """Abort a workflow"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.abort(workflow_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="workflow not found")
    return item

@router.post("/api/workflows/{workflow_id}/advance")
async def api_advance(workflow_id: str, request: Request):
    """Advance to next step"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.advance(workflow_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="workflow not found")
    return item
