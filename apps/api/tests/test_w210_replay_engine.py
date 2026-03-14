"""Tests for Wave 210: Replay Engine v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w210_replay_engine import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w210_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w210_create(client):
    r = await client.post("/api/replay-engine", json={'close_period_id': 'test-close_period_id', 'artifact_id': 'test-artifact_id', 'replay_steps': [], 'current_step': 1, 'total_steps': 1, 'step_hashes': {}, 'binder_hash': 'test-binder_hash', 'dossier_hash': 'test-dossier_hash', 'replay_result': 'test-replay_result', 'failure_reason': 'test-failure_reason', 'status': 'test-status', 'replayed_at': 'test-replayed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "replay_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w210_list(client):
    await client.post("/api/replay-engine", json={'close_period_id': 'test-close_period_id', 'artifact_id': 'test-artifact_id', 'replay_steps': [], 'current_step': 1, 'total_steps': 1, 'step_hashes': {}, 'binder_hash': 'test-binder_hash', 'dossier_hash': 'test-dossier_hash', 'replay_result': 'test-replay_result', 'failure_reason': 'test-failure_reason', 'status': 'test-status', 'replayed_at': 'test-replayed_at'})
    await client.post("/api/replay-engine", json={'close_period_id': 'test-close_period_id', 'artifact_id': 'test-artifact_id', 'replay_steps': [], 'current_step': 1, 'total_steps': 1, 'step_hashes': {}, 'binder_hash': 'test-binder_hash', 'dossier_hash': 'test-dossier_hash', 'replay_result': 'test-replay_result', 'failure_reason': 'test-failure_reason', 'status': 'test-status', 'replayed_at': 'test-replayed_at'})
    r = await client.get("/api/replay-engine")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w210_get_by_id(client):
    r = await client.post("/api/replay-engine", json={'close_period_id': 'test-close_period_id', 'artifact_id': 'test-artifact_id', 'replay_steps': [], 'current_step': 1, 'total_steps': 1, 'step_hashes': {}, 'binder_hash': 'test-binder_hash', 'dossier_hash': 'test-dossier_hash', 'replay_result': 'test-replay_result', 'failure_reason': 'test-failure_reason', 'status': 'test-status', 'replayed_at': 'test-replayed_at'})
    item_id = r.json()["replay_id"]
    r2 = await client.get(f"/api/replay-engine/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["replay_id"] == item_id

@pytest.mark.asyncio
async def test_w210_get_not_found(client):
    r = await client.get("/api/replay-engine/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w210_advance_step(client):
    r = await client.post("/api/replay-engine", json={'close_period_id': 'test-close_period_id', 'artifact_id': 'test-artifact_id', 'replay_steps': [], 'current_step': 1, 'total_steps': 1, 'step_hashes': {}, 'binder_hash': 'test-binder_hash', 'dossier_hash': 'test-dossier_hash', 'replay_result': 'test-replay_result', 'failure_reason': 'test-failure_reason', 'status': 'test-status', 'replayed_at': 'test-replayed_at'})
    item_id = r.json()["replay_id"]
    r2 = await client.post(f"/api/replay-engine/{item_id}/advance", json={})
    assert r2.status_code == 200
    assert r2.json()["replay_id"] == item_id

@pytest.mark.asyncio
async def test_w210_verify_replay(client):
    r = await client.post("/api/replay-engine", json={'close_period_id': 'test-close_period_id', 'artifact_id': 'test-artifact_id', 'replay_steps': [], 'current_step': 1, 'total_steps': 1, 'step_hashes': {}, 'binder_hash': 'test-binder_hash', 'dossier_hash': 'test-dossier_hash', 'replay_result': 'test-replay_result', 'failure_reason': 'test-failure_reason', 'status': 'test-status', 'replayed_at': 'test-replayed_at'})
    item_id = r.json()["replay_id"]
    r2 = await client.post(f"/api/replay-engine/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["replay_id"] == item_id

@pytest.mark.asyncio
async def test_w210_advance_step_not_found(client):
    r = await client.post("/api/replay-engine/nonexistent-id/advance", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w210_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/replay-engine", json={'close_period_id': 'test-close_period_id', 'artifact_id': 'test-artifact_id', 'replay_steps': [], 'current_step': 1, 'total_steps': 1, 'step_hashes': {}, 'binder_hash': 'test-binder_hash', 'dossier_hash': 'test-dossier_hash', 'replay_result': 'test-replay_result', 'failure_reason': 'test-failure_reason', 'status': 'test-status', 'replayed_at': 'test-replayed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "replay_engine"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w210_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/replay-engine", json={'close_period_id': 'test-close_period_id', 'artifact_id': 'test-artifact_id', 'replay_steps': [], 'current_step': 1, 'total_steps': 1, 'step_hashes': {}, 'binder_hash': 'test-binder_hash', 'dossier_hash': 'test-dossier_hash', 'replay_result': 'test-replay_result', 'failure_reason': 'test-failure_reason', 'status': 'test-status', 'replayed_at': 'test-replayed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/replay-engine", json={'close_period_id': 'test-close_period_id', 'artifact_id': 'test-artifact_id', 'replay_steps': [], 'current_step': 1, 'total_steps': 1, 'step_hashes': {}, 'binder_hash': 'test-binder_hash', 'dossier_hash': 'test-dossier_hash', 'replay_result': 'test-replay_result', 'failure_reason': 'test-failure_reason', 'status': 'test-status', 'replayed_at': 'test-replayed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "replay_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w210_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/replay-engine", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w210_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/replay-engine", json={'close_period_id': 'test-close_period_id', 'artifact_id': 'test-artifact_id', 'replay_steps': [], 'current_step': 1, 'total_steps': 1, 'step_hashes': {}, 'binder_hash': 'test-binder_hash', 'dossier_hash': 'test-dossier_hash', 'replay_result': 'test-replay_result', 'failure_reason': 'test-failure_reason', 'status': 'test-status', 'replayed_at': 'test-replayed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["replay_id"]
    r2 = await client.get("/api/replay-engine")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/replay-engine/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["replay_id"] == item_id
