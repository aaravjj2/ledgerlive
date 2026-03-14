"""Tests for Wave 7: Exception Management

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w07_exception import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w07_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w07_create(client):
    r = await client.post("/api/exceptions", json={'recon_id': 'test-recon_id', 'category': 'test-category', 'severity': 'test-severity', 'description': 'test-description', 'status': 'test-status', 'assigned_to': 'test-assigned_to', 'resolved_at': 'test-resolved_at'})
    assert r.status_code == 201
    data = r.json()
    assert "exception_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w07_list(client):
    await client.post("/api/exceptions", json={'recon_id': 'test-recon_id', 'category': 'test-category', 'severity': 'test-severity', 'description': 'test-description', 'status': 'test-status', 'assigned_to': 'test-assigned_to', 'resolved_at': 'test-resolved_at'})
    await client.post("/api/exceptions", json={'recon_id': 'test-recon_id', 'category': 'test-category', 'severity': 'test-severity', 'description': 'test-description', 'status': 'test-status', 'assigned_to': 'test-assigned_to', 'resolved_at': 'test-resolved_at'})
    r = await client.get("/api/exceptions")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w07_get_by_id(client):
    r = await client.post("/api/exceptions", json={'recon_id': 'test-recon_id', 'category': 'test-category', 'severity': 'test-severity', 'description': 'test-description', 'status': 'test-status', 'assigned_to': 'test-assigned_to', 'resolved_at': 'test-resolved_at'})
    item_id = r.json()["exception_id"]
    r2 = await client.get(f"/api/exceptions/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["exception_id"] == item_id

@pytest.mark.asyncio
async def test_w07_get_not_found(client):
    r = await client.get("/api/exceptions/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w07_assign(client):
    r = await client.post("/api/exceptions", json={'recon_id': 'test-recon_id', 'category': 'test-category', 'severity': 'test-severity', 'description': 'test-description', 'status': 'test-status', 'assigned_to': 'test-assigned_to', 'resolved_at': 'test-resolved_at'})
    item_id = r.json()["exception_id"]
    r2 = await client.post(f"/api/exceptions/{item_id}/assign", json={})
    assert r2.status_code == 200
    assert r2.json()["exception_id"] == item_id

@pytest.mark.asyncio
async def test_w07_resolve(client):
    r = await client.post("/api/exceptions", json={'recon_id': 'test-recon_id', 'category': 'test-category', 'severity': 'test-severity', 'description': 'test-description', 'status': 'test-status', 'assigned_to': 'test-assigned_to', 'resolved_at': 'test-resolved_at'})
    item_id = r.json()["exception_id"]
    r2 = await client.post(f"/api/exceptions/{item_id}/resolve", json={})
    assert r2.status_code == 200
    assert r2.json()["exception_id"] == item_id

@pytest.mark.asyncio
async def test_w07_assign_not_found(client):
    r = await client.post("/api/exceptions/nonexistent-id/assign", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w07_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/exceptions", json={'recon_id': 'test-recon_id', 'category': 'test-category', 'severity': 'test-severity', 'description': 'test-description', 'status': 'test-status', 'assigned_to': 'test-assigned_to', 'resolved_at': 'test-resolved_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "exception"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w07_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/exceptions", json={'recon_id': 'test-recon_id', 'category': 'test-category', 'severity': 'test-severity', 'description': 'test-description', 'status': 'test-status', 'assigned_to': 'test-assigned_to', 'resolved_at': 'test-resolved_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/exceptions", json={'recon_id': 'test-recon_id', 'category': 'test-category', 'severity': 'test-severity', 'description': 'test-description', 'status': 'test-status', 'assigned_to': 'test-assigned_to', 'resolved_at': 'test-resolved_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "exception_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w07_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/exceptions", json={})
    assert r.status_code == 201
