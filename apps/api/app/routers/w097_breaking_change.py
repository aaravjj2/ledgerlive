"""Wave 97: Breaking Change Detector Router — Schema breaking-change detector for workflow/report/mapping templates.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w097_breaking_change import service

router = APIRouter(tags=["Breaking Change Detector"])

@router.get("/api/breaking-changes")
async def api_breaking_change_w97_list_detections(limit: int = 100):
    """List breaking change detections"""
    items = service.list_detections(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/breaking-changes", status_code=201)
async def api_breaking_change_w97_detect(request: Request):
    """Run breaking change detection"""
    data = await request.json()
    item = service.detect(data)
    return item

@router.get("/api/breaking-changes/report")
async def api_breaking_change_w97_detection_report(limit: int = 100):
    """Get detection report"""
    items = service.detection_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/breaking-changes/{detection_id}")
async def api_breaking_change_w97_get_detection(detection_id: str):
    """Get detection details"""
    item = service.get_detection(detection_id)
    if not item:
        raise HTTPException(status_code=404, detail="breaking_change not found")
    return item

@router.post("/api/breaking-changes/{detection_id}/migrate")
async def api_breaking_change_w97_suggest_migration(detection_id: str, request: Request):
    """Suggest migration"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.suggest_migration(detection_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="breaking_change not found")
    return item
