"""Tests for Wave 183: Session Interruption Resume Safety

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w183_session_resume import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w183_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w183_create(client):
    r = await client.post("/api/session-resume", json={'session_id': 'test-session_id', 'job_id': 'test-job_id', 'idempotency_key': 'test-idempotency_key', 'checkpoint_index': 1, 'total_steps': 1, 'side_effects_count': 1, 'binder_hash': 'test-binder_hash', 'interrupted': True, 'resumed_from': 1, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "resume_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w183_list(client):
    await client.post("/api/session-resume", json={'session_id': 'test-session_id', 'job_id': 'test-job_id', 'idempotency_key': 'test-idempotency_key', 'checkpoint_index': 1, 'total_steps': 1, 'side_effects_count': 1, 'binder_hash': 'test-binder_hash', 'interrupted': True, 'resumed_from': 1, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/session-resume", json={'session_id': 'test-session_id', 'job_id': 'test-job_id', 'idempotency_key': 'test-idempotency_key', 'checkpoint_index': 1, 'total_steps': 1, 'side_effects_count': 1, 'binder_hash': 'test-binder_hash', 'interrupted': True, 'resumed_from': 1, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/session-resume")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w183_get_by_id(client):
    r = await client.post("/api/session-resume", json={'session_id': 'test-session_id', 'job_id': 'test-job_id', 'idempotency_key': 'test-idempotency_key', 'checkpoint_index': 1, 'total_steps': 1, 'side_effects_count': 1, 'binder_hash': 'test-binder_hash', 'interrupted': True, 'resumed_from': 1, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["resume_id"]
    r2 = await client.get(f"/api/session-resume/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["resume_id"] == item_id

@pytest.mark.asyncio
async def test_w183_get_not_found(client):
    r = await client.get("/api/session-resume/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w183_interrupt_session(client):
    r = await client.post("/api/session-resume", json={'session_id': 'test-session_id', 'job_id': 'test-job_id', 'idempotency_key': 'test-idempotency_key', 'checkpoint_index': 1, 'total_steps': 1, 'side_effects_count': 1, 'binder_hash': 'test-binder_hash', 'interrupted': True, 'resumed_from': 1, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["resume_id"]
    r2 = await client.post(f"/api/session-resume/{item_id}/interrupt", json={})
    assert r2.status_code == 200
    assert r2.json()["resume_id"] == item_id

@pytest.mark.asyncio
async def test_w183_resume_session(client):
    r = await client.post("/api/session-resume", json={'session_id': 'test-session_id', 'job_id': 'test-job_id', 'idempotency_key': 'test-idempotency_key', 'checkpoint_index': 1, 'total_steps': 1, 'side_effects_count': 1, 'binder_hash': 'test-binder_hash', 'interrupted': True, 'resumed_from': 1, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["resume_id"]
    r2 = await client.post(f"/api/session-resume/{item_id}/resume", json={})
    assert r2.status_code == 200
    assert r2.json()["resume_id"] == item_id

@pytest.mark.asyncio
async def test_w183_verify_idempotency(client):
    r = await client.post("/api/session-resume", json={'session_id': 'test-session_id', 'job_id': 'test-job_id', 'idempotency_key': 'test-idempotency_key', 'checkpoint_index': 1, 'total_steps': 1, 'side_effects_count': 1, 'binder_hash': 'test-binder_hash', 'interrupted': True, 'resumed_from': 1, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["resume_id"]
    r2 = await client.post(f"/api/session-resume/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["resume_id"] == item_id

@pytest.mark.asyncio
async def test_w183_interrupt_session_not_found(client):
    r = await client.post("/api/session-resume/nonexistent-id/interrupt", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w183_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/session-resume", json={'session_id': 'test-session_id', 'job_id': 'test-job_id', 'idempotency_key': 'test-idempotency_key', 'checkpoint_index': 1, 'total_steps': 1, 'side_effects_count': 1, 'binder_hash': 'test-binder_hash', 'interrupted': True, 'resumed_from': 1, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "session_resume"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w183_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/session-resume", json={'session_id': 'test-session_id', 'job_id': 'test-job_id', 'idempotency_key': 'test-idempotency_key', 'checkpoint_index': 1, 'total_steps': 1, 'side_effects_count': 1, 'binder_hash': 'test-binder_hash', 'interrupted': True, 'resumed_from': 1, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/session-resume", json={'session_id': 'test-session_id', 'job_id': 'test-job_id', 'idempotency_key': 'test-idempotency_key', 'checkpoint_index': 1, 'total_steps': 1, 'side_effects_count': 1, 'binder_hash': 'test-binder_hash', 'interrupted': True, 'resumed_from': 1, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "resume_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w183_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/session-resume", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w183_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/session-resume", json={'session_id': 'test-session_id', 'job_id': 'test-job_id', 'idempotency_key': 'test-idempotency_key', 'checkpoint_index': 1, 'total_steps': 1, 'side_effects_count': 1, 'binder_hash': 'test-binder_hash', 'interrupted': True, 'resumed_from': 1, 'final_hash': 'test-final_hash', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["resume_id"]
    r2 = await client.get("/api/session-resume")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/session-resume/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["resume_id"] == item_id
