"""Wave 30: Ultra-Hardening Router — System hardening: rate limits, CSP headers, input validation.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w30_hardening import service

router = APIRouter(tags=["Ultra-Hardening"])

@router.get("/api/hardening/rules")
async def api_list_rules(limit: int = 100):
    """List hardening rules"""
    items = service.list_rules(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/hardening/rules", status_code=201)
async def api_create_rule(request: Request):
    """Create a hardening rule"""
    data = await request.json()
    item = service.create_rule(data)
    return item

@router.post("/api/hardening/scan", status_code=201)
async def api_audit_scan(request: Request):
    """Run security audit scan"""
    data = await request.json()
    item = service.audit_scan(data)
    return item

@router.get("/api/hardening/rules/{rule_id}")
async def api_get_rule(rule_id: str):
    """Get rule details"""
    item = service.get_rule(rule_id)
    if not item:
        raise HTTPException(status_code=404, detail="hardening not found")
    return item

@router.post("/api/hardening/rules/{rule_id}/toggle")
async def api_toggle(rule_id: str, request: Request):
    """Toggle rule on/off"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.toggle(rule_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="hardening not found")
    return item
