"""Tests for Wave 274: Notification Hub v4

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w274_notification_hub_v4 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w274_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w274_create(client):
    r = await client.post("/api/notification-hub-v4", json={'user_id': 'test-user_id', 'channel': 'test-channel', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'routing_rule_ref': 'test-routing_rule_ref', 'quiet_hours_blocked': True, 'deduplicated': True, 'sla_escalation': True, 'delivery_status': 'test-delivery_status', 'frozen_time': 'test-frozen_time', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "notification_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w274_list(client):
    await client.post("/api/notification-hub-v4", json={'user_id': 'test-user_id', 'channel': 'test-channel', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'routing_rule_ref': 'test-routing_rule_ref', 'quiet_hours_blocked': True, 'deduplicated': True, 'sla_escalation': True, 'delivery_status': 'test-delivery_status', 'frozen_time': 'test-frozen_time', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/notification-hub-v4", json={'user_id': 'test-user_id', 'channel': 'test-channel', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'routing_rule_ref': 'test-routing_rule_ref', 'quiet_hours_blocked': True, 'deduplicated': True, 'sla_escalation': True, 'delivery_status': 'test-delivery_status', 'frozen_time': 'test-frozen_time', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/notification-hub-v4")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w274_get_by_id(client):
    r = await client.post("/api/notification-hub-v4", json={'user_id': 'test-user_id', 'channel': 'test-channel', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'routing_rule_ref': 'test-routing_rule_ref', 'quiet_hours_blocked': True, 'deduplicated': True, 'sla_escalation': True, 'delivery_status': 'test-delivery_status', 'frozen_time': 'test-frozen_time', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["notification_id"]
    r2 = await client.get(f"/api/notification-hub-v4/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["notification_id"] == item_id

@pytest.mark.asyncio
async def test_w274_get_not_found(client):
    r = await client.get("/api/notification-hub-v4/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w274_apply_routing(client):
    r = await client.post("/api/notification-hub-v4", json={'user_id': 'test-user_id', 'channel': 'test-channel', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'routing_rule_ref': 'test-routing_rule_ref', 'quiet_hours_blocked': True, 'deduplicated': True, 'sla_escalation': True, 'delivery_status': 'test-delivery_status', 'frozen_time': 'test-frozen_time', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["notification_id"]
    r2 = await client.post(f"/api/notification-hub-v4/{item_id}/route", json={})
    assert r2.status_code == 200
    assert r2.json()["notification_id"] == item_id

@pytest.mark.asyncio
async def test_w274_check_quiet_hours(client):
    r = await client.post("/api/notification-hub-v4", json={'user_id': 'test-user_id', 'channel': 'test-channel', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'routing_rule_ref': 'test-routing_rule_ref', 'quiet_hours_blocked': True, 'deduplicated': True, 'sla_escalation': True, 'delivery_status': 'test-delivery_status', 'frozen_time': 'test-frozen_time', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["notification_id"]
    r2 = await client.post(f"/api/notification-hub-v4/{item_id}/quiet", json={})
    assert r2.status_code == 200
    assert r2.json()["notification_id"] == item_id

@pytest.mark.asyncio
async def test_w274_dedup_check(client):
    r = await client.post("/api/notification-hub-v4", json={'user_id': 'test-user_id', 'channel': 'test-channel', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'routing_rule_ref': 'test-routing_rule_ref', 'quiet_hours_blocked': True, 'deduplicated': True, 'sla_escalation': True, 'delivery_status': 'test-delivery_status', 'frozen_time': 'test-frozen_time', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["notification_id"]
    r2 = await client.post(f"/api/notification-hub-v4/{item_id}/dedup", json={})
    assert r2.status_code == 200
    assert r2.json()["notification_id"] == item_id

@pytest.mark.asyncio
async def test_w274_apply_routing_not_found(client):
    r = await client.post("/api/notification-hub-v4/nonexistent-id/route", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w274_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/notification-hub-v4", json={'user_id': 'test-user_id', 'channel': 'test-channel', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'routing_rule_ref': 'test-routing_rule_ref', 'quiet_hours_blocked': True, 'deduplicated': True, 'sla_escalation': True, 'delivery_status': 'test-delivery_status', 'frozen_time': 'test-frozen_time', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "notification_hub_v4"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w274_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/notification-hub-v4", json={'user_id': 'test-user_id', 'channel': 'test-channel', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'routing_rule_ref': 'test-routing_rule_ref', 'quiet_hours_blocked': True, 'deduplicated': True, 'sla_escalation': True, 'delivery_status': 'test-delivery_status', 'frozen_time': 'test-frozen_time', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/notification-hub-v4", json={'user_id': 'test-user_id', 'channel': 'test-channel', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'routing_rule_ref': 'test-routing_rule_ref', 'quiet_hours_blocked': True, 'deduplicated': True, 'sla_escalation': True, 'delivery_status': 'test-delivery_status', 'frozen_time': 'test-frozen_time', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "notification_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w274_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/notification-hub-v4", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w274_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/notification-hub-v4", json={'user_id': 'test-user_id', 'channel': 'test-channel', 'subject': 'test-subject', 'body': 'test-body', 'priority': 'test-priority', 'routing_rule_ref': 'test-routing_rule_ref', 'quiet_hours_blocked': True, 'deduplicated': True, 'sla_escalation': True, 'delivery_status': 'test-delivery_status', 'frozen_time': 'test-frozen_time', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["notification_id"]
    r2 = await client.get("/api/notification-hub-v4")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/notification-hub-v4/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["notification_id"] == item_id
