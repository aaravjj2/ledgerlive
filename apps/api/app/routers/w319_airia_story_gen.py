"""Wave 319: Airia Story Generator v1 Router — Auto-write a short agent description from blueprint and capabilities (deterministic, no LLM).

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w319_airia_story_gen import service

router = APIRouter(tags=["Airia Story Generator v1"])

@router.get("/api/airia-story-gen")
async def api_airia_story_gen_w319_list_stories(limit: int = 100):
    """List generated stories"""
    items = service.list_stories(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/airia-story-gen", status_code=201)
async def api_airia_story_gen_w319_generate_story(request: Request):
    """Generate agent story"""
    data = await request.json()
    item = service.generate_story(data)
    return item

@router.get("/api/airia-story-gen/report")
async def api_airia_story_gen_w319_story_report(limit: int = 100):
    """Get story generation report"""
    items = service.story_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/airia-story-gen/{story_id}")
async def api_airia_story_gen_w319_get_story(story_id: str):
    """Get story details"""
    item = service.get_story(story_id)
    if not item:
        raise HTTPException(status_code=404, detail="airia_story_gen not found")
    return item

@router.post("/api/airia-story-gen/{story_id}/preview")
async def api_airia_story_gen_w319_preview_story(story_id: str, request: Request):
    """Preview story rendering"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.preview_story(story_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="airia_story_gen not found")
    return item

@router.post("/api/airia-story-gen/{story_id}/regenerate")
async def api_airia_story_gen_w319_regenerate_story(story_id: str, request: Request):
    """Regenerate story"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.regenerate_story(story_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="airia_story_gen not found")
    return item
