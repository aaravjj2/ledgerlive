"""Tests for Wave 127: Export Permission Gate

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w127_export_perm_gate import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w127_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w127_create(client):
    r = await client.post("/api/export-perm-gates", json={'export_type': 'test-export_type', 'requester': 'test-requester', 'permission_checked': True, 'allowed': True, 'deny_reason': 'test-deny_reason', 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r.status_code == 201
    data = r.json()
    assert "gate_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w127_list(client):
    await client.post("/api/export-perm-gates", json={'export_type': 'test-export_type', 'requester': 'test-requester', 'permission_checked': True, 'allowed': True, 'deny_reason': 'test-deny_reason', 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    await client.post("/api/export-perm-gates", json={'export_type': 'test-export_type', 'requester': 'test-requester', 'permission_checked': True, 'allowed': True, 'deny_reason': 'test-deny_reason', 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    r = await client.get("/api/export-perm-gates")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w127_get_by_id(client):
    r = await client.post("/api/export-perm-gates", json={'export_type': 'test-export_type', 'requester': 'test-requester', 'permission_checked': True, 'allowed': True, 'deny_reason': 'test-deny_reason', 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["gate_id"]
    r2 = await client.get(f"/api/export-perm-gates/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["gate_id"] == item_id

@pytest.mark.asyncio
async def test_w127_get_not_found(client):
    r = await client.get("/api/export-perm-gates/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w127_audit_access(client):
    r = await client.post("/api/export-perm-gates", json={'export_type': 'test-export_type', 'requester': 'test-requester', 'permission_checked': True, 'allowed': True, 'deny_reason': 'test-deny_reason', 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["gate_id"]
    r2 = await client.post(f"/api/export-perm-gates/{item_id}/audit", json={})
    assert r2.status_code == 200
    assert r2.json()["gate_id"] == item_id

@pytest.mark.asyncio
async def test_w127_audit_access_not_found(client):
    r = await client.post("/api/export-perm-gates/nonexistent-id/audit", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w127_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/export-perm-gates", json={'export_type': 'test-export_type', 'requester': 'test-requester', 'permission_checked': True, 'allowed': True, 'deny_reason': 'test-deny_reason', 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "export_perm_gate"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w127_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/export-perm-gates", json={'export_type': 'test-export_type', 'requester': 'test-requester', 'permission_checked': True, 'allowed': True, 'deny_reason': 'test-deny_reason', 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/export-perm-gates", json={'export_type': 'test-export_type', 'requester': 'test-requester', 'permission_checked': True, 'allowed': True, 'deny_reason': 'test-deny_reason', 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "gate_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w127_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/export-perm-gates", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w127_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/export-perm-gates", json={'export_type': 'test-export_type', 'requester': 'test-requester', 'permission_checked': True, 'allowed': True, 'deny_reason': 'test-deny_reason', 'audit_ref': 'test-audit_ref', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r1.status_code == 201
    item_id = r1.json()["gate_id"]
    r2 = await client.get("/api/export-perm-gates")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/export-perm-gates/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["gate_id"] == item_id
