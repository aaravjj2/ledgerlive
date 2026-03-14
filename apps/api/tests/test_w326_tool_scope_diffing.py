"""Tests for Wave 326: Tool Scope Diffing v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w326_tool_scope_diffing import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w326_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w326_create(client):
    r = await client.post("/api/tool-scope-diffing", json={'tool_ref': 'test-tool_ref', 'scope_before': [], 'scope_after': [], 'added_scopes': [], 'removed_scopes': [], 'expansion_detected': True, 'approval_required': True, 'approved_by': 'test-approved_by', 'audit_ref': 'test-audit_ref', 'deterministic': True, 'status': 'test-status', 'diffed_at': 'test-diffed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "diff_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w326_list(client):
    await client.post("/api/tool-scope-diffing", json={'tool_ref': 'test-tool_ref', 'scope_before': [], 'scope_after': [], 'added_scopes': [], 'removed_scopes': [], 'expansion_detected': True, 'approval_required': True, 'approved_by': 'test-approved_by', 'audit_ref': 'test-audit_ref', 'deterministic': True, 'status': 'test-status', 'diffed_at': 'test-diffed_at'})
    await client.post("/api/tool-scope-diffing", json={'tool_ref': 'test-tool_ref', 'scope_before': [], 'scope_after': [], 'added_scopes': [], 'removed_scopes': [], 'expansion_detected': True, 'approval_required': True, 'approved_by': 'test-approved_by', 'audit_ref': 'test-audit_ref', 'deterministic': True, 'status': 'test-status', 'diffed_at': 'test-diffed_at'})
    r = await client.get("/api/tool-scope-diffing")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w326_get_by_id(client):
    r = await client.post("/api/tool-scope-diffing", json={'tool_ref': 'test-tool_ref', 'scope_before': [], 'scope_after': [], 'added_scopes': [], 'removed_scopes': [], 'expansion_detected': True, 'approval_required': True, 'approved_by': 'test-approved_by', 'audit_ref': 'test-audit_ref', 'deterministic': True, 'status': 'test-status', 'diffed_at': 'test-diffed_at'})
    item_id = r.json()["diff_id"]
    r2 = await client.get(f"/api/tool-scope-diffing/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["diff_id"] == item_id

@pytest.mark.asyncio
async def test_w326_get_not_found(client):
    r = await client.get("/api/tool-scope-diffing/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w326_approve_expansion(client):
    r = await client.post("/api/tool-scope-diffing", json={'tool_ref': 'test-tool_ref', 'scope_before': [], 'scope_after': [], 'added_scopes': [], 'removed_scopes': [], 'expansion_detected': True, 'approval_required': True, 'approved_by': 'test-approved_by', 'audit_ref': 'test-audit_ref', 'deterministic': True, 'status': 'test-status', 'diffed_at': 'test-diffed_at'})
    item_id = r.json()["diff_id"]
    r2 = await client.post(f"/api/tool-scope-diffing/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["diff_id"] == item_id

@pytest.mark.asyncio
async def test_w326_reject_expansion(client):
    r = await client.post("/api/tool-scope-diffing", json={'tool_ref': 'test-tool_ref', 'scope_before': [], 'scope_after': [], 'added_scopes': [], 'removed_scopes': [], 'expansion_detected': True, 'approval_required': True, 'approved_by': 'test-approved_by', 'audit_ref': 'test-audit_ref', 'deterministic': True, 'status': 'test-status', 'diffed_at': 'test-diffed_at'})
    item_id = r.json()["diff_id"]
    r2 = await client.post(f"/api/tool-scope-diffing/{item_id}/reject", json={})
    assert r2.status_code == 200
    assert r2.json()["diff_id"] == item_id

@pytest.mark.asyncio
async def test_w326_approve_expansion_not_found(client):
    r = await client.post("/api/tool-scope-diffing/nonexistent-id/approve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w326_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/tool-scope-diffing", json={'tool_ref': 'test-tool_ref', 'scope_before': [], 'scope_after': [], 'added_scopes': [], 'removed_scopes': [], 'expansion_detected': True, 'approval_required': True, 'approved_by': 'test-approved_by', 'audit_ref': 'test-audit_ref', 'deterministic': True, 'status': 'test-status', 'diffed_at': 'test-diffed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "tool_scope_diffing"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w326_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/tool-scope-diffing", json={'tool_ref': 'test-tool_ref', 'scope_before': [], 'scope_after': [], 'added_scopes': [], 'removed_scopes': [], 'expansion_detected': True, 'approval_required': True, 'approved_by': 'test-approved_by', 'audit_ref': 'test-audit_ref', 'deterministic': True, 'status': 'test-status', 'diffed_at': 'test-diffed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/tool-scope-diffing", json={'tool_ref': 'test-tool_ref', 'scope_before': [], 'scope_after': [], 'added_scopes': [], 'removed_scopes': [], 'expansion_detected': True, 'approval_required': True, 'approved_by': 'test-approved_by', 'audit_ref': 'test-audit_ref', 'deterministic': True, 'status': 'test-status', 'diffed_at': 'test-diffed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "diff_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w326_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/tool-scope-diffing", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w326_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/tool-scope-diffing", json={'tool_ref': 'test-tool_ref', 'scope_before': [], 'scope_after': [], 'added_scopes': [], 'removed_scopes': [], 'expansion_detected': True, 'approval_required': True, 'approved_by': 'test-approved_by', 'audit_ref': 'test-audit_ref', 'deterministic': True, 'status': 'test-status', 'diffed_at': 'test-diffed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["diff_id"]
    r2 = await client.get("/api/tool-scope-diffing")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/tool-scope-diffing/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["diff_id"] == item_id
