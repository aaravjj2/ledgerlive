"""Tests for Wave 170: Connector Real-Mode Interface

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w170_connector_realmode import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w170_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w170_create(client):
    r = await client.post("/api/connector-realmode", json={'provider': 'test-provider', 'enabled': True, 'has_keys': True, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'fallback_to_mock': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "config_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w170_list(client):
    await client.post("/api/connector-realmode", json={'provider': 'test-provider', 'enabled': True, 'has_keys': True, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'fallback_to_mock': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    await client.post("/api/connector-realmode", json={'provider': 'test-provider', 'enabled': True, 'has_keys': True, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'fallback_to_mock': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    r = await client.get("/api/connector-realmode")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w170_get_by_id(client):
    r = await client.post("/api/connector-realmode", json={'provider': 'test-provider', 'enabled': True, 'has_keys': True, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'fallback_to_mock': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    item_id = r.json()["config_id"]
    r2 = await client.get(f"/api/connector-realmode/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["config_id"] == item_id

@pytest.mark.asyncio
async def test_w170_get_not_found(client):
    r = await client.get("/api/connector-realmode/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w170_validate_keys(client):
    r = await client.post("/api/connector-realmode", json={'provider': 'test-provider', 'enabled': True, 'has_keys': True, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'fallback_to_mock': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    item_id = r.json()["config_id"]
    r2 = await client.post(f"/api/connector-realmode/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["config_id"] == item_id

@pytest.mark.asyncio
async def test_w170_test_connection(client):
    r = await client.post("/api/connector-realmode", json={'provider': 'test-provider', 'enabled': True, 'has_keys': True, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'fallback_to_mock': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    item_id = r.json()["config_id"]
    r2 = await client.post(f"/api/connector-realmode/{item_id}/test", json={})
    assert r2.status_code == 200
    assert r2.json()["config_id"] == item_id

@pytest.mark.asyncio
async def test_w170_validate_keys_not_found(client):
    r = await client.post("/api/connector-realmode/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w170_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/connector-realmode", json={'provider': 'test-provider', 'enabled': True, 'has_keys': True, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'fallback_to_mock': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "connector_realmode"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w170_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/connector-realmode", json={'provider': 'test-provider', 'enabled': True, 'has_keys': True, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'fallback_to_mock': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/connector-realmode", json={'provider': 'test-provider', 'enabled': True, 'has_keys': True, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'fallback_to_mock': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "config_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w170_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/connector-realmode", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w170_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/connector-realmode", json={'provider': 'test-provider', 'enabled': True, 'has_keys': True, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'fallback_to_mock': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["config_id"]
    r2 = await client.get("/api/connector-realmode")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/connector-realmode/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["config_id"] == item_id
