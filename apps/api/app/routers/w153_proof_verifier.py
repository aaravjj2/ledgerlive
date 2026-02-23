"""Wave 153: Proof Pack Verifier Router — Verify all referenced proof packs exist and PASS.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w153_proof_verifier import service

router = APIRouter(tags=["Proof Pack Verifier"])

@router.get("/api/proof-verifiers")
async def api_proof_verifier_w153_list_verifiers(limit: int = 100):
    """List proof verifier runs"""
    items = service.list_verifiers(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/proof-verifiers", status_code=201)
async def api_proof_verifier_w153_verify_all(request: Request):
    """Verify all proof packs"""
    data = await request.json()
    item = service.verify_all(data)
    return item

@router.get("/api/proof-verifiers/report")
async def api_proof_verifier_w153_verifier_report(limit: int = 100):
    """Get verifier report"""
    items = service.verifier_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/proof-verifiers/{verifier_id}")
async def api_proof_verifier_w153_get_verifier(verifier_id: str):
    """Get verifier details"""
    item = service.get_verifier(verifier_id)
    if not item:
        raise HTTPException(status_code=404, detail="proof_verifier not found")
    return item

@router.post("/api/proof-verifiers/{verifier_id}/check")
async def api_proof_verifier_w153_check_proof(verifier_id: str, request: Request):
    """Check specific proof"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_proof(verifier_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="proof_verifier not found")
    return item
