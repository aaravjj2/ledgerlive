"""Wave 264: Reproduce Close v1 Router — From Race Control, regenerate binder/board pack from replay. Byte-identical hard gate ensures reproducibility of close artifacts.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w264_reproduce_close import service

router = APIRouter(tags=["Reproduce Close v1"])

@router.get("/api/reproduce-close")
async def api_reproduce_close_w264_list_reproductions(limit: int = 100):
    """List close reproductions"""
    items = service.list_reproductions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/reproduce-close", status_code=201)
async def api_reproduce_close_w264_create_reproduction(request: Request):
    """Create close reproduction"""
    data = await request.json()
    item = service.create_reproduction(data)
    return item

@router.get("/api/reproduce-close/report")
async def api_reproduce_close_w264_reproduction_report(limit: int = 100):
    """Get reproduction report"""
    items = service.reproduction_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/reproduce-close/{reproduce_id}")
async def api_reproduce_close_w264_get_reproduction(reproduce_id: str):
    """Get reproduction details"""
    item = service.get_reproduction(reproduce_id)
    if not item:
        raise HTTPException(status_code=404, detail="reproduce_close not found")
    return item

@router.post("/api/reproduce-close/{reproduce_id}/regenerate")
async def api_reproduce_close_w264_regenerate_binder(reproduce_id: str, request: Request):
    """Regenerate binder from replay"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.regenerate_binder(reproduce_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="reproduce_close not found")
    return item

@router.post("/api/reproduce-close/{reproduce_id}/verify")
async def api_reproduce_close_w264_verify_hashes(reproduce_id: str, request: Request):
    """Verify hash match"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_hashes(reproduce_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="reproduce_close not found")
    return item
