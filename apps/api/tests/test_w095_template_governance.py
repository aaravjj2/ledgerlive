"""Tests for Wave 95: Template Governance

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w095_template_governance import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w095_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w095_create(client):
    r = await client.post("/api/template-governance", json={'template_id': 'test-template_id', 'template_type': 'test-template_type', 'requested_by': 'test-requested_by', 'approved_by': 'test-approved_by', 'governance_action': 'test-governance_action', 'rbac_role_required': 'test-rbac_role_required', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "governance_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w095_list(client):
    await client.post("/api/template-governance", json={'template_id': 'test-template_id', 'template_type': 'test-template_type', 'requested_by': 'test-requested_by', 'approved_by': 'test-approved_by', 'governance_action': 'test-governance_action', 'rbac_role_required': 'test-rbac_role_required', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/template-governance", json={'template_id': 'test-template_id', 'template_type': 'test-template_type', 'requested_by': 'test-requested_by', 'approved_by': 'test-approved_by', 'governance_action': 'test-governance_action', 'rbac_role_required': 'test-rbac_role_required', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/template-governance")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w095_get_by_id(client):
    r = await client.post("/api/template-governance", json={'template_id': 'test-template_id', 'template_type': 'test-template_type', 'requested_by': 'test-requested_by', 'approved_by': 'test-approved_by', 'governance_action': 'test-governance_action', 'rbac_role_required': 'test-rbac_role_required', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["governance_id"]
    r2 = await client.get(f"/api/template-governance/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["governance_id"] == item_id

@pytest.mark.asyncio
async def test_w095_get_not_found(client):
    r = await client.get("/api/template-governance/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w095_approve(client):
    r = await client.post("/api/template-governance", json={'template_id': 'test-template_id', 'template_type': 'test-template_type', 'requested_by': 'test-requested_by', 'approved_by': 'test-approved_by', 'governance_action': 'test-governance_action', 'rbac_role_required': 'test-rbac_role_required', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["governance_id"]
    r2 = await client.post(f"/api/template-governance/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["governance_id"] == item_id

@pytest.mark.asyncio
async def test_w095_deny(client):
    r = await client.post("/api/template-governance", json={'template_id': 'test-template_id', 'template_type': 'test-template_type', 'requested_by': 'test-requested_by', 'approved_by': 'test-approved_by', 'governance_action': 'test-governance_action', 'rbac_role_required': 'test-rbac_role_required', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["governance_id"]
    r2 = await client.post(f"/api/template-governance/{item_id}/deny", json={})
    assert r2.status_code == 200
    assert r2.json()["governance_id"] == item_id

@pytest.mark.asyncio
async def test_w095_approve_not_found(client):
    r = await client.post("/api/template-governance/nonexistent-id/approve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w095_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/template-governance", json={'template_id': 'test-template_id', 'template_type': 'test-template_type', 'requested_by': 'test-requested_by', 'approved_by': 'test-approved_by', 'governance_action': 'test-governance_action', 'rbac_role_required': 'test-rbac_role_required', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "template_governance"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w095_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/template-governance", json={'template_id': 'test-template_id', 'template_type': 'test-template_type', 'requested_by': 'test-requested_by', 'approved_by': 'test-approved_by', 'governance_action': 'test-governance_action', 'rbac_role_required': 'test-rbac_role_required', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/template-governance", json={'template_id': 'test-template_id', 'template_type': 'test-template_type', 'requested_by': 'test-requested_by', 'approved_by': 'test-approved_by', 'governance_action': 'test-governance_action', 'rbac_role_required': 'test-rbac_role_required', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "governance_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w095_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/template-governance", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w095_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/template-governance", json={'template_id': 'test-template_id', 'template_type': 'test-template_type', 'requested_by': 'test-requested_by', 'approved_by': 'test-approved_by', 'governance_action': 'test-governance_action', 'rbac_role_required': 'test-rbac_role_required', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["governance_id"]
    r2 = await client.get("/api/template-governance")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/template-governance/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["governance_id"] == item_id
