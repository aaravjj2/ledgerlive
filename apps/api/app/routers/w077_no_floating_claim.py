"""Wave 77: No Floating Claim Guard Router — Meta-test enforcement ensuring no claim exists without evidence pointer.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w077_no_floating_claim import service

router = APIRouter(tags=["No Floating Claim Guard"])

@router.get("/api/no-floating-claims")
async def api_no_floating_claim_w77_list_guards(limit: int = 100):
    """List floating claim guards"""
    items = service.list_guards(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/no-floating-claims", status_code=201)
async def api_no_floating_claim_w77_run_scan(request: Request):
    """Run floating claim scan"""
    data = await request.json()
    item = service.run_scan(data)
    return item

@router.get("/api/no-floating-claims/coverage")
async def api_no_floating_claim_w77_coverage(limit: int = 100):
    """Get evidence coverage metrics"""
    items = service.coverage(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/no-floating-claims/report")
async def api_no_floating_claim_w77_scan_report(limit: int = 100):
    """Get scan report"""
    items = service.scan_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/no-floating-claims/{guard_id}")
async def api_no_floating_claim_w77_get_guard(guard_id: str):
    """Get guard result"""
    item = service.get_guard(guard_id)
    if not item:
        raise HTTPException(status_code=404, detail="no_floating_claim not found")
    return item

@router.post("/api/no-floating-claims/{guard_id}/fix")
async def api_no_floating_claim_w77_fix_violation(guard_id: str, request: Request):
    """Fix floating claim violation"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.fix_violation(guard_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="no_floating_claim not found")
    return item
