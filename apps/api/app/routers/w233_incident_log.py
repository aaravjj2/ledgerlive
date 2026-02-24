"""Wave 233: Incident Log v1 Router — Logs incidents during close: system outages, data issues, process failures. Each incident has severity, impact assessment, resolution timeline, and root cause.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w233_incident_log import service

router = APIRouter(tags=["Incident Log v1"])

@router.get("/api/incident-log")
async def api_incident_log_w233_list_incidents(limit: int = 100):
    """List incidents"""
    items = service.list_incidents(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/incident-log", status_code=201)
async def api_incident_log_w233_create_incident(request: Request):
    """Create incident"""
    data = await request.json()
    item = service.create_incident(data)
    return item

@router.get("/api/incident-log/report")
async def api_incident_log_w233_incident_report(limit: int = 100):
    """Get incident log report"""
    items = service.incident_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/incident-log/{incident_id}")
async def api_incident_log_w233_get_incident(incident_id: str):
    """Get incident details"""
    item = service.get_incident(incident_id)
    if not item:
        raise HTTPException(status_code=404, detail="incident_log not found")
    return item

@router.post("/api/incident-log/{incident_id}/impact")
async def api_incident_log_w233_assess_impact(incident_id: str, request: Request):
    """Assess incident impact"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.assess_impact(incident_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="incident_log not found")
    return item

@router.post("/api/incident-log/{incident_id}/resolve")
async def api_incident_log_w233_resolve_incident(incident_id: str, request: Request):
    """Resolve incident"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.resolve_incident(incident_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="incident_log not found")
    return item
