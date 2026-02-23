"""Wave 6: Reconciliation Engine Router — Explainable scoring-based reconciliation of financial records.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w06_reconciliation import service

router = APIRouter(tags=["Reconciliation Engine"])

@router.get("/api/reconciliations")
async def api_list(limit: int = 100):
    """List reconciliation runs"""
    items = service.list(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/reconciliations", status_code=201)
async def api_run_recon(request: Request):
    """Start a reconciliation run"""
    data = await request.json()
    item = service.run_recon(data)
    return item

@router.get("/api/reconciliations/{recon_id}")
async def api_get(recon_id: str):
    """Get reconciliation details"""
    item = service.get(recon_id)
    if not item:
        raise HTTPException(status_code=404, detail="reconciliation not found")
    return item

@router.post("/api/reconciliations/{recon_id}/approve")
async def api_approve(recon_id: str, request: Request):
    """Approve a match"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve(recon_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="reconciliation not found")
    return item

@router.post("/api/reconciliations/{recon_id}/reject")
async def api_reject(recon_id: str, request: Request):
    """Reject a match"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reject(recon_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="reconciliation not found")
    return item
