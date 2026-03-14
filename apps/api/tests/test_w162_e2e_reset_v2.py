"""Tests for Wave 162: E2E Reset Seed State v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w162_e2e_reset_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w162_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w162_create(client):
    r = await client.post("/api/ops/e2e-snapshots/reset", json={'snapshot_type': 'test-snapshot_type', 'entity_count': 1, 'close_period_present': True, 'canonical_ids': {}, 'state_hash': 'test-state_hash', 'seed_version': 'test-seed_version', 'status': 'test-status', 'executed_at': 'test-executed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "snapshot_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w162_list(client):
    await client.post("/api/ops/e2e-snapshots/reset", json={'snapshot_type': 'test-snapshot_type', 'entity_count': 1, 'close_period_present': True, 'canonical_ids': {}, 'state_hash': 'test-state_hash', 'seed_version': 'test-seed_version', 'status': 'test-status', 'executed_at': 'test-executed_at'})
    await client.post("/api/ops/e2e-snapshots/reset", json={'snapshot_type': 'test-snapshot_type', 'entity_count': 1, 'close_period_present': True, 'canonical_ids': {}, 'state_hash': 'test-state_hash', 'seed_version': 'test-seed_version', 'status': 'test-status', 'executed_at': 'test-executed_at'})
    r = await client.get("/api/ops/e2e-snapshots")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w162_get_by_id(client):
    r = await client.post("/api/ops/e2e-snapshots/reset", json={'snapshot_type': 'test-snapshot_type', 'entity_count': 1, 'close_period_present': True, 'canonical_ids': {}, 'state_hash': 'test-state_hash', 'seed_version': 'test-seed_version', 'status': 'test-status', 'executed_at': 'test-executed_at'})
    item_id = r.json()["snapshot_id"]
    r2 = await client.get(f"/api/ops/e2e-snapshots/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["snapshot_id"] == item_id

@pytest.mark.asyncio
async def test_w162_get_not_found(client):
    r = await client.get("/api/ops/e2e-snapshots/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w162_verify_state(client):
    r = await client.post("/api/ops/e2e-snapshots/reset", json={'snapshot_type': 'test-snapshot_type', 'entity_count': 1, 'close_period_present': True, 'canonical_ids': {}, 'state_hash': 'test-state_hash', 'seed_version': 'test-seed_version', 'status': 'test-status', 'executed_at': 'test-executed_at'})
    item_id = r.json()["snapshot_id"]
    r2 = await client.post(f"/api/ops/e2e-snapshots/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["snapshot_id"] == item_id

@pytest.mark.asyncio
async def test_w162_verify_state_not_found(client):
    r = await client.post("/api/ops/e2e-snapshots/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w162_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/ops/e2e-snapshots/reset", json={'snapshot_type': 'test-snapshot_type', 'entity_count': 1, 'close_period_present': True, 'canonical_ids': {}, 'state_hash': 'test-state_hash', 'seed_version': 'test-seed_version', 'status': 'test-status', 'executed_at': 'test-executed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "e2e_reset_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w162_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/ops/e2e-snapshots/reset", json={'snapshot_type': 'test-snapshot_type', 'entity_count': 1, 'close_period_present': True, 'canonical_ids': {}, 'state_hash': 'test-state_hash', 'seed_version': 'test-seed_version', 'status': 'test-status', 'executed_at': 'test-executed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/ops/e2e-snapshots/reset", json={'snapshot_type': 'test-snapshot_type', 'entity_count': 1, 'close_period_present': True, 'canonical_ids': {}, 'state_hash': 'test-state_hash', 'seed_version': 'test-seed_version', 'status': 'test-status', 'executed_at': 'test-executed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "snapshot_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w162_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/ops/e2e-snapshots/reset", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w162_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/ops/e2e-snapshots/reset", json={'snapshot_type': 'test-snapshot_type', 'entity_count': 1, 'close_period_present': True, 'canonical_ids': {}, 'state_hash': 'test-state_hash', 'seed_version': 'test-seed_version', 'status': 'test-status', 'executed_at': 'test-executed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["snapshot_id"]
    r2 = await client.get("/api/ops/e2e-snapshots")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/ops/e2e-snapshots/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["snapshot_id"] == item_id
