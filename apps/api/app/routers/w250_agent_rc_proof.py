"""Wave 250: Agent RC Proof Wave v1 Router — End-to-end proof covering Next Actions, Plan Preview, Approve, Execute, Dossier, and Replay link. Deterministic twice-run verification.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w250_agent_rc_proof import service

router = APIRouter(tags=["Agent RC Proof Wave v1"])

@router.get("/api/agent-rc-proof")
async def api_agent_rc_proof_w250_list_proofs(limit: int = 100):
    """List agent RC proofs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/agent-rc-proof", status_code=201)
async def api_agent_rc_proof_w250_generate_proof(request: Request):
    """Generate agent RC proof"""
    data = await request.json()
    item = service.generate_proof(data)
    return item

@router.get("/api/agent-rc-proof/report")
async def api_agent_rc_proof_w250_proof_report(limit: int = 100):
    """Get agent RC proof report"""
    items = service.proof_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/agent-rc-proof/{proof_id}")
async def api_agent_rc_proof_w250_get_proof(proof_id: str):
    """Get proof details"""
    item = service.get_proof(proof_id)
    if not item:
        raise HTTPException(status_code=404, detail="agent_rc_proof not found")
    return item

@router.post("/api/agent-rc-proof/{proof_id}/seal")
async def api_agent_rc_proof_w250_seal_proof(proof_id: str, request: Request):
    """Seal agent RC proof"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.seal_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="agent_rc_proof not found")
    return item

@router.post("/api/agent-rc-proof/{proof_id}/verify")
async def api_agent_rc_proof_w250_verify_proof(proof_id: str, request: Request):
    """Verify proof integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="agent_rc_proof not found")
    return item
