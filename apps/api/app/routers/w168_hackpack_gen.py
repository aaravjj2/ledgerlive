"""Wave 168: Hackpack Generator v1 Router — Generates deterministic hackathon pack: architecture diagram, tool schemas, demo script, proof pack pointer, deployment placeholders.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w168_hackpack_gen import service

router = APIRouter(tags=["Hackpack Generator v1"])

@router.get("/api/hackpacks")
async def api_hackpack_gen_w168_list_hackpacks(limit: int = 100):
    """List generated hackpacks"""
    items = service.list_hackpacks(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/hackpacks", status_code=201)
async def api_hackpack_gen_w168_generate_hackpack(request: Request):
    """Generate hackathon pack"""
    data = await request.json()
    item = service.generate_hackpack(data)
    return item

@router.get("/api/hackpacks/report")
async def api_hackpack_gen_w168_hackpack_report(limit: int = 100):
    """Get hackpack generation report"""
    items = service.hackpack_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/hackpacks/{hackpack_id}")
async def api_hackpack_gen_w168_get_hackpack(hackpack_id: str):
    """Get hackpack details"""
    item = service.get_hackpack(hackpack_id)
    if not item:
        raise HTTPException(status_code=404, detail="hackpack_gen not found")
    return item

@router.post("/api/hackpacks/{hackpack_id}/export")
async def api_hackpack_gen_w168_export_hackpack(hackpack_id: str, request: Request):
    """Export hackpack bundle"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_hackpack(hackpack_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="hackpack_gen not found")
    return item

@router.post("/api/hackpacks/{hackpack_id}/validate")
async def api_hackpack_gen_w168_validate_hackpack(hackpack_id: str, request: Request):
    """Validate hackpack integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_hackpack(hackpack_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="hackpack_gen not found")
    return item
