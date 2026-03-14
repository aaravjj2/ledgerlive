"""Tests for Wave 148: Batch Workflow Performance

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w148_batch_workflow_perf import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w148_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w148_create(client):
    r = await client.post("/api/batch-workflow-perf", json={'workflow_name': 'test-workflow_name', 'batch_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'throughput_rps': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert r.status_code == 201
    data = r.json()
    assert "perf_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w148_list(client):
    await client.post("/api/batch-workflow-perf", json={'workflow_name': 'test-workflow_name', 'batch_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'throughput_rps': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    await client.post("/api/batch-workflow-perf", json={'workflow_name': 'test-workflow_name', 'batch_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'throughput_rps': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    r = await client.get("/api/batch-workflow-perf")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w148_get_by_id(client):
    r = await client.post("/api/batch-workflow-perf", json={'workflow_name': 'test-workflow_name', 'batch_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'throughput_rps': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["perf_id"]
    r2 = await client.get(f"/api/batch-workflow-perf/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["perf_id"] == item_id

@pytest.mark.asyncio
async def test_w148_get_not_found(client):
    r = await client.get("/api/batch-workflow-perf/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w148_set_budget(client):
    r = await client.post("/api/batch-workflow-perf", json={'workflow_name': 'test-workflow_name', 'batch_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'throughput_rps': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    item_id = r.json()["perf_id"]
    r2 = await client.post(f"/api/batch-workflow-perf/{item_id}/budget", json={})
    assert r2.status_code == 200
    assert r2.json()["perf_id"] == item_id

@pytest.mark.asyncio
async def test_w148_set_budget_not_found(client):
    r = await client.post("/api/batch-workflow-perf/nonexistent-id/budget", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w148_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/batch-workflow-perf", json={'workflow_name': 'test-workflow_name', 'batch_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'throughput_rps': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "batch_workflow_perf"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w148_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/batch-workflow-perf", json={'workflow_name': 'test-workflow_name', 'batch_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'throughput_rps': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/batch-workflow-perf", json={'workflow_name': 'test-workflow_name', 'batch_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'throughput_rps': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "perf_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w148_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/batch-workflow-perf", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w148_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/batch-workflow-perf", json={'workflow_name': 'test-workflow_name', 'batch_size': 1, 'target_ms': 1.0, 'actual_ms': 1.0, 'throughput_rps': 1.0, 'within_budget': True, 'status': 'test-status', 'measured_at': 'test-measured_at'})
    assert r1.status_code == 201
    item_id = r1.json()["perf_id"]
    r2 = await client.get("/api/batch-workflow-perf")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/batch-workflow-perf/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["perf_id"] == item_id
