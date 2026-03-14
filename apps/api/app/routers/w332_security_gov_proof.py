"""Wave 332: Security Governance Proof v1 Router — Security posture demonstrated in Race Control with deterministic exports.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w332_security_gov_proof import service

router = APIRouter(tags=["Security Governance Proof v1"])

@router.get("/api/security-gov-proof")
async def api_security_gov_proof_w332_list_proofs(limit: int = 100):
    """List governance proofs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/security-gov-proof", status_code=201)
async def api_security_gov_proof_w332_generate_proof(request: Request):
    """Generate governance proof"""
    data = await request.json()
    item = service.generate_proof(data)
    return item

@router.get("/api/security-gov-proof/report")
async def api_security_gov_proof_w332_proof_report(limit: int = 100):
    """Get governance proof report"""
    items = service.proof_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/security-gov-proof/{proof_id}")
async def api_security_gov_proof_w332_get_proof(proof_id: str):
    """Get proof details"""
    item = service.get_proof(proof_id)
    if not item:
        raise HTTPException(status_code=404, detail="security_gov_proof not found")
    return item

@router.post("/api/security-gov-proof/{proof_id}/seal")
async def api_security_gov_proof_w332_seal_proof(proof_id: str, request: Request):
    """Seal governance proof"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.seal_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="security_gov_proof not found")
    return item

@router.post("/api/security-gov-proof/{proof_id}/verify")
async def api_security_gov_proof_w332_verify_posture(proof_id: str, request: Request):
    """Verify security posture"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_posture(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="security_gov_proof not found")
    return item
