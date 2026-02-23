"""Wave 143: Caching with Output Proofs Router — Caching layer with 'no output changes' proofs for correctness.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w143_caching_proof import service

router = APIRouter(tags=["Caching with Output Proofs"])

@router.get("/api/caching-proofs")
async def api_caching_proof_w143_list_caches(limit: int = 100):
    """List cache proof tests"""
    items = service.list_caches(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/caching-proofs", status_code=201)
async def api_caching_proof_w143_test_cache(request: Request):
    """Test cache output correctness"""
    data = await request.json()
    item = service.test_cache(data)
    return item

@router.get("/api/caching-proofs/report")
async def api_caching_proof_w143_cache_report(limit: int = 100):
    """Get caching proof report"""
    items = service.cache_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/caching-proofs/{cache_id}")
async def api_caching_proof_w143_get_cache(cache_id: str):
    """Get cache test details"""
    item = service.get_cache(cache_id)
    if not item:
        raise HTTPException(status_code=404, detail="caching_proof not found")
    return item

@router.post("/api/caching-proofs/{cache_id}/verify")
async def api_caching_proof_w143_verify_output(cache_id: str, request: Request):
    """Verify output equality"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_output(cache_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="caching_proof not found")
    return item
