"""Tests for Wave 257: Tamper Simulation v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w257_tamper_simulation import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w257_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w257_create(client):
    r = await client.post("/api/tamper-simulation", json={'target_entity': 'test-target_entity', 'tamper_type': 'test-tamper_type', 'injected_failure': {}, 'detection_method': 'test-detection_method', 'detected': True, 'detection_latency_ms': 1, 'recovery_steps': [], 'recovery_successful': True, 'explanation': 'test-explanation', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "simulation_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w257_list(client):
    await client.post("/api/tamper-simulation", json={'target_entity': 'test-target_entity', 'tamper_type': 'test-tamper_type', 'injected_failure': {}, 'detection_method': 'test-detection_method', 'detected': True, 'detection_latency_ms': 1, 'recovery_steps': [], 'recovery_successful': True, 'explanation': 'test-explanation', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    await client.post("/api/tamper-simulation", json={'target_entity': 'test-target_entity', 'tamper_type': 'test-tamper_type', 'injected_failure': {}, 'detection_method': 'test-detection_method', 'detected': True, 'detection_latency_ms': 1, 'recovery_steps': [], 'recovery_successful': True, 'explanation': 'test-explanation', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    r = await client.get("/api/tamper-simulation")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w257_get_by_id(client):
    r = await client.post("/api/tamper-simulation", json={'target_entity': 'test-target_entity', 'tamper_type': 'test-tamper_type', 'injected_failure': {}, 'detection_method': 'test-detection_method', 'detected': True, 'detection_latency_ms': 1, 'recovery_steps': [], 'recovery_successful': True, 'explanation': 'test-explanation', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    item_id = r.json()["simulation_id"]
    r2 = await client.get(f"/api/tamper-simulation/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["simulation_id"] == item_id

@pytest.mark.asyncio
async def test_w257_get_not_found(client):
    r = await client.get("/api/tamper-simulation/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w257_inject_failure(client):
    r = await client.post("/api/tamper-simulation", json={'target_entity': 'test-target_entity', 'tamper_type': 'test-tamper_type', 'injected_failure': {}, 'detection_method': 'test-detection_method', 'detected': True, 'detection_latency_ms': 1, 'recovery_steps': [], 'recovery_successful': True, 'explanation': 'test-explanation', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    item_id = r.json()["simulation_id"]
    r2 = await client.post(f"/api/tamper-simulation/{item_id}/inject", json={})
    assert r2.status_code == 200
    assert r2.json()["simulation_id"] == item_id

@pytest.mark.asyncio
async def test_w257_detect_tamper(client):
    r = await client.post("/api/tamper-simulation", json={'target_entity': 'test-target_entity', 'tamper_type': 'test-tamper_type', 'injected_failure': {}, 'detection_method': 'test-detection_method', 'detected': True, 'detection_latency_ms': 1, 'recovery_steps': [], 'recovery_successful': True, 'explanation': 'test-explanation', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    item_id = r.json()["simulation_id"]
    r2 = await client.post(f"/api/tamper-simulation/{item_id}/detect", json={})
    assert r2.status_code == 200
    assert r2.json()["simulation_id"] == item_id

@pytest.mark.asyncio
async def test_w257_recover(client):
    r = await client.post("/api/tamper-simulation", json={'target_entity': 'test-target_entity', 'tamper_type': 'test-tamper_type', 'injected_failure': {}, 'detection_method': 'test-detection_method', 'detected': True, 'detection_latency_ms': 1, 'recovery_steps': [], 'recovery_successful': True, 'explanation': 'test-explanation', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    item_id = r.json()["simulation_id"]
    r2 = await client.post(f"/api/tamper-simulation/{item_id}/recover", json={})
    assert r2.status_code == 200
    assert r2.json()["simulation_id"] == item_id

@pytest.mark.asyncio
async def test_w257_inject_failure_not_found(client):
    r = await client.post("/api/tamper-simulation/nonexistent-id/inject", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w257_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/tamper-simulation", json={'target_entity': 'test-target_entity', 'tamper_type': 'test-tamper_type', 'injected_failure': {}, 'detection_method': 'test-detection_method', 'detected': True, 'detection_latency_ms': 1, 'recovery_steps': [], 'recovery_successful': True, 'explanation': 'test-explanation', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "tamper_simulation"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w257_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/tamper-simulation", json={'target_entity': 'test-target_entity', 'tamper_type': 'test-tamper_type', 'injected_failure': {}, 'detection_method': 'test-detection_method', 'detected': True, 'detection_latency_ms': 1, 'recovery_steps': [], 'recovery_successful': True, 'explanation': 'test-explanation', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/tamper-simulation", json={'target_entity': 'test-target_entity', 'tamper_type': 'test-tamper_type', 'injected_failure': {}, 'detection_method': 'test-detection_method', 'detected': True, 'detection_latency_ms': 1, 'recovery_steps': [], 'recovery_successful': True, 'explanation': 'test-explanation', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "simulation_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w257_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/tamper-simulation", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w257_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/tamper-simulation", json={'target_entity': 'test-target_entity', 'tamper_type': 'test-tamper_type', 'injected_failure': {}, 'detection_method': 'test-detection_method', 'detected': True, 'detection_latency_ms': 1, 'recovery_steps': [], 'recovery_successful': True, 'explanation': 'test-explanation', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["simulation_id"]
    r2 = await client.get("/api/tamper-simulation")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/tamper-simulation/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["simulation_id"] == item_id
