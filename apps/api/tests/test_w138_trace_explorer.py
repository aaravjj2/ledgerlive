"""Tests for Wave 138: Trace Explorer

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w138_trace_explorer import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w138_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w138_create(client):
    r = await client.post("/api/trace-explorer", json={'span_name': 'test-span_name', 'service': 'test-service', 'duration_ms': 1.0, 'status_code': 1, 'parent_trace_id': 'test-parent_trace_id', 'metadata': {}, 'recorded_at': 'test-recorded_at'})
    assert r.status_code == 201
    data = r.json()
    assert "trace_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w138_list(client):
    await client.post("/api/trace-explorer", json={'span_name': 'test-span_name', 'service': 'test-service', 'duration_ms': 1.0, 'status_code': 1, 'parent_trace_id': 'test-parent_trace_id', 'metadata': {}, 'recorded_at': 'test-recorded_at'})
    await client.post("/api/trace-explorer", json={'span_name': 'test-span_name', 'service': 'test-service', 'duration_ms': 1.0, 'status_code': 1, 'parent_trace_id': 'test-parent_trace_id', 'metadata': {}, 'recorded_at': 'test-recorded_at'})
    r = await client.get("/api/trace-explorer")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w138_get_by_id(client):
    r = await client.post("/api/trace-explorer", json={'span_name': 'test-span_name', 'service': 'test-service', 'duration_ms': 1.0, 'status_code': 1, 'parent_trace_id': 'test-parent_trace_id', 'metadata': {}, 'recorded_at': 'test-recorded_at'})
    item_id = r.json()["trace_id"]
    r2 = await client.get(f"/api/trace-explorer/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["trace_id"] == item_id

@pytest.mark.asyncio
async def test_w138_get_not_found(client):
    r = await client.get("/api/trace-explorer/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w138_search_traces(client):
    r = await client.post("/api/trace-explorer", json={'span_name': 'test-span_name', 'service': 'test-service', 'duration_ms': 1.0, 'status_code': 1, 'parent_trace_id': 'test-parent_trace_id', 'metadata': {}, 'recorded_at': 'test-recorded_at'})
    item_id = r.json()["trace_id"]
    r2 = await client.post(f"/api/trace-explorer/{item_id}/search", json={})
    assert r2.status_code == 200
    assert r2.json()["trace_id"] == item_id

@pytest.mark.asyncio
async def test_w138_search_traces_not_found(client):
    r = await client.post("/api/trace-explorer/nonexistent-id/search", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w138_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/trace-explorer", json={'span_name': 'test-span_name', 'service': 'test-service', 'duration_ms': 1.0, 'status_code': 1, 'parent_trace_id': 'test-parent_trace_id', 'metadata': {}, 'recorded_at': 'test-recorded_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "trace_explorer"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w138_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/trace-explorer", json={'span_name': 'test-span_name', 'service': 'test-service', 'duration_ms': 1.0, 'status_code': 1, 'parent_trace_id': 'test-parent_trace_id', 'metadata': {}, 'recorded_at': 'test-recorded_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/trace-explorer", json={'span_name': 'test-span_name', 'service': 'test-service', 'duration_ms': 1.0, 'status_code': 1, 'parent_trace_id': 'test-parent_trace_id', 'metadata': {}, 'recorded_at': 'test-recorded_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "trace_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w138_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/trace-explorer", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w138_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/trace-explorer", json={'span_name': 'test-span_name', 'service': 'test-service', 'duration_ms': 1.0, 'status_code': 1, 'parent_trace_id': 'test-parent_trace_id', 'metadata': {}, 'recorded_at': 'test-recorded_at'})
    assert r1.status_code == 201
    item_id = r1.json()["trace_id"]
    r2 = await client.get("/api/trace-explorer")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/trace-explorer/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["trace_id"] == item_id
