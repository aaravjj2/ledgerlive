"""Tests for Wave 277: RC Channel Actions v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w277_rc_channel_actions import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w277_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w277_create(client):
    r = await client.post("/api/rc-channel-actions", json={'rc_ref': 'test-rc_ref', 'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'target_entity': 'test-target_entity', 'message_content': 'test-message_content', 'approval_ref': 'test-approval_ref', 'incident_ref': 'test-incident_ref', 'delivery_status': 'test-delivery_status', 'routing_deterministic': True, 'no_network_flag': True, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    assert r.status_code == 201
    data = r.json()
    assert "rc_action_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w277_list(client):
    await client.post("/api/rc-channel-actions", json={'rc_ref': 'test-rc_ref', 'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'target_entity': 'test-target_entity', 'message_content': 'test-message_content', 'approval_ref': 'test-approval_ref', 'incident_ref': 'test-incident_ref', 'delivery_status': 'test-delivery_status', 'routing_deterministic': True, 'no_network_flag': True, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    await client.post("/api/rc-channel-actions", json={'rc_ref': 'test-rc_ref', 'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'target_entity': 'test-target_entity', 'message_content': 'test-message_content', 'approval_ref': 'test-approval_ref', 'incident_ref': 'test-incident_ref', 'delivery_status': 'test-delivery_status', 'routing_deterministic': True, 'no_network_flag': True, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    r = await client.get("/api/rc-channel-actions")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w277_get_by_id(client):
    r = await client.post("/api/rc-channel-actions", json={'rc_ref': 'test-rc_ref', 'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'target_entity': 'test-target_entity', 'message_content': 'test-message_content', 'approval_ref': 'test-approval_ref', 'incident_ref': 'test-incident_ref', 'delivery_status': 'test-delivery_status', 'routing_deterministic': True, 'no_network_flag': True, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    item_id = r.json()["rc_action_id"]
    r2 = await client.get(f"/api/rc-channel-actions/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["rc_action_id"] == item_id

@pytest.mark.asyncio
async def test_w277_get_not_found(client):
    r = await client.get("/api/rc-channel-actions/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w277_route_to_channel(client):
    r = await client.post("/api/rc-channel-actions", json={'rc_ref': 'test-rc_ref', 'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'target_entity': 'test-target_entity', 'message_content': 'test-message_content', 'approval_ref': 'test-approval_ref', 'incident_ref': 'test-incident_ref', 'delivery_status': 'test-delivery_status', 'routing_deterministic': True, 'no_network_flag': True, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    item_id = r.json()["rc_action_id"]
    r2 = await client.post(f"/api/rc-channel-actions/{item_id}/route", json={})
    assert r2.status_code == 200
    assert r2.json()["rc_action_id"] == item_id

@pytest.mark.asyncio
async def test_w277_confirm_delivery(client):
    r = await client.post("/api/rc-channel-actions", json={'rc_ref': 'test-rc_ref', 'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'target_entity': 'test-target_entity', 'message_content': 'test-message_content', 'approval_ref': 'test-approval_ref', 'incident_ref': 'test-incident_ref', 'delivery_status': 'test-delivery_status', 'routing_deterministic': True, 'no_network_flag': True, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    item_id = r.json()["rc_action_id"]
    r2 = await client.post(f"/api/rc-channel-actions/{item_id}/confirm", json={})
    assert r2.status_code == 200
    assert r2.json()["rc_action_id"] == item_id

@pytest.mark.asyncio
async def test_w277_route_to_channel_not_found(client):
    r = await client.post("/api/rc-channel-actions/nonexistent-id/route", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w277_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/rc-channel-actions", json={'rc_ref': 'test-rc_ref', 'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'target_entity': 'test-target_entity', 'message_content': 'test-message_content', 'approval_ref': 'test-approval_ref', 'incident_ref': 'test-incident_ref', 'delivery_status': 'test-delivery_status', 'routing_deterministic': True, 'no_network_flag': True, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "rc_channel_actions"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w277_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/rc-channel-actions", json={'rc_ref': 'test-rc_ref', 'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'target_entity': 'test-target_entity', 'message_content': 'test-message_content', 'approval_ref': 'test-approval_ref', 'incident_ref': 'test-incident_ref', 'delivery_status': 'test-delivery_status', 'routing_deterministic': True, 'no_network_flag': True, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/rc-channel-actions", json={'rc_ref': 'test-rc_ref', 'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'target_entity': 'test-target_entity', 'message_content': 'test-message_content', 'approval_ref': 'test-approval_ref', 'incident_ref': 'test-incident_ref', 'delivery_status': 'test-delivery_status', 'routing_deterministic': True, 'no_network_flag': True, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "rc_action_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w277_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/rc-channel-actions", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w277_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/rc-channel-actions", json={'rc_ref': 'test-rc_ref', 'channel_type': 'test-channel_type', 'action_type': 'test-action_type', 'target_entity': 'test-target_entity', 'message_content': 'test-message_content', 'approval_ref': 'test-approval_ref', 'incident_ref': 'test-incident_ref', 'delivery_status': 'test-delivery_status', 'routing_deterministic': True, 'no_network_flag': True, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    assert r1.status_code == 201
    item_id = r1.json()["rc_action_id"]
    r2 = await client.get("/api/rc-channel-actions")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/rc-channel-actions/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["rc_action_id"] == item_id
