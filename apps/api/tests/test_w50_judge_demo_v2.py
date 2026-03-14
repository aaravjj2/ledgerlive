"""Tests for Wave 50: Judge Demo 2.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w50_judge_demo_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w50_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w50_create(client):
    r = await client.post("/api/judge-demo-v2/runs", json={'demo_name': 'test-demo_name', 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'duration_seconds': 1.0, 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "demo_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w50_list(client):
    await client.post("/api/judge-demo-v2/runs", json={'demo_name': 'test-demo_name', 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'duration_seconds': 1.0, 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    await client.post("/api/judge-demo-v2/runs", json={'demo_name': 'test-demo_name', 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'duration_seconds': 1.0, 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    r = await client.get("/api/judge-demo-v2/runs")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w50_get_by_id(client):
    r = await client.post("/api/judge-demo-v2/runs", json={'demo_name': 'test-demo_name', 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'duration_seconds': 1.0, 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["demo_id"]
    r2 = await client.get(f"/api/judge-demo-v2/runs/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["demo_id"] == item_id

@pytest.mark.asyncio
async def test_w50_get_not_found(client):
    r = await client.get("/api/judge-demo-v2/runs/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w50_advance_step(client):
    r = await client.post("/api/judge-demo-v2/runs", json={'demo_name': 'test-demo_name', 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'duration_seconds': 1.0, 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["demo_id"]
    r2 = await client.post(f"/api/judge-demo-v2/runs/{item_id}/advance", json={})
    assert r2.status_code == 200
    assert r2.json()["demo_id"] == item_id

@pytest.mark.asyncio
async def test_w50_verify_demo(client):
    r = await client.post("/api/judge-demo-v2/runs", json={'demo_name': 'test-demo_name', 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'duration_seconds': 1.0, 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["demo_id"]
    r2 = await client.post(f"/api/judge-demo-v2/runs/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["demo_id"] == item_id

@pytest.mark.asyncio
async def test_w50_reset_demo(client):
    r = await client.post("/api/judge-demo-v2/runs", json={'demo_name': 'test-demo_name', 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'duration_seconds': 1.0, 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["demo_id"]
    r2 = await client.post(f"/api/judge-demo-v2/runs/{item_id}/reset", json={})
    assert r2.status_code == 200
    assert r2.json()["demo_id"] == item_id

@pytest.mark.asyncio
async def test_w50_advance_step_not_found(client):
    r = await client.post("/api/judge-demo-v2/runs/nonexistent-id/advance", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w50_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/judge-demo-v2/runs", json={'demo_name': 'test-demo_name', 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'duration_seconds': 1.0, 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "judge_demo_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w50_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/judge-demo-v2/runs", json={'demo_name': 'test-demo_name', 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'duration_seconds': 1.0, 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/judge-demo-v2/runs", json={'demo_name': 'test-demo_name', 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'duration_seconds': 1.0, 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "demo_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w50_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/judge-demo-v2/runs", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w50_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/judge-demo-v2/runs", json={'demo_name': 'test-demo_name', 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'duration_seconds': 1.0, 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["demo_id"]
    r2 = await client.get("/api/judge-demo-v2/runs")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/judge-demo-v2/runs/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["demo_id"] == item_id
