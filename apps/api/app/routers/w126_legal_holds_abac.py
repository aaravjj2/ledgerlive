"""Wave 126: Legal Holds + ABAC Router — Legal holds integrated with ABAC policy rules.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w126_legal_holds_abac import service

router = APIRouter(tags=["Legal Holds + ABAC"])

@router.get("/api/legal-holds-abac")
async def api_legal_holds_abac_w126_list_holds(limit: int = 100):
    """List ABAC legal holds"""
    items = service.list_holds(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/legal-holds-abac", status_code=201)
async def api_legal_holds_abac_w126_create_hold(request: Request):
    """Create ABAC legal hold"""
    data = await request.json()
    item = service.create_hold(data)
    return item

@router.get("/api/legal-holds-abac/report")
async def api_legal_holds_abac_w126_hold_report(limit: int = 100):
    """Get legal holds report"""
    items = service.hold_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/legal-holds-abac/{hold_id}")
async def api_legal_holds_abac_w126_get_hold(hold_id: str):
    """Get hold details"""
    item = service.get_hold(hold_id)
    if not item:
        raise HTTPException(status_code=404, detail="legal_holds_abac not found")
    return item

@router.post("/api/legal-holds-abac/{hold_id}/enforce")
async def api_legal_holds_abac_w126_enforce(hold_id: str, request: Request):
    """Enforce hold with ABAC"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.enforce(hold_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="legal_holds_abac not found")
    return item

@router.post("/api/legal-holds-abac/{hold_id}/release")
async def api_legal_holds_abac_w126_release_hold(hold_id: str, request: Request):
    """Release hold"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.release_hold(hold_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="legal_holds_abac not found")
    return item
