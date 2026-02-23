"""Wave 133: Proof of Proof of Proof Router — Run make proof twice, compare pack hashes — must be identical.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w133_proof_of_proof import service

router = APIRouter(tags=["Proof of Proof of Proof"])

@router.get("/api/proof-of-proof")
async def api_proof_of_proof_w133_list_pops(limit: int = 100):
    """List proof-of-proof runs"""
    items = service.list_pops(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/proof-of-proof", status_code=201)
async def api_proof_of_proof_w133_run_pop(request: Request):
    """Run proof-of-proof comparison"""
    data = await request.json()
    item = service.run_pop(data)
    return item

@router.get("/api/proof-of-proof/report")
async def api_proof_of_proof_w133_pop_report(limit: int = 100):
    """Get PoP report"""
    items = service.pop_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/proof-of-proof/{pop_id}")
async def api_proof_of_proof_w133_get_pop(pop_id: str):
    """Get PoP details"""
    item = service.get_pop(pop_id)
    if not item:
        raise HTTPException(status_code=404, detail="proof_of_proof not found")
    return item

@router.post("/api/proof-of-proof/{pop_id}/verify")
async def api_proof_of_proof_w133_verify_match(pop_id: str, request: Request):
    """Verify hash match"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_match(pop_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="proof_of_proof not found")
    return item
