"""Tests for Wave 94: Mapping Template Marketplace

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w094_mapping_marketplace import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w094_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w094_create(client):
    r = await client.post("/api/mapping-marketplace", json={'name': 'test-name', 'mapping_type': 'test-mapping_type', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'fields_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "mapping_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w094_list(client):
    await client.post("/api/mapping-marketplace", json={'name': 'test-name', 'mapping_type': 'test-mapping_type', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'fields_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/mapping-marketplace", json={'name': 'test-name', 'mapping_type': 'test-mapping_type', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'fields_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/mapping-marketplace")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w094_get_by_id(client):
    r = await client.post("/api/mapping-marketplace", json={'name': 'test-name', 'mapping_type': 'test-mapping_type', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'fields_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["mapping_id"]
    r2 = await client.get(f"/api/mapping-marketplace/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["mapping_id"] == item_id

@pytest.mark.asyncio
async def test_w094_get_not_found(client):
    r = await client.get("/api/mapping-marketplace/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w094_import_mapping(client):
    r = await client.post("/api/mapping-marketplace", json={'name': 'test-name', 'mapping_type': 'test-mapping_type', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'fields_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["mapping_id"]
    r2 = await client.post(f"/api/mapping-marketplace/{item_id}/import", json={})
    assert r2.status_code == 200
    assert r2.json()["mapping_id"] == item_id

@pytest.mark.asyncio
async def test_w094_verify_mapping(client):
    r = await client.post("/api/mapping-marketplace", json={'name': 'test-name', 'mapping_type': 'test-mapping_type', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'fields_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["mapping_id"]
    r2 = await client.post(f"/api/mapping-marketplace/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["mapping_id"] == item_id

@pytest.mark.asyncio
async def test_w094_import_mapping_not_found(client):
    r = await client.post("/api/mapping-marketplace/nonexistent-id/import", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w094_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/mapping-marketplace", json={'name': 'test-name', 'mapping_type': 'test-mapping_type', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'fields_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "mapping_marketplace"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w094_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/mapping-marketplace", json={'name': 'test-name', 'mapping_type': 'test-mapping_type', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'fields_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/mapping-marketplace", json={'name': 'test-name', 'mapping_type': 'test-mapping_type', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'fields_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "mapping_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w094_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/mapping-marketplace", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w094_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/mapping-marketplace", json={'name': 'test-name', 'mapping_type': 'test-mapping_type', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'fields_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["mapping_id"]
    r2 = await client.get("/api/mapping-marketplace")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/mapping-marketplace/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["mapping_id"] == item_id
