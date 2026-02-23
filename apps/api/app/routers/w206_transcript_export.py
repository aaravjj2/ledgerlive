"""Wave 206: Transcript Tool Trace Exporter v1 Router — Session transcript pack: transcript.jsonl, tool_trace.jsonl, verifier_results.json, checksums, signature. Deterministic ordering and stable hashes.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w206_transcript_export import service

router = APIRouter(tags=["Transcript Tool Trace Exporter v1"])

@router.get("/api/transcript-export")
async def api_transcript_export_w206_list_exports(limit: int = 100):
    """List transcript exports"""
    items = service.list_exports(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/transcript-export", status_code=201)
async def api_transcript_export_w206_create_export(request: Request):
    """Create transcript export"""
    data = await request.json()
    item = service.create_export(data)
    return item

@router.get("/api/transcript-export/report")
async def api_transcript_export_w206_export_report(limit: int = 100):
    """Get transcript export report"""
    items = service.export_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/transcript-export/{export_id}")
async def api_transcript_export_w206_get_export(export_id: str):
    """Get export details"""
    item = service.get_export(export_id)
    if not item:
        raise HTTPException(status_code=404, detail="transcript_export not found")
    return item

@router.post("/api/transcript-export/{export_id}/download")
async def api_transcript_export_w206_download_pack(export_id: str, request: Request):
    """Download transcript pack"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.download_pack(export_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="transcript_export not found")
    return item

@router.post("/api/transcript-export/{export_id}/verify")
async def api_transcript_export_w206_verify_checksums(export_id: str, request: Request):
    """Verify checksums and signature"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_checksums(export_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="transcript_export not found")
    return item
