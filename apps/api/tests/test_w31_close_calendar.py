"""Tests for Wave 31: Close Calendar 2.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w31_close_calendar import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w31_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w31_create(client):
    r = await client.post("/api/close-calendar/tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'owner': 'test-owner', 'depends_on': [], 'sla_hours': 1, 'status': 'test-status', 'escalation_level': 1, 'started_at': 'test-started_at', 'due_at': 'test-due_at', 'completed_at': 'test-completed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "task_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w31_list(client):
    await client.post("/api/close-calendar/tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'owner': 'test-owner', 'depends_on': [], 'sla_hours': 1, 'status': 'test-status', 'escalation_level': 1, 'started_at': 'test-started_at', 'due_at': 'test-due_at', 'completed_at': 'test-completed_at'})
    await client.post("/api/close-calendar/tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'owner': 'test-owner', 'depends_on': [], 'sla_hours': 1, 'status': 'test-status', 'escalation_level': 1, 'started_at': 'test-started_at', 'due_at': 'test-due_at', 'completed_at': 'test-completed_at'})
    r = await client.get("/api/close-calendar/tasks")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w31_get_by_id(client):
    r = await client.post("/api/close-calendar/tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'owner': 'test-owner', 'depends_on': [], 'sla_hours': 1, 'status': 'test-status', 'escalation_level': 1, 'started_at': 'test-started_at', 'due_at': 'test-due_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["task_id"]
    r2 = await client.get(f"/api/close-calendar/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["task_id"] == item_id

@pytest.mark.asyncio
async def test_w31_get_not_found(client):
    r = await client.get("/api/close-calendar/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w31_start_task(client):
    r = await client.post("/api/close-calendar/tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'owner': 'test-owner', 'depends_on': [], 'sla_hours': 1, 'status': 'test-status', 'escalation_level': 1, 'started_at': 'test-started_at', 'due_at': 'test-due_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["task_id"]
    r2 = await client.post(f"/api/close-calendar/{item_id}/start", json={})
    assert r2.status_code == 200
    assert r2.json()["task_id"] == item_id

@pytest.mark.asyncio
async def test_w31_complete_task(client):
    r = await client.post("/api/close-calendar/tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'owner': 'test-owner', 'depends_on': [], 'sla_hours': 1, 'status': 'test-status', 'escalation_level': 1, 'started_at': 'test-started_at', 'due_at': 'test-due_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["task_id"]
    r2 = await client.post(f"/api/close-calendar/{item_id}/complete", json={})
    assert r2.status_code == 200
    assert r2.json()["task_id"] == item_id

@pytest.mark.asyncio
async def test_w31_escalate(client):
    r = await client.post("/api/close-calendar/tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'owner': 'test-owner', 'depends_on': [], 'sla_hours': 1, 'status': 'test-status', 'escalation_level': 1, 'started_at': 'test-started_at', 'due_at': 'test-due_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["task_id"]
    r2 = await client.post(f"/api/close-calendar/{item_id}/escalate", json={})
    assert r2.status_code == 200
    assert r2.json()["task_id"] == item_id

@pytest.mark.asyncio
async def test_w31_start_task_not_found(client):
    r = await client.post("/api/close-calendar/nonexistent-id/start", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w31_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/close-calendar/tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'owner': 'test-owner', 'depends_on': [], 'sla_hours': 1, 'status': 'test-status', 'escalation_level': 1, 'started_at': 'test-started_at', 'due_at': 'test-due_at', 'completed_at': 'test-completed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "close_calendar"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w31_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/close-calendar/tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'owner': 'test-owner', 'depends_on': [], 'sla_hours': 1, 'status': 'test-status', 'escalation_level': 1, 'started_at': 'test-started_at', 'due_at': 'test-due_at', 'completed_at': 'test-completed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/close-calendar/tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'owner': 'test-owner', 'depends_on': [], 'sla_hours': 1, 'status': 'test-status', 'escalation_level': 1, 'started_at': 'test-started_at', 'due_at': 'test-due_at', 'completed_at': 'test-completed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "task_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w31_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/close-calendar/tasks", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w31_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/close-calendar/tasks", json={'period_id': 'test-period_id', 'name': 'test-name', 'owner': 'test-owner', 'depends_on': [], 'sla_hours': 1, 'status': 'test-status', 'escalation_level': 1, 'started_at': 'test-started_at', 'due_at': 'test-due_at', 'completed_at': 'test-completed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["task_id"]
    r2 = await client.get("/api/close-calendar/tasks")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/close-calendar/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["task_id"] == item_id
