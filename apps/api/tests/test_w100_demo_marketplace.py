"""Tests for Wave 100: Demo Mode Marketplace

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w100_demo_marketplace import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w100_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w100_create(client):
    r = await client.post("/api/demo-marketplace", json={'demo_name': 'test-demo_name', 'templates_imported': [], 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "demo_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w100_list(client):
    await client.post("/api/demo-marketplace", json={'demo_name': 'test-demo_name', 'templates_imported': [], 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    await client.post("/api/demo-marketplace", json={'demo_name': 'test-demo_name', 'templates_imported': [], 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    r = await client.get("/api/demo-marketplace")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w100_get_by_id(client):
    r = await client.post("/api/demo-marketplace", json={'demo_name': 'test-demo_name', 'templates_imported': [], 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["demo_id"]
    r2 = await client.get(f"/api/demo-marketplace/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["demo_id"] == item_id

@pytest.mark.asyncio
async def test_w100_get_not_found(client):
    r = await client.get("/api/demo-marketplace/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w100_advance(client):
    r = await client.post("/api/demo-marketplace", json={'demo_name': 'test-demo_name', 'templates_imported': [], 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["demo_id"]
    r2 = await client.post(f"/api/demo-marketplace/{item_id}/advance", json={})
    assert r2.status_code == 200
    assert r2.json()["demo_id"] == item_id

@pytest.mark.asyncio
async def test_w100_verify_demo(client):
    r = await client.post("/api/demo-marketplace", json={'demo_name': 'test-demo_name', 'templates_imported': [], 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["demo_id"]
    r2 = await client.post(f"/api/demo-marketplace/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["demo_id"] == item_id

@pytest.mark.asyncio
async def test_w100_advance_not_found(client):
    r = await client.post("/api/demo-marketplace/nonexistent-id/advance", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w100_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/demo-marketplace", json={'demo_name': 'test-demo_name', 'templates_imported': [], 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "demo_marketplace"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w100_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/demo-marketplace", json={'demo_name': 'test-demo_name', 'templates_imported': [], 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/demo-marketplace", json={'demo_name': 'test-demo_name', 'templates_imported': [], 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "demo_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w100_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/demo-marketplace", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w100_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/demo-marketplace", json={'demo_name': 'test-demo_name', 'templates_imported': [], 'steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'hash': 'test-hash', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["demo_id"]
    r2 = await client.get("/api/demo-marketplace")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/demo-marketplace/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["demo_id"] == item_id
