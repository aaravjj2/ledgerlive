"""Tests for Wave 14: Notification Service

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w14_notification import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w14_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w14_create(client):
    r = await client.post("/api/notifications", json={'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'status': 'test-status', 'sent_at': 'test-sent_at'})
    assert r.status_code == 201
    data = r.json()
    assert "notification_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w14_list(client):
    await client.post("/api/notifications", json={'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'status': 'test-status', 'sent_at': 'test-sent_at'})
    await client.post("/api/notifications", json={'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'status': 'test-status', 'sent_at': 'test-sent_at'})
    r = await client.get("/api/notifications")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w14_get_by_id(client):
    r = await client.post("/api/notifications", json={'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'status': 'test-status', 'sent_at': 'test-sent_at'})
    item_id = r.json()["notification_id"]
    r2 = await client.get(f"/api/notifications/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["notification_id"] == item_id

@pytest.mark.asyncio
async def test_w14_get_not_found(client):
    r = await client.get("/api/notifications/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w14_mark_read(client):
    r = await client.post("/api/notifications", json={'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'status': 'test-status', 'sent_at': 'test-sent_at'})
    item_id = r.json()["notification_id"]
    r2 = await client.post(f"/api/notifications/{item_id}/read", json={})
    assert r2.status_code == 200
    assert r2.json()["notification_id"] == item_id

@pytest.mark.asyncio
async def test_w14_mark_read_not_found(client):
    r = await client.post("/api/notifications/nonexistent-id/read", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w14_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/notifications", json={'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'status': 'test-status', 'sent_at': 'test-sent_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "notification"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w14_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/notifications", json={'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'status': 'test-status', 'sent_at': 'test-sent_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/notifications", json={'channel': 'test-channel', 'recipient': 'test-recipient', 'subject': 'test-subject', 'body': 'test-body', 'status': 'test-status', 'sent_at': 'test-sent_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "notification_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w14_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/notifications", json={})
    assert r.status_code == 201
