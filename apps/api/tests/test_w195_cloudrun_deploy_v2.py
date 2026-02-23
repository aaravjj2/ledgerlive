"""Tests for Wave 195: Cloud Run Deploy v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w195_cloudrun_deploy_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w195_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w195_create(client):
    r = await client.post("/api/cloudrun-v2", json={'deploy_target': 'test-deploy_target', 'service_name': 'test-service_name', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'region': 'test-region', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "deploy_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w195_list(client):
    await client.post("/api/cloudrun-v2", json={'deploy_target': 'test-deploy_target', 'service_name': 'test-service_name', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'region': 'test-region', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/cloudrun-v2", json={'deploy_target': 'test-deploy_target', 'service_name': 'test-service_name', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'region': 'test-region', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/cloudrun-v2")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w195_get_by_id(client):
    r = await client.post("/api/cloudrun-v2", json={'deploy_target': 'test-deploy_target', 'service_name': 'test-service_name', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'region': 'test-region', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["deploy_id"]
    r2 = await client.get(f"/api/cloudrun-v2/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["deploy_id"] == item_id

@pytest.mark.asyncio
async def test_w195_get_not_found(client):
    r = await client.get("/api/cloudrun-v2/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w195_validate_config(client):
    r = await client.post("/api/cloudrun-v2", json={'deploy_target': 'test-deploy_target', 'service_name': 'test-service_name', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'region': 'test-region', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["deploy_id"]
    r2 = await client.post(f"/api/cloudrun-v2/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["deploy_id"] == item_id

@pytest.mark.asyncio
async def test_w195_generate_smoke(client):
    r = await client.post("/api/cloudrun-v2", json={'deploy_target': 'test-deploy_target', 'service_name': 'test-service_name', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'region': 'test-region', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["deploy_id"]
    r2 = await client.post(f"/api/cloudrun-v2/{item_id}/smoke", json={})
    assert r2.status_code == 200
    assert r2.json()["deploy_id"] == item_id

@pytest.mark.asyncio
async def test_w195_validate_config_not_found(client):
    r = await client.post("/api/cloudrun-v2/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w195_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/cloudrun-v2", json={'deploy_target': 'test-deploy_target', 'service_name': 'test-service_name', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'region': 'test-region', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "cloudrun_deploy_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w195_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/cloudrun-v2", json={'deploy_target': 'test-deploy_target', 'service_name': 'test-service_name', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'region': 'test-region', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/cloudrun-v2", json={'deploy_target': 'test-deploy_target', 'service_name': 'test-service_name', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'region': 'test-region', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "deploy_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w195_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/cloudrun-v2", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w195_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/cloudrun-v2", json={'deploy_target': 'test-deploy_target', 'service_name': 'test-service_name', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'region': 'test-region', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["deploy_id"]
    r2 = await client.get("/api/cloudrun-v2")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/cloudrun-v2/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["deploy_id"] == item_id
