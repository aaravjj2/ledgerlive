"""Tests for Wave 311: Confluence Adapter v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w311_confluence_adapter_v1 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w311_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w311_create(client):
    r = await client.post("/api/confluence-adapter", json={'page_title': 'test-page_title', 'content_body': 'test-content_body', 'telemetry_ref': 'test-telemetry_ref', 'court_pack_ref': 'test-court_pack_ref', 'template_used': 'test-template_used', 'space_key': 'test-space_key', 'parent_page_ref': 'test-parent_page_ref', 'version_num': 1, 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "page_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w311_list(client):
    await client.post("/api/confluence-adapter", json={'page_title': 'test-page_title', 'content_body': 'test-content_body', 'telemetry_ref': 'test-telemetry_ref', 'court_pack_ref': 'test-court_pack_ref', 'template_used': 'test-template_used', 'space_key': 'test-space_key', 'parent_page_ref': 'test-parent_page_ref', 'version_num': 1, 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/confluence-adapter", json={'page_title': 'test-page_title', 'content_body': 'test-content_body', 'telemetry_ref': 'test-telemetry_ref', 'court_pack_ref': 'test-court_pack_ref', 'template_used': 'test-template_used', 'space_key': 'test-space_key', 'parent_page_ref': 'test-parent_page_ref', 'version_num': 1, 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/confluence-adapter")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w311_get_by_id(client):
    r = await client.post("/api/confluence-adapter", json={'page_title': 'test-page_title', 'content_body': 'test-content_body', 'telemetry_ref': 'test-telemetry_ref', 'court_pack_ref': 'test-court_pack_ref', 'template_used': 'test-template_used', 'space_key': 'test-space_key', 'parent_page_ref': 'test-parent_page_ref', 'version_num': 1, 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["page_id"]
    r2 = await client.get(f"/api/confluence-adapter/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["page_id"] == item_id

@pytest.mark.asyncio
async def test_w311_get_not_found(client):
    r = await client.get("/api/confluence-adapter/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w311_update_content(client):
    r = await client.post("/api/confluence-adapter", json={'page_title': 'test-page_title', 'content_body': 'test-content_body', 'telemetry_ref': 'test-telemetry_ref', 'court_pack_ref': 'test-court_pack_ref', 'template_used': 'test-template_used', 'space_key': 'test-space_key', 'parent_page_ref': 'test-parent_page_ref', 'version_num': 1, 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["page_id"]
    r2 = await client.post(f"/api/confluence-adapter/{item_id}/update", json={})
    assert r2.status_code == 200
    assert r2.json()["page_id"] == item_id

@pytest.mark.asyncio
async def test_w311_render_preview(client):
    r = await client.post("/api/confluence-adapter", json={'page_title': 'test-page_title', 'content_body': 'test-content_body', 'telemetry_ref': 'test-telemetry_ref', 'court_pack_ref': 'test-court_pack_ref', 'template_used': 'test-template_used', 'space_key': 'test-space_key', 'parent_page_ref': 'test-parent_page_ref', 'version_num': 1, 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["page_id"]
    r2 = await client.post(f"/api/confluence-adapter/{item_id}/preview", json={})
    assert r2.status_code == 200
    assert r2.json()["page_id"] == item_id

@pytest.mark.asyncio
async def test_w311_update_content_not_found(client):
    r = await client.post("/api/confluence-adapter/nonexistent-id/update", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w311_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/confluence-adapter", json={'page_title': 'test-page_title', 'content_body': 'test-content_body', 'telemetry_ref': 'test-telemetry_ref', 'court_pack_ref': 'test-court_pack_ref', 'template_used': 'test-template_used', 'space_key': 'test-space_key', 'parent_page_ref': 'test-parent_page_ref', 'version_num': 1, 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "confluence_adapter_v1"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w311_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/confluence-adapter", json={'page_title': 'test-page_title', 'content_body': 'test-content_body', 'telemetry_ref': 'test-telemetry_ref', 'court_pack_ref': 'test-court_pack_ref', 'template_used': 'test-template_used', 'space_key': 'test-space_key', 'parent_page_ref': 'test-parent_page_ref', 'version_num': 1, 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/confluence-adapter", json={'page_title': 'test-page_title', 'content_body': 'test-content_body', 'telemetry_ref': 'test-telemetry_ref', 'court_pack_ref': 'test-court_pack_ref', 'template_used': 'test-template_used', 'space_key': 'test-space_key', 'parent_page_ref': 'test-parent_page_ref', 'version_num': 1, 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "page_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w311_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/confluence-adapter", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w311_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/confluence-adapter", json={'page_title': 'test-page_title', 'content_body': 'test-content_body', 'telemetry_ref': 'test-telemetry_ref', 'court_pack_ref': 'test-court_pack_ref', 'template_used': 'test-template_used', 'space_key': 'test-space_key', 'parent_page_ref': 'test-parent_page_ref', 'version_num': 1, 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["page_id"]
    r2 = await client.get("/api/confluence-adapter")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/confluence-adapter/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["page_id"] == item_id
