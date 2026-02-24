"""Wave 321: Bundle Integrity Proof v1 Router — Signing and verify tool for bundles; tamper must fail deterministically.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w321_bundle_integrity_proof import service

router = APIRouter(tags=["Bundle Integrity Proof v1"])

@router.get("/api/bundle-integrity-proof")
async def api_bundle_integrity_proof_w321_list_proofs(limit: int = 100):
    """List integrity proofs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/bundle-integrity-proof", status_code=201)
async def api_bundle_integrity_proof_w321_sign_bundle(request: Request):
    """Sign bundle"""
    data = await request.json()
    item = service.sign_bundle(data)
    return item

@router.get("/api/bundle-integrity-proof/report")
async def api_bundle_integrity_proof_w321_integrity_report(limit: int = 100):
    """Get integrity report"""
    items = service.integrity_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/bundle-integrity-proof/{integrity_id}")
async def api_bundle_integrity_proof_w321_get_proof(integrity_id: str):
    """Get proof details"""
    item = service.get_proof(integrity_id)
    if not item:
        raise HTTPException(status_code=404, detail="bundle_integrity_proof not found")
    return item

@router.post("/api/bundle-integrity-proof/{integrity_id}/tamper-test")
async def api_bundle_integrity_proof_w321_tamper_test(integrity_id: str, request: Request):
    """Test tamper detection"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.tamper_test(integrity_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="bundle_integrity_proof not found")
    return item

@router.post("/api/bundle-integrity-proof/{integrity_id}/verify")
async def api_bundle_integrity_proof_w321_verify_signature(integrity_id: str, request: Request):
    """Verify bundle signature"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_signature(integrity_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="bundle_integrity_proof not found")
    return item
