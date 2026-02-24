"""Wave 308: Builder Proof Wave v1 Router — Full builder flow proof with determinism twice-run verification.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w308_builder_proof import service

router = APIRouter(tags=["Builder Proof Wave v1"])

@router.get("/api/builder-proof")
async def api_builder_proof_w308_list_proofs(limit: int = 100):
    """List builder proofs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/builder-proof", status_code=201)
async def api_builder_proof_w308_generate_proof(request: Request):
    """Generate builder proof"""
    data = await request.json()
    item = service.generate_proof(data)
    return item

@router.get("/api/builder-proof/report")
async def api_builder_proof_w308_proof_report(limit: int = 100):
    """Get builder proof report"""
    items = service.proof_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/builder-proof/{proof_id}")
async def api_builder_proof_w308_get_proof(proof_id: str):
    """Get proof details"""
    item = service.get_proof(proof_id)
    if not item:
        raise HTTPException(status_code=404, detail="builder_proof not found")
    return item

@router.post("/api/builder-proof/{proof_id}/seal")
async def api_builder_proof_w308_seal_proof(proof_id: str, request: Request):
    """Seal builder proof"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.seal_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="builder_proof not found")
    return item

@router.post("/api/builder-proof/{proof_id}/verify")
async def api_builder_proof_w308_verify_determinism(proof_id: str, request: Request):
    """Verify determinism twice-run"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_determinism(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="builder_proof not found")
    return item
