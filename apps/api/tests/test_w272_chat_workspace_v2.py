"""Tests for Wave 272: Chat Workspace v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w272_chat_workspace_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w272_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w272_create(client):
    r = await client.post("/api/chat-workspace-v2", json={'channel_id': 'test-channel_id', 'sender': 'test-sender', 'content': 'test-content', 'card_data': {}, 'is_card': True, 'is_escalation': True, 'watchers': [], 'reactions': [], 'thread_replies': [], 'ping_targets': [], 'message_order': 1, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    assert r.status_code == 201
    data = r.json()
    assert "message_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w272_list(client):
    await client.post("/api/chat-workspace-v2", json={'channel_id': 'test-channel_id', 'sender': 'test-sender', 'content': 'test-content', 'card_data': {}, 'is_card': True, 'is_escalation': True, 'watchers': [], 'reactions': [], 'thread_replies': [], 'ping_targets': [], 'message_order': 1, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    await client.post("/api/chat-workspace-v2", json={'channel_id': 'test-channel_id', 'sender': 'test-sender', 'content': 'test-content', 'card_data': {}, 'is_card': True, 'is_escalation': True, 'watchers': [], 'reactions': [], 'thread_replies': [], 'ping_targets': [], 'message_order': 1, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    r = await client.get("/api/chat-workspace-v2")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w272_get_by_id(client):
    r = await client.post("/api/chat-workspace-v2", json={'channel_id': 'test-channel_id', 'sender': 'test-sender', 'content': 'test-content', 'card_data': {}, 'is_card': True, 'is_escalation': True, 'watchers': [], 'reactions': [], 'thread_replies': [], 'ping_targets': [], 'message_order': 1, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    item_id = r.json()["message_id"]
    r2 = await client.get(f"/api/chat-workspace-v2/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["message_id"] == item_id

@pytest.mark.asyncio
async def test_w272_get_not_found(client):
    r = await client.get("/api/chat-workspace-v2/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w272_send_card(client):
    r = await client.post("/api/chat-workspace-v2", json={'channel_id': 'test-channel_id', 'sender': 'test-sender', 'content': 'test-content', 'card_data': {}, 'is_card': True, 'is_escalation': True, 'watchers': [], 'reactions': [], 'thread_replies': [], 'ping_targets': [], 'message_order': 1, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    item_id = r.json()["message_id"]
    r2 = await client.post(f"/api/chat-workspace-v2/{item_id}/card", json={})
    assert r2.status_code == 200
    assert r2.json()["message_id"] == item_id

@pytest.mark.asyncio
async def test_w272_escalate(client):
    r = await client.post("/api/chat-workspace-v2", json={'channel_id': 'test-channel_id', 'sender': 'test-sender', 'content': 'test-content', 'card_data': {}, 'is_card': True, 'is_escalation': True, 'watchers': [], 'reactions': [], 'thread_replies': [], 'ping_targets': [], 'message_order': 1, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    item_id = r.json()["message_id"]
    r2 = await client.post(f"/api/chat-workspace-v2/{item_id}/escalate", json={})
    assert r2.status_code == 200
    assert r2.json()["message_id"] == item_id

@pytest.mark.asyncio
async def test_w272_add_watcher(client):
    r = await client.post("/api/chat-workspace-v2", json={'channel_id': 'test-channel_id', 'sender': 'test-sender', 'content': 'test-content', 'card_data': {}, 'is_card': True, 'is_escalation': True, 'watchers': [], 'reactions': [], 'thread_replies': [], 'ping_targets': [], 'message_order': 1, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    item_id = r.json()["message_id"]
    r2 = await client.post(f"/api/chat-workspace-v2/{item_id}/watcher", json={})
    assert r2.status_code == 200
    assert r2.json()["message_id"] == item_id

@pytest.mark.asyncio
async def test_w272_send_card_not_found(client):
    r = await client.post("/api/chat-workspace-v2/nonexistent-id/card", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w272_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/chat-workspace-v2", json={'channel_id': 'test-channel_id', 'sender': 'test-sender', 'content': 'test-content', 'card_data': {}, 'is_card': True, 'is_escalation': True, 'watchers': [], 'reactions': [], 'thread_replies': [], 'ping_targets': [], 'message_order': 1, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "chat_workspace_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w272_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/chat-workspace-v2", json={'channel_id': 'test-channel_id', 'sender': 'test-sender', 'content': 'test-content', 'card_data': {}, 'is_card': True, 'is_escalation': True, 'watchers': [], 'reactions': [], 'thread_replies': [], 'ping_targets': [], 'message_order': 1, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/chat-workspace-v2", json={'channel_id': 'test-channel_id', 'sender': 'test-sender', 'content': 'test-content', 'card_data': {}, 'is_card': True, 'is_escalation': True, 'watchers': [], 'reactions': [], 'thread_replies': [], 'ping_targets': [], 'message_order': 1, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "message_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w272_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/chat-workspace-v2", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w272_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/chat-workspace-v2", json={'channel_id': 'test-channel_id', 'sender': 'test-sender', 'content': 'test-content', 'card_data': {}, 'is_card': True, 'is_escalation': True, 'watchers': [], 'reactions': [], 'thread_replies': [], 'ping_targets': [], 'message_order': 1, 'status': 'test-status', 'sent_at': 'test-sent_at'})
    assert r1.status_code == 201
    item_id = r1.json()["message_id"]
    r2 = await client.get("/api/chat-workspace-v2")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/chat-workspace-v2/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["message_id"] == item_id
