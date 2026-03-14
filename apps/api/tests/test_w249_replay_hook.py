"""Tests for Wave 249: Replay Hook v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w249_replay_hook import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w249_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w249_create(client):
    r = await client.post("/api/replay-hook", json={'execution_ref': 'test-execution_ref', 'snapshot_data': {}, 'artifact_refs': [], 'snapshot_hash': 'test-snapshot_hash', 'replay_available': True, 'replay_url': 'test-replay_url', 'rc_link': 'test-rc_link', 'reproduction_verified': True, 'snapshot_size_bytes': 1, 'deterministic': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    assert r.status_code == 201
    data = r.json()
    assert "hook_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w249_list(client):
    await client.post("/api/replay-hook", json={'execution_ref': 'test-execution_ref', 'snapshot_data': {}, 'artifact_refs': [], 'snapshot_hash': 'test-snapshot_hash', 'replay_available': True, 'replay_url': 'test-replay_url', 'rc_link': 'test-rc_link', 'reproduction_verified': True, 'snapshot_size_bytes': 1, 'deterministic': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    await client.post("/api/replay-hook", json={'execution_ref': 'test-execution_ref', 'snapshot_data': {}, 'artifact_refs': [], 'snapshot_hash': 'test-snapshot_hash', 'replay_available': True, 'replay_url': 'test-replay_url', 'rc_link': 'test-rc_link', 'reproduction_verified': True, 'snapshot_size_bytes': 1, 'deterministic': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    r = await client.get("/api/replay-hook")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w249_get_by_id(client):
    r = await client.post("/api/replay-hook", json={'execution_ref': 'test-execution_ref', 'snapshot_data': {}, 'artifact_refs': [], 'snapshot_hash': 'test-snapshot_hash', 'replay_available': True, 'replay_url': 'test-replay_url', 'rc_link': 'test-rc_link', 'reproduction_verified': True, 'snapshot_size_bytes': 1, 'deterministic': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    item_id = r.json()["hook_id"]
    r2 = await client.get(f"/api/replay-hook/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["hook_id"] == item_id

@pytest.mark.asyncio
async def test_w249_get_not_found(client):
    r = await client.get("/api/replay-hook/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w249_trigger_replay(client):
    r = await client.post("/api/replay-hook", json={'execution_ref': 'test-execution_ref', 'snapshot_data': {}, 'artifact_refs': [], 'snapshot_hash': 'test-snapshot_hash', 'replay_available': True, 'replay_url': 'test-replay_url', 'rc_link': 'test-rc_link', 'reproduction_verified': True, 'snapshot_size_bytes': 1, 'deterministic': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    item_id = r.json()["hook_id"]
    r2 = await client.post(f"/api/replay-hook/{item_id}/trigger", json={})
    assert r2.status_code == 200
    assert r2.json()["hook_id"] == item_id

@pytest.mark.asyncio
async def test_w249_verify_reproduction(client):
    r = await client.post("/api/replay-hook", json={'execution_ref': 'test-execution_ref', 'snapshot_data': {}, 'artifact_refs': [], 'snapshot_hash': 'test-snapshot_hash', 'replay_available': True, 'replay_url': 'test-replay_url', 'rc_link': 'test-rc_link', 'reproduction_verified': True, 'snapshot_size_bytes': 1, 'deterministic': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    item_id = r.json()["hook_id"]
    r2 = await client.post(f"/api/replay-hook/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["hook_id"] == item_id

@pytest.mark.asyncio
async def test_w249_trigger_replay_not_found(client):
    r = await client.post("/api/replay-hook/nonexistent-id/trigger", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w249_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/replay-hook", json={'execution_ref': 'test-execution_ref', 'snapshot_data': {}, 'artifact_refs': [], 'snapshot_hash': 'test-snapshot_hash', 'replay_available': True, 'replay_url': 'test-replay_url', 'rc_link': 'test-rc_link', 'reproduction_verified': True, 'snapshot_size_bytes': 1, 'deterministic': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "replay_hook"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w249_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/replay-hook", json={'execution_ref': 'test-execution_ref', 'snapshot_data': {}, 'artifact_refs': [], 'snapshot_hash': 'test-snapshot_hash', 'replay_available': True, 'replay_url': 'test-replay_url', 'rc_link': 'test-rc_link', 'reproduction_verified': True, 'snapshot_size_bytes': 1, 'deterministic': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/replay-hook", json={'execution_ref': 'test-execution_ref', 'snapshot_data': {}, 'artifact_refs': [], 'snapshot_hash': 'test-snapshot_hash', 'replay_available': True, 'replay_url': 'test-replay_url', 'rc_link': 'test-rc_link', 'reproduction_verified': True, 'snapshot_size_bytes': 1, 'deterministic': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "hook_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w249_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/replay-hook", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w249_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/replay-hook", json={'execution_ref': 'test-execution_ref', 'snapshot_data': {}, 'artifact_refs': [], 'snapshot_hash': 'test-snapshot_hash', 'replay_available': True, 'replay_url': 'test-replay_url', 'rc_link': 'test-rc_link', 'reproduction_verified': True, 'snapshot_size_bytes': 1, 'deterministic': True, 'status': 'test-status', 'captured_at': 'test-captured_at'})
    assert r1.status_code == 201
    item_id = r1.json()["hook_id"]
    r2 = await client.get("/api/replay-hook")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/replay-hook/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["hook_id"] == item_id
