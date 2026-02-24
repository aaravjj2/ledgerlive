"""Tests for Wave 271: Email Inbox v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w271_email_inbox_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w271_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w271_create(client):
    r = await client.post("/api/email-inbox-v2", json={'thread_id': 'test-thread_id', 'subject': 'test-subject', 'sender': 'test-sender', 'recipients': [], 'body': 'test-body', 'attachments': [], 'is_approval_reply': True, 'approval_decision': 'test-approval_decision', 'parsed_content': {}, 'thread_position': 1, 'read': True, 'status': 'test-status', 'received_at': 'test-received_at'})
    assert r.status_code == 201
    data = r.json()
    assert "email_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w271_list(client):
    await client.post("/api/email-inbox-v2", json={'thread_id': 'test-thread_id', 'subject': 'test-subject', 'sender': 'test-sender', 'recipients': [], 'body': 'test-body', 'attachments': [], 'is_approval_reply': True, 'approval_decision': 'test-approval_decision', 'parsed_content': {}, 'thread_position': 1, 'read': True, 'status': 'test-status', 'received_at': 'test-received_at'})
    await client.post("/api/email-inbox-v2", json={'thread_id': 'test-thread_id', 'subject': 'test-subject', 'sender': 'test-sender', 'recipients': [], 'body': 'test-body', 'attachments': [], 'is_approval_reply': True, 'approval_decision': 'test-approval_decision', 'parsed_content': {}, 'thread_position': 1, 'read': True, 'status': 'test-status', 'received_at': 'test-received_at'})
    r = await client.get("/api/email-inbox-v2")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w271_get_by_id(client):
    r = await client.post("/api/email-inbox-v2", json={'thread_id': 'test-thread_id', 'subject': 'test-subject', 'sender': 'test-sender', 'recipients': [], 'body': 'test-body', 'attachments': [], 'is_approval_reply': True, 'approval_decision': 'test-approval_decision', 'parsed_content': {}, 'thread_position': 1, 'read': True, 'status': 'test-status', 'received_at': 'test-received_at'})
    item_id = r.json()["email_id"]
    r2 = await client.get(f"/api/email-inbox-v2/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["email_id"] == item_id

@pytest.mark.asyncio
async def test_w271_get_not_found(client):
    r = await client.get("/api/email-inbox-v2/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w271_reply_email(client):
    r = await client.post("/api/email-inbox-v2", json={'thread_id': 'test-thread_id', 'subject': 'test-subject', 'sender': 'test-sender', 'recipients': [], 'body': 'test-body', 'attachments': [], 'is_approval_reply': True, 'approval_decision': 'test-approval_decision', 'parsed_content': {}, 'thread_position': 1, 'read': True, 'status': 'test-status', 'received_at': 'test-received_at'})
    item_id = r.json()["email_id"]
    r2 = await client.post(f"/api/email-inbox-v2/{item_id}/reply", json={})
    assert r2.status_code == 200
    assert r2.json()["email_id"] == item_id

@pytest.mark.asyncio
async def test_w271_parse_content(client):
    r = await client.post("/api/email-inbox-v2", json={'thread_id': 'test-thread_id', 'subject': 'test-subject', 'sender': 'test-sender', 'recipients': [], 'body': 'test-body', 'attachments': [], 'is_approval_reply': True, 'approval_decision': 'test-approval_decision', 'parsed_content': {}, 'thread_position': 1, 'read': True, 'status': 'test-status', 'received_at': 'test-received_at'})
    item_id = r.json()["email_id"]
    r2 = await client.post(f"/api/email-inbox-v2/{item_id}/parse", json={})
    assert r2.status_code == 200
    assert r2.json()["email_id"] == item_id

@pytest.mark.asyncio
async def test_w271_mark_read(client):
    r = await client.post("/api/email-inbox-v2", json={'thread_id': 'test-thread_id', 'subject': 'test-subject', 'sender': 'test-sender', 'recipients': [], 'body': 'test-body', 'attachments': [], 'is_approval_reply': True, 'approval_decision': 'test-approval_decision', 'parsed_content': {}, 'thread_position': 1, 'read': True, 'status': 'test-status', 'received_at': 'test-received_at'})
    item_id = r.json()["email_id"]
    r2 = await client.post(f"/api/email-inbox-v2/{item_id}/read", json={})
    assert r2.status_code == 200
    assert r2.json()["email_id"] == item_id

@pytest.mark.asyncio
async def test_w271_reply_email_not_found(client):
    r = await client.post("/api/email-inbox-v2/nonexistent-id/reply", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w271_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/email-inbox-v2", json={'thread_id': 'test-thread_id', 'subject': 'test-subject', 'sender': 'test-sender', 'recipients': [], 'body': 'test-body', 'attachments': [], 'is_approval_reply': True, 'approval_decision': 'test-approval_decision', 'parsed_content': {}, 'thread_position': 1, 'read': True, 'status': 'test-status', 'received_at': 'test-received_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "email_inbox_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w271_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/email-inbox-v2", json={'thread_id': 'test-thread_id', 'subject': 'test-subject', 'sender': 'test-sender', 'recipients': [], 'body': 'test-body', 'attachments': [], 'is_approval_reply': True, 'approval_decision': 'test-approval_decision', 'parsed_content': {}, 'thread_position': 1, 'read': True, 'status': 'test-status', 'received_at': 'test-received_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/email-inbox-v2", json={'thread_id': 'test-thread_id', 'subject': 'test-subject', 'sender': 'test-sender', 'recipients': [], 'body': 'test-body', 'attachments': [], 'is_approval_reply': True, 'approval_decision': 'test-approval_decision', 'parsed_content': {}, 'thread_position': 1, 'read': True, 'status': 'test-status', 'received_at': 'test-received_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "email_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w271_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/email-inbox-v2", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w271_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/email-inbox-v2", json={'thread_id': 'test-thread_id', 'subject': 'test-subject', 'sender': 'test-sender', 'recipients': [], 'body': 'test-body', 'attachments': [], 'is_approval_reply': True, 'approval_decision': 'test-approval_decision', 'parsed_content': {}, 'thread_position': 1, 'read': True, 'status': 'test-status', 'received_at': 'test-received_at'})
    assert r1.status_code == 201
    item_id = r1.json()["email_id"]
    r2 = await client.get("/api/email-inbox-v2")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/email-inbox-v2/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["email_id"] == item_id
