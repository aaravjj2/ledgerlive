"""Tests for Wave 163: Tool Registry v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w163_tool_registry import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w163_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w163_create(client):
    r = await client.post("/api/tool-registry", json={'tool_name': 'test-tool_name', 'schema_version': 'test-schema_version', 'input_schema': {}, 'output_schema': {}, 'args_hash': 'test-args_hash', 'result_hash': 'test-result_hash', 'duration_ms': 1.0, 'trace_id': 'test-trace_id', 'idempotency_key': 'test-idempotency_key', 'status': 'test-status', 'invoked_at': 'test-invoked_at'})
    assert r.status_code == 201
    data = r.json()
    assert "tool_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w163_list(client):
    await client.post("/api/tool-registry", json={'tool_name': 'test-tool_name', 'schema_version': 'test-schema_version', 'input_schema': {}, 'output_schema': {}, 'args_hash': 'test-args_hash', 'result_hash': 'test-result_hash', 'duration_ms': 1.0, 'trace_id': 'test-trace_id', 'idempotency_key': 'test-idempotency_key', 'status': 'test-status', 'invoked_at': 'test-invoked_at'})
    await client.post("/api/tool-registry", json={'tool_name': 'test-tool_name', 'schema_version': 'test-schema_version', 'input_schema': {}, 'output_schema': {}, 'args_hash': 'test-args_hash', 'result_hash': 'test-result_hash', 'duration_ms': 1.0, 'trace_id': 'test-trace_id', 'idempotency_key': 'test-idempotency_key', 'status': 'test-status', 'invoked_at': 'test-invoked_at'})
    r = await client.get("/api/tool-registry")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w163_get_by_id(client):
    r = await client.post("/api/tool-registry", json={'tool_name': 'test-tool_name', 'schema_version': 'test-schema_version', 'input_schema': {}, 'output_schema': {}, 'args_hash': 'test-args_hash', 'result_hash': 'test-result_hash', 'duration_ms': 1.0, 'trace_id': 'test-trace_id', 'idempotency_key': 'test-idempotency_key', 'status': 'test-status', 'invoked_at': 'test-invoked_at'})
    item_id = r.json()["tool_id"]
    r2 = await client.get(f"/api/tool-registry/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["tool_id"] == item_id

@pytest.mark.asyncio
async def test_w163_get_not_found(client):
    r = await client.get("/api/tool-registry/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w163_invoke_tool(client):
    r = await client.post("/api/tool-registry", json={'tool_name': 'test-tool_name', 'schema_version': 'test-schema_version', 'input_schema': {}, 'output_schema': {}, 'args_hash': 'test-args_hash', 'result_hash': 'test-result_hash', 'duration_ms': 1.0, 'trace_id': 'test-trace_id', 'idempotency_key': 'test-idempotency_key', 'status': 'test-status', 'invoked_at': 'test-invoked_at'})
    item_id = r.json()["tool_id"]
    r2 = await client.post(f"/api/tool-registry/{item_id}/invoke", json={})
    assert r2.status_code == 200
    assert r2.json()["tool_id"] == item_id

@pytest.mark.asyncio
async def test_w163_validate_schema(client):
    r = await client.post("/api/tool-registry", json={'tool_name': 'test-tool_name', 'schema_version': 'test-schema_version', 'input_schema': {}, 'output_schema': {}, 'args_hash': 'test-args_hash', 'result_hash': 'test-result_hash', 'duration_ms': 1.0, 'trace_id': 'test-trace_id', 'idempotency_key': 'test-idempotency_key', 'status': 'test-status', 'invoked_at': 'test-invoked_at'})
    item_id = r.json()["tool_id"]
    r2 = await client.post(f"/api/tool-registry/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["tool_id"] == item_id

@pytest.mark.asyncio
async def test_w163_invoke_tool_not_found(client):
    r = await client.post("/api/tool-registry/nonexistent-id/invoke", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w163_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/tool-registry", json={'tool_name': 'test-tool_name', 'schema_version': 'test-schema_version', 'input_schema': {}, 'output_schema': {}, 'args_hash': 'test-args_hash', 'result_hash': 'test-result_hash', 'duration_ms': 1.0, 'trace_id': 'test-trace_id', 'idempotency_key': 'test-idempotency_key', 'status': 'test-status', 'invoked_at': 'test-invoked_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "tool_registry"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w163_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/tool-registry", json={'tool_name': 'test-tool_name', 'schema_version': 'test-schema_version', 'input_schema': {}, 'output_schema': {}, 'args_hash': 'test-args_hash', 'result_hash': 'test-result_hash', 'duration_ms': 1.0, 'trace_id': 'test-trace_id', 'idempotency_key': 'test-idempotency_key', 'status': 'test-status', 'invoked_at': 'test-invoked_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/tool-registry", json={'tool_name': 'test-tool_name', 'schema_version': 'test-schema_version', 'input_schema': {}, 'output_schema': {}, 'args_hash': 'test-args_hash', 'result_hash': 'test-result_hash', 'duration_ms': 1.0, 'trace_id': 'test-trace_id', 'idempotency_key': 'test-idempotency_key', 'status': 'test-status', 'invoked_at': 'test-invoked_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "tool_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w163_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/tool-registry", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w163_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/tool-registry", json={'tool_name': 'test-tool_name', 'schema_version': 'test-schema_version', 'input_schema': {}, 'output_schema': {}, 'args_hash': 'test-args_hash', 'result_hash': 'test-result_hash', 'duration_ms': 1.0, 'trace_id': 'test-trace_id', 'idempotency_key': 'test-idempotency_key', 'status': 'test-status', 'invoked_at': 'test-invoked_at'})
    assert r1.status_code == 201
    item_id = r1.json()["tool_id"]
    r2 = await client.get("/api/tool-registry")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/tool-registry/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["tool_id"] == item_id
