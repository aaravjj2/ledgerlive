"""Tests for Wave 85: Consolidation Adjustments Lock

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w085_consol_adj_lock import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w085_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w085_create(client):
    r = await client.post("/api/consol-adj-locks", json={'consolidation_id': 'test-consolidation_id', 'adj_type': 'test-adj_type', 'amount': 1.0, 'description': 'test-description', 'approved_by': 'test-approved_by', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "adj_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w085_list(client):
    await client.post("/api/consol-adj-locks", json={'consolidation_id': 'test-consolidation_id', 'adj_type': 'test-adj_type', 'amount': 1.0, 'description': 'test-description', 'approved_by': 'test-approved_by', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/consol-adj-locks", json={'consolidation_id': 'test-consolidation_id', 'adj_type': 'test-adj_type', 'amount': 1.0, 'description': 'test-description', 'approved_by': 'test-approved_by', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/consol-adj-locks")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w085_get_by_id(client):
    r = await client.post("/api/consol-adj-locks", json={'consolidation_id': 'test-consolidation_id', 'adj_type': 'test-adj_type', 'amount': 1.0, 'description': 'test-description', 'approved_by': 'test-approved_by', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["adj_id"]
    r2 = await client.get(f"/api/consol-adj-locks/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["adj_id"] == item_id

@pytest.mark.asyncio
async def test_w085_get_not_found(client):
    r = await client.get("/api/consol-adj-locks/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w085_approve(client):
    r = await client.post("/api/consol-adj-locks", json={'consolidation_id': 'test-consolidation_id', 'adj_type': 'test-adj_type', 'amount': 1.0, 'description': 'test-description', 'approved_by': 'test-approved_by', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["adj_id"]
    r2 = await client.post(f"/api/consol-adj-locks/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["adj_id"] == item_id

@pytest.mark.asyncio
async def test_w085_lock_adj(client):
    r = await client.post("/api/consol-adj-locks", json={'consolidation_id': 'test-consolidation_id', 'adj_type': 'test-adj_type', 'amount': 1.0, 'description': 'test-description', 'approved_by': 'test-approved_by', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["adj_id"]
    r2 = await client.post(f"/api/consol-adj-locks/{item_id}/lock", json={})
    assert r2.status_code == 200
    assert r2.json()["adj_id"] == item_id

@pytest.mark.asyncio
async def test_w085_deny_after_lock(client):
    r = await client.post("/api/consol-adj-locks", json={'consolidation_id': 'test-consolidation_id', 'adj_type': 'test-adj_type', 'amount': 1.0, 'description': 'test-description', 'approved_by': 'test-approved_by', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["adj_id"]
    r2 = await client.post(f"/api/consol-adj-locks/{item_id}/deny", json={})
    assert r2.status_code == 200
    assert r2.json()["adj_id"] == item_id

@pytest.mark.asyncio
async def test_w085_approve_not_found(client):
    r = await client.post("/api/consol-adj-locks/nonexistent-id/approve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w085_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/consol-adj-locks", json={'consolidation_id': 'test-consolidation_id', 'adj_type': 'test-adj_type', 'amount': 1.0, 'description': 'test-description', 'approved_by': 'test-approved_by', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "consol_adj_lock"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w085_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/consol-adj-locks", json={'consolidation_id': 'test-consolidation_id', 'adj_type': 'test-adj_type', 'amount': 1.0, 'description': 'test-description', 'approved_by': 'test-approved_by', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/consol-adj-locks", json={'consolidation_id': 'test-consolidation_id', 'adj_type': 'test-adj_type', 'amount': 1.0, 'description': 'test-description', 'approved_by': 'test-approved_by', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "adj_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w085_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/consol-adj-locks", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w085_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/consol-adj-locks", json={'consolidation_id': 'test-consolidation_id', 'adj_type': 'test-adj_type', 'amount': 1.0, 'description': 'test-description', 'approved_by': 'test-approved_by', 'locked': True, 'lock_reason': 'test-lock_reason', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["adj_id"]
    r2 = await client.get("/api/consol-adj-locks")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/consol-adj-locks/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["adj_id"] == item_id
