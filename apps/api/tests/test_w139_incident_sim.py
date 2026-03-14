"""Tests for Wave 139: Offline Incident Simulator

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w139_incident_sim import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w139_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w139_create(client):
    r = await client.post("/api/incident-sims", json={'scenario': 'test-scenario', 'severity': 'test-severity', 'impact_assessment': {}, 'resolution_steps': [], 'recovery_time_ms': 1.0, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "incident_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w139_list(client):
    await client.post("/api/incident-sims", json={'scenario': 'test-scenario', 'severity': 'test-severity', 'impact_assessment': {}, 'resolution_steps': [], 'recovery_time_ms': 1.0, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    await client.post("/api/incident-sims", json={'scenario': 'test-scenario', 'severity': 'test-severity', 'impact_assessment': {}, 'resolution_steps': [], 'recovery_time_ms': 1.0, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    r = await client.get("/api/incident-sims")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w139_get_by_id(client):
    r = await client.post("/api/incident-sims", json={'scenario': 'test-scenario', 'severity': 'test-severity', 'impact_assessment': {}, 'resolution_steps': [], 'recovery_time_ms': 1.0, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    item_id = r.json()["incident_id"]
    r2 = await client.get(f"/api/incident-sims/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["incident_id"] == item_id

@pytest.mark.asyncio
async def test_w139_get_not_found(client):
    r = await client.get("/api/incident-sims/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w139_assess_impact(client):
    r = await client.post("/api/incident-sims", json={'scenario': 'test-scenario', 'severity': 'test-severity', 'impact_assessment': {}, 'resolution_steps': [], 'recovery_time_ms': 1.0, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    item_id = r.json()["incident_id"]
    r2 = await client.post(f"/api/incident-sims/{item_id}/assess", json={})
    assert r2.status_code == 200
    assert r2.json()["incident_id"] == item_id

@pytest.mark.asyncio
async def test_w139_resolution_plan(client):
    r = await client.post("/api/incident-sims", json={'scenario': 'test-scenario', 'severity': 'test-severity', 'impact_assessment': {}, 'resolution_steps': [], 'recovery_time_ms': 1.0, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    item_id = r.json()["incident_id"]
    r2 = await client.post(f"/api/incident-sims/{item_id}/resolve", json={})
    assert r2.status_code == 200
    assert r2.json()["incident_id"] == item_id

@pytest.mark.asyncio
async def test_w139_assess_impact_not_found(client):
    r = await client.post("/api/incident-sims/nonexistent-id/assess", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w139_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/incident-sims", json={'scenario': 'test-scenario', 'severity': 'test-severity', 'impact_assessment': {}, 'resolution_steps': [], 'recovery_time_ms': 1.0, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "incident_sim"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w139_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/incident-sims", json={'scenario': 'test-scenario', 'severity': 'test-severity', 'impact_assessment': {}, 'resolution_steps': [], 'recovery_time_ms': 1.0, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/incident-sims", json={'scenario': 'test-scenario', 'severity': 'test-severity', 'impact_assessment': {}, 'resolution_steps': [], 'recovery_time_ms': 1.0, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "incident_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w139_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/incident-sims", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w139_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/incident-sims", json={'scenario': 'test-scenario', 'severity': 'test-severity', 'impact_assessment': {}, 'resolution_steps': [], 'recovery_time_ms': 1.0, 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["incident_id"]
    r2 = await client.get("/api/incident-sims")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/incident-sims/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["incident_id"] == item_id
