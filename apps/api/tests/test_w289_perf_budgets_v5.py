"""Tests for Wave 289: Performance Budgets v5

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w289_perf_budgets_v5 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w289_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w289_create(client):
    r = await client.post("/api/perf-budgets-v5", json={'fixture_scale': 'test-fixture_scale', 'target_flow': 'test-target_flow', 'budget_ms': 1, 'actual_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_tested': 1, 'throughput_ops': 1.0, 'memory_budget_mb': 1.0, 'memory_actual_mb': 1.0, 'deterministic': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert r.status_code == 201
    data = r.json()
    assert "budget_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w289_list(client):
    await client.post("/api/perf-budgets-v5", json={'fixture_scale': 'test-fixture_scale', 'target_flow': 'test-target_flow', 'budget_ms': 1, 'actual_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_tested': 1, 'throughput_ops': 1.0, 'memory_budget_mb': 1.0, 'memory_actual_mb': 1.0, 'deterministic': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    await client.post("/api/perf-budgets-v5", json={'fixture_scale': 'test-fixture_scale', 'target_flow': 'test-target_flow', 'budget_ms': 1, 'actual_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_tested': 1, 'throughput_ops': 1.0, 'memory_budget_mb': 1.0, 'memory_actual_mb': 1.0, 'deterministic': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    r = await client.get("/api/perf-budgets-v5")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w289_get_by_id(client):
    r = await client.post("/api/perf-budgets-v5", json={'fixture_scale': 'test-fixture_scale', 'target_flow': 'test-target_flow', 'budget_ms': 1, 'actual_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_tested': 1, 'throughput_ops': 1.0, 'memory_budget_mb': 1.0, 'memory_actual_mb': 1.0, 'deterministic': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.get(f"/api/perf-budgets-v5/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w289_get_not_found(client):
    r = await client.get("/api/perf-budgets-v5/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w289_run_benchmark(client):
    r = await client.post("/api/perf-budgets-v5", json={'fixture_scale': 'test-fixture_scale', 'target_flow': 'test-target_flow', 'budget_ms': 1, 'actual_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_tested': 1, 'throughput_ops': 1.0, 'memory_budget_mb': 1.0, 'memory_actual_mb': 1.0, 'deterministic': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.post(f"/api/perf-budgets-v5/{item_id}/benchmark", json={})
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w289_check_pagination(client):
    r = await client.post("/api/perf-budgets-v5", json={'fixture_scale': 'test-fixture_scale', 'target_flow': 'test-target_flow', 'budget_ms': 1, 'actual_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_tested': 1, 'throughput_ops': 1.0, 'memory_budget_mb': 1.0, 'memory_actual_mb': 1.0, 'deterministic': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.post(f"/api/perf-budgets-v5/{item_id}/pagination", json={})
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w289_run_benchmark_not_found(client):
    r = await client.post("/api/perf-budgets-v5/nonexistent-id/benchmark", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w289_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/perf-budgets-v5", json={'fixture_scale': 'test-fixture_scale', 'target_flow': 'test-target_flow', 'budget_ms': 1, 'actual_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_tested': 1, 'throughput_ops': 1.0, 'memory_budget_mb': 1.0, 'memory_actual_mb': 1.0, 'deterministic': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "perf_budgets_v5"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w289_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/perf-budgets-v5", json={'fixture_scale': 'test-fixture_scale', 'target_flow': 'test-target_flow', 'budget_ms': 1, 'actual_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_tested': 1, 'throughput_ops': 1.0, 'memory_budget_mb': 1.0, 'memory_actual_mb': 1.0, 'deterministic': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/perf-budgets-v5", json={'fixture_scale': 'test-fixture_scale', 'target_flow': 'test-target_flow', 'budget_ms': 1, 'actual_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_tested': 1, 'throughput_ops': 1.0, 'memory_budget_mb': 1.0, 'memory_actual_mb': 1.0, 'deterministic': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "budget_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w289_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/perf-budgets-v5", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w289_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/perf-budgets-v5", json={'fixture_scale': 'test-fixture_scale', 'target_flow': 'test-target_flow', 'budget_ms': 1, 'actual_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_tested': 1, 'throughput_ops': 1.0, 'memory_budget_mb': 1.0, 'memory_actual_mb': 1.0, 'deterministic': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert r1.status_code == 201
    item_id = r1.json()["budget_id"]
    r2 = await client.get("/api/perf-budgets-v5")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/perf-budgets-v5/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["budget_id"] == item_id
