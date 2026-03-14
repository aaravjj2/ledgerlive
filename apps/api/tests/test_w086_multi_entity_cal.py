"""Tests for Wave 86: Multi-Entity Close Calendar

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w086_multi_entity_cal import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w086_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w086_create(client):
    r = await client.post("/api/multi-entity-cal", json={'entity_id': 'test-entity_id', 'period_id': 'test-period_id', 'depends_on_entities': [], 'task_count': 1, 'completed_count': 1, 'sla_hours': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "cal_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w086_list(client):
    await client.post("/api/multi-entity-cal", json={'entity_id': 'test-entity_id', 'period_id': 'test-period_id', 'depends_on_entities': [], 'task_count': 1, 'completed_count': 1, 'sla_hours': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/multi-entity-cal", json={'entity_id': 'test-entity_id', 'period_id': 'test-period_id', 'depends_on_entities': [], 'task_count': 1, 'completed_count': 1, 'sla_hours': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/multi-entity-cal")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w086_get_by_id(client):
    r = await client.post("/api/multi-entity-cal", json={'entity_id': 'test-entity_id', 'period_id': 'test-period_id', 'depends_on_entities': [], 'task_count': 1, 'completed_count': 1, 'sla_hours': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["cal_id"]
    r2 = await client.get(f"/api/multi-entity-cal/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["cal_id"] == item_id

@pytest.mark.asyncio
async def test_w086_get_not_found(client):
    r = await client.get("/api/multi-entity-cal/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w086_sync_deps(client):
    r = await client.post("/api/multi-entity-cal", json={'entity_id': 'test-entity_id', 'period_id': 'test-period_id', 'depends_on_entities': [], 'task_count': 1, 'completed_count': 1, 'sla_hours': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["cal_id"]
    r2 = await client.post(f"/api/multi-entity-cal/{item_id}/sync", json={})
    assert r2.status_code == 200
    assert r2.json()["cal_id"] == item_id

@pytest.mark.asyncio
async def test_w086_progress(client):
    r = await client.post("/api/multi-entity-cal", json={'entity_id': 'test-entity_id', 'period_id': 'test-period_id', 'depends_on_entities': [], 'task_count': 1, 'completed_count': 1, 'sla_hours': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["cal_id"]
    r2 = await client.post(f"/api/multi-entity-cal/{item_id}/progress", json={})
    assert r2.status_code == 200
    assert r2.json()["cal_id"] == item_id

@pytest.mark.asyncio
async def test_w086_sync_deps_not_found(client):
    r = await client.post("/api/multi-entity-cal/nonexistent-id/sync", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w086_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/multi-entity-cal", json={'entity_id': 'test-entity_id', 'period_id': 'test-period_id', 'depends_on_entities': [], 'task_count': 1, 'completed_count': 1, 'sla_hours': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "multi_entity_cal"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w086_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/multi-entity-cal", json={'entity_id': 'test-entity_id', 'period_id': 'test-period_id', 'depends_on_entities': [], 'task_count': 1, 'completed_count': 1, 'sla_hours': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/multi-entity-cal", json={'entity_id': 'test-entity_id', 'period_id': 'test-period_id', 'depends_on_entities': [], 'task_count': 1, 'completed_count': 1, 'sla_hours': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "cal_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w086_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/multi-entity-cal", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w086_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/multi-entity-cal", json={'entity_id': 'test-entity_id', 'period_id': 'test-period_id', 'depends_on_entities': [], 'task_count': 1, 'completed_count': 1, 'sla_hours': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["cal_id"]
    r2 = await client.get("/api/multi-entity-cal")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/multi-entity-cal/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["cal_id"] == item_id
