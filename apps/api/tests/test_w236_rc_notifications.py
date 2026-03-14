"""Tests for Wave 236: RC Notification Hub v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w236_rc_notifications import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w236_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w236_create(client):
    r = await client.post("/api/rc-notifications", json={'event_type': 'test-event_type', 'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'delivered': True, 'delivered_at': 'test-delivered_at', 'deduplicated': True, 'throttled': True, 'retry_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "notification_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w236_list(client):
    await client.post("/api/rc-notifications", json={'event_type': 'test-event_type', 'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'delivered': True, 'delivered_at': 'test-delivered_at', 'deduplicated': True, 'throttled': True, 'retry_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/rc-notifications", json={'event_type': 'test-event_type', 'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'delivered': True, 'delivered_at': 'test-delivered_at', 'deduplicated': True, 'throttled': True, 'retry_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/rc-notifications")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w236_get_by_id(client):
    r = await client.post("/api/rc-notifications", json={'event_type': 'test-event_type', 'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'delivered': True, 'delivered_at': 'test-delivered_at', 'deduplicated': True, 'throttled': True, 'retry_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["notification_id"]
    r2 = await client.get(f"/api/rc-notifications/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["notification_id"] == item_id

@pytest.mark.asyncio
async def test_w236_get_not_found(client):
    r = await client.get("/api/rc-notifications/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w236_mark_delivered(client):
    r = await client.post("/api/rc-notifications", json={'event_type': 'test-event_type', 'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'delivered': True, 'delivered_at': 'test-delivered_at', 'deduplicated': True, 'throttled': True, 'retry_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["notification_id"]
    r2 = await client.post(f"/api/rc-notifications/{item_id}/deliver", json={})
    assert r2.status_code == 200
    assert r2.json()["notification_id"] == item_id

@pytest.mark.asyncio
async def test_w236_retry_notification(client):
    r = await client.post("/api/rc-notifications", json={'event_type': 'test-event_type', 'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'delivered': True, 'delivered_at': 'test-delivered_at', 'deduplicated': True, 'throttled': True, 'retry_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["notification_id"]
    r2 = await client.post(f"/api/rc-notifications/{item_id}/retry", json={})
    assert r2.status_code == 200
    assert r2.json()["notification_id"] == item_id

@pytest.mark.asyncio
async def test_w236_mark_delivered_not_found(client):
    r = await client.post("/api/rc-notifications/nonexistent-id/deliver", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w236_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/rc-notifications", json={'event_type': 'test-event_type', 'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'delivered': True, 'delivered_at': 'test-delivered_at', 'deduplicated': True, 'throttled': True, 'retry_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "rc_notifications"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w236_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/rc-notifications", json={'event_type': 'test-event_type', 'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'delivered': True, 'delivered_at': 'test-delivered_at', 'deduplicated': True, 'throttled': True, 'retry_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/rc-notifications", json={'event_type': 'test-event_type', 'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'delivered': True, 'delivered_at': 'test-delivered_at', 'deduplicated': True, 'throttled': True, 'retry_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "notification_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w236_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/rc-notifications", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w236_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/rc-notifications", json={'event_type': 'test-event_type', 'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'delivered': True, 'delivered_at': 'test-delivered_at', 'deduplicated': True, 'throttled': True, 'retry_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["notification_id"]
    r2 = await client.get("/api/rc-notifications")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/rc-notifications/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["notification_id"] == item_id
