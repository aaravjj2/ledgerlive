"""Tests for Wave 199: Hackpack v2 Multi-Bundle

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w199_hackpack_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w199_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w199_create(client):
    r = await client.post("/api/hackpack-v2", json={'hackpack_name': 'test-hackpack_name', 'bundles': [], 'gemini_bundle': {}, 'airia_bundle': {}, 'do_bundle': {}, 'innovation_bundle': {}, 'bundle_checksums': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "hackpack_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w199_list(client):
    await client.post("/api/hackpack-v2", json={'hackpack_name': 'test-hackpack_name', 'bundles': [], 'gemini_bundle': {}, 'airia_bundle': {}, 'do_bundle': {}, 'innovation_bundle': {}, 'bundle_checksums': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/hackpack-v2", json={'hackpack_name': 'test-hackpack_name', 'bundles': [], 'gemini_bundle': {}, 'airia_bundle': {}, 'do_bundle': {}, 'innovation_bundle': {}, 'bundle_checksums': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/hackpack-v2")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w199_get_by_id(client):
    r = await client.post("/api/hackpack-v2", json={'hackpack_name': 'test-hackpack_name', 'bundles': [], 'gemini_bundle': {}, 'airia_bundle': {}, 'do_bundle': {}, 'innovation_bundle': {}, 'bundle_checksums': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["hackpack_id"]
    r2 = await client.get(f"/api/hackpack-v2/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["hackpack_id"] == item_id

@pytest.mark.asyncio
async def test_w199_get_not_found(client):
    r = await client.get("/api/hackpack-v2/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w199_validate_hackpack(client):
    r = await client.post("/api/hackpack-v2", json={'hackpack_name': 'test-hackpack_name', 'bundles': [], 'gemini_bundle': {}, 'airia_bundle': {}, 'do_bundle': {}, 'innovation_bundle': {}, 'bundle_checksums': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["hackpack_id"]
    r2 = await client.post(f"/api/hackpack-v2/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["hackpack_id"] == item_id

@pytest.mark.asyncio
async def test_w199_export_hackpack(client):
    r = await client.post("/api/hackpack-v2", json={'hackpack_name': 'test-hackpack_name', 'bundles': [], 'gemini_bundle': {}, 'airia_bundle': {}, 'do_bundle': {}, 'innovation_bundle': {}, 'bundle_checksums': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["hackpack_id"]
    r2 = await client.post(f"/api/hackpack-v2/{item_id}/export", json={})
    assert r2.status_code == 200
    assert r2.json()["hackpack_id"] == item_id

@pytest.mark.asyncio
async def test_w199_validate_hackpack_not_found(client):
    r = await client.post("/api/hackpack-v2/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w199_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/hackpack-v2", json={'hackpack_name': 'test-hackpack_name', 'bundles': [], 'gemini_bundle': {}, 'airia_bundle': {}, 'do_bundle': {}, 'innovation_bundle': {}, 'bundle_checksums': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "hackpack_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w199_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/hackpack-v2", json={'hackpack_name': 'test-hackpack_name', 'bundles': [], 'gemini_bundle': {}, 'airia_bundle': {}, 'do_bundle': {}, 'innovation_bundle': {}, 'bundle_checksums': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/hackpack-v2", json={'hackpack_name': 'test-hackpack_name', 'bundles': [], 'gemini_bundle': {}, 'airia_bundle': {}, 'do_bundle': {}, 'innovation_bundle': {}, 'bundle_checksums': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "hackpack_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w199_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/hackpack-v2", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w199_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/hackpack-v2", json={'hackpack_name': 'test-hackpack_name', 'bundles': [], 'gemini_bundle': {}, 'airia_bundle': {}, 'do_bundle': {}, 'innovation_bundle': {}, 'bundle_checksums': {}, 'content_hash': 'test-content_hash', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["hackpack_id"]
    r2 = await client.get("/api/hackpack-v2")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/hackpack-v2/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["hackpack_id"] == item_id
