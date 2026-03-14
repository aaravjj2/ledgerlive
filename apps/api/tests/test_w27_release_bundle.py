"""Tests for Wave 27: Release Bundle

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w27_release_bundle import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w27_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w27_create(client):
    r = await client.post("/api/releases", json={'version': 'test-version', 'changelog': 'test-changelog', 'migrations': [], 'status': 'test-status', 'created_at': 'test-created_at', 'deployed_at': 'test-deployed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "release_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w27_list(client):
    await client.post("/api/releases", json={'version': 'test-version', 'changelog': 'test-changelog', 'migrations': [], 'status': 'test-status', 'created_at': 'test-created_at', 'deployed_at': 'test-deployed_at'})
    await client.post("/api/releases", json={'version': 'test-version', 'changelog': 'test-changelog', 'migrations': [], 'status': 'test-status', 'created_at': 'test-created_at', 'deployed_at': 'test-deployed_at'})
    r = await client.get("/api/releases")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w27_get_by_id(client):
    r = await client.post("/api/releases", json={'version': 'test-version', 'changelog': 'test-changelog', 'migrations': [], 'status': 'test-status', 'created_at': 'test-created_at', 'deployed_at': 'test-deployed_at'})
    item_id = r.json()["release_id"]
    r2 = await client.get(f"/api/releases/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["release_id"] == item_id

@pytest.mark.asyncio
async def test_w27_get_not_found(client):
    r = await client.get("/api/releases/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w27_deploy(client):
    r = await client.post("/api/releases", json={'version': 'test-version', 'changelog': 'test-changelog', 'migrations': [], 'status': 'test-status', 'created_at': 'test-created_at', 'deployed_at': 'test-deployed_at'})
    item_id = r.json()["release_id"]
    r2 = await client.post(f"/api/releases/{item_id}/deploy", json={})
    assert r2.status_code == 200
    assert r2.json()["release_id"] == item_id

@pytest.mark.asyncio
async def test_w27_rollback(client):
    r = await client.post("/api/releases", json={'version': 'test-version', 'changelog': 'test-changelog', 'migrations': [], 'status': 'test-status', 'created_at': 'test-created_at', 'deployed_at': 'test-deployed_at'})
    item_id = r.json()["release_id"]
    r2 = await client.post(f"/api/releases/{item_id}/rollback", json={})
    assert r2.status_code == 200
    assert r2.json()["release_id"] == item_id

@pytest.mark.asyncio
async def test_w27_deploy_not_found(client):
    r = await client.post("/api/releases/nonexistent-id/deploy", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w27_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/releases", json={'version': 'test-version', 'changelog': 'test-changelog', 'migrations': [], 'status': 'test-status', 'created_at': 'test-created_at', 'deployed_at': 'test-deployed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "release_bundle"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w27_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/releases", json={'version': 'test-version', 'changelog': 'test-changelog', 'migrations': [], 'status': 'test-status', 'created_at': 'test-created_at', 'deployed_at': 'test-deployed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/releases", json={'version': 'test-version', 'changelog': 'test-changelog', 'migrations': [], 'status': 'test-status', 'created_at': 'test-created_at', 'deployed_at': 'test-deployed_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "release_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w27_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/releases", json={})
    assert r.status_code == 201
