"""Wave 119: Data Platform Proof Pack Router — Proof pack with schema snapshots and lineage verification.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w119_data_proof import service

router = APIRouter(tags=["Data Platform Proof Pack"])

@router.get("/api/data-proofs")
async def api_data_proof_w119_list_proofs(limit: int = 100):
    """List data platform proof packs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/data-proofs", status_code=201)
async def api_data_proof_w119_generate_proof(request: Request):
    """Generate data proof pack"""
    data = await request.json()
    item = service.generate_proof(data)
    return item

@router.get("/api/data-proofs/export")
async def api_data_proof_w119_export_proof(limit: int = 100):
    """Export data proof pack"""
    items = service.export_proof(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/data-proofs/{proof_id}")
async def api_data_proof_w119_get_proof(proof_id: str):
    """Get proof details"""
    item = service.get_proof(proof_id)
    if not item:
        raise HTTPException(status_code=404, detail="data_proof not found")
    return item

@router.post("/api/data-proofs/{proof_id}/verify")
async def api_data_proof_w119_verify_proof(proof_id: str, request: Request):
    """Verify proof pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="data_proof not found")
    return item
