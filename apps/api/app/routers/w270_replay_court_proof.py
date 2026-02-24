"""Wave 270: Replay Court Proof Wave v1 Router — MCP E2E from Race Control to generate court pack, verify, replay, regenerate binder, and hash match. Determinism twice-run verified.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w270_replay_court_proof import service

router = APIRouter(tags=["Replay Court Proof Wave v1"])

@router.get("/api/replay-court-proof")
async def api_replay_court_proof_w270_list_proofs(limit: int = 100):
    """List replay court proofs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/replay-court-proof", status_code=201)
async def api_replay_court_proof_w270_generate_proof(request: Request):
    """Generate replay court proof"""
    data = await request.json()
    item = service.generate_proof(data)
    return item

@router.get("/api/replay-court-proof/report")
async def api_replay_court_proof_w270_proof_report(limit: int = 100):
    """Get replay court proof report"""
    items = service.proof_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/replay-court-proof/{proof_id}")
async def api_replay_court_proof_w270_get_proof(proof_id: str):
    """Get proof details"""
    item = service.get_proof(proof_id)
    if not item:
        raise HTTPException(status_code=404, detail="replay_court_proof not found")
    return item

@router.post("/api/replay-court-proof/{proof_id}/seal")
async def api_replay_court_proof_w270_seal_proof(proof_id: str, request: Request):
    """Seal replay court proof"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.seal_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="replay_court_proof not found")
    return item

@router.post("/api/replay-court-proof/{proof_id}/verify")
async def api_replay_court_proof_w270_verify_proof(proof_id: str, request: Request):
    """Verify proof integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="replay_court_proof not found")
    return item
