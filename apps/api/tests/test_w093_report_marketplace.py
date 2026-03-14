"""Tests for Wave 93: Report Template Marketplace

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w093_report_marketplace import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w093_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w093_create(client):
    r = await client.post("/api/report-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'render_hash': 'test-render_hash', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "report_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w093_list(client):
    await client.post("/api/report-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'render_hash': 'test-render_hash', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/report-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'render_hash': 'test-render_hash', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/report-marketplace")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w093_get_by_id(client):
    r = await client.post("/api/report-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'render_hash': 'test-render_hash', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["report_id"]
    r2 = await client.get(f"/api/report-marketplace/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["report_id"] == item_id

@pytest.mark.asyncio
async def test_w093_get_not_found(client):
    r = await client.get("/api/report-marketplace/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w093_render(client):
    r = await client.post("/api/report-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'render_hash': 'test-render_hash', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["report_id"]
    r2 = await client.post(f"/api/report-marketplace/{item_id}/render", json={})
    assert r2.status_code == 200
    assert r2.json()["report_id"] == item_id

@pytest.mark.asyncio
async def test_w093_verify_render(client):
    r = await client.post("/api/report-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'render_hash': 'test-render_hash', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["report_id"]
    r2 = await client.post(f"/api/report-marketplace/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["report_id"] == item_id

@pytest.mark.asyncio
async def test_w093_import_report(client):
    r = await client.post("/api/report-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'render_hash': 'test-render_hash', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["report_id"]
    r2 = await client.post(f"/api/report-marketplace/{item_id}/import", json={})
    assert r2.status_code == 200
    assert r2.json()["report_id"] == item_id

@pytest.mark.asyncio
async def test_w093_render_not_found(client):
    r = await client.post("/api/report-marketplace/nonexistent-id/render", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w093_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/report-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'render_hash': 'test-render_hash', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "report_marketplace"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w093_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/report-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'render_hash': 'test-render_hash', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/report-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'render_hash': 'test-render_hash', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "report_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w093_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/report-marketplace", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w093_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/report-marketplace", json={'name': 'test-name', 'category': 'test-category', 'version': 'test-version', 'render_hash': 'test-render_hash', 'signature': 'test-signature', 'verified': True, 'download_count': 1, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["report_id"]
    r2 = await client.get("/api/report-marketplace")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/report-marketplace/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["report_id"] == item_id
