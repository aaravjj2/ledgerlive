"""Wave 66: Phase2 Integration Flow E2E Router — Connectors mock→sync→mapping DSL→quality score→override→export E2E flow.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w066_integration_flow_e2e import service

router = APIRouter(tags=["Phase2 Integration Flow E2E"])

@router.get("/api/integration-flow-e2e")
async def api_integration_flow_e2e_w66_list_flows(limit: int = 100):
    """List integration flow E2E runs"""
    items = service.list_flows(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/integration-flow-e2e", status_code=201)
async def api_integration_flow_e2e_w66_start_flow(request: Request):
    """Start integration flow E2E"""
    data = await request.json()
    item = service.start_flow(data)
    return item

@router.get("/api/integration-flow-e2e/report")
async def api_integration_flow_e2e_w66_flow_report(limit: int = 100):
    """Get integration flow report"""
    items = service.flow_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/integration-flow-e2e/{flow_id}")
async def api_integration_flow_e2e_w66_get_flow(flow_id: str):
    """Get flow run details"""
    item = service.get_flow(flow_id)
    if not item:
        raise HTTPException(status_code=404, detail="integration_flow_e2e not found")
    return item

@router.post("/api/integration-flow-e2e/{flow_id}/advance")
async def api_integration_flow_e2e_w66_advance(flow_id: str, request: Request):
    """Advance to next step"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.advance(flow_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="integration_flow_e2e not found")
    return item

@router.post("/api/integration-flow-e2e/{flow_id}/verify")
async def api_integration_flow_e2e_w66_verify_flow(flow_id: str, request: Request):
    """Verify flow completeness"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_flow(flow_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="integration_flow_e2e not found")
    return item
