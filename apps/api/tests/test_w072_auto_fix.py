"""Tests for Wave 72: Auto-Fix Actions

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w072_auto_fix import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w072_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w072_create(client):
    r = await client.post("/api/auto-fixes", json={'exception_id': 'test-exception_id', 'fix_type': 'test-fix_type', 'fix_payload': {}, 'requires_approval': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'audit_trail': [], 'applied_at': 'test-applied_at', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "fix_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w072_list(client):
    await client.post("/api/auto-fixes", json={'exception_id': 'test-exception_id', 'fix_type': 'test-fix_type', 'fix_payload': {}, 'requires_approval': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'audit_trail': [], 'applied_at': 'test-applied_at', 'created_at': 'test-created_at'})
    await client.post("/api/auto-fixes", json={'exception_id': 'test-exception_id', 'fix_type': 'test-fix_type', 'fix_payload': {}, 'requires_approval': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'audit_trail': [], 'applied_at': 'test-applied_at', 'created_at': 'test-created_at'})
    r = await client.get("/api/auto-fixes")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w072_get_by_id(client):
    r = await client.post("/api/auto-fixes", json={'exception_id': 'test-exception_id', 'fix_type': 'test-fix_type', 'fix_payload': {}, 'requires_approval': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'audit_trail': [], 'applied_at': 'test-applied_at', 'created_at': 'test-created_at'})
    item_id = r.json()["fix_id"]
    r2 = await client.get(f"/api/auto-fixes/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["fix_id"] == item_id

@pytest.mark.asyncio
async def test_w072_get_not_found(client):
    r = await client.get("/api/auto-fixes/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w072_approve_fix(client):
    r = await client.post("/api/auto-fixes", json={'exception_id': 'test-exception_id', 'fix_type': 'test-fix_type', 'fix_payload': {}, 'requires_approval': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'audit_trail': [], 'applied_at': 'test-applied_at', 'created_at': 'test-created_at'})
    item_id = r.json()["fix_id"]
    r2 = await client.post(f"/api/auto-fixes/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["fix_id"] == item_id

@pytest.mark.asyncio
async def test_w072_apply_fix(client):
    r = await client.post("/api/auto-fixes", json={'exception_id': 'test-exception_id', 'fix_type': 'test-fix_type', 'fix_payload': {}, 'requires_approval': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'audit_trail': [], 'applied_at': 'test-applied_at', 'created_at': 'test-created_at'})
    item_id = r.json()["fix_id"]
    r2 = await client.post(f"/api/auto-fixes/{item_id}/apply", json={})
    assert r2.status_code == 200
    assert r2.json()["fix_id"] == item_id

@pytest.mark.asyncio
async def test_w072_rollback_fix(client):
    r = await client.post("/api/auto-fixes", json={'exception_id': 'test-exception_id', 'fix_type': 'test-fix_type', 'fix_payload': {}, 'requires_approval': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'audit_trail': [], 'applied_at': 'test-applied_at', 'created_at': 'test-created_at'})
    item_id = r.json()["fix_id"]
    r2 = await client.post(f"/api/auto-fixes/{item_id}/rollback", json={})
    assert r2.status_code == 200
    assert r2.json()["fix_id"] == item_id

@pytest.mark.asyncio
async def test_w072_approve_fix_not_found(client):
    r = await client.post("/api/auto-fixes/nonexistent-id/approve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w072_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/auto-fixes", json={'exception_id': 'test-exception_id', 'fix_type': 'test-fix_type', 'fix_payload': {}, 'requires_approval': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'audit_trail': [], 'applied_at': 'test-applied_at', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "auto_fix"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w072_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/auto-fixes", json={'exception_id': 'test-exception_id', 'fix_type': 'test-fix_type', 'fix_payload': {}, 'requires_approval': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'audit_trail': [], 'applied_at': 'test-applied_at', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/auto-fixes", json={'exception_id': 'test-exception_id', 'fix_type': 'test-fix_type', 'fix_payload': {}, 'requires_approval': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'audit_trail': [], 'applied_at': 'test-applied_at', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "fix_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w072_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/auto-fixes", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w072_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/auto-fixes", json={'exception_id': 'test-exception_id', 'fix_type': 'test-fix_type', 'fix_payload': {}, 'requires_approval': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'audit_trail': [], 'applied_at': 'test-applied_at', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["fix_id"]
    r2 = await client.get("/api/auto-fixes")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/auto-fixes/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["fix_id"] == item_id
