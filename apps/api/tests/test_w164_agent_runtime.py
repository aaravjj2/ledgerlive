"""Tests for Wave 164: Agent Runtime v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w164_agent_runtime import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w164_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w164_create(client):
    r = await client.post("/api/agent-runtime/actions", json={'action_type': 'test-action_type', 'proposed_by': 'test-proposed_by', 'target_entity': 'test-target_entity', 'payload': {}, 'verifier_result': {}, 'invariants_checked': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'execution_status': 'test-execution_status', 'reason_code': 'test-reason_code', 'evidence_links': [], 'trace_id': 'test-trace_id', 'proposed_at': 'test-proposed_at', 'executed_at': 'test-executed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "action_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w164_list(client):
    await client.post("/api/agent-runtime/actions", json={'action_type': 'test-action_type', 'proposed_by': 'test-proposed_by', 'target_entity': 'test-target_entity', 'payload': {}, 'verifier_result': {}, 'invariants_checked': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'execution_status': 'test-execution_status', 'reason_code': 'test-reason_code', 'evidence_links': [], 'trace_id': 'test-trace_id', 'proposed_at': 'test-proposed_at', 'executed_at': 'test-executed_at'})
    await client.post("/api/agent-runtime/actions", json={'action_type': 'test-action_type', 'proposed_by': 'test-proposed_by', 'target_entity': 'test-target_entity', 'payload': {}, 'verifier_result': {}, 'invariants_checked': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'execution_status': 'test-execution_status', 'reason_code': 'test-reason_code', 'evidence_links': [], 'trace_id': 'test-trace_id', 'proposed_at': 'test-proposed_at', 'executed_at': 'test-executed_at'})
    r = await client.get("/api/agent-runtime/actions")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w164_get_by_id(client):
    r = await client.post("/api/agent-runtime/actions", json={'action_type': 'test-action_type', 'proposed_by': 'test-proposed_by', 'target_entity': 'test-target_entity', 'payload': {}, 'verifier_result': {}, 'invariants_checked': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'execution_status': 'test-execution_status', 'reason_code': 'test-reason_code', 'evidence_links': [], 'trace_id': 'test-trace_id', 'proposed_at': 'test-proposed_at', 'executed_at': 'test-executed_at'})
    item_id = r.json()["action_id"]
    r2 = await client.get(f"/api/agent-runtime/actions/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["action_id"] == item_id

@pytest.mark.asyncio
async def test_w164_get_not_found(client):
    r = await client.get("/api/agent-runtime/actions/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w164_verify_action(client):
    r = await client.post("/api/agent-runtime/actions", json={'action_type': 'test-action_type', 'proposed_by': 'test-proposed_by', 'target_entity': 'test-target_entity', 'payload': {}, 'verifier_result': {}, 'invariants_checked': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'execution_status': 'test-execution_status', 'reason_code': 'test-reason_code', 'evidence_links': [], 'trace_id': 'test-trace_id', 'proposed_at': 'test-proposed_at', 'executed_at': 'test-executed_at'})
    item_id = r.json()["action_id"]
    r2 = await client.post(f"/api/agent-runtime/actions/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["action_id"] == item_id

@pytest.mark.asyncio
async def test_w164_approve_action(client):
    r = await client.post("/api/agent-runtime/actions", json={'action_type': 'test-action_type', 'proposed_by': 'test-proposed_by', 'target_entity': 'test-target_entity', 'payload': {}, 'verifier_result': {}, 'invariants_checked': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'execution_status': 'test-execution_status', 'reason_code': 'test-reason_code', 'evidence_links': [], 'trace_id': 'test-trace_id', 'proposed_at': 'test-proposed_at', 'executed_at': 'test-executed_at'})
    item_id = r.json()["action_id"]
    r2 = await client.post(f"/api/agent-runtime/actions/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["action_id"] == item_id

@pytest.mark.asyncio
async def test_w164_execute_action(client):
    r = await client.post("/api/agent-runtime/actions", json={'action_type': 'test-action_type', 'proposed_by': 'test-proposed_by', 'target_entity': 'test-target_entity', 'payload': {}, 'verifier_result': {}, 'invariants_checked': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'execution_status': 'test-execution_status', 'reason_code': 'test-reason_code', 'evidence_links': [], 'trace_id': 'test-trace_id', 'proposed_at': 'test-proposed_at', 'executed_at': 'test-executed_at'})
    item_id = r.json()["action_id"]
    r2 = await client.post(f"/api/agent-runtime/actions/{item_id}/execute", json={})
    assert r2.status_code == 200
    assert r2.json()["action_id"] == item_id

@pytest.mark.asyncio
async def test_w164_verify_action_not_found(client):
    r = await client.post("/api/agent-runtime/actions/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w164_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/agent-runtime/actions", json={'action_type': 'test-action_type', 'proposed_by': 'test-proposed_by', 'target_entity': 'test-target_entity', 'payload': {}, 'verifier_result': {}, 'invariants_checked': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'execution_status': 'test-execution_status', 'reason_code': 'test-reason_code', 'evidence_links': [], 'trace_id': 'test-trace_id', 'proposed_at': 'test-proposed_at', 'executed_at': 'test-executed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "agent_runtime"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w164_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/agent-runtime/actions", json={'action_type': 'test-action_type', 'proposed_by': 'test-proposed_by', 'target_entity': 'test-target_entity', 'payload': {}, 'verifier_result': {}, 'invariants_checked': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'execution_status': 'test-execution_status', 'reason_code': 'test-reason_code', 'evidence_links': [], 'trace_id': 'test-trace_id', 'proposed_at': 'test-proposed_at', 'executed_at': 'test-executed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/agent-runtime/actions", json={'action_type': 'test-action_type', 'proposed_by': 'test-proposed_by', 'target_entity': 'test-target_entity', 'payload': {}, 'verifier_result': {}, 'invariants_checked': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'execution_status': 'test-execution_status', 'reason_code': 'test-reason_code', 'evidence_links': [], 'trace_id': 'test-trace_id', 'proposed_at': 'test-proposed_at', 'executed_at': 'test-executed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "action_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w164_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/agent-runtime/actions", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w164_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/agent-runtime/actions", json={'action_type': 'test-action_type', 'proposed_by': 'test-proposed_by', 'target_entity': 'test-target_entity', 'payload': {}, 'verifier_result': {}, 'invariants_checked': [], 'approval_required': True, 'approved_by': 'test-approved_by', 'execution_status': 'test-execution_status', 'reason_code': 'test-reason_code', 'evidence_links': [], 'trace_id': 'test-trace_id', 'proposed_at': 'test-proposed_at', 'executed_at': 'test-executed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["action_id"]
    r2 = await client.get("/api/agent-runtime/actions")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/agent-runtime/actions/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["action_id"] == item_id
