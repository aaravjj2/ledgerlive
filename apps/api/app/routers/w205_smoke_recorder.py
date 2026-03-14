"""Wave 205: Deployed Smoke Recorder v1 Router — Smoke scripts record deploy evidence pack: timestamps, endpoints, smoke_report, screenshots. Never in CI. Offline validators for format and schema.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w205_smoke_recorder import service

router = APIRouter(tags=["Deployed Smoke Recorder v1"])

@router.get("/api/smoke-recorder")
async def api_smoke_recorder_w205_list_recordings(limit: int = 100):
    """List smoke recordings"""
    items = service.list_recordings(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/smoke-recorder", status_code=201)
async def api_smoke_recorder_w205_create_recording(request: Request):
    """Create smoke recording"""
    data = await request.json()
    item = service.create_recording(data)
    return item

@router.get("/api/smoke-recorder/report")
async def api_smoke_recorder_w205_recorder_report(limit: int = 100):
    """Get smoke recorder report"""
    items = service.recorder_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/smoke-recorder/{recorder_id}")
async def api_smoke_recorder_w205_get_recording(recorder_id: str):
    """Get recording details"""
    item = service.get_recording(recorder_id)
    if not item:
        raise HTTPException(status_code=404, detail="smoke_recorder not found")
    return item

@router.post("/api/smoke-recorder/{recorder_id}/schema")
async def api_smoke_recorder_w205_validate_schema(recorder_id: str, request: Request):
    """Validate smoke report schema"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_schema(recorder_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="smoke_recorder not found")
    return item

@router.post("/api/smoke-recorder/{recorder_id}/validate")
async def api_smoke_recorder_w205_validate_pack(recorder_id: str, request: Request):
    """Validate evidence pack format"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_pack(recorder_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="smoke_recorder not found")
    return item
