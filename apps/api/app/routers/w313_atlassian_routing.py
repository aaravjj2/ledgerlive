"""Wave 313: Atlassian Routing Rules v1 Router — Which events create Jira issues or Confluence pages with frozen-time SLA escalation integration.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w313_atlassian_routing import service

router = APIRouter(tags=["Atlassian Routing Rules v1"])

@router.get("/api/atlassian-routing")
async def api_atlassian_routing_w313_list_rules(limit: int = 100):
    """List routing rules"""
    items = service.list_rules(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/atlassian-routing", status_code=201)
async def api_atlassian_routing_w313_create_rule(request: Request):
    """Create routing rule"""
    data = await request.json()
    item = service.create_rule(data)
    return item

@router.get("/api/atlassian-routing/report")
async def api_atlassian_routing_w313_rule_report(limit: int = 100):
    """Get routing rules report"""
    items = service.rule_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/atlassian-routing/{rule_id}")
async def api_atlassian_routing_w313_get_rule(rule_id: str):
    """Get rule details"""
    item = service.get_rule(rule_id)
    if not item:
        raise HTTPException(status_code=404, detail="atlassian_routing not found")
    return item

@router.post("/api/atlassian-routing/{rule_id}/test")
async def api_atlassian_routing_w313_test_rule(rule_id: str, request: Request):
    """Test rule with sample event"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.test_rule(rule_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="atlassian_routing not found")
    return item

@router.post("/api/atlassian-routing/{rule_id}/trigger")
async def api_atlassian_routing_w313_trigger_rule(rule_id: str, request: Request):
    """Trigger routing rule"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.trigger_rule(rule_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="atlassian_routing not found")
    return item
