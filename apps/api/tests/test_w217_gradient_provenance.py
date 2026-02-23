"""Tests for Wave 217: Gradient Provenance Capture v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w217_gradient_provenance import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w217_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w217_create(client):
    r = await client.post("/api/gradient-provenance", json={'job_spec_hash': 'test-job_spec_hash', 'artifact_hash': 'test-artifact_hash', 'endpoint_hash': 'test-endpoint_hash', 'live_mode': True, 'placeholder_mode': True, 'provenance_data': {}, 'schema_valid': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'captured_at': 'test-captured_at'})
    assert r.status_code == 201
    data = r.json()
    assert "provenance_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w217_list(client):
    await client.post("/api/gradient-provenance", json={'job_spec_hash': 'test-job_spec_hash', 'artifact_hash': 'test-artifact_hash', 'endpoint_hash': 'test-endpoint_hash', 'live_mode': True, 'placeholder_mode': True, 'provenance_data': {}, 'schema_valid': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'captured_at': 'test-captured_at'})
    await client.post("/api/gradient-provenance", json={'job_spec_hash': 'test-job_spec_hash', 'artifact_hash': 'test-artifact_hash', 'endpoint_hash': 'test-endpoint_hash', 'live_mode': True, 'placeholder_mode': True, 'provenance_data': {}, 'schema_valid': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'captured_at': 'test-captured_at'})
    r = await client.get("/api/gradient-provenance")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w217_get_by_id(client):
    r = await client.post("/api/gradient-provenance", json={'job_spec_hash': 'test-job_spec_hash', 'artifact_hash': 'test-artifact_hash', 'endpoint_hash': 'test-endpoint_hash', 'live_mode': True, 'placeholder_mode': True, 'provenance_data': {}, 'schema_valid': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'captured_at': 'test-captured_at'})
    item_id = r.json()["provenance_id"]
    r2 = await client.get(f"/api/gradient-provenance/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["provenance_id"] == item_id

@pytest.mark.asyncio
async def test_w217_get_not_found(client):
    r = await client.get("/api/gradient-provenance/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w217_validate_provenance(client):
    r = await client.post("/api/gradient-provenance", json={'job_spec_hash': 'test-job_spec_hash', 'artifact_hash': 'test-artifact_hash', 'endpoint_hash': 'test-endpoint_hash', 'live_mode': True, 'placeholder_mode': True, 'provenance_data': {}, 'schema_valid': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'captured_at': 'test-captured_at'})
    item_id = r.json()["provenance_id"]
    r2 = await client.post(f"/api/gradient-provenance/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["provenance_id"] == item_id

@pytest.mark.asyncio
async def test_w217_generate_placeholder(client):
    r = await client.post("/api/gradient-provenance", json={'job_spec_hash': 'test-job_spec_hash', 'artifact_hash': 'test-artifact_hash', 'endpoint_hash': 'test-endpoint_hash', 'live_mode': True, 'placeholder_mode': True, 'provenance_data': {}, 'schema_valid': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'captured_at': 'test-captured_at'})
    item_id = r.json()["provenance_id"]
    r2 = await client.post(f"/api/gradient-provenance/{item_id}/placeholder", json={})
    assert r2.status_code == 200
    assert r2.json()["provenance_id"] == item_id

@pytest.mark.asyncio
async def test_w217_validate_provenance_not_found(client):
    r = await client.post("/api/gradient-provenance/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w217_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/gradient-provenance", json={'job_spec_hash': 'test-job_spec_hash', 'artifact_hash': 'test-artifact_hash', 'endpoint_hash': 'test-endpoint_hash', 'live_mode': True, 'placeholder_mode': True, 'provenance_data': {}, 'schema_valid': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'captured_at': 'test-captured_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "gradient_provenance"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w217_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/gradient-provenance", json={'job_spec_hash': 'test-job_spec_hash', 'artifact_hash': 'test-artifact_hash', 'endpoint_hash': 'test-endpoint_hash', 'live_mode': True, 'placeholder_mode': True, 'provenance_data': {}, 'schema_valid': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'captured_at': 'test-captured_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/gradient-provenance", json={'job_spec_hash': 'test-job_spec_hash', 'artifact_hash': 'test-artifact_hash', 'endpoint_hash': 'test-endpoint_hash', 'live_mode': True, 'placeholder_mode': True, 'provenance_data': {}, 'schema_valid': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'captured_at': 'test-captured_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "provenance_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w217_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/gradient-provenance", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w217_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/gradient-provenance", json={'job_spec_hash': 'test-job_spec_hash', 'artifact_hash': 'test-artifact_hash', 'endpoint_hash': 'test-endpoint_hash', 'live_mode': True, 'placeholder_mode': True, 'provenance_data': {}, 'schema_valid': True, 'content_hash': 'test-content_hash', 'status': 'test-status', 'captured_at': 'test-captured_at'})
    assert r1.status_code == 201
    item_id = r1.json()["provenance_id"]
    r2 = await client.get("/api/gradient-provenance")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/gradient-provenance/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["provenance_id"] == item_id
