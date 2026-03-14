"""Tests for Wave 20: Signed Exports

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w20_signed_export import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w20_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w20_create(client):
    r = await client.post("/api/exports", json={'export_type': 'test-export_type', 'format_type': 'test-format_type', 'signature': 'test-signature', 'status': 'test-status', 'created_at': 'test-created_at', 'download_url': 'test-download_url'})
    assert r.status_code == 201
    data = r.json()
    assert "export_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w20_list(client):
    await client.post("/api/exports", json={'export_type': 'test-export_type', 'format_type': 'test-format_type', 'signature': 'test-signature', 'status': 'test-status', 'created_at': 'test-created_at', 'download_url': 'test-download_url'})
    await client.post("/api/exports", json={'export_type': 'test-export_type', 'format_type': 'test-format_type', 'signature': 'test-signature', 'status': 'test-status', 'created_at': 'test-created_at', 'download_url': 'test-download_url'})
    r = await client.get("/api/exports")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w20_get_by_id(client):
    r = await client.post("/api/exports", json={'export_type': 'test-export_type', 'format_type': 'test-format_type', 'signature': 'test-signature', 'status': 'test-status', 'created_at': 'test-created_at', 'download_url': 'test-download_url'})
    item_id = r.json()["export_id"]
    r2 = await client.get(f"/api/exports/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["export_id"] == item_id

@pytest.mark.asyncio
async def test_w20_get_not_found(client):
    r = await client.get("/api/exports/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w20_verify_sig(client):
    r = await client.post("/api/exports", json={'export_type': 'test-export_type', 'format_type': 'test-format_type', 'signature': 'test-signature', 'status': 'test-status', 'created_at': 'test-created_at', 'download_url': 'test-download_url'})
    item_id = r.json()["export_id"]
    r2 = await client.post(f"/api/exports/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["export_id"] == item_id

@pytest.mark.asyncio
async def test_w20_verify_sig_not_found(client):
    r = await client.post("/api/exports/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w20_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/exports", json={'export_type': 'test-export_type', 'format_type': 'test-format_type', 'signature': 'test-signature', 'status': 'test-status', 'created_at': 'test-created_at', 'download_url': 'test-download_url'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "signed_export"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w20_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/exports", json={'export_type': 'test-export_type', 'format_type': 'test-format_type', 'signature': 'test-signature', 'status': 'test-status', 'created_at': 'test-created_at', 'download_url': 'test-download_url'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/exports", json={'export_type': 'test-export_type', 'format_type': 'test-format_type', 'signature': 'test-signature', 'status': 'test-status', 'created_at': 'test-created_at', 'download_url': 'test-download_url'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "export_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w20_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/exports", json={})
    assert r.status_code == 201
