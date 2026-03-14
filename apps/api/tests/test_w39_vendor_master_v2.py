"""Tests for Wave 39: Vendor Master 2.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w39_vendor_master_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w39_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w39_create(client):
    r = await client.post("/api/vendors-v2", json={'name': 'test-name', 'parent_vendor_id': 'test-parent_vendor_id', 'risk_rating': 'test-risk_rating', 'watchlist': True, 'tax_id': 'test-tax_id', 'approval_required': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "vendor_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w39_list(client):
    await client.post("/api/vendors-v2", json={'name': 'test-name', 'parent_vendor_id': 'test-parent_vendor_id', 'risk_rating': 'test-risk_rating', 'watchlist': True, 'tax_id': 'test-tax_id', 'approval_required': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/vendors-v2", json={'name': 'test-name', 'parent_vendor_id': 'test-parent_vendor_id', 'risk_rating': 'test-risk_rating', 'watchlist': True, 'tax_id': 'test-tax_id', 'approval_required': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/vendors-v2")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w39_get_by_id(client):
    r = await client.post("/api/vendors-v2", json={'name': 'test-name', 'parent_vendor_id': 'test-parent_vendor_id', 'risk_rating': 'test-risk_rating', 'watchlist': True, 'tax_id': 'test-tax_id', 'approval_required': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["vendor_id"]
    r2 = await client.get(f"/api/vendors-v2/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["vendor_id"] == item_id

@pytest.mark.asyncio
async def test_w39_get_not_found(client):
    r = await client.get("/api/vendors-v2/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w39_set_risk(client):
    r = await client.post("/api/vendors-v2", json={'name': 'test-name', 'parent_vendor_id': 'test-parent_vendor_id', 'risk_rating': 'test-risk_rating', 'watchlist': True, 'tax_id': 'test-tax_id', 'approval_required': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["vendor_id"]
    r2 = await client.post(f"/api/vendors-v2/{item_id}/risk", json={})
    assert r2.status_code == 200
    assert r2.json()["vendor_id"] == item_id

@pytest.mark.asyncio
async def test_w39_approve_override(client):
    r = await client.post("/api/vendors-v2", json={'name': 'test-name', 'parent_vendor_id': 'test-parent_vendor_id', 'risk_rating': 'test-risk_rating', 'watchlist': True, 'tax_id': 'test-tax_id', 'approval_required': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["vendor_id"]
    r2 = await client.post(f"/api/vendors-v2/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["vendor_id"] == item_id

@pytest.mark.asyncio
async def test_w39_merge_vendors(client):
    r = await client.post("/api/vendors-v2", json={'name': 'test-name', 'parent_vendor_id': 'test-parent_vendor_id', 'risk_rating': 'test-risk_rating', 'watchlist': True, 'tax_id': 'test-tax_id', 'approval_required': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["vendor_id"]
    r2 = await client.post(f"/api/vendors-v2/{item_id}/merge", json={})
    assert r2.status_code == 200
    assert r2.json()["vendor_id"] == item_id

@pytest.mark.asyncio
async def test_w39_set_risk_not_found(client):
    r = await client.post("/api/vendors-v2/nonexistent-id/risk", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w39_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/vendors-v2", json={'name': 'test-name', 'parent_vendor_id': 'test-parent_vendor_id', 'risk_rating': 'test-risk_rating', 'watchlist': True, 'tax_id': 'test-tax_id', 'approval_required': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "vendor_master_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w39_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/vendors-v2", json={'name': 'test-name', 'parent_vendor_id': 'test-parent_vendor_id', 'risk_rating': 'test-risk_rating', 'watchlist': True, 'tax_id': 'test-tax_id', 'approval_required': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/vendors-v2", json={'name': 'test-name', 'parent_vendor_id': 'test-parent_vendor_id', 'risk_rating': 'test-risk_rating', 'watchlist': True, 'tax_id': 'test-tax_id', 'approval_required': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "vendor_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w39_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/vendors-v2", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w39_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/vendors-v2", json={'name': 'test-name', 'parent_vendor_id': 'test-parent_vendor_id', 'risk_rating': 'test-risk_rating', 'watchlist': True, 'tax_id': 'test-tax_id', 'approval_required': True, 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["vendor_id"]
    r2 = await client.get("/api/vendors-v2")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/vendors-v2/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["vendor_id"] == item_id
