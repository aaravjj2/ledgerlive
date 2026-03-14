"""Tests for Wave 132: Mutation Testing Budget

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w132_mutation_budget import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w132_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w132_create(client):
    r = await client.post("/api/mutation-budgets", json={'module_name': 'test-module_name', 'mutations_total': 1, 'mutations_killed': 1, 'kill_rate_pct': 1.0, 'budget_pct': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert r.status_code == 201
    data = r.json()
    assert "budget_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w132_list(client):
    await client.post("/api/mutation-budgets", json={'module_name': 'test-module_name', 'mutations_total': 1, 'mutations_killed': 1, 'kill_rate_pct': 1.0, 'budget_pct': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    await client.post("/api/mutation-budgets", json={'module_name': 'test-module_name', 'mutations_total': 1, 'mutations_killed': 1, 'kill_rate_pct': 1.0, 'budget_pct': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    r = await client.get("/api/mutation-budgets")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w132_get_by_id(client):
    r = await client.post("/api/mutation-budgets", json={'module_name': 'test-module_name', 'mutations_total': 1, 'mutations_killed': 1, 'kill_rate_pct': 1.0, 'budget_pct': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.get(f"/api/mutation-budgets/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w132_get_not_found(client):
    r = await client.get("/api/mutation-budgets/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w132_measure(client):
    r = await client.post("/api/mutation-budgets", json={'module_name': 'test-module_name', 'mutations_total': 1, 'mutations_killed': 1, 'kill_rate_pct': 1.0, 'budget_pct': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.post(f"/api/mutation-budgets/{item_id}/measure", json={})
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w132_measure_not_found(client):
    r = await client.post("/api/mutation-budgets/nonexistent-id/measure", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w132_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/mutation-budgets", json={'module_name': 'test-module_name', 'mutations_total': 1, 'mutations_killed': 1, 'kill_rate_pct': 1.0, 'budget_pct': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "mutation_budget"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w132_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/mutation-budgets", json={'module_name': 'test-module_name', 'mutations_total': 1, 'mutations_killed': 1, 'kill_rate_pct': 1.0, 'budget_pct': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/mutation-budgets", json={'module_name': 'test-module_name', 'mutations_total': 1, 'mutations_killed': 1, 'kill_rate_pct': 1.0, 'budget_pct': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "budget_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w132_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/mutation-budgets", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w132_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/mutation-budgets", json={'module_name': 'test-module_name', 'mutations_total': 1, 'mutations_killed': 1, 'kill_rate_pct': 1.0, 'budget_pct': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert r1.status_code == 201
    item_id = r1.json()["budget_id"]
    r2 = await client.get("/api/mutation-budgets")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/mutation-budgets/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["budget_id"] == item_id
