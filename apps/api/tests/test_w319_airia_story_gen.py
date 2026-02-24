"""Tests for Wave 319: Airia Story Generator v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w319_airia_story_gen import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w319_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w319_create(client):
    r = await client.post("/api/airia-story-gen", json={'blueprint_ref': 'test-blueprint_ref', 'capabilities': [], 'generated_title': 'test-generated_title', 'generated_summary': 'test-generated_summary', 'generated_highlights': [], 'word_count': 1, 'template_used': 'test-template_used', 'content_checksum': 'test-content_checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "story_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w319_list(client):
    await client.post("/api/airia-story-gen", json={'blueprint_ref': 'test-blueprint_ref', 'capabilities': [], 'generated_title': 'test-generated_title', 'generated_summary': 'test-generated_summary', 'generated_highlights': [], 'word_count': 1, 'template_used': 'test-template_used', 'content_checksum': 'test-content_checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/airia-story-gen", json={'blueprint_ref': 'test-blueprint_ref', 'capabilities': [], 'generated_title': 'test-generated_title', 'generated_summary': 'test-generated_summary', 'generated_highlights': [], 'word_count': 1, 'template_used': 'test-template_used', 'content_checksum': 'test-content_checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/airia-story-gen")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w319_get_by_id(client):
    r = await client.post("/api/airia-story-gen", json={'blueprint_ref': 'test-blueprint_ref', 'capabilities': [], 'generated_title': 'test-generated_title', 'generated_summary': 'test-generated_summary', 'generated_highlights': [], 'word_count': 1, 'template_used': 'test-template_used', 'content_checksum': 'test-content_checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["story_id"]
    r2 = await client.get(f"/api/airia-story-gen/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["story_id"] == item_id

@pytest.mark.asyncio
async def test_w319_get_not_found(client):
    r = await client.get("/api/airia-story-gen/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w319_regenerate_story(client):
    r = await client.post("/api/airia-story-gen", json={'blueprint_ref': 'test-blueprint_ref', 'capabilities': [], 'generated_title': 'test-generated_title', 'generated_summary': 'test-generated_summary', 'generated_highlights': [], 'word_count': 1, 'template_used': 'test-template_used', 'content_checksum': 'test-content_checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["story_id"]
    r2 = await client.post(f"/api/airia-story-gen/{item_id}/regenerate", json={})
    assert r2.status_code == 200
    assert r2.json()["story_id"] == item_id

@pytest.mark.asyncio
async def test_w319_preview_story(client):
    r = await client.post("/api/airia-story-gen", json={'blueprint_ref': 'test-blueprint_ref', 'capabilities': [], 'generated_title': 'test-generated_title', 'generated_summary': 'test-generated_summary', 'generated_highlights': [], 'word_count': 1, 'template_used': 'test-template_used', 'content_checksum': 'test-content_checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["story_id"]
    r2 = await client.post(f"/api/airia-story-gen/{item_id}/preview", json={})
    assert r2.status_code == 200
    assert r2.json()["story_id"] == item_id

@pytest.mark.asyncio
async def test_w319_regenerate_story_not_found(client):
    r = await client.post("/api/airia-story-gen/nonexistent-id/regenerate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w319_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/airia-story-gen", json={'blueprint_ref': 'test-blueprint_ref', 'capabilities': [], 'generated_title': 'test-generated_title', 'generated_summary': 'test-generated_summary', 'generated_highlights': [], 'word_count': 1, 'template_used': 'test-template_used', 'content_checksum': 'test-content_checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "airia_story_gen"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w319_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/airia-story-gen", json={'blueprint_ref': 'test-blueprint_ref', 'capabilities': [], 'generated_title': 'test-generated_title', 'generated_summary': 'test-generated_summary', 'generated_highlights': [], 'word_count': 1, 'template_used': 'test-template_used', 'content_checksum': 'test-content_checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/airia-story-gen", json={'blueprint_ref': 'test-blueprint_ref', 'capabilities': [], 'generated_title': 'test-generated_title', 'generated_summary': 'test-generated_summary', 'generated_highlights': [], 'word_count': 1, 'template_used': 'test-template_used', 'content_checksum': 'test-content_checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "story_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w319_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/airia-story-gen", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w319_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/airia-story-gen", json={'blueprint_ref': 'test-blueprint_ref', 'capabilities': [], 'generated_title': 'test-generated_title', 'generated_summary': 'test-generated_summary', 'generated_highlights': [], 'word_count': 1, 'template_used': 'test-template_used', 'content_checksum': 'test-content_checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["story_id"]
    r2 = await client.get("/api/airia-story-gen")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/airia-story-gen/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["story_id"] == item_id
