"""Tests for Wave 291: RC Gate v3

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w291_rc_gate_v3 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w291_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w291_create(client):
    r = await client.post("/api/rc-gate-v3", json={'rc_invariants': [], 'channel_checks': [], 'replay_checks': [], 'security_checks': [], 'ml_checks': [], 'export_checks': [], 'all_passed': True, 'failure_count': 1, 'failure_details': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "gate_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w291_list(client):
    await client.post("/api/rc-gate-v3", json={'rc_invariants': [], 'channel_checks': [], 'replay_checks': [], 'security_checks': [], 'ml_checks': [], 'export_checks': [], 'all_passed': True, 'failure_count': 1, 'failure_details': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    await client.post("/api/rc-gate-v3", json={'rc_invariants': [], 'channel_checks': [], 'replay_checks': [], 'security_checks': [], 'ml_checks': [], 'export_checks': [], 'all_passed': True, 'failure_count': 1, 'failure_details': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    r = await client.get("/api/rc-gate-v3")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w291_get_by_id(client):
    r = await client.post("/api/rc-gate-v3", json={'rc_invariants': [], 'channel_checks': [], 'replay_checks': [], 'security_checks': [], 'ml_checks': [], 'export_checks': [], 'all_passed': True, 'failure_count': 1, 'failure_details': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["gate_id"]
    r2 = await client.get(f"/api/rc-gate-v3/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["gate_id"] == item_id

@pytest.mark.asyncio
async def test_w291_get_not_found(client):
    r = await client.get("/api/rc-gate-v3/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w291_evaluate_all(client):
    r = await client.post("/api/rc-gate-v3", json={'rc_invariants': [], 'channel_checks': [], 'replay_checks': [], 'security_checks': [], 'ml_checks': [], 'export_checks': [], 'all_passed': True, 'failure_count': 1, 'failure_details': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["gate_id"]
    r2 = await client.post(f"/api/rc-gate-v3/{item_id}/evaluate", json={})
    assert r2.status_code == 200
    assert r2.json()["gate_id"] == item_id

@pytest.mark.asyncio
async def test_w291_check_channels(client):
    r = await client.post("/api/rc-gate-v3", json={'rc_invariants': [], 'channel_checks': [], 'replay_checks': [], 'security_checks': [], 'ml_checks': [], 'export_checks': [], 'all_passed': True, 'failure_count': 1, 'failure_details': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["gate_id"]
    r2 = await client.post(f"/api/rc-gate-v3/{item_id}/channels", json={})
    assert r2.status_code == 200
    assert r2.json()["gate_id"] == item_id

@pytest.mark.asyncio
async def test_w291_check_security(client):
    r = await client.post("/api/rc-gate-v3", json={'rc_invariants': [], 'channel_checks': [], 'replay_checks': [], 'security_checks': [], 'ml_checks': [], 'export_checks': [], 'all_passed': True, 'failure_count': 1, 'failure_details': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["gate_id"]
    r2 = await client.post(f"/api/rc-gate-v3/{item_id}/security", json={})
    assert r2.status_code == 200
    assert r2.json()["gate_id"] == item_id

@pytest.mark.asyncio
async def test_w291_evaluate_all_not_found(client):
    r = await client.post("/api/rc-gate-v3/nonexistent-id/evaluate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w291_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/rc-gate-v3", json={'rc_invariants': [], 'channel_checks': [], 'replay_checks': [], 'security_checks': [], 'ml_checks': [], 'export_checks': [], 'all_passed': True, 'failure_count': 1, 'failure_details': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "rc_gate_v3"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w291_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/rc-gate-v3", json={'rc_invariants': [], 'channel_checks': [], 'replay_checks': [], 'security_checks': [], 'ml_checks': [], 'export_checks': [], 'all_passed': True, 'failure_count': 1, 'failure_details': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/rc-gate-v3", json={'rc_invariants': [], 'channel_checks': [], 'replay_checks': [], 'security_checks': [], 'ml_checks': [], 'export_checks': [], 'all_passed': True, 'failure_count': 1, 'failure_details': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "gate_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w291_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/rc-gate-v3", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w291_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/rc-gate-v3", json={'rc_invariants': [], 'channel_checks': [], 'replay_checks': [], 'security_checks': [], 'ml_checks': [], 'export_checks': [], 'all_passed': True, 'failure_count': 1, 'failure_details': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["gate_id"]
    r2 = await client.get("/api/rc-gate-v3")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/rc-gate-v3/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["gate_id"] == item_id
