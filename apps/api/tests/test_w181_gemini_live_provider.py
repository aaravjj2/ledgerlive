"""Tests for Wave 181: Gemini Live Provider v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w181_gemini_live_provider import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w181_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w181_create(client):
    r = await client.post("/api/gemini-live", json={'provider_name': 'test-provider_name', 'enabled': True, 'has_api_key': True, 'config': {}, 'connection_status': 'test-connection_status', 'transcript_events': [], 'tool_calls_issued': [], 'interruption_count': 1, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "provider_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w181_list(client):
    await client.post("/api/gemini-live", json={'provider_name': 'test-provider_name', 'enabled': True, 'has_api_key': True, 'config': {}, 'connection_status': 'test-connection_status', 'transcript_events': [], 'tool_calls_issued': [], 'interruption_count': 1, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/gemini-live", json={'provider_name': 'test-provider_name', 'enabled': True, 'has_api_key': True, 'config': {}, 'connection_status': 'test-connection_status', 'transcript_events': [], 'tool_calls_issued': [], 'interruption_count': 1, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/gemini-live")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w181_get_by_id(client):
    r = await client.post("/api/gemini-live", json={'provider_name': 'test-provider_name', 'enabled': True, 'has_api_key': True, 'config': {}, 'connection_status': 'test-connection_status', 'transcript_events': [], 'tool_calls_issued': [], 'interruption_count': 1, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["provider_id"]
    r2 = await client.get(f"/api/gemini-live/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["provider_id"] == item_id

@pytest.mark.asyncio
async def test_w181_get_not_found(client):
    r = await client.get("/api/gemini-live/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w181_validate_config(client):
    r = await client.post("/api/gemini-live", json={'provider_name': 'test-provider_name', 'enabled': True, 'has_api_key': True, 'config': {}, 'connection_status': 'test-connection_status', 'transcript_events': [], 'tool_calls_issued': [], 'interruption_count': 1, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["provider_id"]
    r2 = await client.post(f"/api/gemini-live/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["provider_id"] == item_id

@pytest.mark.asyncio
async def test_w181_connect_provider(client):
    r = await client.post("/api/gemini-live", json={'provider_name': 'test-provider_name', 'enabled': True, 'has_api_key': True, 'config': {}, 'connection_status': 'test-connection_status', 'transcript_events': [], 'tool_calls_issued': [], 'interruption_count': 1, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["provider_id"]
    r2 = await client.post(f"/api/gemini-live/{item_id}/connect", json={})
    assert r2.status_code == 200
    assert r2.json()["provider_id"] == item_id

@pytest.mark.asyncio
async def test_w181_disconnect_provider(client):
    r = await client.post("/api/gemini-live", json={'provider_name': 'test-provider_name', 'enabled': True, 'has_api_key': True, 'config': {}, 'connection_status': 'test-connection_status', 'transcript_events': [], 'tool_calls_issued': [], 'interruption_count': 1, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["provider_id"]
    r2 = await client.post(f"/api/gemini-live/{item_id}/disconnect", json={})
    assert r2.status_code == 200
    assert r2.json()["provider_id"] == item_id

@pytest.mark.asyncio
async def test_w181_validate_config_not_found(client):
    r = await client.post("/api/gemini-live/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w181_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/gemini-live", json={'provider_name': 'test-provider_name', 'enabled': True, 'has_api_key': True, 'config': {}, 'connection_status': 'test-connection_status', 'transcript_events': [], 'tool_calls_issued': [], 'interruption_count': 1, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "gemini_live_provider"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w181_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/gemini-live", json={'provider_name': 'test-provider_name', 'enabled': True, 'has_api_key': True, 'config': {}, 'connection_status': 'test-connection_status', 'transcript_events': [], 'tool_calls_issued': [], 'interruption_count': 1, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/gemini-live", json={'provider_name': 'test-provider_name', 'enabled': True, 'has_api_key': True, 'config': {}, 'connection_status': 'test-connection_status', 'transcript_events': [], 'tool_calls_issued': [], 'interruption_count': 1, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "provider_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w181_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/gemini-live", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w181_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/gemini-live", json={'provider_name': 'test-provider_name', 'enabled': True, 'has_api_key': True, 'config': {}, 'connection_status': 'test-connection_status', 'transcript_events': [], 'tool_calls_issued': [], 'interruption_count': 1, 'validation_result': 'test-validation_result', 'error_message': 'test-error_message', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["provider_id"]
    r2 = await client.get("/api/gemini-live")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/gemini-live/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["provider_id"] == item_id
