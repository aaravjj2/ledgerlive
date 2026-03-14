"""Tests for Wave 9: Evidence Binder

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w09_evidence_binder import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w09_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w09_create(client):
    r = await client.post("/api/binders", json={'period_id': 'test-period_id', 'title': 'test-title', 'status': 'test-status', 'sections': [], 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    assert r.status_code == 201
    data = r.json()
    assert "binder_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w09_list(client):
    await client.post("/api/binders", json={'period_id': 'test-period_id', 'title': 'test-title', 'status': 'test-status', 'sections': [], 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    await client.post("/api/binders", json={'period_id': 'test-period_id', 'title': 'test-title', 'status': 'test-status', 'sections': [], 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    r = await client.get("/api/binders")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w09_get_by_id(client):
    r = await client.post("/api/binders", json={'period_id': 'test-period_id', 'title': 'test-title', 'status': 'test-status', 'sections': [], 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    item_id = r.json()["binder_id"]
    r2 = await client.get(f"/api/binders/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["binder_id"] == item_id

@pytest.mark.asyncio
async def test_w09_get_not_found(client):
    r = await client.get("/api/binders/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w09_add_section(client):
    r = await client.post("/api/binders", json={'period_id': 'test-period_id', 'title': 'test-title', 'status': 'test-status', 'sections': [], 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    item_id = r.json()["binder_id"]
    r2 = await client.post(f"/api/binders/{item_id}/sections", json={})
    assert r2.status_code == 200
    assert r2.json()["binder_id"] == item_id

@pytest.mark.asyncio
async def test_w09_finalize(client):
    r = await client.post("/api/binders", json={'period_id': 'test-period_id', 'title': 'test-title', 'status': 'test-status', 'sections': [], 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    item_id = r.json()["binder_id"]
    r2 = await client.post(f"/api/binders/{item_id}/finalize", json={})
    assert r2.status_code == 200
    assert r2.json()["binder_id"] == item_id

@pytest.mark.asyncio
async def test_w09_add_section_not_found(client):
    r = await client.post("/api/binders/nonexistent-id/sections", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w09_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/binders", json={'period_id': 'test-period_id', 'title': 'test-title', 'status': 'test-status', 'sections': [], 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "evidence_binder"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w09_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/binders", json={'period_id': 'test-period_id', 'title': 'test-title', 'status': 'test-status', 'sections': [], 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/binders", json={'period_id': 'test-period_id', 'title': 'test-title', 'status': 'test-status', 'sections': [], 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "binder_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w09_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/binders", json={})
    assert r.status_code == 201
