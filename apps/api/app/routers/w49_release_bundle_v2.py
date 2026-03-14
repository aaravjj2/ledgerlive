"""Wave 49: Release Bundle 2.0 Router — Proof index, lineage verifier, signatures. Generate twice = identical hash.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w49_release_bundle_v2 import service

router = APIRouter(tags=["Release Bundle 2.0"])

@router.get("/api/releases-v2")
async def api_release_bundle_v2_w49_list_releases(limit: int = 100):
    """List release bundles v2"""
    items = service.list_releases(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/releases-v2", status_code=201)
async def api_release_bundle_v2_w49_create_release(request: Request):
    """Create a release bundle v2"""
    data = await request.json()
    item = service.create_release(data)
    return item

@router.get("/api/releases-v2/lineage")
async def api_release_bundle_v2_w49_lineage_report(limit: int = 100):
    """Get lineage report"""
    items = service.lineage_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/releases-v2/{release_id}")
async def api_release_bundle_v2_w49_get_release(release_id: str):
    """Get release details"""
    item = service.get_release(release_id)
    if not item:
        raise HTTPException(status_code=404, detail="release_bundle_v2 not found")
    return item

@router.post("/api/releases-v2/{release_id}/deploy")
async def api_release_bundle_v2_w49_deploy(release_id: str, request: Request):
    """Mark release as deployed"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.deploy(release_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="release_bundle_v2 not found")
    return item

@router.post("/api/releases-v2/{release_id}/sign")
async def api_release_bundle_v2_w49_sign_release(release_id: str, request: Request):
    """Sign a release"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.sign_release(release_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="release_bundle_v2 not found")
    return item

@router.post("/api/releases-v2/{release_id}/verify")
async def api_release_bundle_v2_w49_verify_release(release_id: str, request: Request):
    """Verify release integrity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.verify_release(release_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="release_bundle_v2 not found")
    return item
