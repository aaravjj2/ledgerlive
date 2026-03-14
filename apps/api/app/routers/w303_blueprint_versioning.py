"""Wave 303: Blueprint Versioning v1 Router — Immutable versions with diff viewer, rollback, and audit of blueprint changes.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w303_blueprint_versioning import service

router = APIRouter(tags=["Blueprint Versioning v1"])

@router.get("/api/blueprint-versioning")
async def api_blueprint_versioning_w303_list_versions(limit: int = 100):
    """List blueprint versions"""
    items = service.list_versions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/blueprint-versioning", status_code=201)
async def api_blueprint_versioning_w303_create_version(request: Request):
    """Create immutable version"""
    data = await request.json()
    item = service.create_version(data)
    return item

@router.get("/api/blueprint-versioning/report")
async def api_blueprint_versioning_w303_version_report(limit: int = 100):
    """Get versioning report"""
    items = service.version_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/blueprint-versioning/{version_id}")
async def api_blueprint_versioning_w303_get_version(version_id: str):
    """Get version details"""
    item = service.get_version(version_id)
    if not item:
        raise HTTPException(status_code=404, detail="blueprint_versioning not found")
    return item

@router.post("/api/blueprint-versioning/{version_id}/diff")
async def api_blueprint_versioning_w303_diff_versions(version_id: str, request: Request):
    """Diff with previous version"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.diff_versions(version_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="blueprint_versioning not found")
    return item

@router.post("/api/blueprint-versioning/{version_id}/rollback")
async def api_blueprint_versioning_w303_rollback_version(version_id: str, request: Request):
    """Rollback to version"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.rollback_version(version_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="blueprint_versioning not found")
    return item
