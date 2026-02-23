"""Tests for Wave 177: Gemini Live Adapter Skeleton

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w177_gemini_adapter import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w177_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w177_create(client):
    r = await client.post("/api/gemini-adapter", json={'adapter_name': 'test-adapter_name', 'provider': 'test-provider', 'config': {}, 'config_valid': True, 'mock_mode': True, 'deploy_scripts': [], 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "adapter_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w177_list(client):
    await client.post("/api/gemini-adapter", json={'adapter_name': 'test-adapter_name', 'provider': 'test-provider', 'config': {}, 'config_valid': True, 'mock_mode': True, 'deploy_scripts': [], 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/gemini-adapter", json={'adapter_name': 'test-adapter_name', 'provider': 'test-provider', 'config': {}, 'config_valid': True, 'mock_mode': True, 'deploy_scripts': [], 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/gemini-adapter")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w177_get_by_id(client):
    r = await client.post("/api/gemini-adapter", json={'adapter_name': 'test-adapter_name', 'provider': 'test-provider', 'config': {}, 'config_valid': True, 'mock_mode': True, 'deploy_scripts': [], 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["adapter_id"]
    r2 = await client.get(f"/api/gemini-adapter/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["adapter_id"] == item_id

@pytest.mark.asyncio
async def test_w177_get_not_found(client):
    r = await client.get("/api/gemini-adapter/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w177_validate_config(client):
    r = await client.post("/api/gemini-adapter", json={'adapter_name': 'test-adapter_name', 'provider': 'test-provider', 'config': {}, 'config_valid': True, 'mock_mode': True, 'deploy_scripts': [], 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["adapter_id"]
    r2 = await client.post(f"/api/gemini-adapter/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["adapter_id"] == item_id

@pytest.mark.asyncio
async def test_w177_test_adapter(client):
    r = await client.post("/api/gemini-adapter", json={'adapter_name': 'test-adapter_name', 'provider': 'test-provider', 'config': {}, 'config_valid': True, 'mock_mode': True, 'deploy_scripts': [], 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["adapter_id"]
    r2 = await client.post(f"/api/gemini-adapter/{item_id}/test", json={})
    assert r2.status_code == 200
    assert r2.json()["adapter_id"] == item_id

@pytest.mark.asyncio
async def test_w177_validate_config_not_found(client):
    r = await client.post("/api/gemini-adapter/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w177_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/gemini-adapter", json={'adapter_name': 'test-adapter_name', 'provider': 'test-provider', 'config': {}, 'config_valid': True, 'mock_mode': True, 'deploy_scripts': [], 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "gemini_adapter"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w177_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/gemini-adapter", json={'adapter_name': 'test-adapter_name', 'provider': 'test-provider', 'config': {}, 'config_valid': True, 'mock_mode': True, 'deploy_scripts': [], 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/gemini-adapter", json={'adapter_name': 'test-adapter_name', 'provider': 'test-provider', 'config': {}, 'config_valid': True, 'mock_mode': True, 'deploy_scripts': [], 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "adapter_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w177_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/gemini-adapter", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w177_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/gemini-adapter", json={'adapter_name': 'test-adapter_name', 'provider': 'test-provider', 'config': {}, 'config_valid': True, 'mock_mode': True, 'deploy_scripts': [], 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["adapter_id"]
    r2 = await client.get("/api/gemini-adapter")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/gemini-adapter/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["adapter_id"] == item_id
