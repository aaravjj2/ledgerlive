"""Tests for Wave 48: Performance Suite 2.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w48_perf_suite import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w48_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w48_create(client):
    r = await client.post("/api/perf-suite/benchmarks", json={'name': 'test-name', 'fixture_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'queries_counted': 1, 'index_hits': 1, 'run_at': 'test-run_at'})
    assert r.status_code == 201
    data = r.json()
    assert "benchmark_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w48_list(client):
    await client.post("/api/perf-suite/benchmarks", json={'name': 'test-name', 'fixture_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'queries_counted': 1, 'index_hits': 1, 'run_at': 'test-run_at'})
    await client.post("/api/perf-suite/benchmarks", json={'name': 'test-name', 'fixture_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'queries_counted': 1, 'index_hits': 1, 'run_at': 'test-run_at'})
    r = await client.get("/api/perf-suite/benchmarks")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w48_get_by_id(client):
    r = await client.post("/api/perf-suite/benchmarks", json={'name': 'test-name', 'fixture_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'queries_counted': 1, 'index_hits': 1, 'run_at': 'test-run_at'})
    item_id = r.json()["benchmark_id"]
    r2 = await client.get(f"/api/perf-suite/benchmarks/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["benchmark_id"] == item_id

@pytest.mark.asyncio
async def test_w48_get_not_found(client):
    r = await client.get("/api/perf-suite/benchmarks/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w48_set_budget(client):
    r = await client.post("/api/perf-suite/benchmarks", json={'name': 'test-name', 'fixture_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'queries_counted': 1, 'index_hits': 1, 'run_at': 'test-run_at'})
    item_id = r.json()["benchmark_id"]
    r2 = await client.post(f"/api/perf-suite/benchmarks/{item_id}/budget", json={})
    assert r2.status_code == 200
    assert r2.json()["benchmark_id"] == item_id

@pytest.mark.asyncio
async def test_w48_set_budget_not_found(client):
    r = await client.post("/api/perf-suite/benchmarks/nonexistent-id/budget", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w48_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/perf-suite/benchmarks", json={'name': 'test-name', 'fixture_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'queries_counted': 1, 'index_hits': 1, 'run_at': 'test-run_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "perf_suite"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w48_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/perf-suite/benchmarks", json={'name': 'test-name', 'fixture_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'queries_counted': 1, 'index_hits': 1, 'run_at': 'test-run_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/perf-suite/benchmarks", json={'name': 'test-name', 'fixture_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'queries_counted': 1, 'index_hits': 1, 'run_at': 'test-run_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "benchmark_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w48_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/perf-suite/benchmarks", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w48_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/perf-suite/benchmarks", json={'name': 'test-name', 'fixture_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'passed': True, 'queries_counted': 1, 'index_hits': 1, 'run_at': 'test-run_at'})
    assert r1.status_code == 201
    item_id = r1.json()["benchmark_id"]
    r2 = await client.get("/api/perf-suite/benchmarks")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/perf-suite/benchmarks/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["benchmark_id"] == item_id
