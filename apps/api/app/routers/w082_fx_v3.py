"""Wave 82: FX Translation 3.0 Router — CTA handling, rate source snapshots, deterministic multi-currency translation.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w082_fx_v3 import service

router = APIRouter(tags=["FX Translation 3.0"])

@router.get("/api/fx-v3/cta-report")
async def api_fx_v3_w82_cta_report(limit: int = 100):
    """Get CTA summary report"""
    items = service.cta_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/fx-v3/rate-history")
async def api_fx_v3_w82_rate_history(limit: int = 100):
    """Get rate history"""
    items = service.rate_history(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/fx-v3/translations")
async def api_fx_v3_w82_list_translations(limit: int = 100):
    """List FX translations"""
    items = service.list_translations(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/fx-v3/translations", status_code=201)
async def api_fx_v3_w82_translate(request: Request):
    """Create FX translation"""
    data = await request.json()
    item = service.translate(data)
    return item

@router.get("/api/fx-v3/translations/{translation_id}")
async def api_fx_v3_w82_get_translation(translation_id: str):
    """Get translation details"""
    item = service.get_translation(translation_id)
    if not item:
        raise HTTPException(status_code=404, detail="fx_v3 not found")
    return item

@router.post("/api/fx-v3/translations/{translation_id}/cta")
async def api_fx_v3_w82_compute_cta(translation_id: str, request: Request):
    """Compute CTA adjustment"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.compute_cta(translation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="fx_v3 not found")
    return item

@router.post("/api/fx-v3/translations/{translation_id}/snapshot")
async def api_fx_v3_w82_snapshot_rates(translation_id: str, request: Request):
    """Snapshot exchange rates"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.snapshot_rates(translation_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="fx_v3 not found")
    return item
