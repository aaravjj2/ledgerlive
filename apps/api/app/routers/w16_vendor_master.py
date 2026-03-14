"""Wave 16: Vendor Master Router — Vendor master data management and deduplication.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w16_vendor_master import service

router = APIRouter(tags=["Vendor Master"])

@router.get("/api/vendors")
async def api_list(limit: int = 100):
    """List vendors"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/vendors", status_code=201)
async def api_create(request: Request):
    """Create a vendor"""
    data = await request.json()
    item = service.create(data)
    return item

@router.post("/api/vendors/merge", status_code=201)
async def api_merge(request: Request):
    """Merge duplicate vendors"""
    data = await request.json()
    item = service.merge(data)
    return item

@router.get("/api/vendors/{vendor_id}")
async def api_get(vendor_id: str):
    """Get vendor details"""
    item = service.get(vendor_id)
    if not item:
        raise HTTPException(status_code=404, detail="vendor_master not found")
    return item

@router.put("/api/vendors/{vendor_id}")
async def api_update(vendor_id: str, request: Request):
    """Update vendor"""
    data = await request.json()
    item = service.update(vendor_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="vendor_master not found")
    return item
