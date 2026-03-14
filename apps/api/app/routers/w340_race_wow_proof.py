"""Wave 340: Race WOW Proof Wave v1 Router — Run Golden Scenario from Race Control, show optimizer, export readiness pack, verify, RC PASS, determinism twice-run.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w340_race_wow_proof import service

router = APIRouter(tags=["Race WOW Proof Wave v1"])

@router.get("/api/race-wow-proof")
async def api_race_wow_proof_w340_list_proofs(limit: int = 100):
    """List race WOW proofs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/race-wow-proof", status_code=201)
async def api_race_wow_proof_w340_generate_proof(request: Request):
    """Generate race WOW proof"""
    data = await request.json()
    item = service.generate_proof(data)
    return item

@router.get("/api/race-wow-proof/report")
async def api_race_wow_proof_w340_proof_report(limit: int = 100):
    """Get race WOW proof report"""
    items = service.proof_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/race-wow-proof/{proof_id}")
async def api_race_wow_proof_w340_get_proof(proof_id: str):
    """Get proof details"""
    item = service.get_proof(proof_id)
    if not item:
        raise HTTPException(status_code=404, detail="race_wow_proof not found")
    return item

@router.post("/api/race-wow-proof/{proof_id}/seal")
async def api_race_wow_proof_w340_seal_proof(proof_id: str, request: Request):
    """Seal race WOW proof"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.seal_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="race_wow_proof not found")
    return item

@router.post("/api/race-wow-proof/{proof_id}/verify")
async def api_race_wow_proof_w340_verify_wow(proof_id: str, request: Request):
    """Verify WOW proof"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_wow(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="race_wow_proof not found")
    return item
