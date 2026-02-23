"""Tests for Wave 165: Live Session Simulator

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w165_session_sim import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w165_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w165_create(client):
    r = await client.post("/api/session-sim", json={'session_name': 'test-session_name', 'transcript': [], 'tool_calls': [], 'verifier_outcomes': [], 'transcript_hash': 'test-transcript_hash', 'tool_trace_hash': 'test-tool_trace_hash', 'duration_ms': 1.0, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "session_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w165_list(client):
    await client.post("/api/session-sim", json={'session_name': 'test-session_name', 'transcript': [], 'tool_calls': [], 'verifier_outcomes': [], 'transcript_hash': 'test-transcript_hash', 'tool_trace_hash': 'test-tool_trace_hash', 'duration_ms': 1.0, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    await client.post("/api/session-sim", json={'session_name': 'test-session_name', 'transcript': [], 'tool_calls': [], 'verifier_outcomes': [], 'transcript_hash': 'test-transcript_hash', 'tool_trace_hash': 'test-tool_trace_hash', 'duration_ms': 1.0, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    r = await client.get("/api/session-sim")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w165_get_by_id(client):
    r = await client.post("/api/session-sim", json={'session_name': 'test-session_name', 'transcript': [], 'tool_calls': [], 'verifier_outcomes': [], 'transcript_hash': 'test-transcript_hash', 'tool_trace_hash': 'test-tool_trace_hash', 'duration_ms': 1.0, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["session_id"]
    r2 = await client.get(f"/api/session-sim/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["session_id"] == item_id

@pytest.mark.asyncio
async def test_w165_get_not_found(client):
    r = await client.get("/api/session-sim/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w165_advance_session(client):
    r = await client.post("/api/session-sim", json={'session_name': 'test-session_name', 'transcript': [], 'tool_calls': [], 'verifier_outcomes': [], 'transcript_hash': 'test-transcript_hash', 'tool_trace_hash': 'test-tool_trace_hash', 'duration_ms': 1.0, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["session_id"]
    r2 = await client.post(f"/api/session-sim/{item_id}/advance", json={})
    assert r2.status_code == 200
    assert r2.json()["session_id"] == item_id

@pytest.mark.asyncio
async def test_w165_complete_session(client):
    r = await client.post("/api/session-sim", json={'session_name': 'test-session_name', 'transcript': [], 'tool_calls': [], 'verifier_outcomes': [], 'transcript_hash': 'test-transcript_hash', 'tool_trace_hash': 'test-tool_trace_hash', 'duration_ms': 1.0, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["session_id"]
    r2 = await client.post(f"/api/session-sim/{item_id}/complete", json={})
    assert r2.status_code == 200
    assert r2.json()["session_id"] == item_id

@pytest.mark.asyncio
async def test_w165_advance_session_not_found(client):
    r = await client.post("/api/session-sim/nonexistent-id/advance", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w165_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/session-sim", json={'session_name': 'test-session_name', 'transcript': [], 'tool_calls': [], 'verifier_outcomes': [], 'transcript_hash': 'test-transcript_hash', 'tool_trace_hash': 'test-tool_trace_hash', 'duration_ms': 1.0, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "session_sim"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w165_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/session-sim", json={'session_name': 'test-session_name', 'transcript': [], 'tool_calls': [], 'verifier_outcomes': [], 'transcript_hash': 'test-transcript_hash', 'tool_trace_hash': 'test-tool_trace_hash', 'duration_ms': 1.0, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/session-sim", json={'session_name': 'test-session_name', 'transcript': [], 'tool_calls': [], 'verifier_outcomes': [], 'transcript_hash': 'test-transcript_hash', 'tool_trace_hash': 'test-tool_trace_hash', 'duration_ms': 1.0, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "session_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w165_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/session-sim", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w165_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/session-sim", json={'session_name': 'test-session_name', 'transcript': [], 'tool_calls': [], 'verifier_outcomes': [], 'transcript_hash': 'test-transcript_hash', 'tool_trace_hash': 'test-tool_trace_hash', 'duration_ms': 1.0, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["session_id"]
    r2 = await client.get("/api/session-sim")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/session-sim/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["session_id"] == item_id
