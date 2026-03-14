"""Wave 84: Statement Notes & Footnotes Router — Statement notes and footnote evidence packs with audit trail.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w084_statement_notes import service

router = APIRouter(tags=["Statement Notes & Footnotes"])

@router.get("/api/statement-notes")
async def api_statement_notes_w84_list_notes(limit: int = 100):
    """List statement notes"""
    items = service.list_notes(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/statement-notes", status_code=201)
async def api_statement_notes_w84_create_note(request: Request):
    """Create statement note"""
    data = await request.json()
    item = service.create_note(data)
    return item

@router.get("/api/statement-notes/export")
async def api_statement_notes_w84_export_notes(limit: int = 100):
    """Export notes pack"""
    items = service.export_notes(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/statement-notes/{note_id}")
async def api_statement_notes_w84_get_note(note_id: str):
    """Get note details"""
    item = service.get_note(note_id)
    if not item:
        raise HTTPException(status_code=404, detail="statement_notes not found")
    return item

@router.post("/api/statement-notes/{note_id}/approve")
async def api_statement_notes_w84_approve_note(note_id: str, request: Request):
    """Approve note"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.approve_note(note_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="statement_notes not found")
    return item

@router.post("/api/statement-notes/{note_id}/evidence")
async def api_statement_notes_w84_attach_evidence(note_id: str, request: Request):
    """Attach evidence to note"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.attach_evidence(note_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="statement_notes not found")
    return item
