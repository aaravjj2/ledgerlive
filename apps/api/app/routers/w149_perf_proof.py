"""Wave 149: Performance Proof Pack Router — Proof pack including performance snapshots and budget results.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w149_perf_proof import service

router = APIRouter(tags=["Performance Proof Pack"])

@router.get("/api/perf-proofs")
async def api_perf_proof_w149_list_proofs(limit: int = 100):
    """List performance proof packs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/perf-proofs", status_code=201)
async def api_perf_proof_w149_generate_proof(request: Request):
    """Generate performance proof pack"""
    data = await request.json()
    item = service.generate_proof(data)
    return item

@router.get("/api/perf-proofs/export")
async def api_perf_proof_w149_export_proof(limit: int = 100):
    """Export performance proof pack"""
    items = service.export_proof(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/perf-proofs/{proof_id}")
async def api_perf_proof_w149_get_proof(proof_id: str):
    """Get proof details"""
    item = service.get_proof(proof_id)
    if not item:
        raise HTTPException(status_code=404, detail="perf_proof not found")
    return item

@router.post("/api/perf-proofs/{proof_id}/verify")
async def api_perf_proof_w149_verify_proof(proof_id: str, request: Request):
    """Verify proof pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="perf_proof not found")
    return item
