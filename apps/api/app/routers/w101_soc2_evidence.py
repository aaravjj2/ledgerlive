"""Wave 101: SOC2 Evidence Automation 2.0 Router — Continuous SOC2 evidence collector with automated artifact gathering.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w101_soc2_evidence import service

router = APIRouter(tags=["SOC2 Evidence Automation 2.0"])

@router.get("/api/soc2-evidence")
async def api_soc2_evidence_w101_list_evidence(limit: int = 100):
    """List SOC2 evidence"""
    items = service.list_evidence(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/soc2-evidence", status_code=201)
async def api_soc2_evidence_w101_collect(request: Request):
    """Run evidence collection"""
    data = await request.json()
    item = service.collect(data)
    return item

@router.get("/api/soc2-evidence/coverage")
async def api_soc2_evidence_w101_coverage_report(limit: int = 100):
    """Get SOC2 coverage report"""
    items = service.coverage_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/soc2-evidence/export")
async def api_soc2_evidence_w101_export_evidence(limit: int = 100):
    """Export SOC2 evidence pack"""
    items = service.export_evidence(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/soc2-evidence/{evidence_id}")
async def api_soc2_evidence_w101_get_evidence(evidence_id: str):
    """Get evidence details"""
    item = service.get_evidence(evidence_id)
    if not item:
        raise HTTPException(status_code=404, detail="soc2_evidence not found")
    return item

@router.post("/api/soc2-evidence/{evidence_id}/verify")
async def api_soc2_evidence_w101_verify_evidence(evidence_id: str, request: Request):
    """Verify evidence validity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_evidence(evidence_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="soc2_evidence not found")
    return item
