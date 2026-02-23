"""Tests for Wave 57: Cost Allocation

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w57_cost_allocation import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w57_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w57_create(client):
    r = await client.post("/api/cost-allocations", json={'cost_center_id': 'test-cost_center_id', 'cost_center_name': 'test-cost_center_name', 'driver': 'test-driver', 'source_amount': 1.0, 'allocated_amount': 1.0, 'allocation_pct': 1.0, 'period_id': 'test-period_id', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "allocation_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w57_list(client):
    await client.post("/api/cost-allocations", json={'cost_center_id': 'test-cost_center_id', 'cost_center_name': 'test-cost_center_name', 'driver': 'test-driver', 'source_amount': 1.0, 'allocated_amount': 1.0, 'allocation_pct': 1.0, 'period_id': 'test-period_id', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/cost-allocations", json={'cost_center_id': 'test-cost_center_id', 'cost_center_name': 'test-cost_center_name', 'driver': 'test-driver', 'source_amount': 1.0, 'allocated_amount': 1.0, 'allocation_pct': 1.0, 'period_id': 'test-period_id', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/cost-allocations")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w57_get_by_id(client):
    r = await client.post("/api/cost-allocations", json={'cost_center_id': 'test-cost_center_id', 'cost_center_name': 'test-cost_center_name', 'driver': 'test-driver', 'source_amount': 1.0, 'allocated_amount': 1.0, 'allocation_pct': 1.0, 'period_id': 'test-period_id', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["allocation_id"]
    r2 = await client.get(f"/api/cost-allocations/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["allocation_id"] == item_id

@pytest.mark.asyncio
async def test_w57_get_not_found(client):
    r = await client.get("/api/cost-allocations/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w57_recalculate(client):
    r = await client.post("/api/cost-allocations", json={'cost_center_id': 'test-cost_center_id', 'cost_center_name': 'test-cost_center_name', 'driver': 'test-driver', 'source_amount': 1.0, 'allocated_amount': 1.0, 'allocation_pct': 1.0, 'period_id': 'test-period_id', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["allocation_id"]
    r2 = await client.post(f"/api/cost-allocations/{item_id}/recalculate", json={})
    assert r2.status_code == 200
    assert r2.json()["allocation_id"] == item_id

@pytest.mark.asyncio
async def test_w57_recalculate_not_found(client):
    r = await client.post("/api/cost-allocations/nonexistent-id/recalculate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w57_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/cost-allocations", json={'cost_center_id': 'test-cost_center_id', 'cost_center_name': 'test-cost_center_name', 'driver': 'test-driver', 'source_amount': 1.0, 'allocated_amount': 1.0, 'allocation_pct': 1.0, 'period_id': 'test-period_id', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "cost_allocation"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w57_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/cost-allocations", json={'cost_center_id': 'test-cost_center_id', 'cost_center_name': 'test-cost_center_name', 'driver': 'test-driver', 'source_amount': 1.0, 'allocated_amount': 1.0, 'allocation_pct': 1.0, 'period_id': 'test-period_id', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/cost-allocations", json={'cost_center_id': 'test-cost_center_id', 'cost_center_name': 'test-cost_center_name', 'driver': 'test-driver', 'source_amount': 1.0, 'allocated_amount': 1.0, 'allocation_pct': 1.0, 'period_id': 'test-period_id', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "allocation_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w57_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/cost-allocations", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w57_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/cost-allocations", json={'cost_center_id': 'test-cost_center_id', 'cost_center_name': 'test-cost_center_name', 'driver': 'test-driver', 'source_amount': 1.0, 'allocated_amount': 1.0, 'allocation_pct': 1.0, 'period_id': 'test-period_id', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["allocation_id"]
    r2 = await client.get("/api/cost-allocations")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/cost-allocations/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["allocation_id"] == item_id
