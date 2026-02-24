"""Tests for Wave 230: Lane Status Board v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w230_lane_status import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w230_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w230_create(client):
    r = await client.post("/api/lane-status", json={'lane_name': 'test-lane_name', 'workstream': 'test-workstream', 'tasks_in_lane': [], 'lane_color': 'test-lane_color', 'completion_pct': 1.0, 'blocked_count': 1, 'on_track': True, 'owner_team': 'test-owner_team', 'display_order': 1, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "lane_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w230_list(client):
    await client.post("/api/lane-status", json={'lane_name': 'test-lane_name', 'workstream': 'test-workstream', 'tasks_in_lane': [], 'lane_color': 'test-lane_color', 'completion_pct': 1.0, 'blocked_count': 1, 'on_track': True, 'owner_team': 'test-owner_team', 'display_order': 1, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    await client.post("/api/lane-status", json={'lane_name': 'test-lane_name', 'workstream': 'test-workstream', 'tasks_in_lane': [], 'lane_color': 'test-lane_color', 'completion_pct': 1.0, 'blocked_count': 1, 'on_track': True, 'owner_team': 'test-owner_team', 'display_order': 1, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    r = await client.get("/api/lane-status")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w230_get_by_id(client):
    r = await client.post("/api/lane-status", json={'lane_name': 'test-lane_name', 'workstream': 'test-workstream', 'tasks_in_lane': [], 'lane_color': 'test-lane_color', 'completion_pct': 1.0, 'blocked_count': 1, 'on_track': True, 'owner_team': 'test-owner_team', 'display_order': 1, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    item_id = r.json()["lane_id"]
    r2 = await client.get(f"/api/lane-status/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["lane_id"] == item_id

@pytest.mark.asyncio
async def test_w230_get_not_found(client):
    r = await client.get("/api/lane-status/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w230_update_lane(client):
    r = await client.post("/api/lane-status", json={'lane_name': 'test-lane_name', 'workstream': 'test-workstream', 'tasks_in_lane': [], 'lane_color': 'test-lane_color', 'completion_pct': 1.0, 'blocked_count': 1, 'on_track': True, 'owner_team': 'test-owner_team', 'display_order': 1, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    item_id = r.json()["lane_id"]
    r2 = await client.post(f"/api/lane-status/{item_id}/update", json={})
    assert r2.status_code == 200
    assert r2.json()["lane_id"] == item_id

@pytest.mark.asyncio
async def test_w230_reorder_lane(client):
    r = await client.post("/api/lane-status", json={'lane_name': 'test-lane_name', 'workstream': 'test-workstream', 'tasks_in_lane': [], 'lane_color': 'test-lane_color', 'completion_pct': 1.0, 'blocked_count': 1, 'on_track': True, 'owner_team': 'test-owner_team', 'display_order': 1, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    item_id = r.json()["lane_id"]
    r2 = await client.post(f"/api/lane-status/{item_id}/reorder", json={})
    assert r2.status_code == 200
    assert r2.json()["lane_id"] == item_id

@pytest.mark.asyncio
async def test_w230_update_lane_not_found(client):
    r = await client.post("/api/lane-status/nonexistent-id/update", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w230_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/lane-status", json={'lane_name': 'test-lane_name', 'workstream': 'test-workstream', 'tasks_in_lane': [], 'lane_color': 'test-lane_color', 'completion_pct': 1.0, 'blocked_count': 1, 'on_track': True, 'owner_team': 'test-owner_team', 'display_order': 1, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "lane_status"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w230_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/lane-status", json={'lane_name': 'test-lane_name', 'workstream': 'test-workstream', 'tasks_in_lane': [], 'lane_color': 'test-lane_color', 'completion_pct': 1.0, 'blocked_count': 1, 'on_track': True, 'owner_team': 'test-owner_team', 'display_order': 1, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/lane-status", json={'lane_name': 'test-lane_name', 'workstream': 'test-workstream', 'tasks_in_lane': [], 'lane_color': 'test-lane_color', 'completion_pct': 1.0, 'blocked_count': 1, 'on_track': True, 'owner_team': 'test-owner_team', 'display_order': 1, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "lane_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w230_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/lane-status", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w230_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/lane-status", json={'lane_name': 'test-lane_name', 'workstream': 'test-workstream', 'tasks_in_lane': [], 'lane_color': 'test-lane_color', 'completion_pct': 1.0, 'blocked_count': 1, 'on_track': True, 'owner_team': 'test-owner_team', 'display_order': 1, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["lane_id"]
    r2 = await client.get("/api/lane-status")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/lane-status/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["lane_id"] == item_id
