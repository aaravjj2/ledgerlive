"""Tests for Wave 268: Replay Performance v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w268_replay_performance import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w268_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w268_create(client):
    r = await client.post("/api/replay-performance", json={'fixture_scale': 'test-fixture_scale', 'fixture_count': 1, 'replay_duration_ms': 1, 'budget_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_replayed': 1, 'throughput_rps': 1.0, 'memory_peak_mb': 1.0, 'perf_hash': 'test-perf_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert r.status_code == 201
    data = r.json()
    assert "perf_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w268_list(client):
    await client.post("/api/replay-performance", json={'fixture_scale': 'test-fixture_scale', 'fixture_count': 1, 'replay_duration_ms': 1, 'budget_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_replayed': 1, 'throughput_rps': 1.0, 'memory_peak_mb': 1.0, 'perf_hash': 'test-perf_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    await client.post("/api/replay-performance", json={'fixture_scale': 'test-fixture_scale', 'fixture_count': 1, 'replay_duration_ms': 1, 'budget_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_replayed': 1, 'throughput_rps': 1.0, 'memory_peak_mb': 1.0, 'perf_hash': 'test-perf_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    r = await client.get("/api/replay-performance")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w268_get_by_id(client):
    r = await client.post("/api/replay-performance", json={'fixture_scale': 'test-fixture_scale', 'fixture_count': 1, 'replay_duration_ms': 1, 'budget_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_replayed': 1, 'throughput_rps': 1.0, 'memory_peak_mb': 1.0, 'perf_hash': 'test-perf_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["perf_id"]
    r2 = await client.get(f"/api/replay-performance/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["perf_id"] == item_id

@pytest.mark.asyncio
async def test_w268_get_not_found(client):
    r = await client.get("/api/replay-performance/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w268_run_10x(client):
    r = await client.post("/api/replay-performance", json={'fixture_scale': 'test-fixture_scale', 'fixture_count': 1, 'replay_duration_ms': 1, 'budget_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_replayed': 1, 'throughput_rps': 1.0, 'memory_peak_mb': 1.0, 'perf_hash': 'test-perf_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["perf_id"]
    r2 = await client.post(f"/api/replay-performance/{item_id}/run-10x", json={})
    assert r2.status_code == 200
    assert r2.json()["perf_id"] == item_id

@pytest.mark.asyncio
async def test_w268_run_25x(client):
    r = await client.post("/api/replay-performance", json={'fixture_scale': 'test-fixture_scale', 'fixture_count': 1, 'replay_duration_ms': 1, 'budget_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_replayed': 1, 'throughput_rps': 1.0, 'memory_peak_mb': 1.0, 'perf_hash': 'test-perf_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["perf_id"]
    r2 = await client.post(f"/api/replay-performance/{item_id}/run-25x", json={})
    assert r2.status_code == 200
    assert r2.json()["perf_id"] == item_id

@pytest.mark.asyncio
async def test_w268_run_10x_not_found(client):
    r = await client.post("/api/replay-performance/nonexistent-id/run-10x", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w268_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/replay-performance", json={'fixture_scale': 'test-fixture_scale', 'fixture_count': 1, 'replay_duration_ms': 1, 'budget_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_replayed': 1, 'throughput_rps': 1.0, 'memory_peak_mb': 1.0, 'perf_hash': 'test-perf_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "replay_performance"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w268_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/replay-performance", json={'fixture_scale': 'test-fixture_scale', 'fixture_count': 1, 'replay_duration_ms': 1, 'budget_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_replayed': 1, 'throughput_rps': 1.0, 'memory_peak_mb': 1.0, 'perf_hash': 'test-perf_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/replay-performance", json={'fixture_scale': 'test-fixture_scale', 'fixture_count': 1, 'replay_duration_ms': 1, 'budget_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_replayed': 1, 'throughput_rps': 1.0, 'memory_peak_mb': 1.0, 'perf_hash': 'test-perf_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "perf_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w268_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/replay-performance", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w268_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/replay-performance", json={'fixture_scale': 'test-fixture_scale', 'fixture_count': 1, 'replay_duration_ms': 1, 'budget_ms': 1, 'within_budget': True, 'pagination_stable': True, 'pages_replayed': 1, 'throughput_rps': 1.0, 'memory_peak_mb': 1.0, 'perf_hash': 'test-perf_hash', 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert r1.status_code == 201
    item_id = r1.json()["perf_id"]
    r2 = await client.get("/api/replay-performance")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/replay-performance/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["perf_id"] == item_id
