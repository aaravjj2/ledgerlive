"""Wave 193: No-Floating-Claim Enforcement Router — Agent suggestions and decisions must include dossier_id references. Export blocked if any resolution lacks dossier. Guard enforcement.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w193_claim_enforcement import service

router = APIRouter(tags=["No-Floating-Claim Enforcement"])

@router.get("/api/claim-enforcement")
async def api_claim_enforcement_w193_list_enforcements(limit: int = 100):
    """List claim enforcements"""
    items = service.list_enforcements(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/claim-enforcement", status_code=201)
async def api_claim_enforcement_w193_check_claim(request: Request):
    """Check claim has dossier reference"""
    data = await request.json()
    item = service.check_claim(data)
    return item

@router.get("/api/claim-enforcement/report")
async def api_claim_enforcement_w193_enforcement_report(limit: int = 100):
    """Get claim enforcement report"""
    items = service.enforcement_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/claim-enforcement/{enforcement_id}")
async def api_claim_enforcement_w193_get_enforcement(enforcement_id: str):
    """Get enforcement details"""
    item = service.get_enforcement(enforcement_id)
    if not item:
        raise HTTPException(status_code=404, detail="claim_enforcement not found")
    return item

@router.post("/api/claim-enforcement/{enforcement_id}/block")
async def api_claim_enforcement_w193_block_export(enforcement_id: str, request: Request):
    """Block export for missing dossier"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.block_export(enforcement_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="claim_enforcement not found")
    return item

@router.post("/api/claim-enforcement/{enforcement_id}/unblock")
async def api_claim_enforcement_w193_unblock_export(enforcement_id: str, request: Request):
    """Unblock after dossier attached"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.unblock_export(enforcement_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="claim_enforcement not found")
    return item
