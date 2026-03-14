"""Wave 271: Email Inbox v2 Router — Mock email inbox with threads, attachments, and approval replies. Deterministic ordering, parsing, and content rendering.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w271_email_inbox_v2 import service

router = APIRouter(tags=["Email Inbox v2"])

@router.get("/api/email-inbox-v2")
async def api_email_inbox_v2_w271_list_emails(limit: int = 100):
    """List emails"""
    items = service.list_emails(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/email-inbox-v2", status_code=201)
async def api_email_inbox_v2_w271_create_email(request: Request):
    """Create email"""
    data = await request.json()
    item = service.create_email(data)
    return item

@router.get("/api/email-inbox-v2/report")
async def api_email_inbox_v2_w271_email_report(limit: int = 100):
    """Get email inbox report"""
    items = service.email_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/email-inbox-v2/{email_id}")
async def api_email_inbox_v2_w271_get_email(email_id: str):
    """Get email details"""
    item = service.get_email(email_id)
    if not item:
        raise HTTPException(status_code=404, detail="email_inbox_v2 not found")
    return item

@router.post("/api/email-inbox-v2/{email_id}/parse")
async def api_email_inbox_v2_w271_parse_content(email_id: str, request: Request):
    """Parse email content"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.parse_content(email_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="email_inbox_v2 not found")
    return item

@router.post("/api/email-inbox-v2/{email_id}/read")
async def api_email_inbox_v2_w271_mark_read(email_id: str, request: Request):
    """Mark email as read"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.mark_read(email_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="email_inbox_v2 not found")
    return item

@router.post("/api/email-inbox-v2/{email_id}/reply")
async def api_email_inbox_v2_w271_reply_email(email_id: str, request: Request):
    """Reply to email"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reply_email(email_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="email_inbox_v2 not found")
    return item
