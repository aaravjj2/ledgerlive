"""Wave 244: Execute-from-Plan v1 Router — Executes approved plan with idempotency keys, updates tool trace and incident telemetry live, tracks execution progress step by step.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w244_execute_from_plan import service

router = APIRouter(tags=["Execute-from-Plan v1"])

@router.get("/api/plan-execution")
async def api_execute_from_plan_w244_list_executions(limit: int = 100):
    """List plan executions"""
    items = service.list_executions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/plan-execution", status_code=201)
async def api_execute_from_plan_w244_start_execution(request: Request):
    """Start plan execution"""
    data = await request.json()
    item = service.start_execution(data)
    return item

@router.get("/api/plan-execution/report")
async def api_execute_from_plan_w244_execution_report(limit: int = 100):
    """Get execution report"""
    items = service.execution_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/plan-execution/{execution_id}")
async def api_execute_from_plan_w244_get_execution(execution_id: str):
    """Get execution details"""
    item = service.get_execution(execution_id)
    if not item:
        raise HTTPException(status_code=404, detail="execute_from_plan not found")
    return item

@router.post("/api/plan-execution/{execution_id}/advance")
async def api_execute_from_plan_w244_advance_step(execution_id: str, request: Request):
    """Advance execution step"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.advance_step(execution_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="execute_from_plan not found")
    return item

@router.post("/api/plan-execution/{execution_id}/rollback")
async def api_execute_from_plan_w244_rollback_execution(execution_id: str, request: Request):
    """Rollback execution"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.rollback_execution(execution_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="execute_from_plan not found")
    return item

@router.post("/api/plan-execution/{execution_id}/telemetry")
async def api_execute_from_plan_w244_record_telemetry(execution_id: str, request: Request):
    """Record telemetry update"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.record_telemetry(execution_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="execute_from_plan not found")
    return item
