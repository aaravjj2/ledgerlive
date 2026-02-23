"""Tests for Wave 208: Fail-Closed Posture v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w208_fail_closed import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w208_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w208_create(client):
    r = await client.post("/api/fail-closed", json={'action_type': 'test-action_type', 'verifier_result': 'test-verifier_result', 'evidence_present': True, 'invariants_proven': True, 'fail_closed_triggered': True, 'approval_required': True, 'blocked': True, 'reason': 'test-reason', 'fallback_decision': 'test-fallback_decision', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "posture_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w208_list(client):
    await client.post("/api/fail-closed", json={'action_type': 'test-action_type', 'verifier_result': 'test-verifier_result', 'evidence_present': True, 'invariants_proven': True, 'fail_closed_triggered': True, 'approval_required': True, 'blocked': True, 'reason': 'test-reason', 'fallback_decision': 'test-fallback_decision', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    await client.post("/api/fail-closed", json={'action_type': 'test-action_type', 'verifier_result': 'test-verifier_result', 'evidence_present': True, 'invariants_proven': True, 'fail_closed_triggered': True, 'approval_required': True, 'blocked': True, 'reason': 'test-reason', 'fallback_decision': 'test-fallback_decision', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    r = await client.get("/api/fail-closed")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w208_get_by_id(client):
    r = await client.post("/api/fail-closed", json={'action_type': 'test-action_type', 'verifier_result': 'test-verifier_result', 'evidence_present': True, 'invariants_proven': True, 'fail_closed_triggered': True, 'approval_required': True, 'blocked': True, 'reason': 'test-reason', 'fallback_decision': 'test-fallback_decision', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["posture_id"]
    r2 = await client.get(f"/api/fail-closed/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["posture_id"] == item_id

@pytest.mark.asyncio
async def test_w208_get_not_found(client):
    r = await client.get("/api/fail-closed/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w208_trigger_fail_closed(client):
    r = await client.post("/api/fail-closed", json={'action_type': 'test-action_type', 'verifier_result': 'test-verifier_result', 'evidence_present': True, 'invariants_proven': True, 'fail_closed_triggered': True, 'approval_required': True, 'blocked': True, 'reason': 'test-reason', 'fallback_decision': 'test-fallback_decision', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["posture_id"]
    r2 = await client.post(f"/api/fail-closed/{item_id}/trigger", json={})
    assert r2.status_code == 200
    assert r2.json()["posture_id"] == item_id

@pytest.mark.asyncio
async def test_w208_verify_blocked(client):
    r = await client.post("/api/fail-closed", json={'action_type': 'test-action_type', 'verifier_result': 'test-verifier_result', 'evidence_present': True, 'invariants_proven': True, 'fail_closed_triggered': True, 'approval_required': True, 'blocked': True, 'reason': 'test-reason', 'fallback_decision': 'test-fallback_decision', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["posture_id"]
    r2 = await client.post(f"/api/fail-closed/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["posture_id"] == item_id

@pytest.mark.asyncio
async def test_w208_trigger_fail_closed_not_found(client):
    r = await client.post("/api/fail-closed/nonexistent-id/trigger", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w208_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/fail-closed", json={'action_type': 'test-action_type', 'verifier_result': 'test-verifier_result', 'evidence_present': True, 'invariants_proven': True, 'fail_closed_triggered': True, 'approval_required': True, 'blocked': True, 'reason': 'test-reason', 'fallback_decision': 'test-fallback_decision', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "fail_closed"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w208_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/fail-closed", json={'action_type': 'test-action_type', 'verifier_result': 'test-verifier_result', 'evidence_present': True, 'invariants_proven': True, 'fail_closed_triggered': True, 'approval_required': True, 'blocked': True, 'reason': 'test-reason', 'fallback_decision': 'test-fallback_decision', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/fail-closed", json={'action_type': 'test-action_type', 'verifier_result': 'test-verifier_result', 'evidence_present': True, 'invariants_proven': True, 'fail_closed_triggered': True, 'approval_required': True, 'blocked': True, 'reason': 'test-reason', 'fallback_decision': 'test-fallback_decision', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "posture_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w208_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/fail-closed", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w208_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/fail-closed", json={'action_type': 'test-action_type', 'verifier_result': 'test-verifier_result', 'evidence_present': True, 'invariants_proven': True, 'fail_closed_triggered': True, 'approval_required': True, 'blocked': True, 'reason': 'test-reason', 'fallback_decision': 'test-fallback_decision', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["posture_id"]
    r2 = await client.get("/api/fail-closed")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/fail-closed/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["posture_id"] == item_id
