"""Wave 224: SLA Monitor v1 Router — Monitors service level agreements for close tasks. Tracks expected vs actual completion times, computes SLA breach risk, and triggers escalation alerts.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w224_sla_monitor import service

router = APIRouter(tags=["SLA Monitor v1"])

@router.get("/api/sla-monitor")
async def api_sla_monitor_w224_list_slas(limit: int = 100):
    """List SLA monitors"""
    items = service.list_slas(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/sla-monitor", status_code=201)
async def api_sla_monitor_w224_create_sla(request: Request):
    """Create SLA monitor"""
    data = await request.json()
    item = service.create_sla(data)
    return item

@router.get("/api/sla-monitor/report")
async def api_sla_monitor_w224_sla_report(limit: int = 100):
    """Get SLA monitor report"""
    items = service.sla_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/sla-monitor/{sla_id}")
async def api_sla_monitor_w224_get_sla(sla_id: str):
    """Get SLA details"""
    item = service.get_sla(sla_id)
    if not item:
        raise HTTPException(status_code=404, detail="sla_monitor not found")
    return item

@router.post("/api/sla-monitor/{sla_id}/breach")
async def api_sla_monitor_w224_check_breach(sla_id: str, request: Request):
    """Check for SLA breach"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.check_breach(sla_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="sla_monitor not found")
    return item

@router.post("/api/sla-monitor/{sla_id}/escalate")
async def api_sla_monitor_w224_escalate(sla_id: str, request: Request):
    """Trigger escalation alert"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.escalate(sla_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="sla_monitor not found")
    return item
