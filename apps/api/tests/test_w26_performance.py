"""Tests for Wave 26: Performance Monitor

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w26_performance import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w26_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w26_create(client):
    r = await client.post("/api/performance/metrics", json={'endpoint': 'test-endpoint', 'method': 'test-method', 'p50_ms': 1.0, 'p95_ms': 1.0, 'p99_ms': 1.0, 'count': 1, 'window': 'test-window'})
    assert r.status_code == 201
    data = r.json()
    assert "metric_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w26_list(client):
    await client.post("/api/performance/metrics", json={'endpoint': 'test-endpoint', 'method': 'test-method', 'p50_ms': 1.0, 'p95_ms': 1.0, 'p99_ms': 1.0, 'count': 1, 'window': 'test-window'})
    await client.post("/api/performance/metrics", json={'endpoint': 'test-endpoint', 'method': 'test-method', 'p50_ms': 1.0, 'p95_ms': 1.0, 'p99_ms': 1.0, 'count': 1, 'window': 'test-window'})
    r = await client.get("/api/performance/metrics")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w26_get_by_id(client):
    r = await client.post("/api/performance/metrics", json={'endpoint': 'test-endpoint', 'method': 'test-method', 'p50_ms': 1.0, 'p95_ms': 1.0, 'p99_ms': 1.0, 'count': 1, 'window': 'test-window'})
    item_id = r.json()["metric_id"]
    r2 = await client.get(f"/api/performance/metrics/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["metric_id"] == item_id

@pytest.mark.asyncio
async def test_w26_get_not_found(client):
    r = await client.get("/api/performance/metrics/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w26_chaos_flag(client):
    r = await client.post("/api/performance/metrics", json={'endpoint': 'test-endpoint', 'method': 'test-method', 'p50_ms': 1.0, 'p95_ms': 1.0, 'p99_ms': 1.0, 'count': 1, 'window': 'test-window'})
    item_id = r.json()["metric_id"]
    r2 = await client.post(f"/api/performance/metrics/{item_id}/chaos", json={})
    assert r2.status_code == 200
    assert r2.json()["metric_id"] == item_id

@pytest.mark.asyncio
async def test_w26_clear_metrics(client):
    r = await client.post("/api/performance/metrics", json={'endpoint': 'test-endpoint', 'method': 'test-method', 'p50_ms': 1.0, 'p95_ms': 1.0, 'p99_ms': 1.0, 'count': 1, 'window': 'test-window'})
    item_id = r.json()["metric_id"]
    r2 = await client.post(f"/api/performance/metrics/{item_id}/clear", json={})
    assert r2.status_code == 200
    assert r2.json()["metric_id"] == item_id

@pytest.mark.asyncio
async def test_w26_chaos_flag_not_found(client):
    r = await client.post("/api/performance/metrics/nonexistent-id/chaos", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w26_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/performance/metrics", json={'endpoint': 'test-endpoint', 'method': 'test-method', 'p50_ms': 1.0, 'p95_ms': 1.0, 'p99_ms': 1.0, 'count': 1, 'window': 'test-window'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "performance"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w26_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/performance/metrics", json={'endpoint': 'test-endpoint', 'method': 'test-method', 'p50_ms': 1.0, 'p95_ms': 1.0, 'p99_ms': 1.0, 'count': 1, 'window': 'test-window'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/performance/metrics", json={'endpoint': 'test-endpoint', 'method': 'test-method', 'p50_ms': 1.0, 'p95_ms': 1.0, 'p99_ms': 1.0, 'count': 1, 'window': 'test-window'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "metric_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w26_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/performance/metrics", json={})
    assert r.status_code == 201
