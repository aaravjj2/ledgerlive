"""Tests for Wave 192: Policy Engine v4

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w192_policy_engine import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w192_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w192_create(client):
    r = await client.post("/api/policy-engine", json={'tool_name': 'test-tool_name', 'role': 'test-role', 'scope': 'test-scope', 'data_sensitivity': 'test-data_sensitivity', 'approval_required': True, 'deny_reason': 'test-deny_reason', 'approved_by': 'test-approved_by', 'audit_trace_id': 'test-audit_trace_id', 'action_allowed': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "policy_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w192_list(client):
    await client.post("/api/policy-engine", json={'tool_name': 'test-tool_name', 'role': 'test-role', 'scope': 'test-scope', 'data_sensitivity': 'test-data_sensitivity', 'approval_required': True, 'deny_reason': 'test-deny_reason', 'approved_by': 'test-approved_by', 'audit_trace_id': 'test-audit_trace_id', 'action_allowed': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    await client.post("/api/policy-engine", json={'tool_name': 'test-tool_name', 'role': 'test-role', 'scope': 'test-scope', 'data_sensitivity': 'test-data_sensitivity', 'approval_required': True, 'deny_reason': 'test-deny_reason', 'approved_by': 'test-approved_by', 'audit_trace_id': 'test-audit_trace_id', 'action_allowed': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    r = await client.get("/api/policy-engine")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w192_get_by_id(client):
    r = await client.post("/api/policy-engine", json={'tool_name': 'test-tool_name', 'role': 'test-role', 'scope': 'test-scope', 'data_sensitivity': 'test-data_sensitivity', 'approval_required': True, 'deny_reason': 'test-deny_reason', 'approved_by': 'test-approved_by', 'audit_trace_id': 'test-audit_trace_id', 'action_allowed': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["policy_id"]
    r2 = await client.get(f"/api/policy-engine/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["policy_id"] == item_id

@pytest.mark.asyncio
async def test_w192_get_not_found(client):
    r = await client.get("/api/policy-engine/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w192_approve_action(client):
    r = await client.post("/api/policy-engine", json={'tool_name': 'test-tool_name', 'role': 'test-role', 'scope': 'test-scope', 'data_sensitivity': 'test-data_sensitivity', 'approval_required': True, 'deny_reason': 'test-deny_reason', 'approved_by': 'test-approved_by', 'audit_trace_id': 'test-audit_trace_id', 'action_allowed': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["policy_id"]
    r2 = await client.post(f"/api/policy-engine/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["policy_id"] == item_id

@pytest.mark.asyncio
async def test_w192_deny_action(client):
    r = await client.post("/api/policy-engine", json={'tool_name': 'test-tool_name', 'role': 'test-role', 'scope': 'test-scope', 'data_sensitivity': 'test-data_sensitivity', 'approval_required': True, 'deny_reason': 'test-deny_reason', 'approved_by': 'test-approved_by', 'audit_trace_id': 'test-audit_trace_id', 'action_allowed': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["policy_id"]
    r2 = await client.post(f"/api/policy-engine/{item_id}/deny", json={})
    assert r2.status_code == 200
    assert r2.json()["policy_id"] == item_id

@pytest.mark.asyncio
async def test_w192_check_scope(client):
    r = await client.post("/api/policy-engine", json={'tool_name': 'test-tool_name', 'role': 'test-role', 'scope': 'test-scope', 'data_sensitivity': 'test-data_sensitivity', 'approval_required': True, 'deny_reason': 'test-deny_reason', 'approved_by': 'test-approved_by', 'audit_trace_id': 'test-audit_trace_id', 'action_allowed': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["policy_id"]
    r2 = await client.post(f"/api/policy-engine/{item_id}/scope", json={})
    assert r2.status_code == 200
    assert r2.json()["policy_id"] == item_id

@pytest.mark.asyncio
async def test_w192_approve_action_not_found(client):
    r = await client.post("/api/policy-engine/nonexistent-id/approve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w192_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/policy-engine", json={'tool_name': 'test-tool_name', 'role': 'test-role', 'scope': 'test-scope', 'data_sensitivity': 'test-data_sensitivity', 'approval_required': True, 'deny_reason': 'test-deny_reason', 'approved_by': 'test-approved_by', 'audit_trace_id': 'test-audit_trace_id', 'action_allowed': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "policy_engine"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w192_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/policy-engine", json={'tool_name': 'test-tool_name', 'role': 'test-role', 'scope': 'test-scope', 'data_sensitivity': 'test-data_sensitivity', 'approval_required': True, 'deny_reason': 'test-deny_reason', 'approved_by': 'test-approved_by', 'audit_trace_id': 'test-audit_trace_id', 'action_allowed': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/policy-engine", json={'tool_name': 'test-tool_name', 'role': 'test-role', 'scope': 'test-scope', 'data_sensitivity': 'test-data_sensitivity', 'approval_required': True, 'deny_reason': 'test-deny_reason', 'approved_by': 'test-approved_by', 'audit_trace_id': 'test-audit_trace_id', 'action_allowed': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "policy_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w192_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/policy-engine", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w192_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/policy-engine", json={'tool_name': 'test-tool_name', 'role': 'test-role', 'scope': 'test-scope', 'data_sensitivity': 'test-data_sensitivity', 'approval_required': True, 'deny_reason': 'test-deny_reason', 'approved_by': 'test-approved_by', 'audit_trace_id': 'test-audit_trace_id', 'action_allowed': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["policy_id"]
    r2 = await client.get("/api/policy-engine")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/policy-engine/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["policy_id"] == item_id
