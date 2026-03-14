"""Tests for Wave 167: Close Orchestrator Workflow v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w167_close_orchestrator import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w167_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w167_create(client):
    r = await client.post("/api/close-orchestrator/jobs", json={'workflow_name': 'test-workflow_name', 'dag_steps': [], 'current_step': 1, 'total_steps': 1, 'step_outputs': {}, 'binder_hash': 'test-binder_hash', 'board_pack_hash': 'test-board_pack_hash', 'resumable': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "job_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w167_list(client):
    await client.post("/api/close-orchestrator/jobs", json={'workflow_name': 'test-workflow_name', 'dag_steps': [], 'current_step': 1, 'total_steps': 1, 'step_outputs': {}, 'binder_hash': 'test-binder_hash', 'board_pack_hash': 'test-board_pack_hash', 'resumable': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    await client.post("/api/close-orchestrator/jobs", json={'workflow_name': 'test-workflow_name', 'dag_steps': [], 'current_step': 1, 'total_steps': 1, 'step_outputs': {}, 'binder_hash': 'test-binder_hash', 'board_pack_hash': 'test-board_pack_hash', 'resumable': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    r = await client.get("/api/close-orchestrator/jobs")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w167_get_by_id(client):
    r = await client.post("/api/close-orchestrator/jobs", json={'workflow_name': 'test-workflow_name', 'dag_steps': [], 'current_step': 1, 'total_steps': 1, 'step_outputs': {}, 'binder_hash': 'test-binder_hash', 'board_pack_hash': 'test-board_pack_hash', 'resumable': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["job_id"]
    r2 = await client.get(f"/api/close-orchestrator/jobs/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["job_id"] == item_id

@pytest.mark.asyncio
async def test_w167_get_not_found(client):
    r = await client.get("/api/close-orchestrator/jobs/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w167_advance_step(client):
    r = await client.post("/api/close-orchestrator/jobs", json={'workflow_name': 'test-workflow_name', 'dag_steps': [], 'current_step': 1, 'total_steps': 1, 'step_outputs': {}, 'binder_hash': 'test-binder_hash', 'board_pack_hash': 'test-board_pack_hash', 'resumable': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["job_id"]
    r2 = await client.post(f"/api/close-orchestrator/jobs/{item_id}/advance", json={})
    assert r2.status_code == 200
    assert r2.json()["job_id"] == item_id

@pytest.mark.asyncio
async def test_w167_resume_job(client):
    r = await client.post("/api/close-orchestrator/jobs", json={'workflow_name': 'test-workflow_name', 'dag_steps': [], 'current_step': 1, 'total_steps': 1, 'step_outputs': {}, 'binder_hash': 'test-binder_hash', 'board_pack_hash': 'test-board_pack_hash', 'resumable': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["job_id"]
    r2 = await client.post(f"/api/close-orchestrator/jobs/{item_id}/resume", json={})
    assert r2.status_code == 200
    assert r2.json()["job_id"] == item_id

@pytest.mark.asyncio
async def test_w167_verify_outputs(client):
    r = await client.post("/api/close-orchestrator/jobs", json={'workflow_name': 'test-workflow_name', 'dag_steps': [], 'current_step': 1, 'total_steps': 1, 'step_outputs': {}, 'binder_hash': 'test-binder_hash', 'board_pack_hash': 'test-board_pack_hash', 'resumable': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["job_id"]
    r2 = await client.post(f"/api/close-orchestrator/jobs/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["job_id"] == item_id

@pytest.mark.asyncio
async def test_w167_advance_step_not_found(client):
    r = await client.post("/api/close-orchestrator/jobs/nonexistent-id/advance", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w167_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/close-orchestrator/jobs", json={'workflow_name': 'test-workflow_name', 'dag_steps': [], 'current_step': 1, 'total_steps': 1, 'step_outputs': {}, 'binder_hash': 'test-binder_hash', 'board_pack_hash': 'test-board_pack_hash', 'resumable': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "close_orchestrator"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w167_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/close-orchestrator/jobs", json={'workflow_name': 'test-workflow_name', 'dag_steps': [], 'current_step': 1, 'total_steps': 1, 'step_outputs': {}, 'binder_hash': 'test-binder_hash', 'board_pack_hash': 'test-board_pack_hash', 'resumable': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/close-orchestrator/jobs", json={'workflow_name': 'test-workflow_name', 'dag_steps': [], 'current_step': 1, 'total_steps': 1, 'step_outputs': {}, 'binder_hash': 'test-binder_hash', 'board_pack_hash': 'test-board_pack_hash', 'resumable': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "job_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w167_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/close-orchestrator/jobs", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w167_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/close-orchestrator/jobs", json={'workflow_name': 'test-workflow_name', 'dag_steps': [], 'current_step': 1, 'total_steps': 1, 'step_outputs': {}, 'binder_hash': 'test-binder_hash', 'board_pack_hash': 'test-board_pack_hash', 'resumable': True, 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["job_id"]
    r2 = await client.get("/api/close-orchestrator/jobs")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/close-orchestrator/jobs/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["job_id"] == item_id
