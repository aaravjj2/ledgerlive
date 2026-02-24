"""Tests for Wave 278: Collaboration v3

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w278_collab_v3 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w278_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w278_create(client):
    r = await client.post("/api/collab-v3", json={'entity_ref': 'test-entity_ref', 'entity_type': 'test-entity_type', 'mentions': [], 'watchers': [], 'activity_feed': [], 'lane_ref': 'test-lane_ref', 'feed_ordering_key': 1, 'notification_sent': True, 'cross_channel': True, 'deterministic_feed': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "collab_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w278_list(client):
    await client.post("/api/collab-v3", json={'entity_ref': 'test-entity_ref', 'entity_type': 'test-entity_type', 'mentions': [], 'watchers': [], 'activity_feed': [], 'lane_ref': 'test-lane_ref', 'feed_ordering_key': 1, 'notification_sent': True, 'cross_channel': True, 'deterministic_feed': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    await client.post("/api/collab-v3", json={'entity_ref': 'test-entity_ref', 'entity_type': 'test-entity_type', 'mentions': [], 'watchers': [], 'activity_feed': [], 'lane_ref': 'test-lane_ref', 'feed_ordering_key': 1, 'notification_sent': True, 'cross_channel': True, 'deterministic_feed': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    r = await client.get("/api/collab-v3")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w278_get_by_id(client):
    r = await client.post("/api/collab-v3", json={'entity_ref': 'test-entity_ref', 'entity_type': 'test-entity_type', 'mentions': [], 'watchers': [], 'activity_feed': [], 'lane_ref': 'test-lane_ref', 'feed_ordering_key': 1, 'notification_sent': True, 'cross_channel': True, 'deterministic_feed': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    item_id = r.json()["collab_id"]
    r2 = await client.get(f"/api/collab-v3/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["collab_id"] == item_id

@pytest.mark.asyncio
async def test_w278_get_not_found(client):
    r = await client.get("/api/collab-v3/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w278_add_mention(client):
    r = await client.post("/api/collab-v3", json={'entity_ref': 'test-entity_ref', 'entity_type': 'test-entity_type', 'mentions': [], 'watchers': [], 'activity_feed': [], 'lane_ref': 'test-lane_ref', 'feed_ordering_key': 1, 'notification_sent': True, 'cross_channel': True, 'deterministic_feed': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    item_id = r.json()["collab_id"]
    r2 = await client.post(f"/api/collab-v3/{item_id}/mention", json={})
    assert r2.status_code == 200
    assert r2.json()["collab_id"] == item_id

@pytest.mark.asyncio
async def test_w278_add_watcher(client):
    r = await client.post("/api/collab-v3", json={'entity_ref': 'test-entity_ref', 'entity_type': 'test-entity_type', 'mentions': [], 'watchers': [], 'activity_feed': [], 'lane_ref': 'test-lane_ref', 'feed_ordering_key': 1, 'notification_sent': True, 'cross_channel': True, 'deterministic_feed': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    item_id = r.json()["collab_id"]
    r2 = await client.post(f"/api/collab-v3/{item_id}/watcher", json={})
    assert r2.status_code == 200
    assert r2.json()["collab_id"] == item_id

@pytest.mark.asyncio
async def test_w278_get_feed(client):
    r = await client.post("/api/collab-v3", json={'entity_ref': 'test-entity_ref', 'entity_type': 'test-entity_type', 'mentions': [], 'watchers': [], 'activity_feed': [], 'lane_ref': 'test-lane_ref', 'feed_ordering_key': 1, 'notification_sent': True, 'cross_channel': True, 'deterministic_feed': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    item_id = r.json()["collab_id"]
    r2 = await client.post(f"/api/collab-v3/{item_id}/feed", json={})
    assert r2.status_code == 200
    assert r2.json()["collab_id"] == item_id

@pytest.mark.asyncio
async def test_w278_add_mention_not_found(client):
    r = await client.post("/api/collab-v3/nonexistent-id/mention", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w278_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/collab-v3", json={'entity_ref': 'test-entity_ref', 'entity_type': 'test-entity_type', 'mentions': [], 'watchers': [], 'activity_feed': [], 'lane_ref': 'test-lane_ref', 'feed_ordering_key': 1, 'notification_sent': True, 'cross_channel': True, 'deterministic_feed': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "collab_v3"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w278_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/collab-v3", json={'entity_ref': 'test-entity_ref', 'entity_type': 'test-entity_type', 'mentions': [], 'watchers': [], 'activity_feed': [], 'lane_ref': 'test-lane_ref', 'feed_ordering_key': 1, 'notification_sent': True, 'cross_channel': True, 'deterministic_feed': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/collab-v3", json={'entity_ref': 'test-entity_ref', 'entity_type': 'test-entity_type', 'mentions': [], 'watchers': [], 'activity_feed': [], 'lane_ref': 'test-lane_ref', 'feed_ordering_key': 1, 'notification_sent': True, 'cross_channel': True, 'deterministic_feed': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "collab_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w278_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/collab-v3", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w278_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/collab-v3", json={'entity_ref': 'test-entity_ref', 'entity_type': 'test-entity_type', 'mentions': [], 'watchers': [], 'activity_feed': [], 'lane_ref': 'test-lane_ref', 'feed_ordering_key': 1, 'notification_sent': True, 'cross_channel': True, 'deterministic_feed': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["collab_id"]
    r2 = await client.get("/api/collab-v3")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/collab-v3/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["collab_id"] == item_id
