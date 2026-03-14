"""Wave 76: Reconciliation Explainability Router — Reason DAG for reconciliation decisions with evidence pointers.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w076_recon_explain import service

router = APIRouter(tags=["Reconciliation Explainability"])

@router.get("/api/recon-explain")
async def api_recon_explain_w76_list_explanations(limit: int = 100):
    """List recon explanations"""
    items = service.list_explanations(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/recon-explain", status_code=201)
async def api_recon_explain_w76_generate_explanation(request: Request):
    """Generate reconciliation explanation"""
    data = await request.json()
    item = service.generate_explanation(data)
    return item

@router.get("/api/recon-explain/export")
async def api_recon_explain_w76_export_explanations(limit: int = 100):
    """Export explanations report"""
    items = service.export_explanations(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/recon-explain/{explain_id}")
async def api_recon_explain_w76_get_explanation(explain_id: str):
    """Get explanation details"""
    item = service.get_explanation(explain_id)
    if not item:
        raise HTTPException(status_code=404, detail="recon_explain not found")
    return item

@router.post("/api/recon-explain/{explain_id}/evidence")
async def api_recon_explain_w76_add_evidence(explain_id: str, request: Request):
    """Add evidence pointer"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_evidence(explain_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="recon_explain not found")
    return item

@router.post("/api/recon-explain/{explain_id}/verify")
async def api_recon_explain_w76_verify_dag(explain_id: str, request: Request):
    """Verify reason DAG"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_dag(explain_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="recon_explain not found")
    return item
