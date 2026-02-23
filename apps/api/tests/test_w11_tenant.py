"""Tests for Wave 11: Multi-Tenant Management

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w11_tenant import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w11_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w11_create(client):
    r = await client.post("/api/tenants", json={'name': 'test-name', 'slug': 'test-slug', 'plan': 'test-plan', 'active': True, 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "tenant_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w11_list(client):
    await client.post("/api/tenants", json={'name': 'test-name', 'slug': 'test-slug', 'plan': 'test-plan', 'active': True, 'created_at': 'test-created_at'})
    await client.post("/api/tenants", json={'name': 'test-name', 'slug': 'test-slug', 'plan': 'test-plan', 'active': True, 'created_at': 'test-created_at'})
    r = await client.get("/api/tenants")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w11_get_by_id(client):
    r = await client.post("/api/tenants", json={'name': 'test-name', 'slug': 'test-slug', 'plan': 'test-plan', 'active': True, 'created_at': 'test-created_at'})
    item_id = r.json()["tenant_id"]
    r2 = await client.get(f"/api/tenants/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["tenant_id"] == item_id

@pytest.mark.asyncio
async def test_w11_get_not_found(client):
    r = await client.get("/api/tenants/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w11_update(client):
    r = await client.post("/api/tenants", json={'name': 'test-name', 'slug': 'test-slug', 'plan': 'test-plan', 'active': True, 'created_at': 'test-created_at'})
    item_id = r.json()["tenant_id"]
    r2 = await client.put(f"/api/tenants/{item_id}", json={"name": "updated"})
    assert r2.status_code == 200
    assert r2.json()["name"] == "updated"

@pytest.mark.asyncio
async def test_w11_suspend(client):
    r = await client.post("/api/tenants", json={'name': 'test-name', 'slug': 'test-slug', 'plan': 'test-plan', 'active': True, 'created_at': 'test-created_at'})
    item_id = r.json()["tenant_id"]
    r2 = await client.post(f"/api/tenants/{item_id}/suspend", json={})
    assert r2.status_code == 200
    assert r2.json()["tenant_id"] == item_id

@pytest.mark.asyncio
async def test_w11_suspend_not_found(client):
    r = await client.post("/api/tenants/nonexistent-id/suspend", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w11_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/tenants", json={'name': 'test-name', 'slug': 'test-slug', 'plan': 'test-plan', 'active': True, 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "tenant"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w11_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/tenants", json={'name': 'test-name', 'slug': 'test-slug', 'plan': 'test-plan', 'active': True, 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/tenants", json={'name': 'test-name', 'slug': 'test-slug', 'plan': 'test-plan', 'active': True, 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "tenant_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w11_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/tenants", json={})
    assert r.status_code == 201
