"""Wave 201: Provider Parity Harness v1 Router — Runs canonical close session script through simulator, gemini shim, and airia shim. Outputs parity_report with tool plan, trace, binder, board pack, dossier hashes.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w201_parity_harness import service

router = APIRouter(tags=["Provider Parity Harness v1"])

@router.get("/api/parity-harness")
async def api_parity_harness_w201_list_parity(limit: int = 100):
    """List parity harness runs"""
    items = service.list_parity(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/parity-harness", status_code=201)
async def api_parity_harness_w201_run_parity(request: Request):
    """Run parity harness against provider shim"""
    data = await request.json()
    item = service.run_parity(data)
    return item

@router.get("/api/parity-harness/report")
async def api_parity_harness_w201_parity_report(limit: int = 100):
    """Get parity report"""
    items = service.parity_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/parity-harness/{parity_id}")
async def api_parity_harness_w201_get_parity(parity_id: str):
    """Get parity run details"""
    item = service.get_parity(parity_id)
    if not item:
        raise HTTPException(status_code=404, detail="parity_harness not found")
    return item

@router.post("/api/parity-harness/{parity_id}/compare")
async def api_parity_harness_w201_compare_providers(parity_id: str, request: Request):
    """Compare provider outputs"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.compare_providers(parity_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="parity_harness not found")
    return item

@router.post("/api/parity-harness/{parity_id}/verify")
async def api_parity_harness_w201_verify_hashes(parity_id: str, request: Request):
    """Verify all hashes match"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_hashes(parity_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="parity_harness not found")
    return item
