"""Tests for Wave 303: Blueprint Versioning v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w303_blueprint_versioning import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w303_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w303_create(client):
    r = await client.post("/api/blueprint-versioning", json={'blueprint_ref': 'test-blueprint_ref', 'version_num': 1, 'snapshot': {}, 'diff_from_prev': {}, 'is_immutable': True, 'rolled_back_from': 'test-rolled_back_from', 'change_audit': [], 'checksum': 'test-checksum', 'author': 'test-author', 'deterministic': True, 'status': 'test-status', 'versioned_at': 'test-versioned_at'})
    assert r.status_code == 201
    data = r.json()
    assert "version_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w303_list(client):
    await client.post("/api/blueprint-versioning", json={'blueprint_ref': 'test-blueprint_ref', 'version_num': 1, 'snapshot': {}, 'diff_from_prev': {}, 'is_immutable': True, 'rolled_back_from': 'test-rolled_back_from', 'change_audit': [], 'checksum': 'test-checksum', 'author': 'test-author', 'deterministic': True, 'status': 'test-status', 'versioned_at': 'test-versioned_at'})
    await client.post("/api/blueprint-versioning", json={'blueprint_ref': 'test-blueprint_ref', 'version_num': 1, 'snapshot': {}, 'diff_from_prev': {}, 'is_immutable': True, 'rolled_back_from': 'test-rolled_back_from', 'change_audit': [], 'checksum': 'test-checksum', 'author': 'test-author', 'deterministic': True, 'status': 'test-status', 'versioned_at': 'test-versioned_at'})
    r = await client.get("/api/blueprint-versioning")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w303_get_by_id(client):
    r = await client.post("/api/blueprint-versioning", json={'blueprint_ref': 'test-blueprint_ref', 'version_num': 1, 'snapshot': {}, 'diff_from_prev': {}, 'is_immutable': True, 'rolled_back_from': 'test-rolled_back_from', 'change_audit': [], 'checksum': 'test-checksum', 'author': 'test-author', 'deterministic': True, 'status': 'test-status', 'versioned_at': 'test-versioned_at'})
    item_id = r.json()["version_id"]
    r2 = await client.get(f"/api/blueprint-versioning/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["version_id"] == item_id

@pytest.mark.asyncio
async def test_w303_get_not_found(client):
    r = await client.get("/api/blueprint-versioning/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w303_diff_versions(client):
    r = await client.post("/api/blueprint-versioning", json={'blueprint_ref': 'test-blueprint_ref', 'version_num': 1, 'snapshot': {}, 'diff_from_prev': {}, 'is_immutable': True, 'rolled_back_from': 'test-rolled_back_from', 'change_audit': [], 'checksum': 'test-checksum', 'author': 'test-author', 'deterministic': True, 'status': 'test-status', 'versioned_at': 'test-versioned_at'})
    item_id = r.json()["version_id"]
    r2 = await client.post(f"/api/blueprint-versioning/{item_id}/diff", json={})
    assert r2.status_code == 200
    assert r2.json()["version_id"] == item_id

@pytest.mark.asyncio
async def test_w303_rollback_version(client):
    r = await client.post("/api/blueprint-versioning", json={'blueprint_ref': 'test-blueprint_ref', 'version_num': 1, 'snapshot': {}, 'diff_from_prev': {}, 'is_immutable': True, 'rolled_back_from': 'test-rolled_back_from', 'change_audit': [], 'checksum': 'test-checksum', 'author': 'test-author', 'deterministic': True, 'status': 'test-status', 'versioned_at': 'test-versioned_at'})
    item_id = r.json()["version_id"]
    r2 = await client.post(f"/api/blueprint-versioning/{item_id}/rollback", json={})
    assert r2.status_code == 200
    assert r2.json()["version_id"] == item_id

@pytest.mark.asyncio
async def test_w303_diff_versions_not_found(client):
    r = await client.post("/api/blueprint-versioning/nonexistent-id/diff", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w303_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/blueprint-versioning", json={'blueprint_ref': 'test-blueprint_ref', 'version_num': 1, 'snapshot': {}, 'diff_from_prev': {}, 'is_immutable': True, 'rolled_back_from': 'test-rolled_back_from', 'change_audit': [], 'checksum': 'test-checksum', 'author': 'test-author', 'deterministic': True, 'status': 'test-status', 'versioned_at': 'test-versioned_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "blueprint_versioning"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w303_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/blueprint-versioning", json={'blueprint_ref': 'test-blueprint_ref', 'version_num': 1, 'snapshot': {}, 'diff_from_prev': {}, 'is_immutable': True, 'rolled_back_from': 'test-rolled_back_from', 'change_audit': [], 'checksum': 'test-checksum', 'author': 'test-author', 'deterministic': True, 'status': 'test-status', 'versioned_at': 'test-versioned_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/blueprint-versioning", json={'blueprint_ref': 'test-blueprint_ref', 'version_num': 1, 'snapshot': {}, 'diff_from_prev': {}, 'is_immutable': True, 'rolled_back_from': 'test-rolled_back_from', 'change_audit': [], 'checksum': 'test-checksum', 'author': 'test-author', 'deterministic': True, 'status': 'test-status', 'versioned_at': 'test-versioned_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "version_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w303_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/blueprint-versioning", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w303_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/blueprint-versioning", json={'blueprint_ref': 'test-blueprint_ref', 'version_num': 1, 'snapshot': {}, 'diff_from_prev': {}, 'is_immutable': True, 'rolled_back_from': 'test-rolled_back_from', 'change_audit': [], 'checksum': 'test-checksum', 'author': 'test-author', 'deterministic': True, 'status': 'test-status', 'versioned_at': 'test-versioned_at'})
    assert r1.status_code == 201
    item_id = r1.json()["version_id"]
    r2 = await client.get("/api/blueprint-versioning")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/blueprint-versioning/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["version_id"] == item_id
