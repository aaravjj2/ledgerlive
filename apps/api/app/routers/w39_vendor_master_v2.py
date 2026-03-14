"""Wave 39: Vendor Master 2.0 Router — Vendor families, risk ratings, watchlists, approval-required overrides for risky vendors.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w39_vendor_master_v2 import service

router = APIRouter(tags=["Vendor Master 2.0"])

@router.get("/api/vendors-v2")
async def api_vendor_master_v2_w39_list_vendors(limit: int = 100):
    """List vendors with hierarchy"""
    items = service.list_vendors(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/vendors-v2", status_code=201)
async def api_vendor_master_v2_w39_create_vendor(request: Request):
    """Create a vendor"""
    data = await request.json()
    item = service.create_vendor(data)
    return item

@router.get("/api/vendors-v2/watchlist")
async def api_vendor_master_v2_w39_watchlist_report(limit: int = 100):
    """Get vendor watchlist report"""
    items = service.watchlist_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/vendors-v2/{vendor_id}")
async def api_vendor_master_v2_w39_get_vendor(vendor_id: str):
    """Get vendor details"""
    item = service.get_vendor(vendor_id)
    if not item:
        raise HTTPException(status_code=404, detail="vendor_master_v2 not found")
    return item

@router.post("/api/vendors-v2/{vendor_id}/approve")
async def api_vendor_master_v2_w39_approve_override(vendor_id: str, request: Request):
    """Approve risky vendor override"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_override(vendor_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="vendor_master_v2 not found")
    return item

@router.post("/api/vendors-v2/{vendor_id}/merge")
async def api_vendor_master_v2_w39_merge_vendors(vendor_id: str, request: Request):
    """Merge duplicate vendors"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.merge_vendors(vendor_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="vendor_master_v2 not found")
    return item

@router.post("/api/vendors-v2/{vendor_id}/risk")
async def api_vendor_master_v2_w39_set_risk(vendor_id: str, request: Request):
    """Set vendor risk rating"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.set_risk(vendor_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="vendor_master_v2 not found")
    return item
