"""Wave 260: Security Proof Wave v1 Router — MCP E2E proof showing blocked action to security event to fix path to approval to proceed. Export posture pack with determinism twice-run.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w260_security_proof import service

router = APIRouter(tags=["Security Proof Wave v1"])

@router.get("/api/security-proof")
async def api_security_proof_w260_list_proofs(limit: int = 100):
    """List security proofs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/security-proof", status_code=201)
async def api_security_proof_w260_generate_proof(request: Request):
    """Generate security proof"""
    data = await request.json()
    item = service.generate_proof(data)
    return item

@router.get("/api/security-proof/report")
async def api_security_proof_w260_proof_report(limit: int = 100):
    """Get security proof report"""
    items = service.proof_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/security-proof/{proof_id}")
async def api_security_proof_w260_get_proof(proof_id: str):
    """Get proof details"""
    item = service.get_proof(proof_id)
    if not item:
        raise HTTPException(status_code=404, detail="security_proof not found")
    return item

@router.post("/api/security-proof/{proof_id}/seal")
async def api_security_proof_w260_seal_proof(proof_id: str, request: Request):
    """Seal security proof"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.seal_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="security_proof not found")
    return item

@router.post("/api/security-proof/{proof_id}/verify")
async def api_security_proof_w260_verify_proof(proof_id: str, request: Request):
    """Verify proof integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="security_proof not found")
    return item
