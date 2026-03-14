"""Tests for Wave 68: Determinism Harness

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w068_determinism_harness import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w068_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w068_create(client):
    r = await client.post("/api/determinism-harness", json={'test_suite': 'test-test_suite', 'run_1_hash': 'test-run_1_hash', 'run_2_hash': 'test-run_2_hash', 'matched': True, 'diffs': [], 'run_count': 1, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "harness_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w068_list(client):
    await client.post("/api/determinism-harness", json={'test_suite': 'test-test_suite', 'run_1_hash': 'test-run_1_hash', 'run_2_hash': 'test-run_2_hash', 'matched': True, 'diffs': [], 'run_count': 1, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    await client.post("/api/determinism-harness", json={'test_suite': 'test-test_suite', 'run_1_hash': 'test-run_1_hash', 'run_2_hash': 'test-run_2_hash', 'matched': True, 'diffs': [], 'run_count': 1, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    r = await client.get("/api/determinism-harness")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w068_get_by_id(client):
    r = await client.post("/api/determinism-harness", json={'test_suite': 'test-test_suite', 'run_1_hash': 'test-run_1_hash', 'run_2_hash': 'test-run_2_hash', 'matched': True, 'diffs': [], 'run_count': 1, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["harness_id"]
    r2 = await client.get(f"/api/determinism-harness/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["harness_id"] == item_id

@pytest.mark.asyncio
async def test_w068_get_not_found(client):
    r = await client.get("/api/determinism-harness/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w068_compare(client):
    r = await client.post("/api/determinism-harness", json={'test_suite': 'test-test_suite', 'run_1_hash': 'test-run_1_hash', 'run_2_hash': 'test-run_2_hash', 'matched': True, 'diffs': [], 'run_count': 1, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["harness_id"]
    r2 = await client.post(f"/api/determinism-harness/{item_id}/compare", json={})
    assert r2.status_code == 200
    assert r2.json()["harness_id"] == item_id

@pytest.mark.asyncio
async def test_w068_compare_not_found(client):
    r = await client.post("/api/determinism-harness/nonexistent-id/compare", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w068_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/determinism-harness", json={'test_suite': 'test-test_suite', 'run_1_hash': 'test-run_1_hash', 'run_2_hash': 'test-run_2_hash', 'matched': True, 'diffs': [], 'run_count': 1, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "determinism_harness"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w068_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/determinism-harness", json={'test_suite': 'test-test_suite', 'run_1_hash': 'test-run_1_hash', 'run_2_hash': 'test-run_2_hash', 'matched': True, 'diffs': [], 'run_count': 1, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/determinism-harness", json={'test_suite': 'test-test_suite', 'run_1_hash': 'test-run_1_hash', 'run_2_hash': 'test-run_2_hash', 'matched': True, 'diffs': [], 'run_count': 1, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "harness_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w068_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/determinism-harness", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w068_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/determinism-harness", json={'test_suite': 'test-test_suite', 'run_1_hash': 'test-run_1_hash', 'run_2_hash': 'test-run_2_hash', 'matched': True, 'diffs': [], 'run_count': 1, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["harness_id"]
    r2 = await client.get("/api/determinism-harness")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/determinism-harness/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["harness_id"] == item_id
