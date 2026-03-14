"""Wave 310: Jira Cards in Race Control v1 Router — Link Jira issues to Race Control blockers with deep links and deterministic ordering.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w310_jira_cards_rc import service

router = APIRouter(tags=["Jira Cards in Race Control v1"])

@router.get("/api/jira-cards-rc")
async def api_jira_cards_rc_w310_list_cards(limit: int = 100):
    """List Jira cards in RC"""
    items = service.list_cards(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/jira-cards-rc", status_code=201)
async def api_jira_cards_rc_w310_create_card(request: Request):
    """Create Jira card link"""
    data = await request.json()
    item = service.create_card(data)
    return item

@router.get("/api/jira-cards-rc/report")
async def api_jira_cards_rc_w310_card_report(limit: int = 100):
    """Get Jira cards RC report"""
    items = service.card_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/jira-cards-rc/{card_id}")
async def api_jira_cards_rc_w310_get_card(card_id: str):
    """Get card details"""
    item = service.get_card(card_id)
    if not item:
        raise HTTPException(status_code=404, detail="jira_cards_rc not found")
    return item

@router.post("/api/jira-cards-rc/{card_id}/reorder")
async def api_jira_cards_rc_w310_reorder_cards(card_id: str, request: Request):
    """Reorder cards"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.reorder_cards(card_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="jira_cards_rc not found")
    return item

@router.post("/api/jira-cards-rc/{card_id}/resolve")
async def api_jira_cards_rc_w310_resolve_card(card_id: str, request: Request):
    """Mark card resolved"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.resolve_card(card_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="jira_cards_rc not found")
    return item
