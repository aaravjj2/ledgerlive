"""Tests for Wave 63: Route Sweep E2E

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w063_route_sweep import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w063_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w063_create(client):
    r = await client.post("/api/route-sweeps", json={'route_path': 'test-route_path', 'loaded': True, 'deep_refresh_ok': True, 'testid_present': True, 'status_code': 1, 'response_time_ms': 1.0, 'swept_at': 'test-swept_at'})
    assert r.status_code == 201
    data = r.json()
    assert "sweep_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w063_list(client):
    await client.post("/api/route-sweeps", json={'route_path': 'test-route_path', 'loaded': True, 'deep_refresh_ok': True, 'testid_present': True, 'status_code': 1, 'response_time_ms': 1.0, 'swept_at': 'test-swept_at'})
    await client.post("/api/route-sweeps", json={'route_path': 'test-route_path', 'loaded': True, 'deep_refresh_ok': True, 'testid_present': True, 'status_code': 1, 'response_time_ms': 1.0, 'swept_at': 'test-swept_at'})
    r = await client.get("/api/route-sweeps")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w063_get_by_id(client):
    r = await client.post("/api/route-sweeps", json={'route_path': 'test-route_path', 'loaded': True, 'deep_refresh_ok': True, 'testid_present': True, 'status_code': 1, 'response_time_ms': 1.0, 'swept_at': 'test-swept_at'})
    item_id = r.json()["sweep_id"]
    r2 = await client.get(f"/api/route-sweeps/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["sweep_id"] == item_id

@pytest.mark.asyncio
async def test_w063_get_not_found(client):
    r = await client.get("/api/route-sweeps/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w063_retry_failed(client):
    r = await client.post("/api/route-sweeps", json={'route_path': 'test-route_path', 'loaded': True, 'deep_refresh_ok': True, 'testid_present': True, 'status_code': 1, 'response_time_ms': 1.0, 'swept_at': 'test-swept_at'})
    item_id = r.json()["sweep_id"]
    r2 = await client.post(f"/api/route-sweeps/{item_id}/retry", json={})
    assert r2.status_code == 200
    assert r2.json()["sweep_id"] == item_id

@pytest.mark.asyncio
async def test_w063_retry_failed_not_found(client):
    r = await client.post("/api/route-sweeps/nonexistent-id/retry", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w063_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/route-sweeps", json={'route_path': 'test-route_path', 'loaded': True, 'deep_refresh_ok': True, 'testid_present': True, 'status_code': 1, 'response_time_ms': 1.0, 'swept_at': 'test-swept_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "route_sweep"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w063_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/route-sweeps", json={'route_path': 'test-route_path', 'loaded': True, 'deep_refresh_ok': True, 'testid_present': True, 'status_code': 1, 'response_time_ms': 1.0, 'swept_at': 'test-swept_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/route-sweeps", json={'route_path': 'test-route_path', 'loaded': True, 'deep_refresh_ok': True, 'testid_present': True, 'status_code': 1, 'response_time_ms': 1.0, 'swept_at': 'test-swept_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "sweep_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w063_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/route-sweeps", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w063_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/route-sweeps", json={'route_path': 'test-route_path', 'loaded': True, 'deep_refresh_ok': True, 'testid_present': True, 'status_code': 1, 'response_time_ms': 1.0, 'swept_at': 'test-swept_at'})
    assert r1.status_code == 201
    item_id = r1.json()["sweep_id"]
    r2 = await client.get("/api/route-sweeps")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/route-sweeps/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["sweep_id"] == item_id
