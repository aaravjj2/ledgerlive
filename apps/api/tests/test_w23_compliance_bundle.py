"""Tests for Wave 23: Compliance Bundle

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w23_compliance_bundle import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w23_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w23_create(client):
    r = await client.post("/api/compliance-bundles", json={'regulation': 'test-regulation', 'period_id': 'test-period_id', 'status': 'test-status', 'items': [], 'created_at': 'test-created_at', 'submitted_at': 'test-submitted_at'})
    assert r.status_code == 201
    data = r.json()
    assert "bundle_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w23_list(client):
    await client.post("/api/compliance-bundles", json={'regulation': 'test-regulation', 'period_id': 'test-period_id', 'status': 'test-status', 'items': [], 'created_at': 'test-created_at', 'submitted_at': 'test-submitted_at'})
    await client.post("/api/compliance-bundles", json={'regulation': 'test-regulation', 'period_id': 'test-period_id', 'status': 'test-status', 'items': [], 'created_at': 'test-created_at', 'submitted_at': 'test-submitted_at'})
    r = await client.get("/api/compliance-bundles")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w23_get_by_id(client):
    r = await client.post("/api/compliance-bundles", json={'regulation': 'test-regulation', 'period_id': 'test-period_id', 'status': 'test-status', 'items': [], 'created_at': 'test-created_at', 'submitted_at': 'test-submitted_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.get(f"/api/compliance-bundles/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w23_get_not_found(client):
    r = await client.get("/api/compliance-bundles/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w23_add_item(client):
    r = await client.post("/api/compliance-bundles", json={'regulation': 'test-regulation', 'period_id': 'test-period_id', 'status': 'test-status', 'items': [], 'created_at': 'test-created_at', 'submitted_at': 'test-submitted_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.post(f"/api/compliance-bundles/{item_id}/items", json={})
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w23_submit(client):
    r = await client.post("/api/compliance-bundles", json={'regulation': 'test-regulation', 'period_id': 'test-period_id', 'status': 'test-status', 'items': [], 'created_at': 'test-created_at', 'submitted_at': 'test-submitted_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.post(f"/api/compliance-bundles/{item_id}/submit", json={})
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w23_add_item_not_found(client):
    r = await client.post("/api/compliance-bundles/nonexistent-id/items", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w23_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/compliance-bundles", json={'regulation': 'test-regulation', 'period_id': 'test-period_id', 'status': 'test-status', 'items': [], 'created_at': 'test-created_at', 'submitted_at': 'test-submitted_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "compliance_bundle"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w23_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/compliance-bundles", json={'regulation': 'test-regulation', 'period_id': 'test-period_id', 'status': 'test-status', 'items': [], 'created_at': 'test-created_at', 'submitted_at': 'test-submitted_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/compliance-bundles", json={'regulation': 'test-regulation', 'period_id': 'test-period_id', 'status': 'test-status', 'items': [], 'created_at': 'test-created_at', 'submitted_at': 'test-submitted_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "bundle_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w23_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/compliance-bundles", json={})
    assert r.status_code == 201
