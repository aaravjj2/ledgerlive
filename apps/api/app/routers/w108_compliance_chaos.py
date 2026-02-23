"""Wave 108: Compliance Chaos Tests Router — Chaos tests: failed compliance exports must be deterministic and safe.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w108_compliance_chaos import service

router = APIRouter(tags=["Compliance Chaos Tests"])

@router.get("/api/compliance-chaos")
async def api_compliance_chaos_w108_list_chaos(limit: int = 100):
    """List chaos test results"""
    items = service.list_chaos(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/compliance-chaos", status_code=201)
async def api_compliance_chaos_w108_run_chaos(request: Request):
    """Run compliance chaos test"""
    data = await request.json()
    item = service.run_chaos(data)
    return item

@router.get("/api/compliance-chaos/report")
async def api_compliance_chaos_w108_chaos_report(limit: int = 100):
    """Get chaos test report"""
    items = service.chaos_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/compliance-chaos/{chaos_id}")
async def api_compliance_chaos_w108_get_chaos(chaos_id: str):
    """Get chaos test details"""
    item = service.get_chaos(chaos_id)
    if not item:
        raise HTTPException(status_code=404, detail="compliance_chaos not found")
    return item

@router.post("/api/compliance-chaos/{chaos_id}/verify")
async def api_compliance_chaos_w108_verify_safety(chaos_id: str, request: Request):
    """Verify data safety"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_safety(chaos_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="compliance_chaos not found")
    return item
