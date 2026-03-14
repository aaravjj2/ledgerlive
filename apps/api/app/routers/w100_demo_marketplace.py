"""Wave 100: Demo Mode Marketplace Router — End-to-end demo mode including marketplace template import and execution.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w100_demo_marketplace import service

router = APIRouter(tags=["Demo Mode Marketplace"])

@router.get("/api/demo-marketplace")
async def api_demo_marketplace_w100_list_demos(limit: int = 100):
    """List demo marketplace runs"""
    items = service.list_demos(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/demo-marketplace", status_code=201)
async def api_demo_marketplace_w100_start_demo(request: Request):
    """Start demo marketplace run"""
    data = await request.json()
    item = service.start_demo(data)
    return item

@router.get("/api/demo-marketplace/report")
async def api_demo_marketplace_w100_demo_report(limit: int = 100):
    """Get demo marketplace report"""
    items = service.demo_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/demo-marketplace/{demo_id}")
async def api_demo_marketplace_w100_get_demo(demo_id: str):
    """Get demo details"""
    item = service.get_demo(demo_id)
    if not item:
        raise HTTPException(status_code=404, detail="demo_marketplace not found")
    return item

@router.post("/api/demo-marketplace/{demo_id}/advance")
async def api_demo_marketplace_w100_advance(demo_id: str, request: Request):
    """Advance to next step"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.advance(demo_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="demo_marketplace not found")
    return item

@router.post("/api/demo-marketplace/{demo_id}/verify")
async def api_demo_marketplace_w100_verify_demo(demo_id: str, request: Request):
    """Verify demo hash"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_demo(demo_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="demo_marketplace not found")
    return item
