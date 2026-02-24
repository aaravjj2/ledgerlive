"""Wave 254: Exfil Detector v2 Router — Extended exfiltration and injection detection covering inbound docs and channel content. Deterministic classification with evidence-backed reasons.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w254_exfil_detector_v2 import service

router = APIRouter(tags=["Exfil Detector v2"])

@router.get("/api/exfil-detector-v2")
async def api_exfil_detector_v2_w254_list_detections(limit: int = 100):
    """List exfil detections"""
    items = service.list_detections(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/exfil-detector-v2", status_code=201)
async def api_exfil_detector_v2_w254_scan_content(request: Request):
    """Scan content for exfil/injection"""
    data = await request.json()
    item = service.scan_content(data)
    return item

@router.get("/api/exfil-detector-v2/report")
async def api_exfil_detector_v2_w254_detection_report(limit: int = 100):
    """Get exfil detector report"""
    items = service.detection_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/exfil-detector-v2/{detection_id}")
async def api_exfil_detector_v2_w254_get_detection(detection_id: str):
    """Get detection details"""
    item = service.get_detection(detection_id)
    if not item:
        raise HTTPException(status_code=404, detail="exfil_detector_v2 not found")
    return item

@router.post("/api/exfil-detector-v2/{detection_id}/block")
async def api_exfil_detector_v2_w254_block_content(detection_id: str, request: Request):
    """Block detected content"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.block_content(detection_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="exfil_detector_v2 not found")
    return item

@router.post("/api/exfil-detector-v2/{detection_id}/classify")
async def api_exfil_detector_v2_w254_classify_threat(detection_id: str, request: Request):
    """Classify threat type"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.classify_threat(detection_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="exfil_detector_v2 not found")
    return item
