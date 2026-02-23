"""Tests for Wave 150: Release Performance Bundle

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w150_release_perf_bundle import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w150_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w150_create(client):
    r = await client.post("/api/release-perf-bundles", json={'release_id': 'test-release_id', 'perf_evidence': [], 'budget_compliance': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "bundle_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w150_list(client):
    await client.post("/api/release-perf-bundles", json={'release_id': 'test-release_id', 'perf_evidence': [], 'budget_compliance': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/release-perf-bundles", json={'release_id': 'test-release_id', 'perf_evidence': [], 'budget_compliance': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/release-perf-bundles")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w150_get_by_id(client):
    r = await client.post("/api/release-perf-bundles", json={'release_id': 'test-release_id', 'perf_evidence': [], 'budget_compliance': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.get(f"/api/release-perf-bundles/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w150_get_not_found(client):
    r = await client.get("/api/release-perf-bundles/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w150_verify_bundle(client):
    r = await client.post("/api/release-perf-bundles", json={'release_id': 'test-release_id', 'perf_evidence': [], 'budget_compliance': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.post(f"/api/release-perf-bundles/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w150_verify_bundle_not_found(client):
    r = await client.post("/api/release-perf-bundles/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w150_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/release-perf-bundles", json={'release_id': 'test-release_id', 'perf_evidence': [], 'budget_compliance': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "release_perf_bundle"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w150_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/release-perf-bundles", json={'release_id': 'test-release_id', 'perf_evidence': [], 'budget_compliance': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/release-perf-bundles", json={'release_id': 'test-release_id', 'perf_evidence': [], 'budget_compliance': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "bundle_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w150_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/release-perf-bundles", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w150_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/release-perf-bundles", json={'release_id': 'test-release_id', 'perf_evidence': [], 'budget_compliance': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["bundle_id"]
    r2 = await client.get("/api/release-perf-bundles")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/release-perf-bundles/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["bundle_id"] == item_id
