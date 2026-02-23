"""Wave 31: Close Calendar 2.0 Router — Dependency graph for close tasks with SLA timers, escalation rules, and owner assignments.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w31_close_calendar import service

router = APIRouter(tags=["Close Calendar 2.0"])

@router.get("/api/close-calendar/dependency-chain")
async def api_close_calendar_w31_dependency_chain(limit: int = 100):
    """Get dependency chain view"""
    items = service.dependency_chain(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/close-calendar/tasks")
async def api_close_calendar_w31_list_tasks(limit: int = 100):
    """List close calendar tasks"""
    items = service.list_tasks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/close-calendar/tasks", status_code=201)
async def api_close_calendar_w31_create_task(request: Request):
    """Create a close calendar task"""
    data = await request.json()
    item = service.create_task(data)
    return item

@router.get("/api/close-calendar/{task_id}")
async def api_close_calendar_w31_get_task(task_id: str):
    """Get task details"""
    item = service.get_task(task_id)
    if not item:
        raise HTTPException(status_code=404, detail="close_calendar not found")
    return item

@router.post("/api/close-calendar/{task_id}/complete")
async def api_close_calendar_w31_complete_task(task_id: str, request: Request):
    """Complete a task"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.complete_task(task_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_calendar not found")
    return item

@router.post("/api/close-calendar/{task_id}/escalate")
async def api_close_calendar_w31_escalate(task_id: str, request: Request):
    """Escalate a task"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.escalate(task_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_calendar not found")
    return item

@router.post("/api/close-calendar/{task_id}/start")
async def api_close_calendar_w31_start_task(task_id: str, request: Request):
    """Start a task"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.start_task(task_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_calendar not found")
    return item
