"""Tests for Wave 228: Close Checkpoint Manager v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w228_close_checkpoint import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w228_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w228_create(client):
    r = await client.post("/api/close-checkpoint", json={'checkpoint_name': 'test-checkpoint_name', 'period_id': 'test-period_id', 'gate_criteria': [], 'evidence_required': [], 'evidence_submitted': [], 'criteria_met': True, 'approved_by': 'test-approved_by', 'approval_timestamp': 'test-approval_timestamp', 'gate_result': 'test-gate_result', 'notes': 'test-notes', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "checkpoint_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w228_list(client):
    await client.post("/api/close-checkpoint", json={'checkpoint_name': 'test-checkpoint_name', 'period_id': 'test-period_id', 'gate_criteria': [], 'evidence_required': [], 'evidence_submitted': [], 'criteria_met': True, 'approved_by': 'test-approved_by', 'approval_timestamp': 'test-approval_timestamp', 'gate_result': 'test-gate_result', 'notes': 'test-notes', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    await client.post("/api/close-checkpoint", json={'checkpoint_name': 'test-checkpoint_name', 'period_id': 'test-period_id', 'gate_criteria': [], 'evidence_required': [], 'evidence_submitted': [], 'criteria_met': True, 'approved_by': 'test-approved_by', 'approval_timestamp': 'test-approval_timestamp', 'gate_result': 'test-gate_result', 'notes': 'test-notes', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    r = await client.get("/api/close-checkpoint")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w228_get_by_id(client):
    r = await client.post("/api/close-checkpoint", json={'checkpoint_name': 'test-checkpoint_name', 'period_id': 'test-period_id', 'gate_criteria': [], 'evidence_required': [], 'evidence_submitted': [], 'criteria_met': True, 'approved_by': 'test-approved_by', 'approval_timestamp': 'test-approval_timestamp', 'gate_result': 'test-gate_result', 'notes': 'test-notes', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["checkpoint_id"]
    r2 = await client.get(f"/api/close-checkpoint/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["checkpoint_id"] == item_id

@pytest.mark.asyncio
async def test_w228_get_not_found(client):
    r = await client.get("/api/close-checkpoint/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w228_evaluate_gate(client):
    r = await client.post("/api/close-checkpoint", json={'checkpoint_name': 'test-checkpoint_name', 'period_id': 'test-period_id', 'gate_criteria': [], 'evidence_required': [], 'evidence_submitted': [], 'criteria_met': True, 'approved_by': 'test-approved_by', 'approval_timestamp': 'test-approval_timestamp', 'gate_result': 'test-gate_result', 'notes': 'test-notes', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["checkpoint_id"]
    r2 = await client.post(f"/api/close-checkpoint/{item_id}/evaluate", json={})
    assert r2.status_code == 200
    assert r2.json()["checkpoint_id"] == item_id

@pytest.mark.asyncio
async def test_w228_submit_evidence(client):
    r = await client.post("/api/close-checkpoint", json={'checkpoint_name': 'test-checkpoint_name', 'period_id': 'test-period_id', 'gate_criteria': [], 'evidence_required': [], 'evidence_submitted': [], 'criteria_met': True, 'approved_by': 'test-approved_by', 'approval_timestamp': 'test-approval_timestamp', 'gate_result': 'test-gate_result', 'notes': 'test-notes', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["checkpoint_id"]
    r2 = await client.post(f"/api/close-checkpoint/{item_id}/evidence", json={})
    assert r2.status_code == 200
    assert r2.json()["checkpoint_id"] == item_id

@pytest.mark.asyncio
async def test_w228_approve_checkpoint(client):
    r = await client.post("/api/close-checkpoint", json={'checkpoint_name': 'test-checkpoint_name', 'period_id': 'test-period_id', 'gate_criteria': [], 'evidence_required': [], 'evidence_submitted': [], 'criteria_met': True, 'approved_by': 'test-approved_by', 'approval_timestamp': 'test-approval_timestamp', 'gate_result': 'test-gate_result', 'notes': 'test-notes', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["checkpoint_id"]
    r2 = await client.post(f"/api/close-checkpoint/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["checkpoint_id"] == item_id

@pytest.mark.asyncio
async def test_w228_evaluate_gate_not_found(client):
    r = await client.post("/api/close-checkpoint/nonexistent-id/evaluate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w228_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/close-checkpoint", json={'checkpoint_name': 'test-checkpoint_name', 'period_id': 'test-period_id', 'gate_criteria': [], 'evidence_required': [], 'evidence_submitted': [], 'criteria_met': True, 'approved_by': 'test-approved_by', 'approval_timestamp': 'test-approval_timestamp', 'gate_result': 'test-gate_result', 'notes': 'test-notes', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "close_checkpoint"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w228_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/close-checkpoint", json={'checkpoint_name': 'test-checkpoint_name', 'period_id': 'test-period_id', 'gate_criteria': [], 'evidence_required': [], 'evidence_submitted': [], 'criteria_met': True, 'approved_by': 'test-approved_by', 'approval_timestamp': 'test-approval_timestamp', 'gate_result': 'test-gate_result', 'notes': 'test-notes', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/close-checkpoint", json={'checkpoint_name': 'test-checkpoint_name', 'period_id': 'test-period_id', 'gate_criteria': [], 'evidence_required': [], 'evidence_submitted': [], 'criteria_met': True, 'approved_by': 'test-approved_by', 'approval_timestamp': 'test-approval_timestamp', 'gate_result': 'test-gate_result', 'notes': 'test-notes', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "checkpoint_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w228_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/close-checkpoint", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w228_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/close-checkpoint", json={'checkpoint_name': 'test-checkpoint_name', 'period_id': 'test-period_id', 'gate_criteria': [], 'evidence_required': [], 'evidence_submitted': [], 'criteria_met': True, 'approved_by': 'test-approved_by', 'approval_timestamp': 'test-approval_timestamp', 'gate_result': 'test-gate_result', 'notes': 'test-notes', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["checkpoint_id"]
    r2 = await client.get("/api/close-checkpoint")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/close-checkpoint/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["checkpoint_id"] == item_id
