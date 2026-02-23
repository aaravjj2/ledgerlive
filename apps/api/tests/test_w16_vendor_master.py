"""Tests for Wave 16: Vendor Master

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w16_vendor_master import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w16_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w16_create(client):
    r = await client.post("/api/vendors", json={'name': 'test-name', 'tax_id': 'test-tax_id', 'address': 'test-address', 'payment_terms': 'test-payment_terms', 'active': True, 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "vendor_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w16_list(client):
    await client.post("/api/vendors", json={'name': 'test-name', 'tax_id': 'test-tax_id', 'address': 'test-address', 'payment_terms': 'test-payment_terms', 'active': True, 'created_at': 'test-created_at'})
    await client.post("/api/vendors", json={'name': 'test-name', 'tax_id': 'test-tax_id', 'address': 'test-address', 'payment_terms': 'test-payment_terms', 'active': True, 'created_at': 'test-created_at'})
    r = await client.get("/api/vendors")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w16_get_by_id(client):
    r = await client.post("/api/vendors", json={'name': 'test-name', 'tax_id': 'test-tax_id', 'address': 'test-address', 'payment_terms': 'test-payment_terms', 'active': True, 'created_at': 'test-created_at'})
    item_id = r.json()["vendor_id"]
    r2 = await client.get(f"/api/vendors/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["vendor_id"] == item_id

@pytest.mark.asyncio
async def test_w16_get_not_found(client):
    r = await client.get("/api/vendors/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w16_update(client):
    r = await client.post("/api/vendors", json={'name': 'test-name', 'tax_id': 'test-tax_id', 'address': 'test-address', 'payment_terms': 'test-payment_terms', 'active': True, 'created_at': 'test-created_at'})
    item_id = r.json()["vendor_id"]
    r2 = await client.put(f"/api/vendors/{item_id}", json={"name": "updated"})
    assert r2.status_code == 200
    assert r2.json()["name"] == "updated"

@pytest.mark.asyncio
async def test_w16_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/vendors", json={'name': 'test-name', 'tax_id': 'test-tax_id', 'address': 'test-address', 'payment_terms': 'test-payment_terms', 'active': True, 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "vendor_master"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w16_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/vendors", json={'name': 'test-name', 'tax_id': 'test-tax_id', 'address': 'test-address', 'payment_terms': 'test-payment_terms', 'active': True, 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/vendors", json={'name': 'test-name', 'tax_id': 'test-tax_id', 'address': 'test-address', 'payment_terms': 'test-payment_terms', 'active': True, 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "vendor_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w16_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/vendors", json={})
    assert r.status_code == 201
