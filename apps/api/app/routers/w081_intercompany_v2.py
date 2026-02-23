"""Wave 81: Intercompany 2.0 Router — Intercompany settlements, aging, disputes, and elimination workflows.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w081_intercompany_v2 import service

router = APIRouter(tags=["Intercompany 2.0"])

@router.get("/api/intercompany-v2")
async def api_intercompany_v2_w81_list_transactions(limit: int = 100):
    """List IC transactions"""
    items = service.list_transactions(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/intercompany-v2", status_code=201)
async def api_intercompany_v2_w81_create_transaction(request: Request):
    """Create IC transaction"""
    data = await request.json()
    item = service.create_transaction(data)
    return item

@router.get("/api/intercompany-v2/aging")
async def api_intercompany_v2_w81_aging_report(limit: int = 100):
    """Get IC aging report"""
    items = service.aging_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/intercompany-v2/{ic_id}")
async def api_intercompany_v2_w81_get_transaction(ic_id: str):
    """Get IC transaction details"""
    item = service.get_transaction(ic_id)
    if not item:
        raise HTTPException(status_code=404, detail="intercompany_v2 not found")
    return item

@router.post("/api/intercompany-v2/{ic_id}/dispute")
async def api_intercompany_v2_w81_dispute(ic_id: str, request: Request):
    """Dispute IC transaction"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.dispute(ic_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="intercompany_v2 not found")
    return item

@router.post("/api/intercompany-v2/{ic_id}/eliminate")
async def api_intercompany_v2_w81_eliminate(ic_id: str, request: Request):
    """Create elimination entry"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.eliminate(ic_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="intercompany_v2 not found")
    return item

@router.post("/api/intercompany-v2/{ic_id}/settle")
async def api_intercompany_v2_w81_settle(ic_id: str, request: Request):
    """Settle IC transaction"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.settle(ic_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="intercompany_v2 not found")
    return item
