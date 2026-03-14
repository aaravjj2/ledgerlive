"""Tests for Wave 196: DigitalOcean Deploy Automation v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w196_do_deploy import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w196_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w196_create(client):
    r = await client.post("/api/do-deploy", json={'deploy_target': 'test-deploy_target', 'platform': 'test-platform', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "deploy_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w196_list(client):
    await client.post("/api/do-deploy", json={'deploy_target': 'test-deploy_target', 'platform': 'test-platform', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/do-deploy", json={'deploy_target': 'test-deploy_target', 'platform': 'test-platform', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/do-deploy")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w196_get_by_id(client):
    r = await client.post("/api/do-deploy", json={'deploy_target': 'test-deploy_target', 'platform': 'test-platform', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["deploy_id"]
    r2 = await client.get(f"/api/do-deploy/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["deploy_id"] == item_id

@pytest.mark.asyncio
async def test_w196_get_not_found(client):
    r = await client.get("/api/do-deploy/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w196_validate_config(client):
    r = await client.post("/api/do-deploy", json={'deploy_target': 'test-deploy_target', 'platform': 'test-platform', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["deploy_id"]
    r2 = await client.post(f"/api/do-deploy/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["deploy_id"] == item_id

@pytest.mark.asyncio
async def test_w196_generate_smoke(client):
    r = await client.post("/api/do-deploy", json={'deploy_target': 'test-deploy_target', 'platform': 'test-platform', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["deploy_id"]
    r2 = await client.post(f"/api/do-deploy/{item_id}/smoke", json={})
    assert r2.status_code == 200
    assert r2.json()["deploy_id"] == item_id

@pytest.mark.asyncio
async def test_w196_validate_config_not_found(client):
    r = await client.post("/api/do-deploy/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w196_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/do-deploy", json={'deploy_target': 'test-deploy_target', 'platform': 'test-platform', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "do_deploy"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w196_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/do-deploy", json={'deploy_target': 'test-deploy_target', 'platform': 'test-platform', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/do-deploy", json={'deploy_target': 'test-deploy_target', 'platform': 'test-platform', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "deploy_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w196_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/do-deploy", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w196_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/do-deploy", json={'deploy_target': 'test-deploy_target', 'platform': 'test-platform', 'config': {}, 'scripts_valid': True, 'smoke_report': {}, 'smoke_report_hash': 'test-smoke_report_hash', 'schema_valid': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["deploy_id"]
    r2 = await client.get("/api/do-deploy")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/do-deploy/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["deploy_id"] == item_id
