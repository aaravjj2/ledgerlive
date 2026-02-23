"""Wave 17: Chart of Accounts & JE Router — Chart of accounts management and journal entry creation.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w17_chart_of_accounts import service

router = APIRouter(tags=["Chart of Accounts & JE"])

@router.get("/api/coa/accounts")
async def api_list_accounts(limit: int = 100):
    """List accounts"""
    items = service.list_accounts(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/coa/accounts", status_code=201)
async def api_create_account(request: Request):
    """Create an account"""
    data = await request.json()
    item = service.create_account(data)
    return item

@router.post("/api/coa/journal-entries", status_code=201)
async def api_create_je(request: Request):
    """Create journal entry"""
    data = await request.json()
    item = service.create_je(data)
    return item

@router.get("/api/coa/journal-entries")
async def api_list_je(limit: int = 100):
    """List journal entries"""
    items = service.list_je(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/coa/accounts/{account_id}")
async def api_get_account(account_id: str):
    """Get account details"""
    item = service.get_account(account_id)
    if not item:
        raise HTTPException(status_code=404, detail="chart_of_accounts not found")
    return item
