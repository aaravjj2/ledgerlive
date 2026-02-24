"""Wave 240: RC Proof Pack v1 Router — Final Race Control proof pack: aggregates all RC components (state machine, lanes, critical path, scoreboard, incidents, rules, approvals) into a single verified artifact with content hash.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w240_rc_proof_pack import service

router = APIRouter(tags=["RC Proof Pack v1"])

@router.get("/api/rc-proof-pack")
async def api_rc_proof_pack_w240_list_proofs(limit: int = 100):
    """List RC proof packs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/rc-proof-pack", status_code=201)
async def api_rc_proof_pack_w240_generate_proof(request: Request):
    """Generate RC proof pack"""
    data = await request.json()
    item = service.generate_proof(data)
    return item

@router.get("/api/rc-proof-pack/report")
async def api_rc_proof_pack_w240_proof_report(limit: int = 100):
    """Get RC proof pack report"""
    items = service.proof_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/rc-proof-pack/{proof_id}")
async def api_rc_proof_pack_w240_get_proof(proof_id: str):
    """Get proof pack details"""
    item = service.get_proof(proof_id)
    if not item:
        raise HTTPException(status_code=404, detail="rc_proof_pack not found")
    return item

@router.post("/api/rc-proof-pack/{proof_id}/download")
async def api_rc_proof_pack_w240_download_proof(proof_id: str, request: Request):
    """Download proof pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.download_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_proof_pack not found")
    return item

@router.post("/api/rc-proof-pack/{proof_id}/seal")
async def api_rc_proof_pack_w240_seal_proof(proof_id: str, request: Request):
    """Seal proof pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.seal_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_proof_pack not found")
    return item

@router.post("/api/rc-proof-pack/{proof_id}/verify")
async def api_rc_proof_pack_w240_verify_proof(proof_id: str, request: Request):
    """Verify proof pack integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_proof_pack not found")
    return item
