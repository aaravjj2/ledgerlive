"""Wave 252: Security Timeline v1 Router — Incidents and security events unified in a filterable, exportable timeline view within Race Control. Deterministic ordering and rendering.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w252_security_timeline import service

router = APIRouter(tags=["Security Timeline v1"])

@router.get("/api/security-timeline")
async def api_security_timeline_w252_list_timelines(limit: int = 100):
    """List security timelines"""
    items = service.list_timelines(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/security-timeline", status_code=201)
async def api_security_timeline_w252_create_timeline(request: Request):
    """Create security timeline"""
    data = await request.json()
    item = service.create_timeline(data)
    return item

@router.get("/api/security-timeline/report")
async def api_security_timeline_w252_timeline_report(limit: int = 100):
    """Get security timeline report"""
    items = service.timeline_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/security-timeline/{timeline_id}")
async def api_security_timeline_w252_get_timeline(timeline_id: str):
    """Get timeline details"""
    item = service.get_timeline(timeline_id)
    if not item:
        raise HTTPException(status_code=404, detail="security_timeline not found")
    return item

@router.post("/api/security-timeline/{timeline_id}/export")
async def api_security_timeline_w252_export_timeline(timeline_id: str, request: Request):
    """Export timeline"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_timeline(timeline_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="security_timeline not found")
    return item

@router.post("/api/security-timeline/{timeline_id}/filter")
async def api_security_timeline_w252_filter_timeline(timeline_id: str, request: Request):
    """Filter timeline entries"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.filter_timeline(timeline_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="security_timeline not found")
    return item
