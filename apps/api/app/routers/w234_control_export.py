"""Wave 234: Control Room Export v1 Router — Exports Race Control dashboard state as a comprehensive snapshot: lane statuses, scoreboard, critical path, incidents, checkpoints. Deterministic pack with content hash.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w234_control_export import service

router = APIRouter(tags=["Control Room Export v1"])

@router.get("/api/control-export")
async def api_control_export_w234_list_exports(limit: int = 100):
    """List control room exports"""
    items = service.list_exports(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/control-export", status_code=201)
async def api_control_export_w234_create_export(request: Request):
    """Create control room export"""
    data = await request.json()
    item = service.create_export(data)
    return item

@router.get("/api/control-export/report")
async def api_control_export_w234_export_report(limit: int = 100):
    """Get control export report"""
    items = service.export_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/control-export/{export_id}")
async def api_control_export_w234_get_export(export_id: str):
    """Get export details"""
    item = service.get_export(export_id)
    if not item:
        raise HTTPException(status_code=404, detail="control_export not found")
    return item

@router.post("/api/control-export/{export_id}/download")
async def api_control_export_w234_download_export(export_id: str, request: Request):
    """Download export pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.download_export(export_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="control_export not found")
    return item

@router.post("/api/control-export/{export_id}/verify")
async def api_control_export_w234_verify_hash(export_id: str, request: Request):
    """Verify content hash"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_hash(export_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="control_export not found")
    return item
