"""Wave 140: Reliability Proof Pack Router — Proof pack including chaos, mutation, and loop reports.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w140_reliability_proof import service

router = APIRouter(tags=["Reliability Proof Pack"])

@router.get("/api/reliability-proofs")
async def api_reliability_proof_w140_list_proofs(limit: int = 100):
    """List reliability proof packs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/reliability-proofs", status_code=201)
async def api_reliability_proof_w140_generate_proof(request: Request):
    """Generate reliability proof pack"""
    data = await request.json()
    item = service.generate_proof(data)
    return item

@router.get("/api/reliability-proofs/export")
async def api_reliability_proof_w140_export_proof(limit: int = 100):
    """Export reliability proof pack"""
    items = service.export_proof(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/reliability-proofs/{proof_id}")
async def api_reliability_proof_w140_get_proof(proof_id: str):
    """Get proof details"""
    item = service.get_proof(proof_id)
    if not item:
        raise HTTPException(status_code=404, detail="reliability_proof not found")
    return item

@router.post("/api/reliability-proofs/{proof_id}/verify")
async def api_reliability_proof_w140_verify_proof(proof_id: str, request: Request):
    """Verify proof pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="reliability_proof not found")
    return item
