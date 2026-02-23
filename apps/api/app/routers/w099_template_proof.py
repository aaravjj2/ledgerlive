"""Wave 99: Template Proof Pack Router — Proof packs including template signatures and verify logs.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w099_template_proof import service

router = APIRouter(tags=["Template Proof Pack"])

@router.get("/api/template-proofs")
async def api_template_proof_w99_list_proofs(limit: int = 100):
    """List template proof packs"""
    items = service.list_proofs(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/template-proofs", status_code=201)
async def api_template_proof_w99_generate_proof(request: Request):
    """Generate template proof pack"""
    data = await request.json()
    item = service.generate_proof(data)
    return item

@router.get("/api/template-proofs/export")
async def api_template_proof_w99_export_proof(limit: int = 100):
    """Export template proof pack"""
    items = service.export_proof(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/template-proofs/{proof_id}")
async def api_template_proof_w99_get_proof(proof_id: str):
    """Get proof details"""
    item = service.get_proof(proof_id)
    if not item:
        raise HTTPException(status_code=404, detail="template_proof not found")
    return item

@router.post("/api/template-proofs/{proof_id}/verify")
async def api_template_proof_w99_verify_proof(proof_id: str, request: Request):
    """Verify proof pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_proof(proof_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="template_proof not found")
    return item
