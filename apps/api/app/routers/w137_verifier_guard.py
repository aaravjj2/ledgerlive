"""Wave 137: Verifier-First Guards Router — Verifier-first blocking checks everywhere — no unverified output passes.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w137_verifier_guard import service

router = APIRouter(tags=["Verifier-First Guards"])

@router.get("/api/verifier-guards")
async def api_verifier_guard_w137_list_guards(limit: int = 100):
    """List verifier guards"""
    items = service.list_guards(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/verifier-guards", status_code=201)
async def api_verifier_guard_w137_check_guard(request: Request):
    """Check verifier guard"""
    data = await request.json()
    item = service.check_guard(data)
    return item

@router.get("/api/verifier-guards/report")
async def api_verifier_guard_w137_guard_report(limit: int = 100):
    """Get verifier guard report"""
    items = service.guard_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/verifier-guards/{guard_id}")
async def api_verifier_guard_w137_get_guard(guard_id: str):
    """Get guard details"""
    item = service.get_guard(guard_id)
    if not item:
        raise HTTPException(status_code=404, detail="verifier_guard not found")
    return item

@router.post("/api/verifier-guards/{guard_id}/override")
async def api_verifier_guard_w137_override(guard_id: str, request: Request):
    """Approve override"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.override(guard_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="verifier_guard not found")
    return item
