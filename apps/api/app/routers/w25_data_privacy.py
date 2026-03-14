"""Wave 25: Data Privacy / GDPR Router — GDPR-compliant data access, export, and erasure.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w25_data_privacy import service

router = APIRouter(tags=["Data Privacy / GDPR"])

@router.get("/api/privacy/requests")
async def api_list_requests(limit: int = 100):
    """List privacy requests"""
    items = service.list_requests(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/privacy/requests", status_code=201)
async def api_create_request(request: Request):
    """Create a privacy request"""
    data = await request.json()
    item = service.create_request(data)
    return item

@router.get("/api/privacy/requests/{request_id}")
async def api_get_request(request_id: str):
    """Get request details"""
    item = service.get_request(request_id)
    if not item:
        raise HTTPException(status_code=404, detail="data_privacy not found")
    return item

@router.get("/api/privacy/requests/{request_id}/export")
async def api_export_data(request_id: str):
    """Export subject data"""
    item = service.export_data(request_id)
    if not item:
        raise HTTPException(status_code=404, detail="data_privacy not found")
    return item

@router.post("/api/privacy/requests/{request_id}/process")
async def api_process(request_id: str, request: Request):
    """Process request"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.process(request_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="data_privacy not found")
    return item
