"""Tests for Wave 134: Judge Demo 20x Loop

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w134_judge_loop_20x import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w134_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w134_create(client):
    r = await client.post("/api/judge-loop-20x", json={'loop_count': 1, 'target_loops': 1, 'loop_hashes': [], 'all_identical': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "loop_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w134_list(client):
    await client.post("/api/judge-loop-20x", json={'loop_count': 1, 'target_loops': 1, 'loop_hashes': [], 'all_identical': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    await client.post("/api/judge-loop-20x", json={'loop_count': 1, 'target_loops': 1, 'loop_hashes': [], 'all_identical': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    r = await client.get("/api/judge-loop-20x")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w134_get_by_id(client):
    r = await client.post("/api/judge-loop-20x", json={'loop_count': 1, 'target_loops': 1, 'loop_hashes': [], 'all_identical': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["loop_id"]
    r2 = await client.get(f"/api/judge-loop-20x/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["loop_id"] == item_id

@pytest.mark.asyncio
async def test_w134_get_not_found(client):
    r = await client.get("/api/judge-loop-20x/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w134_verify_hashes(client):
    r = await client.post("/api/judge-loop-20x", json={'loop_count': 1, 'target_loops': 1, 'loop_hashes': [], 'all_identical': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["loop_id"]
    r2 = await client.post(f"/api/judge-loop-20x/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["loop_id"] == item_id

@pytest.mark.asyncio
async def test_w134_verify_hashes_not_found(client):
    r = await client.post("/api/judge-loop-20x/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w134_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/judge-loop-20x", json={'loop_count': 1, 'target_loops': 1, 'loop_hashes': [], 'all_identical': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "judge_loop_20x"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w134_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/judge-loop-20x", json={'loop_count': 1, 'target_loops': 1, 'loop_hashes': [], 'all_identical': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/judge-loop-20x", json={'loop_count': 1, 'target_loops': 1, 'loop_hashes': [], 'all_identical': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "loop_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w134_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/judge-loop-20x", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w134_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/judge-loop-20x", json={'loop_count': 1, 'target_loops': 1, 'loop_hashes': [], 'all_identical': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["loop_id"]
    r2 = await client.get("/api/judge-loop-20x")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/judge-loop-20x/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["loop_id"] == item_id
