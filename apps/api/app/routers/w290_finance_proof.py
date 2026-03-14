"""Wave 290: Finance Proof Wave v1 Router — MCP E2E shows a real close run where tie-out variance triggers incident, approval resolves, exports verify. Determinism twice-run.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w290_finance_proof import service

router = APIRouter(tags=["Finance Proof Wave v1"])

@router.get("/api/finance-proof")
async def api_finance_proof_w290_list_proofs(limit: int = 100):
    """List finance proofs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/finance-proof", status_code=201)
async def api_finance_proof_w290_generate_proof(request: Request):
    """Generate finance proof"""
    data = await request.json()
    item = service.generate_proof(data)
    return item

@router.get("/api/finance-proof/report")
async def api_finance_proof_w290_proof_report(limit: int = 100):
    """Get finance proof report"""
    items = service.proof_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/finance-proof/{proof_id}")
async def api_finance_proof_w290_get_proof(proof_id: str):
    """Get proof details"""
    item = service.get_proof(proof_id)
    if not item:
        raise HTTPException(status_code=404, detail="finance_proof not found")
    return item

@router.post("/api/finance-proof/{proof_id}/seal")
async def api_finance_proof_w290_seal_proof(proof_id: str, request: Request):
    """Seal finance proof"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.seal_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="finance_proof not found")
    return item

@router.post("/api/finance-proof/{proof_id}/verify")
async def api_finance_proof_w290_verify_proof(proof_id: str, request: Request):
    """Verify proof integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="finance_proof not found")
    return item
