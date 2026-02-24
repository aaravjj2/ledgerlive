"""Wave 247: Pit Crew Routing v1 Router — Next actions assigned to specialized agents. Quorum and veto shown in Race Control. Multi-agent coordination with skill-based routing.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w247_pit_crew_routing import service

router = APIRouter(tags=["Pit Crew Routing v1"])

@router.get("/api/pit-crew")
async def api_pit_crew_routing_w247_list_routings(limit: int = 100):
    """List pit crew routings"""
    items = service.list_routings(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/pit-crew", status_code=201)
async def api_pit_crew_routing_w247_create_routing(request: Request):
    """Create pit crew routing"""
    data = await request.json()
    item = service.create_routing(data)
    return item

@router.get("/api/pit-crew/report")
async def api_pit_crew_routing_w247_routing_report(limit: int = 100):
    """Get pit crew routing report"""
    items = service.routing_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/pit-crew/{routing_id}")
async def api_pit_crew_routing_w247_get_routing(routing_id: str):
    """Get routing details"""
    item = service.get_routing(routing_id)
    if not item:
        raise HTTPException(status_code=404, detail="pit_crew_routing not found")
    return item

@router.post("/api/pit-crew/{routing_id}/assign")
async def api_pit_crew_routing_w247_assign_agent(routing_id: str, request: Request):
    """Assign agent to action"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.assign_agent(routing_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="pit_crew_routing not found")
    return item

@router.post("/api/pit-crew/{routing_id}/quorum")
async def api_pit_crew_routing_w247_check_quorum(routing_id: str, request: Request):
    """Check quorum status"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_quorum(routing_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="pit_crew_routing not found")
    return item

@router.post("/api/pit-crew/{routing_id}/veto")
async def api_pit_crew_routing_w247_record_veto(routing_id: str, request: Request):
    """Record agent veto"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.record_veto(routing_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="pit_crew_routing not found")
    return item
