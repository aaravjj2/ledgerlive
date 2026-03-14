"""Wave 129: Policy Proof Pack Router — Proof pack including policy matrix outputs and deny logs.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w129_policy_proof import service

router = APIRouter(tags=["Policy Proof Pack"])

@router.get("/api/policy-proofs")
async def api_policy_proof_w129_list_proofs(limit: int = 100):
    """List policy proof packs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/policy-proofs", status_code=201)
async def api_policy_proof_w129_generate_proof(request: Request):
    """Generate policy proof pack"""
    data = await request.json()
    item = service.generate_proof(data)
    return item

@router.get("/api/policy-proofs/export")
async def api_policy_proof_w129_export_proof(limit: int = 100):
    """Export policy proof pack"""
    items = service.export_proof(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/policy-proofs/{proof_id}")
async def api_policy_proof_w129_get_proof(proof_id: str):
    """Get proof details"""
    item = service.get_proof(proof_id)
    if not item:
        raise HTTPException(status_code=404, detail="policy_proof not found")
    return item

@router.post("/api/policy-proofs/{proof_id}/verify")
async def api_policy_proof_w129_verify_proof(proof_id: str, request: Request):
    """Verify proof pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="policy_proof not found")
    return item
