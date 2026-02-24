"""Tests for Wave 226: Handoff Protocol v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w226_handoff_protocol import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w226_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w226_create(client):
    r = await client.post("/api/handoff-protocol", json={'from_team': 'test-from_team', 'to_team': 'test-to_team', 'task_id': 'test-task_id', 'evidence_refs': [], 'notes': 'test-notes', 'initiated_at': 'test-initiated_at', 'accepted_at': 'test-accepted_at', 'signed_off': True, 'sign_off_by': 'test-sign_off_by', 'handoff_hash': 'test-handoff_hash', 'status': 'test-status'})
    assert r.status_code == 201
    data = r.json()
    assert "handoff_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w226_list(client):
    await client.post("/api/handoff-protocol", json={'from_team': 'test-from_team', 'to_team': 'test-to_team', 'task_id': 'test-task_id', 'evidence_refs': [], 'notes': 'test-notes', 'initiated_at': 'test-initiated_at', 'accepted_at': 'test-accepted_at', 'signed_off': True, 'sign_off_by': 'test-sign_off_by', 'handoff_hash': 'test-handoff_hash', 'status': 'test-status'})
    await client.post("/api/handoff-protocol", json={'from_team': 'test-from_team', 'to_team': 'test-to_team', 'task_id': 'test-task_id', 'evidence_refs': [], 'notes': 'test-notes', 'initiated_at': 'test-initiated_at', 'accepted_at': 'test-accepted_at', 'signed_off': True, 'sign_off_by': 'test-sign_off_by', 'handoff_hash': 'test-handoff_hash', 'status': 'test-status'})
    r = await client.get("/api/handoff-protocol")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w226_get_by_id(client):
    r = await client.post("/api/handoff-protocol", json={'from_team': 'test-from_team', 'to_team': 'test-to_team', 'task_id': 'test-task_id', 'evidence_refs': [], 'notes': 'test-notes', 'initiated_at': 'test-initiated_at', 'accepted_at': 'test-accepted_at', 'signed_off': True, 'sign_off_by': 'test-sign_off_by', 'handoff_hash': 'test-handoff_hash', 'status': 'test-status'})
    item_id = r.json()["handoff_id"]
    r2 = await client.get(f"/api/handoff-protocol/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["handoff_id"] == item_id

@pytest.mark.asyncio
async def test_w226_get_not_found(client):
    r = await client.get("/api/handoff-protocol/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w226_accept_handoff(client):
    r = await client.post("/api/handoff-protocol", json={'from_team': 'test-from_team', 'to_team': 'test-to_team', 'task_id': 'test-task_id', 'evidence_refs': [], 'notes': 'test-notes', 'initiated_at': 'test-initiated_at', 'accepted_at': 'test-accepted_at', 'signed_off': True, 'sign_off_by': 'test-sign_off_by', 'handoff_hash': 'test-handoff_hash', 'status': 'test-status'})
    item_id = r.json()["handoff_id"]
    r2 = await client.post(f"/api/handoff-protocol/{item_id}/accept", json={})
    assert r2.status_code == 200
    assert r2.json()["handoff_id"] == item_id

@pytest.mark.asyncio
async def test_w226_sign_off(client):
    r = await client.post("/api/handoff-protocol", json={'from_team': 'test-from_team', 'to_team': 'test-to_team', 'task_id': 'test-task_id', 'evidence_refs': [], 'notes': 'test-notes', 'initiated_at': 'test-initiated_at', 'accepted_at': 'test-accepted_at', 'signed_off': True, 'sign_off_by': 'test-sign_off_by', 'handoff_hash': 'test-handoff_hash', 'status': 'test-status'})
    item_id = r.json()["handoff_id"]
    r2 = await client.post(f"/api/handoff-protocol/{item_id}/signoff", json={})
    assert r2.status_code == 200
    assert r2.json()["handoff_id"] == item_id

@pytest.mark.asyncio
async def test_w226_accept_handoff_not_found(client):
    r = await client.post("/api/handoff-protocol/nonexistent-id/accept", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w226_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/handoff-protocol", json={'from_team': 'test-from_team', 'to_team': 'test-to_team', 'task_id': 'test-task_id', 'evidence_refs': [], 'notes': 'test-notes', 'initiated_at': 'test-initiated_at', 'accepted_at': 'test-accepted_at', 'signed_off': True, 'sign_off_by': 'test-sign_off_by', 'handoff_hash': 'test-handoff_hash', 'status': 'test-status'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "handoff_protocol"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w226_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/handoff-protocol", json={'from_team': 'test-from_team', 'to_team': 'test-to_team', 'task_id': 'test-task_id', 'evidence_refs': [], 'notes': 'test-notes', 'initiated_at': 'test-initiated_at', 'accepted_at': 'test-accepted_at', 'signed_off': True, 'sign_off_by': 'test-sign_off_by', 'handoff_hash': 'test-handoff_hash', 'status': 'test-status'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/handoff-protocol", json={'from_team': 'test-from_team', 'to_team': 'test-to_team', 'task_id': 'test-task_id', 'evidence_refs': [], 'notes': 'test-notes', 'initiated_at': 'test-initiated_at', 'accepted_at': 'test-accepted_at', 'signed_off': True, 'sign_off_by': 'test-sign_off_by', 'handoff_hash': 'test-handoff_hash', 'status': 'test-status'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "handoff_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w226_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/handoff-protocol", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w226_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/handoff-protocol", json={'from_team': 'test-from_team', 'to_team': 'test-to_team', 'task_id': 'test-task_id', 'evidence_refs': [], 'notes': 'test-notes', 'initiated_at': 'test-initiated_at', 'accepted_at': 'test-accepted_at', 'signed_off': True, 'sign_off_by': 'test-sign_off_by', 'handoff_hash': 'test-handoff_hash', 'status': 'test-status'})
    assert r1.status_code == 201
    item_id = r1.json()["handoff_id"]
    r2 = await client.get("/api/handoff-protocol")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/handoff-protocol/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["handoff_id"] == item_id
