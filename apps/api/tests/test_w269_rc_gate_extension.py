"""Tests for Wave 269: RC Gate Extension v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w269_rc_gate_extension import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w269_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w269_create(client):
    r = await client.post("/api/rc-gate-extension", json={'court_pack_verified': True, 'replay_verified': True, 'telemetry_verified': True, 'drift_budget_passed': True, 'drift_actual': 1.0, 'drift_limit': 1.0, 'gate_checks': [], 'all_passed': True, 'failure_reasons': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "gate_ext_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w269_list(client):
    await client.post("/api/rc-gate-extension", json={'court_pack_verified': True, 'replay_verified': True, 'telemetry_verified': True, 'drift_budget_passed': True, 'drift_actual': 1.0, 'drift_limit': 1.0, 'gate_checks': [], 'all_passed': True, 'failure_reasons': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    await client.post("/api/rc-gate-extension", json={'court_pack_verified': True, 'replay_verified': True, 'telemetry_verified': True, 'drift_budget_passed': True, 'drift_actual': 1.0, 'drift_limit': 1.0, 'gate_checks': [], 'all_passed': True, 'failure_reasons': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    r = await client.get("/api/rc-gate-extension")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w269_get_by_id(client):
    r = await client.post("/api/rc-gate-extension", json={'court_pack_verified': True, 'replay_verified': True, 'telemetry_verified': True, 'drift_budget_passed': True, 'drift_actual': 1.0, 'drift_limit': 1.0, 'gate_checks': [], 'all_passed': True, 'failure_reasons': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["gate_ext_id"]
    r2 = await client.get(f"/api/rc-gate-extension/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["gate_ext_id"] == item_id

@pytest.mark.asyncio
async def test_w269_get_not_found(client):
    r = await client.get("/api/rc-gate-extension/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w269_evaluate_all(client):
    r = await client.post("/api/rc-gate-extension", json={'court_pack_verified': True, 'replay_verified': True, 'telemetry_verified': True, 'drift_budget_passed': True, 'drift_actual': 1.0, 'drift_limit': 1.0, 'gate_checks': [], 'all_passed': True, 'failure_reasons': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["gate_ext_id"]
    r2 = await client.post(f"/api/rc-gate-extension/{item_id}/evaluate", json={})
    assert r2.status_code == 200
    assert r2.json()["gate_ext_id"] == item_id

@pytest.mark.asyncio
async def test_w269_check_drift(client):
    r = await client.post("/api/rc-gate-extension", json={'court_pack_verified': True, 'replay_verified': True, 'telemetry_verified': True, 'drift_budget_passed': True, 'drift_actual': 1.0, 'drift_limit': 1.0, 'gate_checks': [], 'all_passed': True, 'failure_reasons': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["gate_ext_id"]
    r2 = await client.post(f"/api/rc-gate-extension/{item_id}/drift", json={})
    assert r2.status_code == 200
    assert r2.json()["gate_ext_id"] == item_id

@pytest.mark.asyncio
async def test_w269_evaluate_all_not_found(client):
    r = await client.post("/api/rc-gate-extension/nonexistent-id/evaluate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w269_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/rc-gate-extension", json={'court_pack_verified': True, 'replay_verified': True, 'telemetry_verified': True, 'drift_budget_passed': True, 'drift_actual': 1.0, 'drift_limit': 1.0, 'gate_checks': [], 'all_passed': True, 'failure_reasons': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "rc_gate_extension"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w269_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/rc-gate-extension", json={'court_pack_verified': True, 'replay_verified': True, 'telemetry_verified': True, 'drift_budget_passed': True, 'drift_actual': 1.0, 'drift_limit': 1.0, 'gate_checks': [], 'all_passed': True, 'failure_reasons': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/rc-gate-extension", json={'court_pack_verified': True, 'replay_verified': True, 'telemetry_verified': True, 'drift_budget_passed': True, 'drift_actual': 1.0, 'drift_limit': 1.0, 'gate_checks': [], 'all_passed': True, 'failure_reasons': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "gate_ext_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w269_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/rc-gate-extension", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w269_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/rc-gate-extension", json={'court_pack_verified': True, 'replay_verified': True, 'telemetry_verified': True, 'drift_budget_passed': True, 'drift_actual': 1.0, 'drift_limit': 1.0, 'gate_checks': [], 'all_passed': True, 'failure_reasons': [], 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["gate_ext_id"]
    r2 = await client.get("/api/rc-gate-extension")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/rc-gate-extension/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["gate_ext_id"] == item_id
