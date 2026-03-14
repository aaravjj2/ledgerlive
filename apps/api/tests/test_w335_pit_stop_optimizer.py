"""Tests for Wave 335: Pit Stop Optimizer v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w335_pit_stop_optimizer import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w335_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w335_create(client):
    r = await client.post("/api/pit-stop-optimizer", json={'current_blockers': [], 'available_steps': [], 'suggested_order': [], 'time_estimate_ms': 1, 'critical_path_impact': 1.0, 'optimization_score': 1.0, 'constraints': [], 'algorithm_version': 'test-algorithm_version', 'deterministic': True, 'status': 'test-status', 'optimized_at': 'test-optimized_at'})
    assert r.status_code == 201
    data = r.json()
    assert "optimizer_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w335_list(client):
    await client.post("/api/pit-stop-optimizer", json={'current_blockers': [], 'available_steps': [], 'suggested_order': [], 'time_estimate_ms': 1, 'critical_path_impact': 1.0, 'optimization_score': 1.0, 'constraints': [], 'algorithm_version': 'test-algorithm_version', 'deterministic': True, 'status': 'test-status', 'optimized_at': 'test-optimized_at'})
    await client.post("/api/pit-stop-optimizer", json={'current_blockers': [], 'available_steps': [], 'suggested_order': [], 'time_estimate_ms': 1, 'critical_path_impact': 1.0, 'optimization_score': 1.0, 'constraints': [], 'algorithm_version': 'test-algorithm_version', 'deterministic': True, 'status': 'test-status', 'optimized_at': 'test-optimized_at'})
    r = await client.get("/api/pit-stop-optimizer")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w335_get_by_id(client):
    r = await client.post("/api/pit-stop-optimizer", json={'current_blockers': [], 'available_steps': [], 'suggested_order': [], 'time_estimate_ms': 1, 'critical_path_impact': 1.0, 'optimization_score': 1.0, 'constraints': [], 'algorithm_version': 'test-algorithm_version', 'deterministic': True, 'status': 'test-status', 'optimized_at': 'test-optimized_at'})
    item_id = r.json()["optimizer_id"]
    r2 = await client.get(f"/api/pit-stop-optimizer/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["optimizer_id"] == item_id

@pytest.mark.asyncio
async def test_w335_get_not_found(client):
    r = await client.get("/api/pit-stop-optimizer/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w335_reoptimize(client):
    r = await client.post("/api/pit-stop-optimizer", json={'current_blockers': [], 'available_steps': [], 'suggested_order': [], 'time_estimate_ms': 1, 'critical_path_impact': 1.0, 'optimization_score': 1.0, 'constraints': [], 'algorithm_version': 'test-algorithm_version', 'deterministic': True, 'status': 'test-status', 'optimized_at': 'test-optimized_at'})
    item_id = r.json()["optimizer_id"]
    r2 = await client.post(f"/api/pit-stop-optimizer/{item_id}/reoptimize", json={})
    assert r2.status_code == 200
    assert r2.json()["optimizer_id"] == item_id

@pytest.mark.asyncio
async def test_w335_apply_suggestion(client):
    r = await client.post("/api/pit-stop-optimizer", json={'current_blockers': [], 'available_steps': [], 'suggested_order': [], 'time_estimate_ms': 1, 'critical_path_impact': 1.0, 'optimization_score': 1.0, 'constraints': [], 'algorithm_version': 'test-algorithm_version', 'deterministic': True, 'status': 'test-status', 'optimized_at': 'test-optimized_at'})
    item_id = r.json()["optimizer_id"]
    r2 = await client.post(f"/api/pit-stop-optimizer/{item_id}/apply", json={})
    assert r2.status_code == 200
    assert r2.json()["optimizer_id"] == item_id

@pytest.mark.asyncio
async def test_w335_reoptimize_not_found(client):
    r = await client.post("/api/pit-stop-optimizer/nonexistent-id/reoptimize", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w335_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/pit-stop-optimizer", json={'current_blockers': [], 'available_steps': [], 'suggested_order': [], 'time_estimate_ms': 1, 'critical_path_impact': 1.0, 'optimization_score': 1.0, 'constraints': [], 'algorithm_version': 'test-algorithm_version', 'deterministic': True, 'status': 'test-status', 'optimized_at': 'test-optimized_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "pit_stop_optimizer"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w335_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/pit-stop-optimizer", json={'current_blockers': [], 'available_steps': [], 'suggested_order': [], 'time_estimate_ms': 1, 'critical_path_impact': 1.0, 'optimization_score': 1.0, 'constraints': [], 'algorithm_version': 'test-algorithm_version', 'deterministic': True, 'status': 'test-status', 'optimized_at': 'test-optimized_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/pit-stop-optimizer", json={'current_blockers': [], 'available_steps': [], 'suggested_order': [], 'time_estimate_ms': 1, 'critical_path_impact': 1.0, 'optimization_score': 1.0, 'constraints': [], 'algorithm_version': 'test-algorithm_version', 'deterministic': True, 'status': 'test-status', 'optimized_at': 'test-optimized_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "optimizer_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w335_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/pit-stop-optimizer", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w335_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/pit-stop-optimizer", json={'current_blockers': [], 'available_steps': [], 'suggested_order': [], 'time_estimate_ms': 1, 'critical_path_impact': 1.0, 'optimization_score': 1.0, 'constraints': [], 'algorithm_version': 'test-algorithm_version', 'deterministic': True, 'status': 'test-status', 'optimized_at': 'test-optimized_at'})
    assert r1.status_code == 201
    item_id = r1.json()["optimizer_id"]
    r2 = await client.get("/api/pit-stop-optimizer")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/pit-stop-optimizer/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["optimizer_id"] == item_id
