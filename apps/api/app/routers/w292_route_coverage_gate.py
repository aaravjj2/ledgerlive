"""Wave 292: Route Coverage Gate v1 Router — All critical routes must have MCP E2E coverage. Waivers require explicit config. Deterministic coverage measurement.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w292_route_coverage_gate import service

router = APIRouter(tags=["Route Coverage Gate v1"])

@router.get("/api/route-coverage-gate")
async def api_route_coverage_gate_w292_list_coverage_gates(limit: int = 100):
    """List route coverage gates"""
    items = service.list_coverage_gates(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/route-coverage-gate", status_code=201)
async def api_route_coverage_gate_w292_create_coverage_gate(request: Request):
    """Create route coverage gate"""
    data = await request.json()
    item = service.create_coverage_gate(data)
    return item

@router.get("/api/route-coverage-gate/report")
async def api_route_coverage_gate_w292_coverage_gate_report(limit: int = 100):
    """Get route coverage gate report"""
    items = service.coverage_gate_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/route-coverage-gate/{coverage_gate_id}")
async def api_route_coverage_gate_w292_get_coverage_gate(coverage_gate_id: str):
    """Get coverage gate details"""
    item = service.get_coverage_gate(coverage_gate_id)
    if not item:
        raise HTTPException(status_code=404, detail="route_coverage_gate not found")
    return item

@router.post("/api/route-coverage-gate/{coverage_gate_id}/measure")
async def api_route_coverage_gate_w292_measure_coverage(coverage_gate_id: str, request: Request):
    """Measure route coverage"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.measure_coverage(coverage_gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="route_coverage_gate not found")
    return item

@router.post("/api/route-coverage-gate/{coverage_gate_id}/waiver")
async def api_route_coverage_gate_w292_add_waiver(coverage_gate_id: str, request: Request):
    """Add route waiver"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_waiver(coverage_gate_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="route_coverage_gate not found")
    return item
