"""Wave 324: Readiness Proof Wave v1 Router — Readiness PASS with verified artifacts and determinism twice-run.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w324_readiness_proof import service

router = APIRouter(tags=["Readiness Proof Wave v1"])

@router.get("/api/readiness-proof")
async def api_readiness_proof_w324_list_proofs(limit: int = 100):
    """List readiness proofs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/readiness-proof", status_code=201)
async def api_readiness_proof_w324_generate_proof(request: Request):
    """Generate readiness proof"""
    data = await request.json()
    item = service.generate_proof(data)
    return item

@router.get("/api/readiness-proof/report")
async def api_readiness_proof_w324_proof_report(limit: int = 100):
    """Get readiness proof report"""
    items = service.proof_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/readiness-proof/{proof_id}")
async def api_readiness_proof_w324_get_proof(proof_id: str):
    """Get proof details"""
    item = service.get_proof(proof_id)
    if not item:
        raise HTTPException(status_code=404, detail="readiness_proof not found")
    return item

@router.post("/api/readiness-proof/{proof_id}/seal")
async def api_readiness_proof_w324_seal_proof(proof_id: str, request: Request):
    """Seal readiness proof"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.seal_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="readiness_proof not found")
    return item

@router.post("/api/readiness-proof/{proof_id}/verify")
async def api_readiness_proof_w324_verify_readiness(proof_id: str, request: Request):
    """Verify readiness"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_readiness(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="readiness_proof not found")
    return item
