"""Tests for Wave 92: Workflow Template Marketplace

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w092_workflow_marketplace import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w092_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w092_create(client):
    r = await client.post("/api/workflow-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'published_at': 'test-published_at', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "template_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w092_list(client):
    await client.post("/api/workflow-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'published_at': 'test-published_at', 'created_at': 'test-created_at'})
    await client.post("/api/workflow-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'published_at': 'test-published_at', 'created_at': 'test-created_at'})
    r = await client.get("/api/workflow-marketplace")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w092_get_by_id(client):
    r = await client.post("/api/workflow-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'published_at': 'test-published_at', 'created_at': 'test-created_at'})
    item_id = r.json()["template_id"]
    r2 = await client.get(f"/api/workflow-marketplace/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["template_id"] == item_id

@pytest.mark.asyncio
async def test_w092_get_not_found(client):
    r = await client.get("/api/workflow-marketplace/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w092_import_template(client):
    r = await client.post("/api/workflow-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'published_at': 'test-published_at', 'created_at': 'test-created_at'})
    item_id = r.json()["template_id"]
    r2 = await client.post(f"/api/workflow-marketplace/{item_id}/import", json={})
    assert r2.status_code == 200
    assert r2.json()["template_id"] == item_id

@pytest.mark.asyncio
async def test_w092_verify_template(client):
    r = await client.post("/api/workflow-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'published_at': 'test-published_at', 'created_at': 'test-created_at'})
    item_id = r.json()["template_id"]
    r2 = await client.post(f"/api/workflow-marketplace/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["template_id"] == item_id

@pytest.mark.asyncio
async def test_w092_import_template_not_found(client):
    r = await client.post("/api/workflow-marketplace/nonexistent-id/import", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w092_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/workflow-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'published_at': 'test-published_at', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "workflow_marketplace"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w092_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/workflow-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'published_at': 'test-published_at', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/workflow-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'published_at': 'test-published_at', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "template_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w092_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/workflow-marketplace", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w092_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/workflow-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'published_at': 'test-published_at', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["template_id"]
    r2 = await client.get("/api/workflow-marketplace")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/workflow-marketplace/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["template_id"] == item_id
