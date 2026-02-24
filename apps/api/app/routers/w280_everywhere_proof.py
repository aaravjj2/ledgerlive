"""Wave 280: Everywhere Proof Wave v1 Router — MCP E2E triggers approval to mock chat/email, approves via channel, Race Control updates, export ops pack. Determinism twice-run.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w280_everywhere_proof import service

router = APIRouter(tags=["Everywhere Proof Wave v1"])

@router.get("/api/everywhere-proof")
async def api_everywhere_proof_w280_list_proofs(limit: int = 100):
    """List everywhere proofs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/everywhere-proof", status_code=201)
async def api_everywhere_proof_w280_generate_proof(request: Request):
    """Generate everywhere proof"""
    data = await request.json()
    item = service.generate_proof(data)
    return item

@router.get("/api/everywhere-proof/report")
async def api_everywhere_proof_w280_proof_report(limit: int = 100):
    """Get everywhere proof report"""
    items = service.proof_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/everywhere-proof/{proof_id}")
async def api_everywhere_proof_w280_get_proof(proof_id: str):
    """Get proof details"""
    item = service.get_proof(proof_id)
    if not item:
        raise HTTPException(status_code=404, detail="everywhere_proof not found")
    return item

@router.post("/api/everywhere-proof/{proof_id}/seal")
async def api_everywhere_proof_w280_seal_proof(proof_id: str, request: Request):
    """Seal everywhere proof"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.seal_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="everywhere_proof not found")
    return item

@router.post("/api/everywhere-proof/{proof_id}/verify")
async def api_everywhere_proof_w280_verify_proof(proof_id: str, request: Request):
    """Verify proof integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="everywhere_proof not found")
    return item
