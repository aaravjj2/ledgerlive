"""Wave 155: Lineage Verifier Strict Mode Router — End-to-end lineage verifier in strict mode — no unverified lineage passes.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w155_lineage_strict import service

router = APIRouter(tags=["Lineage Verifier Strict Mode"])

@router.get("/api/lineage-strict")
async def api_lineage_strict_w155_list_verifiers(limit: int = 100):
    """List strict lineage verifiers"""
    items = service.list_verifiers(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/lineage-strict", status_code=201)
async def api_lineage_strict_w155_verify_lineage(request: Request):
    """Verify lineage in strict mode"""
    data = await request.json()
    item = service.verify_lineage(data)
    return item

@router.get("/api/lineage-strict/report")
async def api_lineage_strict_w155_strict_report(limit: int = 100):
    """Get strict mode report"""
    items = service.strict_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/lineage-strict/{verifier_id}")
async def api_lineage_strict_w155_get_verifier(verifier_id: str):
    """Get verifier details"""
    item = service.get_verifier(verifier_id)
    if not item:
        raise HTTPException(status_code=404, detail="lineage_strict not found")
    return item

@router.post("/api/lineage-strict/{verifier_id}/check")
async def api_lineage_strict_w155_check_ref(verifier_id: str, request: Request):
    """Check specific lineage ref"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_ref(verifier_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="lineage_strict not found")
    return item
