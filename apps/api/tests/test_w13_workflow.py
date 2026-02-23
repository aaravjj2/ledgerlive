"""Tests for Wave 13: Workflow Engine

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w13_workflow import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w13_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w13_create(client):
    r = await client.post("/api/workflows", json={'name': 'test-name', 'steps': [], 'status': 'test-status', 'current_step': 1, 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "workflow_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w13_list(client):
    await client.post("/api/workflows", json={'name': 'test-name', 'steps': [], 'status': 'test-status', 'current_step': 1, 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    await client.post("/api/workflows", json={'name': 'test-name', 'steps': [], 'status': 'test-status', 'current_step': 1, 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    r = await client.get("/api/workflows")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w13_get_by_id(client):
    r = await client.post("/api/workflows", json={'name': 'test-name', 'steps': [], 'status': 'test-status', 'current_step': 1, 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["workflow_id"]
    r2 = await client.get(f"/api/workflows/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["workflow_id"] == item_id

@pytest.mark.asyncio
async def test_w13_get_not_found(client):
    r = await client.get("/api/workflows/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w13_advance(client):
    r = await client.post("/api/workflows", json={'name': 'test-name', 'steps': [], 'status': 'test-status', 'current_step': 1, 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["workflow_id"]
    r2 = await client.post(f"/api/workflows/{item_id}/advance", json={})
    assert r2.status_code == 200
    assert r2.json()["workflow_id"] == item_id

@pytest.mark.asyncio
async def test_w13_abort(client):
    r = await client.post("/api/workflows", json={'name': 'test-name', 'steps': [], 'status': 'test-status', 'current_step': 1, 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["workflow_id"]
    r2 = await client.post(f"/api/workflows/{item_id}/abort", json={})
    assert r2.status_code == 200
    assert r2.json()["workflow_id"] == item_id

@pytest.mark.asyncio
async def test_w13_advance_not_found(client):
    r = await client.post("/api/workflows/nonexistent-id/advance", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w13_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/workflows", json={'name': 'test-name', 'steps': [], 'status': 'test-status', 'current_step': 1, 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "workflow"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w13_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/workflows", json={'name': 'test-name', 'steps': [], 'status': 'test-status', 'current_step': 1, 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/workflows", json={'name': 'test-name', 'steps': [], 'status': 'test-status', 'current_step': 1, 'created_at': 'test-created_at', 'completed_at': 'test-completed_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "workflow_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w13_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/workflows", json={})
    assert r.status_code == 201
