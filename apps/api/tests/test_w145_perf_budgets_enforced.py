"""Tests for Wave 145: Performance Budgets Enforced

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w145_perf_budgets_enforced import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w145_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w145_create(client):
    r = await client.post("/api/perf-budgets-enforced", json={'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'within_budget': True, 'regression_detected': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert r.status_code == 201
    data = r.json()
    assert "budget_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w145_list(client):
    await client.post("/api/perf-budgets-enforced", json={'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'within_budget': True, 'regression_detected': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    await client.post("/api/perf-budgets-enforced", json={'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'within_budget': True, 'regression_detected': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    r = await client.get("/api/perf-budgets-enforced")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w145_get_by_id(client):
    r = await client.post("/api/perf-budgets-enforced", json={'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'within_budget': True, 'regression_detected': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.get(f"/api/perf-budgets-enforced/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w145_get_not_found(client):
    r = await client.get("/api/perf-budgets-enforced/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w145_measure(client):
    r = await client.post("/api/perf-budgets-enforced", json={'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'within_budget': True, 'regression_detected': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.post(f"/api/perf-budgets-enforced/{item_id}/measure", json={})
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w145_enforce(client):
    r = await client.post("/api/perf-budgets-enforced", json={'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'within_budget': True, 'regression_detected': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.post(f"/api/perf-budgets-enforced/{item_id}/enforce", json={})
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w145_measure_not_found(client):
    r = await client.post("/api/perf-budgets-enforced/nonexistent-id/measure", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w145_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/perf-budgets-enforced", json={'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'within_budget': True, 'regression_detected': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "perf_budgets_enforced"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w145_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/perf-budgets-enforced", json={'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'within_budget': True, 'regression_detected': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/perf-budgets-enforced", json={'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'within_budget': True, 'regression_detected': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "budget_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w145_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/perf-budgets-enforced", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w145_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/perf-budgets-enforced", json={'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'within_budget': True, 'regression_detected': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert r1.status_code == 201
    item_id = r1.json()["budget_id"]
    r2 = await client.get("/api/perf-budgets-enforced")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/perf-budgets-enforced/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["budget_id"] == item_id
