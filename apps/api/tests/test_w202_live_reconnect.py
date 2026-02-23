"""Tests for Wave 202: Live Reconnect Buffering Resume v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w202_live_reconnect import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w202_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w202_create(client):
    r = await client.post("/api/live-reconnect", json={'session_id': 'test-session_id', 'resume_token': 'test-resume_token', 'buffer_size': 1, 'events_buffered': [], 'reconnect_count': 1, 'duplicate_calls_prevented': 1, 'protocol_version': 'test-protocol_version', 'schema_valid': True, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "reconnect_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w202_list(client):
    await client.post("/api/live-reconnect", json={'session_id': 'test-session_id', 'resume_token': 'test-resume_token', 'buffer_size': 1, 'events_buffered': [], 'reconnect_count': 1, 'duplicate_calls_prevented': 1, 'protocol_version': 'test-protocol_version', 'schema_valid': True, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/live-reconnect", json={'session_id': 'test-session_id', 'resume_token': 'test-resume_token', 'buffer_size': 1, 'events_buffered': [], 'reconnect_count': 1, 'duplicate_calls_prevented': 1, 'protocol_version': 'test-protocol_version', 'schema_valid': True, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/live-reconnect")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w202_get_by_id(client):
    r = await client.post("/api/live-reconnect", json={'session_id': 'test-session_id', 'resume_token': 'test-resume_token', 'buffer_size': 1, 'events_buffered': [], 'reconnect_count': 1, 'duplicate_calls_prevented': 1, 'protocol_version': 'test-protocol_version', 'schema_valid': True, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["reconnect_id"]
    r2 = await client.get(f"/api/live-reconnect/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["reconnect_id"] == item_id

@pytest.mark.asyncio
async def test_w202_get_not_found(client):
    r = await client.get("/api/live-reconnect/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w202_buffer_event(client):
    r = await client.post("/api/live-reconnect", json={'session_id': 'test-session_id', 'resume_token': 'test-resume_token', 'buffer_size': 1, 'events_buffered': [], 'reconnect_count': 1, 'duplicate_calls_prevented': 1, 'protocol_version': 'test-protocol_version', 'schema_valid': True, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["reconnect_id"]
    r2 = await client.post(f"/api/live-reconnect/{item_id}/buffer", json={})
    assert r2.status_code == 200
    assert r2.json()["reconnect_id"] == item_id

@pytest.mark.asyncio
async def test_w202_resume_session(client):
    r = await client.post("/api/live-reconnect", json={'session_id': 'test-session_id', 'resume_token': 'test-resume_token', 'buffer_size': 1, 'events_buffered': [], 'reconnect_count': 1, 'duplicate_calls_prevented': 1, 'protocol_version': 'test-protocol_version', 'schema_valid': True, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["reconnect_id"]
    r2 = await client.post(f"/api/live-reconnect/{item_id}/resume", json={})
    assert r2.status_code == 200
    assert r2.json()["reconnect_id"] == item_id

@pytest.mark.asyncio
async def test_w202_validate_protocol(client):
    r = await client.post("/api/live-reconnect", json={'session_id': 'test-session_id', 'resume_token': 'test-resume_token', 'buffer_size': 1, 'events_buffered': [], 'reconnect_count': 1, 'duplicate_calls_prevented': 1, 'protocol_version': 'test-protocol_version', 'schema_valid': True, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["reconnect_id"]
    r2 = await client.post(f"/api/live-reconnect/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["reconnect_id"] == item_id

@pytest.mark.asyncio
async def test_w202_buffer_event_not_found(client):
    r = await client.post("/api/live-reconnect/nonexistent-id/buffer", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w202_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/live-reconnect", json={'session_id': 'test-session_id', 'resume_token': 'test-resume_token', 'buffer_size': 1, 'events_buffered': [], 'reconnect_count': 1, 'duplicate_calls_prevented': 1, 'protocol_version': 'test-protocol_version', 'schema_valid': True, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "live_reconnect"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w202_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/live-reconnect", json={'session_id': 'test-session_id', 'resume_token': 'test-resume_token', 'buffer_size': 1, 'events_buffered': [], 'reconnect_count': 1, 'duplicate_calls_prevented': 1, 'protocol_version': 'test-protocol_version', 'schema_valid': True, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/live-reconnect", json={'session_id': 'test-session_id', 'resume_token': 'test-resume_token', 'buffer_size': 1, 'events_buffered': [], 'reconnect_count': 1, 'duplicate_calls_prevented': 1, 'protocol_version': 'test-protocol_version', 'schema_valid': True, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "reconnect_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w202_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/live-reconnect", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w202_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/live-reconnect", json={'session_id': 'test-session_id', 'resume_token': 'test-resume_token', 'buffer_size': 1, 'events_buffered': [], 'reconnect_count': 1, 'duplicate_calls_prevented': 1, 'protocol_version': 'test-protocol_version', 'schema_valid': True, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["reconnect_id"]
    r2 = await client.get("/api/live-reconnect")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/live-reconnect/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["reconnect_id"] == item_id
