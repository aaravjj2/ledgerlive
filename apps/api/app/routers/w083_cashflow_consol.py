"""Wave 83: Consolidated Cash Flow Router — Consolidated cash flow statement with tie-outs to source entity statements.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w083_cashflow_consol import service

router = APIRouter(tags=["Consolidated Cash Flow"])

@router.get("/api/cashflow-consol")
async def api_cashflow_consol_w83_list_statements(limit: int = 100):
    """List consolidated CF statements"""
    items = service.list_statements(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/cashflow-consol", status_code=201)
async def api_cashflow_consol_w83_generate(request: Request):
    """Generate consolidated CF statement"""
    data = await request.json()
    item = service.generate(data)
    return item

@router.get("/api/cashflow-consol/export")
async def api_cashflow_consol_w83_export_cf(limit: int = 100):
    """Export CF statement"""
    items = service.export_cf(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/cashflow-consol/{cf_id}")
async def api_cashflow_consol_w83_get_statement(cf_id: str):
    """Get CF statement details"""
    item = service.get_statement(cf_id)
    if not item:
        raise HTTPException(status_code=404, detail="cashflow_consol not found")
    return item

@router.post("/api/cashflow-consol/{cf_id}/drilldown")
async def api_cashflow_consol_w83_drill_down(cf_id: str, request: Request):
    """Drill down to source"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.drill_down(cf_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="cashflow_consol not found")
    return item

@router.post("/api/cashflow-consol/{cf_id}/tie-out")
async def api_cashflow_consol_w83_tie_out(cf_id: str, request: Request):
    """Run tie-out verification"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.tie_out(cf_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="cashflow_consol not found")
    return item
