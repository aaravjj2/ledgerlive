"""Tests for Wave 279: Ops Pack Export v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w279_ops_pack_export import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w279_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w279_create(client):
    r = await client.post("/api/ops-pack-export", json={'channel_interactions': [], 'approvals_data': [], 'incidents_data': [], 'verify_script': 'test-verify_script', 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'pack_size_bytes': 1, 'deterministic': True, 'export_format': 'test-export_format', 'verification_passed': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    assert r.status_code == 201
    data = r.json()
    assert "ops_pack_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w279_list(client):
    await client.post("/api/ops-pack-export", json={'channel_interactions': [], 'approvals_data': [], 'incidents_data': [], 'verify_script': 'test-verify_script', 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'pack_size_bytes': 1, 'deterministic': True, 'export_format': 'test-export_format', 'verification_passed': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    await client.post("/api/ops-pack-export", json={'channel_interactions': [], 'approvals_data': [], 'incidents_data': [], 'verify_script': 'test-verify_script', 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'pack_size_bytes': 1, 'deterministic': True, 'export_format': 'test-export_format', 'verification_passed': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    r = await client.get("/api/ops-pack-export")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w279_get_by_id(client):
    r = await client.post("/api/ops-pack-export", json={'channel_interactions': [], 'approvals_data': [], 'incidents_data': [], 'verify_script': 'test-verify_script', 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'pack_size_bytes': 1, 'deterministic': True, 'export_format': 'test-export_format', 'verification_passed': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    item_id = r.json()["ops_pack_id"]
    r2 = await client.get(f"/api/ops-pack-export/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["ops_pack_id"] == item_id

@pytest.mark.asyncio
async def test_w279_get_not_found(client):
    r = await client.get("/api/ops-pack-export/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w279_verify_ops_pack(client):
    r = await client.post("/api/ops-pack-export", json={'channel_interactions': [], 'approvals_data': [], 'incidents_data': [], 'verify_script': 'test-verify_script', 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'pack_size_bytes': 1, 'deterministic': True, 'export_format': 'test-export_format', 'verification_passed': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    item_id = r.json()["ops_pack_id"]
    r2 = await client.post(f"/api/ops-pack-export/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["ops_pack_id"] == item_id

@pytest.mark.asyncio
async def test_w279_sign_ops_pack(client):
    r = await client.post("/api/ops-pack-export", json={'channel_interactions': [], 'approvals_data': [], 'incidents_data': [], 'verify_script': 'test-verify_script', 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'pack_size_bytes': 1, 'deterministic': True, 'export_format': 'test-export_format', 'verification_passed': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    item_id = r.json()["ops_pack_id"]
    r2 = await client.post(f"/api/ops-pack-export/{item_id}/sign", json={})
    assert r2.status_code == 200
    assert r2.json()["ops_pack_id"] == item_id

@pytest.mark.asyncio
async def test_w279_verify_ops_pack_not_found(client):
    r = await client.post("/api/ops-pack-export/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w279_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/ops-pack-export", json={'channel_interactions': [], 'approvals_data': [], 'incidents_data': [], 'verify_script': 'test-verify_script', 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'pack_size_bytes': 1, 'deterministic': True, 'export_format': 'test-export_format', 'verification_passed': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "ops_pack_export"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w279_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/ops-pack-export", json={'channel_interactions': [], 'approvals_data': [], 'incidents_data': [], 'verify_script': 'test-verify_script', 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'pack_size_bytes': 1, 'deterministic': True, 'export_format': 'test-export_format', 'verification_passed': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/ops-pack-export", json={'channel_interactions': [], 'approvals_data': [], 'incidents_data': [], 'verify_script': 'test-verify_script', 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'pack_size_bytes': 1, 'deterministic': True, 'export_format': 'test-export_format', 'verification_passed': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "ops_pack_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w279_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/ops-pack-export", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w279_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/ops-pack-export", json={'channel_interactions': [], 'approvals_data': [], 'incidents_data': [], 'verify_script': 'test-verify_script', 'signature': 'test-signature', 'content_hash': 'test-content_hash', 'pack_size_bytes': 1, 'deterministic': True, 'export_format': 'test-export_format', 'verification_passed': True, 'status': 'test-status', 'exported_at': 'test-exported_at'})
    assert r1.status_code == 201
    item_id = r1.json()["ops_pack_id"]
    r2 = await client.get("/api/ops-pack-export")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/ops-pack-export/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["ops_pack_id"] == item_id
