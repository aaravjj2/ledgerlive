"""Tests for Wave 200: Submission Hardening v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w200_submit_all import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w200_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w200_create(client):
    r = await client.post("/api/submit-all", json={'check_type': 'test-check_type', 'target': 'test-target', 'make_targets_valid': True, 'doc_commands_valid': True, 'index_generated': True, 'tour_duration_s': 1.0, 'determinism_pass': True, 'twice_run_hash_1': 'test-twice_run_hash_1', 'twice_run_hash_2': 'test-twice_run_hash_2', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r.status_code == 201
    data = r.json()
    assert "submission_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w200_list(client):
    await client.post("/api/submit-all", json={'check_type': 'test-check_type', 'target': 'test-target', 'make_targets_valid': True, 'doc_commands_valid': True, 'index_generated': True, 'tour_duration_s': 1.0, 'determinism_pass': True, 'twice_run_hash_1': 'test-twice_run_hash_1', 'twice_run_hash_2': 'test-twice_run_hash_2', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    await client.post("/api/submit-all", json={'check_type': 'test-check_type', 'target': 'test-target', 'make_targets_valid': True, 'doc_commands_valid': True, 'index_generated': True, 'tour_duration_s': 1.0, 'determinism_pass': True, 'twice_run_hash_1': 'test-twice_run_hash_1', 'twice_run_hash_2': 'test-twice_run_hash_2', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    r = await client.get("/api/submit-all")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w200_get_by_id(client):
    r = await client.post("/api/submit-all", json={'check_type': 'test-check_type', 'target': 'test-target', 'make_targets_valid': True, 'doc_commands_valid': True, 'index_generated': True, 'tour_duration_s': 1.0, 'determinism_pass': True, 'twice_run_hash_1': 'test-twice_run_hash_1', 'twice_run_hash_2': 'test-twice_run_hash_2', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["submission_id"]
    r2 = await client.get(f"/api/submit-all/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["submission_id"] == item_id

@pytest.mark.asyncio
async def test_w200_get_not_found(client):
    r = await client.get("/api/submit-all/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w200_verify_docs(client):
    r = await client.post("/api/submit-all", json={'check_type': 'test-check_type', 'target': 'test-target', 'make_targets_valid': True, 'doc_commands_valid': True, 'index_generated': True, 'tour_duration_s': 1.0, 'determinism_pass': True, 'twice_run_hash_1': 'test-twice_run_hash_1', 'twice_run_hash_2': 'test-twice_run_hash_2', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["submission_id"]
    r2 = await client.post(f"/api/submit-all/{item_id}/docs", json={})
    assert r2.status_code == 200
    assert r2.json()["submission_id"] == item_id

@pytest.mark.asyncio
async def test_w200_verify_determinism(client):
    r = await client.post("/api/submit-all", json={'check_type': 'test-check_type', 'target': 'test-target', 'make_targets_valid': True, 'doc_commands_valid': True, 'index_generated': True, 'tour_duration_s': 1.0, 'determinism_pass': True, 'twice_run_hash_1': 'test-twice_run_hash_1', 'twice_run_hash_2': 'test-twice_run_hash_2', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["submission_id"]
    r2 = await client.post(f"/api/submit-all/{item_id}/determinism", json={})
    assert r2.status_code == 200
    assert r2.json()["submission_id"] == item_id

@pytest.mark.asyncio
async def test_w200_verify_docs_not_found(client):
    r = await client.post("/api/submit-all/nonexistent-id/docs", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w200_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/submit-all", json={'check_type': 'test-check_type', 'target': 'test-target', 'make_targets_valid': True, 'doc_commands_valid': True, 'index_generated': True, 'tour_duration_s': 1.0, 'determinism_pass': True, 'twice_run_hash_1': 'test-twice_run_hash_1', 'twice_run_hash_2': 'test-twice_run_hash_2', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "submit_all"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w200_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/submit-all", json={'check_type': 'test-check_type', 'target': 'test-target', 'make_targets_valid': True, 'doc_commands_valid': True, 'index_generated': True, 'tour_duration_s': 1.0, 'determinism_pass': True, 'twice_run_hash_1': 'test-twice_run_hash_1', 'twice_run_hash_2': 'test-twice_run_hash_2', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/submit-all", json={'check_type': 'test-check_type', 'target': 'test-target', 'make_targets_valid': True, 'doc_commands_valid': True, 'index_generated': True, 'tour_duration_s': 1.0, 'determinism_pass': True, 'twice_run_hash_1': 'test-twice_run_hash_1', 'twice_run_hash_2': 'test-twice_run_hash_2', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "submission_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w200_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/submit-all", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w200_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/submit-all", json={'check_type': 'test-check_type', 'target': 'test-target', 'make_targets_valid': True, 'doc_commands_valid': True, 'index_generated': True, 'tour_duration_s': 1.0, 'determinism_pass': True, 'twice_run_hash_1': 'test-twice_run_hash_1', 'twice_run_hash_2': 'test-twice_run_hash_2', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r1.status_code == 201
    item_id = r1.json()["submission_id"]
    r2 = await client.get("/api/submit-all")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/submit-all/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["submission_id"] == item_id
