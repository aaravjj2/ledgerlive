"""Tests for Wave 18: Continuous Close

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w18_continuous_close import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w18_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w18_create(client):
    r = await client.post("/api/close-tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'category': 'test-category', 'status': 'test-status', 'owner': 'test-owner', 'due_date': 'test-due_date', 'completed_at': 'test-completed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "task_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w18_list(client):
    await client.post("/api/close-tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'category': 'test-category', 'status': 'test-status', 'owner': 'test-owner', 'due_date': 'test-due_date', 'completed_at': 'test-completed_at'})
    await client.post("/api/close-tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'category': 'test-category', 'status': 'test-status', 'owner': 'test-owner', 'due_date': 'test-due_date', 'completed_at': 'test-completed_at'})
    r = await client.get("/api/close-tasks")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w18_get_by_id(client):
    r = await client.post("/api/close-tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'category': 'test-category', 'status': 'test-status', 'owner': 'test-owner', 'due_date': 'test-due_date', 'completed_at': 'test-completed_at'})
    item_id = r.json()["task_id"]
    r2 = await client.get(f"/api/close-tasks/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["task_id"] == item_id

@pytest.mark.asyncio
async def test_w18_get_not_found(client):
    r = await client.get("/api/close-tasks/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w18_complete_task(client):
    r = await client.post("/api/close-tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'category': 'test-category', 'status': 'test-status', 'owner': 'test-owner', 'due_date': 'test-due_date', 'completed_at': 'test-completed_at'})
    item_id = r.json()["task_id"]
    r2 = await client.post(f"/api/close-tasks/{item_id}/complete", json={})
    assert r2.status_code == 200
    assert r2.json()["task_id"] == item_id

@pytest.mark.asyncio
async def test_w18_complete_task_not_found(client):
    r = await client.post("/api/close-tasks/nonexistent-id/complete", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w18_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/close-tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'category': 'test-category', 'status': 'test-status', 'owner': 'test-owner', 'due_date': 'test-due_date', 'completed_at': 'test-completed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "continuous_close"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w18_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/close-tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'category': 'test-category', 'status': 'test-status', 'owner': 'test-owner', 'due_date': 'test-due_date', 'completed_at': 'test-completed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/close-tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'category': 'test-category', 'status': 'test-status', 'owner': 'test-owner', 'due_date': 'test-due_date', 'completed_at': 'test-completed_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "task_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w18_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/close-tasks", json={})
    assert r.status_code == 201
