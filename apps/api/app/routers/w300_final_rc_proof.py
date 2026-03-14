"""Wave 300: Final RC Proof Wave v1 Router — Race Control RC Run end-to-end: plan preview, approvals via channel, execute, incidents resolved, replay regen equality, court pack verify, telemetry pack verify. MCP E2E twice-run determinism.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w300_final_rc_proof import service

router = APIRouter(tags=["Final RC Proof Wave v1"])

@router.get("/api/final-rc-proof")
async def api_final_rc_proof_w300_list_proofs(limit: int = 100):
    """List final RC proofs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/final-rc-proof", status_code=201)
async def api_final_rc_proof_w300_generate_proof(request: Request):
    """Generate final RC proof"""
    data = await request.json()
    item = service.generate_proof(data)
    return item

@router.get("/api/final-rc-proof/report")
async def api_final_rc_proof_w300_proof_report(limit: int = 100):
    """Get final RC proof report"""
    items = service.proof_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/final-rc-proof/{proof_id}")
async def api_final_rc_proof_w300_get_proof(proof_id: str):
    """Get proof details"""
    item = service.get_proof(proof_id)
    if not item:
        raise HTTPException(status_code=404, detail="final_rc_proof not found")
    return item

@router.post("/api/final-rc-proof/{proof_id}/seal")
async def api_final_rc_proof_w300_seal_proof(proof_id: str, request: Request):
    """Seal final RC proof"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.seal_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="final_rc_proof not found")
    return item

@router.post("/api/final-rc-proof/{proof_id}/verify")
async def api_final_rc_proof_w300_verify_proof(proof_id: str, request: Request):
    """Verify proof integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="final_rc_proof not found")
    return item
