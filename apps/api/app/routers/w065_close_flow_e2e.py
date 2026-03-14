"""Wave 65: Phase1 Close Flow E2E Router — Full close flow: period→tasks→JE→3-way→cash app→accrual→controls→binder→verify.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w065_close_flow_e2e import service

router = APIRouter(tags=["Phase1 Close Flow E2E"])

@router.get("/api/close-flow-e2e")
async def api_close_flow_e2e_w65_list_flows(limit: int = 100):
    """List close flow E2E runs"""
    items = service.list_flows(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/close-flow-e2e", status_code=201)
async def api_close_flow_e2e_w65_start_flow(request: Request):
    """Start full close flow E2E"""
    data = await request.json()
    item = service.start_flow(data)
    return item

@router.get("/api/close-flow-e2e/report")
async def api_close_flow_e2e_w65_flow_report(limit: int = 100):
    """Get flow coverage report"""
    items = service.flow_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/close-flow-e2e/{flow_id}")
async def api_close_flow_e2e_w65_get_flow(flow_id: str):
    """Get flow run details"""
    item = service.get_flow(flow_id)
    if not item:
        raise HTTPException(status_code=404, detail="close_flow_e2e not found")
    return item

@router.post("/api/close-flow-e2e/{flow_id}/advance")
async def api_close_flow_e2e_w65_advance(flow_id: str, request: Request):
    """Advance to next step"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.advance(flow_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_flow_e2e not found")
    return item

@router.post("/api/close-flow-e2e/{flow_id}/verify")
async def api_close_flow_e2e_w65_verify_flow(flow_id: str, request: Request):
    """Verify flow completeness"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_flow(flow_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="close_flow_e2e not found")
    return item
