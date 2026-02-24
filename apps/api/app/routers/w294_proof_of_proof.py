"""Wave 294: Proof-of-Proof v2 Router â€” Generate proof pack twice for a milestone and compare pack hash manifests. Meta-verification of proof generation determinism.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w294_proof_of_proof import service

router = APIRouter(tags=["Proof-of-Proof v2"])

@router.get("/api/proof-of-proof-v2")
async def api_proof_of_proof_w294_list_pops(limit: int = 100):
    """List proof-of-proof verifications"""
    items = service.list_pops(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/proof-of-proof-v2", status_code=201)
async def api_proof_of_proof_w294_create_pop(request: Request):
    """Create proof-of-proof verification"""
    data = await request.json()
    item = service.create_pop(data)
    return item

@router.get("/api/proof-of-proof-v2/report")
async def api_proof_of_proof_w294_pop_report(limit: int = 100):
    """Get proof-of-proof report"""
    items = service.pop_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/proof-of-proof-v2/{pop_id}")
async def api_proof_of_proof_w294_get_pop(pop_id: str):
    """Get proof-of-proof details"""
    item = service.get_pop(pop_id)
    if not item:
        raise HTTPException(status_code=404, detail="proof_of_proof not found")
    return item

@router.post("/api/proof-of-proof-v2/{pop_id}/compare")
async def api_proof_of_proof_w294_compare_manifests(pop_id: str, request: Request):
    """Compare manifests"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.compare_manifests(pop_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="proof_of_proof not found")
    return item

@router.post("/api/proof-of-proof-v2/{pop_id}/generate-twice")
async def api_proof_of_proof_w294_generate_twice(pop_id: str, request: Request):
    """Generate proof pack twice"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.generate_twice(pop_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="proof_of_proof not found")
    return item

