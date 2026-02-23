"""Wave 59: Board Pack Generator Router — Deterministic board pack export combining statements, KPIs, treasury, risks.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w59_board_pack import service

router = APIRouter(tags=["Board Pack Generator"])

@router.get("/api/board-packs")
async def api_board_pack_w59_list_packs(limit: int = 100):
    """List board packs"""
    items = service.list_packs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/board-packs", status_code=201)
async def api_board_pack_w59_create_pack(request: Request):
    """Create a board pack"""
    data = await request.json()
    item = service.create_pack(data)
    return item

@router.get("/api/board-packs/export")
async def api_board_pack_w59_export_pack(limit: int = 100):
    """Export latest board pack"""
    items = service.export_pack(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/board-packs/{pack_id}")
async def api_board_pack_w59_get_pack(pack_id: str):
    """Get board pack details"""
    item = service.get_pack(pack_id)
    if not item:
        raise HTTPException(status_code=404, detail="board_pack not found")
    return item

@router.post("/api/board-packs/{pack_id}/generate")
async def api_board_pack_w59_generate(pack_id: str, request: Request):
    """Generate board pack export"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.generate(pack_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="board_pack not found")
    return item

@router.post("/api/board-packs/{pack_id}/sections")
async def api_board_pack_w59_add_section(pack_id: str, request: Request):
    """Add section to board pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_section(pack_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="board_pack not found")
    return item

@router.post("/api/board-packs/{pack_id}/verify")
async def api_board_pack_w59_verify_pack(pack_id: str, request: Request):
    """Verify board pack hash"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_pack(pack_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="board_pack not found")
    return item
