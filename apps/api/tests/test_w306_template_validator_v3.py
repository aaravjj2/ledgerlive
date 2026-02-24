"""Tests for Wave 306: Template Validator v3

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w306_template_validator_v3 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w306_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w306_create(client):
    r = await client.post("/api/template-validator-v3", json={'template_ref': 'test-template_ref', 'check_results': [], 'completeness_score': 1.0, 'is_complete': True, 'missing_fields': [], 'checksum': 'test-checksum', 'checksum_match': True, 'validator_version': 'test-validator_version', 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "validation_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w306_list(client):
    await client.post("/api/template-validator-v3", json={'template_ref': 'test-template_ref', 'check_results': [], 'completeness_score': 1.0, 'is_complete': True, 'missing_fields': [], 'checksum': 'test-checksum', 'checksum_match': True, 'validator_version': 'test-validator_version', 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    await client.post("/api/template-validator-v3", json={'template_ref': 'test-template_ref', 'check_results': [], 'completeness_score': 1.0, 'is_complete': True, 'missing_fields': [], 'checksum': 'test-checksum', 'checksum_match': True, 'validator_version': 'test-validator_version', 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    r = await client.get("/api/template-validator-v3")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w306_get_by_id(client):
    r = await client.post("/api/template-validator-v3", json={'template_ref': 'test-template_ref', 'check_results': [], 'completeness_score': 1.0, 'is_complete': True, 'missing_fields': [], 'checksum': 'test-checksum', 'checksum_match': True, 'validator_version': 'test-validator_version', 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    item_id = r.json()["validation_id"]
    r2 = await client.get(f"/api/template-validator-v3/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["validation_id"] == item_id

@pytest.mark.asyncio
async def test_w306_get_not_found(client):
    r = await client.get("/api/template-validator-v3/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w306_revalidate(client):
    r = await client.post("/api/template-validator-v3", json={'template_ref': 'test-template_ref', 'check_results': [], 'completeness_score': 1.0, 'is_complete': True, 'missing_fields': [], 'checksum': 'test-checksum', 'checksum_match': True, 'validator_version': 'test-validator_version', 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    item_id = r.json()["validation_id"]
    r2 = await client.post(f"/api/template-validator-v3/{item_id}/revalidate", json={})
    assert r2.status_code == 200
    assert r2.json()["validation_id"] == item_id

@pytest.mark.asyncio
async def test_w306_checksum_verify(client):
    r = await client.post("/api/template-validator-v3", json={'template_ref': 'test-template_ref', 'check_results': [], 'completeness_score': 1.0, 'is_complete': True, 'missing_fields': [], 'checksum': 'test-checksum', 'checksum_match': True, 'validator_version': 'test-validator_version', 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    item_id = r.json()["validation_id"]
    r2 = await client.post(f"/api/template-validator-v3/{item_id}/checksum", json={})
    assert r2.status_code == 200
    assert r2.json()["validation_id"] == item_id

@pytest.mark.asyncio
async def test_w306_revalidate_not_found(client):
    r = await client.post("/api/template-validator-v3/nonexistent-id/revalidate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w306_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/template-validator-v3", json={'template_ref': 'test-template_ref', 'check_results': [], 'completeness_score': 1.0, 'is_complete': True, 'missing_fields': [], 'checksum': 'test-checksum', 'checksum_match': True, 'validator_version': 'test-validator_version', 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "template_validator_v3"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w306_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/template-validator-v3", json={'template_ref': 'test-template_ref', 'check_results': [], 'completeness_score': 1.0, 'is_complete': True, 'missing_fields': [], 'checksum': 'test-checksum', 'checksum_match': True, 'validator_version': 'test-validator_version', 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/template-validator-v3", json={'template_ref': 'test-template_ref', 'check_results': [], 'completeness_score': 1.0, 'is_complete': True, 'missing_fields': [], 'checksum': 'test-checksum', 'checksum_match': True, 'validator_version': 'test-validator_version', 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "validation_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w306_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/template-validator-v3", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w306_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/template-validator-v3", json={'template_ref': 'test-template_ref', 'check_results': [], 'completeness_score': 1.0, 'is_complete': True, 'missing_fields': [], 'checksum': 'test-checksum', 'checksum_match': True, 'validator_version': 'test-validator_version', 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["validation_id"]
    r2 = await client.get("/api/template-validator-v3")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/template-validator-v3/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["validation_id"] == item_id
