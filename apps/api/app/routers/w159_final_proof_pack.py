"""Wave 159: Final Proof of Proofs Router — Final proof pack aggregating all proof packs across all phases.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w159_final_proof_pack import service

router = APIRouter(tags=["Final Proof of Proofs"])

@router.get("/api/final-proof-packs")
async def api_final_proof_pack_w159_list_proofs(limit: int = 100):
    """List final proof packs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/final-proof-packs", status_code=201)
async def api_final_proof_pack_w159_generate_proof(request: Request):
    """Generate final proof of proofs"""
    data = await request.json()
    item = service.generate_proof(data)
    return item

@router.get("/api/final-proof-packs/export")
async def api_final_proof_pack_w159_export_proof(limit: int = 100):
    """Export final proof pack"""
    items = service.export_proof(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/final-proof-packs/{final_proof_id}")
async def api_final_proof_pack_w159_get_proof(final_proof_id: str):
    """Get final proof details"""
    item = service.get_proof(final_proof_id)
    if not item:
        raise HTTPException(status_code=404, detail="final_proof_pack not found")
    return item

@router.post("/api/final-proof-packs/{final_proof_id}/verify")
async def api_final_proof_pack_w159_verify_proof(final_proof_id: str, request: Request):
    """Verify final proof"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_proof(final_proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="final_proof_pack not found")
    return item
