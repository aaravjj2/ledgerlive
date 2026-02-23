"""Tests for Wave 117: Data Performance 25x

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w117_data_perf_25x import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w117_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w117_create(client):
    r = await client.post("/api/data-perf-25x", json={'fixture_scale': 1, 'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'record_count': 1, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert r.status_code == 201
    data = r.json()
    assert "perf_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w117_list(client):
    await client.post("/api/data-perf-25x", json={'fixture_scale': 1, 'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'record_count': 1, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    await client.post("/api/data-perf-25x", json={'fixture_scale': 1, 'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'record_count': 1, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    r = await client.get("/api/data-perf-25x")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w117_get_by_id(client):
    r = await client.post("/api/data-perf-25x", json={'fixture_scale': 1, 'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'record_count': 1, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["perf_id"]
    r2 = await client.get(f"/api/data-perf-25x/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["perf_id"] == item_id

@pytest.mark.asyncio
async def test_w117_get_not_found(client):
    r = await client.get("/api/data-perf-25x/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w117_set_budget(client):
    r = await client.post("/api/data-perf-25x", json={'fixture_scale': 1, 'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'record_count': 1, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["perf_id"]
    r2 = await client.post(f"/api/data-perf-25x/{item_id}/budget", json={})
    assert r2.status_code == 200
    assert r2.json()["perf_id"] == item_id

@pytest.mark.asyncio
async def test_w117_set_budget_not_found(client):
    r = await client.post("/api/data-perf-25x/nonexistent-id/budget", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w117_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/data-perf-25x", json={'fixture_scale': 1, 'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'record_count': 1, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "data_perf_25x"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w117_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/data-perf-25x", json={'fixture_scale': 1, 'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'record_count': 1, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/data-perf-25x", json={'fixture_scale': 1, 'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'record_count': 1, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "perf_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w117_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/data-perf-25x", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w117_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/data-perf-25x", json={'fixture_scale': 1, 'operation': 'test-operation', 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'record_count': 1, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert r1.status_code == 201
    item_id = r1.json()["perf_id"]
    r2 = await client.get("/api/data-perf-25x")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/data-perf-25x/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["perf_id"] == item_id
