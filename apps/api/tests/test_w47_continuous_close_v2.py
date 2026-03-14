"""Tests for Wave 47: Continuous Close 2.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w47_continuous_close_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w47_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w47_create(client):
    r = await client.post("/api/continuous-close-v2/jobs", json={'job_type': 'test-job_type', 'period_id': 'test-period_id', 'status': 'test-status', 'progress_pct': 1.0, 'exceptions_found': 1, 'resumable': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'paused_at': 'test-paused_at', 'completed_at': 'test-completed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "job_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w47_list(client):
    await client.post("/api/continuous-close-v2/jobs", json={'job_type': 'test-job_type', 'period_id': 'test-period_id', 'status': 'test-status', 'progress_pct': 1.0, 'exceptions_found': 1, 'resumable': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'paused_at': 'test-paused_at', 'completed_at': 'test-completed_at'})
    await client.post("/api/continuous-close-v2/jobs", json={'job_type': 'test-job_type', 'period_id': 'test-period_id', 'status': 'test-status', 'progress_pct': 1.0, 'exceptions_found': 1, 'resumable': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'paused_at': 'test-paused_at', 'completed_at': 'test-completed_at'})
    r = await client.get("/api/continuous-close-v2/jobs")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w47_get_by_id(client):
    r = await client.post("/api/continuous-close-v2/jobs", json={'job_type': 'test-job_type', 'period_id': 'test-period_id', 'status': 'test-status', 'progress_pct': 1.0, 'exceptions_found': 1, 'resumable': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'paused_at': 'test-paused_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["job_id"]
    r2 = await client.get(f"/api/continuous-close-v2/jobs/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["job_id"] == item_id

@pytest.mark.asyncio
async def test_w47_get_not_found(client):
    r = await client.get("/api/continuous-close-v2/jobs/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w47_pause_job(client):
    r = await client.post("/api/continuous-close-v2/jobs", json={'job_type': 'test-job_type', 'period_id': 'test-period_id', 'status': 'test-status', 'progress_pct': 1.0, 'exceptions_found': 1, 'resumable': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'paused_at': 'test-paused_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["job_id"]
    r2 = await client.post(f"/api/continuous-close-v2/jobs/{item_id}/pause", json={})
    assert r2.status_code == 200
    assert r2.json()["job_id"] == item_id

@pytest.mark.asyncio
async def test_w47_resume_job(client):
    r = await client.post("/api/continuous-close-v2/jobs", json={'job_type': 'test-job_type', 'period_id': 'test-period_id', 'status': 'test-status', 'progress_pct': 1.0, 'exceptions_found': 1, 'resumable': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'paused_at': 'test-paused_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["job_id"]
    r2 = await client.post(f"/api/continuous-close-v2/jobs/{item_id}/resume", json={})
    assert r2.status_code == 200
    assert r2.json()["job_id"] == item_id

@pytest.mark.asyncio
async def test_w47_cancel_job(client):
    r = await client.post("/api/continuous-close-v2/jobs", json={'job_type': 'test-job_type', 'period_id': 'test-period_id', 'status': 'test-status', 'progress_pct': 1.0, 'exceptions_found': 1, 'resumable': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'paused_at': 'test-paused_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["job_id"]
    r2 = await client.post(f"/api/continuous-close-v2/jobs/{item_id}/cancel", json={})
    assert r2.status_code == 200
    assert r2.json()["job_id"] == item_id

@pytest.mark.asyncio
async def test_w47_pause_job_not_found(client):
    r = await client.post("/api/continuous-close-v2/jobs/nonexistent-id/pause", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w47_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/continuous-close-v2/jobs", json={'job_type': 'test-job_type', 'period_id': 'test-period_id', 'status': 'test-status', 'progress_pct': 1.0, 'exceptions_found': 1, 'resumable': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'paused_at': 'test-paused_at', 'completed_at': 'test-completed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "continuous_close_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w47_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/continuous-close-v2/jobs", json={'job_type': 'test-job_type', 'period_id': 'test-period_id', 'status': 'test-status', 'progress_pct': 1.0, 'exceptions_found': 1, 'resumable': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'paused_at': 'test-paused_at', 'completed_at': 'test-completed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/continuous-close-v2/jobs", json={'job_type': 'test-job_type', 'period_id': 'test-period_id', 'status': 'test-status', 'progress_pct': 1.0, 'exceptions_found': 1, 'resumable': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'paused_at': 'test-paused_at', 'completed_at': 'test-completed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "job_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w47_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/continuous-close-v2/jobs", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w47_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/continuous-close-v2/jobs", json={'job_type': 'test-job_type', 'period_id': 'test-period_id', 'status': 'test-status', 'progress_pct': 1.0, 'exceptions_found': 1, 'resumable': True, 'idempotency_key': 'test-idempotency_key', 'started_at': 'test-started_at', 'paused_at': 'test-paused_at', 'completed_at': 'test-completed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["job_id"]
    r2 = await client.get("/api/continuous-close-v2/jobs")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/continuous-close-v2/jobs/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["job_id"] == item_id
