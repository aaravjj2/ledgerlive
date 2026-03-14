"""Tests for Wave 112: Lineage Manifest 2.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w112_lineage_manifest import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w112_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w112_create(client):
    r = await client.post("/api/lineage-manifests", json={'export_id': 'test-export_id', 'source_hashes': [], 'transform_chain': [], 'output_hash': 'test-output_hash', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "manifest_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w112_list(client):
    await client.post("/api/lineage-manifests", json={'export_id': 'test-export_id', 'source_hashes': [], 'transform_chain': [], 'output_hash': 'test-output_hash', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/lineage-manifests", json={'export_id': 'test-export_id', 'source_hashes': [], 'transform_chain': [], 'output_hash': 'test-output_hash', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/lineage-manifests")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w112_get_by_id(client):
    r = await client.post("/api/lineage-manifests", json={'export_id': 'test-export_id', 'source_hashes': [], 'transform_chain': [], 'output_hash': 'test-output_hash', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["manifest_id"]
    r2 = await client.get(f"/api/lineage-manifests/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["manifest_id"] == item_id

@pytest.mark.asyncio
async def test_w112_get_not_found(client):
    r = await client.get("/api/lineage-manifests/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w112_verify_manifest(client):
    r = await client.post("/api/lineage-manifests", json={'export_id': 'test-export_id', 'source_hashes': [], 'transform_chain': [], 'output_hash': 'test-output_hash', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["manifest_id"]
    r2 = await client.post(f"/api/lineage-manifests/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["manifest_id"] == item_id

@pytest.mark.asyncio
async def test_w112_verify_manifest_not_found(client):
    r = await client.post("/api/lineage-manifests/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w112_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/lineage-manifests", json={'export_id': 'test-export_id', 'source_hashes': [], 'transform_chain': [], 'output_hash': 'test-output_hash', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "lineage_manifest"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w112_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/lineage-manifests", json={'export_id': 'test-export_id', 'source_hashes': [], 'transform_chain': [], 'output_hash': 'test-output_hash', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/lineage-manifests", json={'export_id': 'test-export_id', 'source_hashes': [], 'transform_chain': [], 'output_hash': 'test-output_hash', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "manifest_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w112_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/lineage-manifests", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w112_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/lineage-manifests", json={'export_id': 'test-export_id', 'source_hashes': [], 'transform_chain': [], 'output_hash': 'test-output_hash', 'verified': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["manifest_id"]
    r2 = await client.get("/api/lineage-manifests")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/lineage-manifests/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["manifest_id"] == item_id
