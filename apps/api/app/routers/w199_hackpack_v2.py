"""Wave 199: Hackpack v2 Multi-Bundle Router — Multi-hackathon bundle generator: Gemini bundle skeleton, Airia validated bundle, DO Gradient bundle, Automation Innovation bundle. All deterministic offline.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w199_hackpack_v2 import service

router = APIRouter(tags=["Hackpack v2 Multi-Bundle"])

@router.get("/api/hackpack-v2")
async def api_hackpack_v2_w199_list_hackpacks(limit: int = 100):
    """List hackpack v2 bundles"""
    items = service.list_hackpacks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/hackpack-v2", status_code=201)
async def api_hackpack_v2_w199_generate_hackpack(request: Request):
    """Generate multi-hackathon pack"""
    data = await request.json()
    item = service.generate_hackpack(data)
    return item

@router.get("/api/hackpack-v2/report")
async def api_hackpack_v2_w199_hackpack_report(limit: int = 100):
    """Get hackpack v2 report"""
    items = service.hackpack_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/hackpack-v2/{hackpack_id}")
async def api_hackpack_v2_w199_get_hackpack(hackpack_id: str):
    """Get hackpack details"""
    item = service.get_hackpack(hackpack_id)
    if not item:
        raise HTTPException(status_code=404, detail="hackpack_v2 not found")
    return item

@router.post("/api/hackpack-v2/{hackpack_id}/export")
async def api_hackpack_v2_w199_export_hackpack(hackpack_id: str, request: Request):
    """Export hackpack archive"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_hackpack(hackpack_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="hackpack_v2 not found")
    return item

@router.post("/api/hackpack-v2/{hackpack_id}/validate")
async def api_hackpack_v2_w199_validate_hackpack(hackpack_id: str, request: Request):
    """Validate all sub-bundles"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_hackpack(hackpack_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="hackpack_v2 not found")
    return item
