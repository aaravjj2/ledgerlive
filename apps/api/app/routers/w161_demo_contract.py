"""Wave 161: DEMO Contract Router — Single authoritative APP_MODE switch with frozen time, seeded RNG, deterministic IDs, stable ordering, outbound network deny.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w161_demo_contract import service

router = APIRouter(tags=["DEMO Contract"])

@router.get("/api/ops/demo-contracts")
async def api_demo_contract_w161_list_contracts(limit: int = 100):
    """List DEMO contract checks"""
    items = service.list_contracts(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/ops/demo-contracts", status_code=201)
async def api_demo_contract_w161_check_contract(request: Request):
    """Check DEMO contract invariants"""
    data = await request.json()
    item = service.check_contract(data)
    return item

@router.get("/api/ops/demo-contracts/hash")
async def api_demo_contract_w161_demo_contract_hash(limit: int = 100):
    """Get deterministic invariants hash"""
    items = service.demo_contract_hash(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/ops/demo-contracts/report")
async def api_demo_contract_w161_demo_contract_report(limit: int = 100):
    """Get DEMO contract report"""
    items = service.demo_contract_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/ops/demo-contracts/{contract_id}")
async def api_demo_contract_w161_get_contract(contract_id: str):
    """Get contract details"""
    item = service.get_contract(contract_id)
    if not item:
        raise HTTPException(status_code=404, detail="demo_contract not found")
    return item

@router.post("/api/ops/demo-contracts/{contract_id}/verify")
async def api_demo_contract_w161_verify_invariants(contract_id: str, request: Request):
    """Verify invariants hold"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_invariants(contract_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="demo_contract not found")
    return item
