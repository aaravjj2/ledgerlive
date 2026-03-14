"""Tests for Wave 314: Adapter Failure Simulation v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w314_adapter_failure_sim import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w314_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w314_create(client):
    r = await client.post("/api/adapter-failure-sim", json={'adapter_name': 'test-adapter_name', 'failure_type': 'test-failure_type', 'failure_injected': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'recovery_action': 'test-recovery_action', 'recovery_successful': True, 'audit_trail': [], 'deterministic': True, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "sim_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w314_list(client):
    await client.post("/api/adapter-failure-sim", json={'adapter_name': 'test-adapter_name', 'failure_type': 'test-failure_type', 'failure_injected': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'recovery_action': 'test-recovery_action', 'recovery_successful': True, 'audit_trail': [], 'deterministic': True, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    await client.post("/api/adapter-failure-sim", json={'adapter_name': 'test-adapter_name', 'failure_type': 'test-failure_type', 'failure_injected': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'recovery_action': 'test-recovery_action', 'recovery_successful': True, 'audit_trail': [], 'deterministic': True, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    r = await client.get("/api/adapter-failure-sim")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w314_get_by_id(client):
    r = await client.post("/api/adapter-failure-sim", json={'adapter_name': 'test-adapter_name', 'failure_type': 'test-failure_type', 'failure_injected': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'recovery_action': 'test-recovery_action', 'recovery_successful': True, 'audit_trail': [], 'deterministic': True, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    item_id = r.json()["sim_id"]
    r2 = await client.get(f"/api/adapter-failure-sim/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["sim_id"] == item_id

@pytest.mark.asyncio
async def test_w314_get_not_found(client):
    r = await client.get("/api/adapter-failure-sim/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w314_inject_failure(client):
    r = await client.post("/api/adapter-failure-sim", json={'adapter_name': 'test-adapter_name', 'failure_type': 'test-failure_type', 'failure_injected': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'recovery_action': 'test-recovery_action', 'recovery_successful': True, 'audit_trail': [], 'deterministic': True, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    item_id = r.json()["sim_id"]
    r2 = await client.post(f"/api/adapter-failure-sim/{item_id}/inject", json={})
    assert r2.status_code == 200
    assert r2.json()["sim_id"] == item_id

@pytest.mark.asyncio
async def test_w314_recover(client):
    r = await client.post("/api/adapter-failure-sim", json={'adapter_name': 'test-adapter_name', 'failure_type': 'test-failure_type', 'failure_injected': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'recovery_action': 'test-recovery_action', 'recovery_successful': True, 'audit_trail': [], 'deterministic': True, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    item_id = r.json()["sim_id"]
    r2 = await client.post(f"/api/adapter-failure-sim/{item_id}/recover", json={})
    assert r2.status_code == 200
    assert r2.json()["sim_id"] == item_id

@pytest.mark.asyncio
async def test_w314_inject_failure_not_found(client):
    r = await client.post("/api/adapter-failure-sim/nonexistent-id/inject", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w314_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/adapter-failure-sim", json={'adapter_name': 'test-adapter_name', 'failure_type': 'test-failure_type', 'failure_injected': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'recovery_action': 'test-recovery_action', 'recovery_successful': True, 'audit_trail': [], 'deterministic': True, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "adapter_failure_sim"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w314_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/adapter-failure-sim", json={'adapter_name': 'test-adapter_name', 'failure_type': 'test-failure_type', 'failure_injected': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'recovery_action': 'test-recovery_action', 'recovery_successful': True, 'audit_trail': [], 'deterministic': True, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/adapter-failure-sim", json={'adapter_name': 'test-adapter_name', 'failure_type': 'test-failure_type', 'failure_injected': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'recovery_action': 'test-recovery_action', 'recovery_successful': True, 'audit_trail': [], 'deterministic': True, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "sim_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w314_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/adapter-failure-sim", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w314_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/adapter-failure-sim", json={'adapter_name': 'test-adapter_name', 'failure_type': 'test-failure_type', 'failure_injected': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'recovery_action': 'test-recovery_action', 'recovery_successful': True, 'audit_trail': [], 'deterministic': True, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["sim_id"]
    r2 = await client.get("/api/adapter-failure-sim")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/adapter-failure-sim/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["sim_id"] == item_id
