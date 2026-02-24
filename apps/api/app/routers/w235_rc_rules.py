"""Wave 235: RC Automation Rules v1 Router — Rule engine for Race Control automation. Rules trigger actions based on conditions: auto-escalate breached SLAs, auto-notify on blocker creation, auto-lock on checkpoint failure.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w235_rc_rules import service

router = APIRouter(tags=["RC Automation Rules v1"])

@router.get("/api/rc-rules")
async def api_rc_rules_w235_list_rules(limit: int = 100):
    """List automation rules"""
    items = service.list_rules(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/rc-rules", status_code=201)
async def api_rc_rules_w235_create_rule(request: Request):
    """Create automation rule"""
    data = await request.json()
    item = service.create_rule(data)
    return item

@router.get("/api/rc-rules/report")
async def api_rc_rules_w235_rules_report(limit: int = 100):
    """Get automation rules report"""
    items = service.rules_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/rc-rules/{rule_id}")
async def api_rc_rules_w235_get_rule(rule_id: str):
    """Get rule details"""
    item = service.get_rule(rule_id)
    if not item:
        raise HTTPException(status_code=404, detail="rc_rules not found")
    return item

@router.post("/api/rc-rules/{rule_id}/toggle")
async def api_rc_rules_w235_toggle_rule(rule_id: str, request: Request):
    """Enable/disable rule"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.toggle_rule(rule_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_rules not found")
    return item

@router.post("/api/rc-rules/{rule_id}/trigger")
async def api_rc_rules_w235_trigger_rule(rule_id: str, request: Request):
    """Trigger rule manually"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.trigger_rule(rule_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="rc_rules not found")
    return item
