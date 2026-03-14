"""Tests for Wave 292: Route Coverage Gate v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w292_route_coverage_gate import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w292_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w292_create(client):
    r = await client.post("/api/route-coverage-gate", json={'total_routes': 1, 'covered_routes': 1, 'uncovered_routes': [], 'coverage_pct': 1.0, 'waived_routes': [], 'waiver_config_ref': 'test-waiver_config_ref', 'above_threshold': True, 'threshold_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "coverage_gate_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w292_list(client):
    await client.post("/api/route-coverage-gate", json={'total_routes': 1, 'covered_routes': 1, 'uncovered_routes': [], 'coverage_pct': 1.0, 'waived_routes': [], 'waiver_config_ref': 'test-waiver_config_ref', 'above_threshold': True, 'threshold_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    await client.post("/api/route-coverage-gate", json={'total_routes': 1, 'covered_routes': 1, 'uncovered_routes': [], 'coverage_pct': 1.0, 'waived_routes': [], 'waiver_config_ref': 'test-waiver_config_ref', 'above_threshold': True, 'threshold_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    r = await client.get("/api/route-coverage-gate")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w292_get_by_id(client):
    r = await client.post("/api/route-coverage-gate", json={'total_routes': 1, 'covered_routes': 1, 'uncovered_routes': [], 'coverage_pct': 1.0, 'waived_routes': [], 'waiver_config_ref': 'test-waiver_config_ref', 'above_threshold': True, 'threshold_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["coverage_gate_id"]
    r2 = await client.get(f"/api/route-coverage-gate/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["coverage_gate_id"] == item_id

@pytest.mark.asyncio
async def test_w292_get_not_found(client):
    r = await client.get("/api/route-coverage-gate/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w292_measure_coverage(client):
    r = await client.post("/api/route-coverage-gate", json={'total_routes': 1, 'covered_routes': 1, 'uncovered_routes': [], 'coverage_pct': 1.0, 'waived_routes': [], 'waiver_config_ref': 'test-waiver_config_ref', 'above_threshold': True, 'threshold_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["coverage_gate_id"]
    r2 = await client.post(f"/api/route-coverage-gate/{item_id}/measure", json={})
    assert r2.status_code == 200
    assert r2.json()["coverage_gate_id"] == item_id

@pytest.mark.asyncio
async def test_w292_add_waiver(client):
    r = await client.post("/api/route-coverage-gate", json={'total_routes': 1, 'covered_routes': 1, 'uncovered_routes': [], 'coverage_pct': 1.0, 'waived_routes': [], 'waiver_config_ref': 'test-waiver_config_ref', 'above_threshold': True, 'threshold_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["coverage_gate_id"]
    r2 = await client.post(f"/api/route-coverage-gate/{item_id}/waiver", json={})
    assert r2.status_code == 200
    assert r2.json()["coverage_gate_id"] == item_id

@pytest.mark.asyncio
async def test_w292_measure_coverage_not_found(client):
    r = await client.post("/api/route-coverage-gate/nonexistent-id/measure", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w292_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/route-coverage-gate", json={'total_routes': 1, 'covered_routes': 1, 'uncovered_routes': [], 'coverage_pct': 1.0, 'waived_routes': [], 'waiver_config_ref': 'test-waiver_config_ref', 'above_threshold': True, 'threshold_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "route_coverage_gate"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w292_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/route-coverage-gate", json={'total_routes': 1, 'covered_routes': 1, 'uncovered_routes': [], 'coverage_pct': 1.0, 'waived_routes': [], 'waiver_config_ref': 'test-waiver_config_ref', 'above_threshold': True, 'threshold_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/route-coverage-gate", json={'total_routes': 1, 'covered_routes': 1, 'uncovered_routes': [], 'coverage_pct': 1.0, 'waived_routes': [], 'waiver_config_ref': 'test-waiver_config_ref', 'above_threshold': True, 'threshold_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "coverage_gate_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w292_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/route-coverage-gate", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w292_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/route-coverage-gate", json={'total_routes': 1, 'covered_routes': 1, 'uncovered_routes': [], 'coverage_pct': 1.0, 'waived_routes': [], 'waiver_config_ref': 'test-waiver_config_ref', 'above_threshold': True, 'threshold_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["coverage_gate_id"]
    r2 = await client.get("/api/route-coverage-gate")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/route-coverage-gate/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["coverage_gate_id"] == item_id
