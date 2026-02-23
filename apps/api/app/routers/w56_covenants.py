"""Wave 56: Covenants Monitoring Router — Covenant rules, breach detection, alerts, evidence links.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w56_covenants import service

router = APIRouter(tags=["Covenants Monitoring"])

@router.get("/api/covenants")
async def api_covenants_w56_list_covenants(limit: int = 100):
    """List covenants"""
    items = service.list_covenants(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/covenants", status_code=201)
async def api_covenants_w56_create_covenant(request: Request):
    """Create a covenant rule"""
    data = await request.json()
    item = service.create_covenant(data)
    return item

@router.get("/api/covenants/breach-summary")
async def api_covenants_w56_breach_summary(limit: int = 100):
    """Get breach summary report"""
    items = service.breach_summary(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/covenants/{covenant_id}")
async def api_covenants_w56_get_covenant(covenant_id: str):
    """Get covenant details"""
    item = service.get_covenant(covenant_id)
    if not item:
        raise HTTPException(status_code=404, detail="covenants not found")
    return item

@router.post("/api/covenants/{covenant_id}/check")
async def api_covenants_w56_check_breach(covenant_id: str, request: Request):
    """Check covenant for breach"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_breach(covenant_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="covenants not found")
    return item

@router.post("/api/covenants/{covenant_id}/evidence")
async def api_covenants_w56_link_evidence(covenant_id: str, request: Request):
    """Link evidence to covenant"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.link_evidence(covenant_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="covenants not found")
    return item
