"""Tests for Wave 317: Airia Listing Bundle v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w317_airia_listing_bundle import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w317_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w317_create(client):
    r = await client.post("/api/airia-listing-bundle", json={'agent_name': 'test-agent_name', 'agent_description': 'test-agent_description', 'tags': [], 'screenshots_manifest': [], 'icon_ref': 'test-icon_ref', 'category': 'test-category', 'listing_version': 1, 'checksum': 'test-checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "bundle_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w317_list(client):
    await client.post("/api/airia-listing-bundle", json={'agent_name': 'test-agent_name', 'agent_description': 'test-agent_description', 'tags': [], 'screenshots_manifest': [], 'icon_ref': 'test-icon_ref', 'category': 'test-category', 'listing_version': 1, 'checksum': 'test-checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/airia-listing-bundle", json={'agent_name': 'test-agent_name', 'agent_description': 'test-agent_description', 'tags': [], 'screenshots_manifest': [], 'icon_ref': 'test-icon_ref', 'category': 'test-category', 'listing_version': 1, 'checksum': 'test-checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/airia-listing-bundle")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w317_get_by_id(client):
    r = await client.post("/api/airia-listing-bundle", json={'agent_name': 'test-agent_name', 'agent_description': 'test-agent_description', 'tags': [], 'screenshots_manifest': [], 'icon_ref': 'test-icon_ref', 'category': 'test-category', 'listing_version': 1, 'checksum': 'test-checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.get(f"/api/airia-listing-bundle/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w317_get_not_found(client):
    r = await client.get("/api/airia-listing-bundle/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w317_update_metadata(client):
    r = await client.post("/api/airia-listing-bundle", json={'agent_name': 'test-agent_name', 'agent_description': 'test-agent_description', 'tags': [], 'screenshots_manifest': [], 'icon_ref': 'test-icon_ref', 'category': 'test-category', 'listing_version': 1, 'checksum': 'test-checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.post(f"/api/airia-listing-bundle/{item_id}/metadata", json={})
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w317_generate_manifest(client):
    r = await client.post("/api/airia-listing-bundle", json={'agent_name': 'test-agent_name', 'agent_description': 'test-agent_description', 'tags': [], 'screenshots_manifest': [], 'icon_ref': 'test-icon_ref', 'category': 'test-category', 'listing_version': 1, 'checksum': 'test-checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.post(f"/api/airia-listing-bundle/{item_id}/manifest", json={})
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w317_update_metadata_not_found(client):
    r = await client.post("/api/airia-listing-bundle/nonexistent-id/metadata", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w317_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/airia-listing-bundle", json={'agent_name': 'test-agent_name', 'agent_description': 'test-agent_description', 'tags': [], 'screenshots_manifest': [], 'icon_ref': 'test-icon_ref', 'category': 'test-category', 'listing_version': 1, 'checksum': 'test-checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "airia_listing_bundle"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w317_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/airia-listing-bundle", json={'agent_name': 'test-agent_name', 'agent_description': 'test-agent_description', 'tags': [], 'screenshots_manifest': [], 'icon_ref': 'test-icon_ref', 'category': 'test-category', 'listing_version': 1, 'checksum': 'test-checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/airia-listing-bundle", json={'agent_name': 'test-agent_name', 'agent_description': 'test-agent_description', 'tags': [], 'screenshots_manifest': [], 'icon_ref': 'test-icon_ref', 'category': 'test-category', 'listing_version': 1, 'checksum': 'test-checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "bundle_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w317_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/airia-listing-bundle", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w317_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/airia-listing-bundle", json={'agent_name': 'test-agent_name', 'agent_description': 'test-agent_description', 'tags': [], 'screenshots_manifest': [], 'icon_ref': 'test-icon_ref', 'category': 'test-category', 'listing_version': 1, 'checksum': 'test-checksum', 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["bundle_id"]
    r2 = await client.get("/api/airia-listing-bundle")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/airia-listing-bundle/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["bundle_id"] == item_id
