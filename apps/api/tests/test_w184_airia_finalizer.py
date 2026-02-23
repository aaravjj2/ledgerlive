"""Tests for Wave 184: Airia Package Finalizer v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w184_airia_finalizer import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w184_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w184_create(client):
    r = await client.post("/api/airia-finalizer", json={'bundle_name': 'test-bundle_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'metadata': {}, 'file_ordering': [], 'checksums': {}, 'content_hash': 'test-content_hash', 'validation_errors': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "bundle_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w184_list(client):
    await client.post("/api/airia-finalizer", json={'bundle_name': 'test-bundle_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'metadata': {}, 'file_ordering': [], 'checksums': {}, 'content_hash': 'test-content_hash', 'validation_errors': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/airia-finalizer", json={'bundle_name': 'test-bundle_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'metadata': {}, 'file_ordering': [], 'checksums': {}, 'content_hash': 'test-content_hash', 'validation_errors': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/airia-finalizer")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w184_get_by_id(client):
    r = await client.post("/api/airia-finalizer", json={'bundle_name': 'test-bundle_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'metadata': {}, 'file_ordering': [], 'checksums': {}, 'content_hash': 'test-content_hash', 'validation_errors': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.get(f"/api/airia-finalizer/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w184_get_not_found(client):
    r = await client.get("/api/airia-finalizer/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w184_validate_bundle(client):
    r = await client.post("/api/airia-finalizer", json={'bundle_name': 'test-bundle_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'metadata': {}, 'file_ordering': [], 'checksums': {}, 'content_hash': 'test-content_hash', 'validation_errors': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.post(f"/api/airia-finalizer/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w184_export_bundle(client):
    r = await client.post("/api/airia-finalizer", json={'bundle_name': 'test-bundle_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'metadata': {}, 'file_ordering': [], 'checksums': {}, 'content_hash': 'test-content_hash', 'validation_errors': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["bundle_id"]
    r2 = await client.post(f"/api/airia-finalizer/{item_id}/export", json={})
    assert r2.status_code == 200
    assert r2.json()["bundle_id"] == item_id

@pytest.mark.asyncio
async def test_w184_validate_bundle_not_found(client):
    r = await client.post("/api/airia-finalizer/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w184_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/airia-finalizer", json={'bundle_name': 'test-bundle_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'metadata': {}, 'file_ordering': [], 'checksums': {}, 'content_hash': 'test-content_hash', 'validation_errors': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "airia_finalizer"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w184_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/airia-finalizer", json={'bundle_name': 'test-bundle_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'metadata': {}, 'file_ordering': [], 'checksums': {}, 'content_hash': 'test-content_hash', 'validation_errors': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/airia-finalizer", json={'bundle_name': 'test-bundle_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'metadata': {}, 'file_ordering': [], 'checksums': {}, 'content_hash': 'test-content_hash', 'validation_errors': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "bundle_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w184_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/airia-finalizer", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w184_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/airia-finalizer", json={'bundle_name': 'test-bundle_name', 'tool_schemas': [], 'runbooks': [], 'persona_config': {}, 'metadata': {}, 'file_ordering': [], 'checksums': {}, 'content_hash': 'test-content_hash', 'validation_errors': [], 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["bundle_id"]
    r2 = await client.get("/api/airia-finalizer")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/airia-finalizer/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["bundle_id"] == item_id
