"""Tests for Wave 25: Data Privacy / GDPR

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w25_data_privacy import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w25_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w25_create(client):
    r = await client.post("/api/privacy/requests", json={'request_type': 'test-request_type', 'subject_email': 'test-subject_email', 'status': 'test-status', 'requested_at': 'test-requested_at', 'completed_at': 'test-completed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "request_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w25_list(client):
    await client.post("/api/privacy/requests", json={'request_type': 'test-request_type', 'subject_email': 'test-subject_email', 'status': 'test-status', 'requested_at': 'test-requested_at', 'completed_at': 'test-completed_at'})
    await client.post("/api/privacy/requests", json={'request_type': 'test-request_type', 'subject_email': 'test-subject_email', 'status': 'test-status', 'requested_at': 'test-requested_at', 'completed_at': 'test-completed_at'})
    r = await client.get("/api/privacy/requests")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w25_get_by_id(client):
    r = await client.post("/api/privacy/requests", json={'request_type': 'test-request_type', 'subject_email': 'test-subject_email', 'status': 'test-status', 'requested_at': 'test-requested_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["request_id"]
    r2 = await client.get(f"/api/privacy/requests/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["request_id"] == item_id

@pytest.mark.asyncio
async def test_w25_get_not_found(client):
    r = await client.get("/api/privacy/requests/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w25_process(client):
    r = await client.post("/api/privacy/requests", json={'request_type': 'test-request_type', 'subject_email': 'test-subject_email', 'status': 'test-status', 'requested_at': 'test-requested_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["request_id"]
    r2 = await client.post(f"/api/privacy/requests/{item_id}/process", json={})
    assert r2.status_code == 200
    assert r2.json()["request_id"] == item_id

@pytest.mark.asyncio
async def test_w25_process_not_found(client):
    r = await client.post("/api/privacy/requests/nonexistent-id/process", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w25_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/privacy/requests", json={'request_type': 'test-request_type', 'subject_email': 'test-subject_email', 'status': 'test-status', 'requested_at': 'test-requested_at', 'completed_at': 'test-completed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "data_privacy"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w25_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/privacy/requests", json={'request_type': 'test-request_type', 'subject_email': 'test-subject_email', 'status': 'test-status', 'requested_at': 'test-requested_at', 'completed_at': 'test-completed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/privacy/requests", json={'request_type': 'test-request_type', 'subject_email': 'test-subject_email', 'status': 'test-status', 'requested_at': 'test-requested_at', 'completed_at': 'test-completed_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "request_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w25_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/privacy/requests", json={})
    assert r.status_code == 201
