"""Wave 18: Continuous Close Router — Real-time close progress tracking and bottleneck detection.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w18_continuous_close import service

router = APIRouter(tags=["Continuous Close"])

@router.get("/api/close-tasks")
async def api_list_tasks(limit: int = 100):
    """List close tasks"""
    items = service.list_tasks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/close-tasks", status_code=201)
async def api_create_task(request: Request):
    """Create a close task"""
    data = await request.json()
    item = service.create_task(data)
    return item

@router.get("/api/close-tasks/dashboard")
async def api_dashboard(limit: int = 100):
    """Close progress dashboard"""
    items = service.dashboard(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/close-tasks/{task_id}")
async def api_get_task(task_id: str):
    """Get task details"""
    item = service.get_task(task_id)
    if not item:
        raise HTTPException(status_code=404, detail="continuous_close not found")
    return item

@router.post("/api/close-tasks/{task_id}/complete")
async def api_complete_task(task_id: str, request: Request):
    """Complete a task"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.complete_task(task_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="continuous_close not found")
    return item
