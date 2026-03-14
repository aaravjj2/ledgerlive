"""Wave 194: Audit Narrative Export v1 Router — Human-readable story with citations: what happened, why, evidence support. Citations link to evidence spans and dossier IDs. Included in binder.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w194_audit_narrative import service

router = APIRouter(tags=["Audit Narrative Export v1"])

@router.get("/api/audit-narratives")
async def api_audit_narrative_w194_list_narratives(limit: int = 100):
    """List audit narratives"""
    items = service.list_narratives(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/audit-narratives", status_code=201)
async def api_audit_narrative_w194_generate_narrative(request: Request):
    """Generate audit narrative"""
    data = await request.json()
    item = service.generate_narrative(data)
    return item

@router.get("/api/audit-narratives/report")
async def api_audit_narrative_w194_narrative_report(limit: int = 100):
    """Get narrative export report"""
    items = service.narrative_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/audit-narratives/{narrative_id}")
async def api_audit_narrative_w194_get_narrative(narrative_id: str):
    """Get narrative details"""
    item = service.get_narrative(narrative_id)
    if not item:
        raise HTTPException(status_code=404, detail="audit_narrative not found")
    return item

@router.post("/api/audit-narratives/{narrative_id}/citation")
async def api_audit_narrative_w194_add_citation(narrative_id: str, request: Request):
    """Add citation to narrative"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_citation(narrative_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="audit_narrative not found")
    return item

@router.post("/api/audit-narratives/{narrative_id}/export")
async def api_audit_narrative_w194_export_narrative(narrative_id: str, request: Request):
    """Export narrative for binder"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.export_narrative(narrative_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="audit_narrative not found")
    return item
