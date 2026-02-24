"""Wave 266: Narrative Export v2 Router — Human narrative cites dossiers, evidence, and policy events. Stable formatting and ordering with deterministic content generation.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w266_narrative_export_v2 import service

router = APIRouter(tags=["Narrative Export v2"])

@router.get("/api/narrative-export-v2")
async def api_narrative_export_v2_w266_list_narratives(limit: int = 100):
    """List narrative exports"""
    items = service.list_narratives(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/narrative-export-v2", status_code=201)
async def api_narrative_export_v2_w266_create_narrative(request: Request):
    """Create narrative export"""
    data = await request.json()
    item = service.create_narrative(data)
    return item

@router.get("/api/narrative-export-v2/report")
async def api_narrative_export_v2_w266_narrative_report(limit: int = 100):
    """Get narrative export report"""
    items = service.narrative_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/narrative-export-v2/{narrative_id}")
async def api_narrative_export_v2_w266_get_narrative(narrative_id: str):
    """Get narrative details"""
    item = service.get_narrative(narrative_id)
    if not item:
        raise HTTPException(status_code=404, detail="narrative_export_v2 not found")
    return item

@router.post("/api/narrative-export-v2/{narrative_id}/citation")
async def api_narrative_export_v2_w266_add_citation(narrative_id: str, request: Request):
    """Add citation to narrative"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_citation(narrative_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="narrative_export_v2 not found")
    return item

@router.post("/api/narrative-export-v2/{narrative_id}/render")
async def api_narrative_export_v2_w266_render_narrative(narrative_id: str, request: Request):
    """Render narrative"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.render_narrative(narrative_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="narrative_export_v2 not found")
    return item
