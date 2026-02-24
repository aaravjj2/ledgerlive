"""Tests for Wave 244: Execute-from-Plan v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w244_execute_from_plan import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w244_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w244_create(client):
    r = await client.post("/api/plan-execution", json={'plan_ref': 'test-plan_ref', 'idempotency_key': 'test-idempotency_key', 'steps_completed': 1, 'steps_total': 1, 'current_step': 'test-current_step', 'tool_trace': [], 'incidents_generated': [], 'telemetry_updates': [], 'execution_hash': 'test-execution_hash', 'rollback_available': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    assert r.status_code == 201
    data = r.json()
    assert "execution_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w244_list(client):
    await client.post("/api/plan-execution", json={'plan_ref': 'test-plan_ref', 'idempotency_key': 'test-idempotency_key', 'steps_completed': 1, 'steps_total': 1, 'current_step': 'test-current_step', 'tool_trace': [], 'incidents_generated': [], 'telemetry_updates': [], 'execution_hash': 'test-execution_hash', 'rollback_available': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    await client.post("/api/plan-execution", json={'plan_ref': 'test-plan_ref', 'idempotency_key': 'test-idempotency_key', 'steps_completed': 1, 'steps_total': 1, 'current_step': 'test-current_step', 'tool_trace': [], 'incidents_generated': [], 'telemetry_updates': [], 'execution_hash': 'test-execution_hash', 'rollback_available': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    r = await client.get("/api/plan-execution")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w244_get_by_id(client):
    r = await client.post("/api/plan-execution", json={'plan_ref': 'test-plan_ref', 'idempotency_key': 'test-idempotency_key', 'steps_completed': 1, 'steps_total': 1, 'current_step': 'test-current_step', 'tool_trace': [], 'incidents_generated': [], 'telemetry_updates': [], 'execution_hash': 'test-execution_hash', 'rollback_available': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    item_id = r.json()["execution_id"]
    r2 = await client.get(f"/api/plan-execution/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["execution_id"] == item_id

@pytest.mark.asyncio
async def test_w244_get_not_found(client):
    r = await client.get("/api/plan-execution/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w244_advance_step(client):
    r = await client.post("/api/plan-execution", json={'plan_ref': 'test-plan_ref', 'idempotency_key': 'test-idempotency_key', 'steps_completed': 1, 'steps_total': 1, 'current_step': 'test-current_step', 'tool_trace': [], 'incidents_generated': [], 'telemetry_updates': [], 'execution_hash': 'test-execution_hash', 'rollback_available': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    item_id = r.json()["execution_id"]
    r2 = await client.post(f"/api/plan-execution/{item_id}/advance", json={})
    assert r2.status_code == 200
    assert r2.json()["execution_id"] == item_id

@pytest.mark.asyncio
async def test_w244_record_telemetry(client):
    r = await client.post("/api/plan-execution", json={'plan_ref': 'test-plan_ref', 'idempotency_key': 'test-idempotency_key', 'steps_completed': 1, 'steps_total': 1, 'current_step': 'test-current_step', 'tool_trace': [], 'incidents_generated': [], 'telemetry_updates': [], 'execution_hash': 'test-execution_hash', 'rollback_available': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    item_id = r.json()["execution_id"]
    r2 = await client.post(f"/api/plan-execution/{item_id}/telemetry", json={})
    assert r2.status_code == 200
    assert r2.json()["execution_id"] == item_id

@pytest.mark.asyncio
async def test_w244_rollback_execution(client):
    r = await client.post("/api/plan-execution", json={'plan_ref': 'test-plan_ref', 'idempotency_key': 'test-idempotency_key', 'steps_completed': 1, 'steps_total': 1, 'current_step': 'test-current_step', 'tool_trace': [], 'incidents_generated': [], 'telemetry_updates': [], 'execution_hash': 'test-execution_hash', 'rollback_available': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    item_id = r.json()["execution_id"]
    r2 = await client.post(f"/api/plan-execution/{item_id}/rollback", json={})
    assert r2.status_code == 200
    assert r2.json()["execution_id"] == item_id

@pytest.mark.asyncio
async def test_w244_advance_step_not_found(client):
    r = await client.post("/api/plan-execution/nonexistent-id/advance", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w244_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/plan-execution", json={'plan_ref': 'test-plan_ref', 'idempotency_key': 'test-idempotency_key', 'steps_completed': 1, 'steps_total': 1, 'current_step': 'test-current_step', 'tool_trace': [], 'incidents_generated': [], 'telemetry_updates': [], 'execution_hash': 'test-execution_hash', 'rollback_available': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "execute_from_plan"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w244_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/plan-execution", json={'plan_ref': 'test-plan_ref', 'idempotency_key': 'test-idempotency_key', 'steps_completed': 1, 'steps_total': 1, 'current_step': 'test-current_step', 'tool_trace': [], 'incidents_generated': [], 'telemetry_updates': [], 'execution_hash': 'test-execution_hash', 'rollback_available': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/plan-execution", json={'plan_ref': 'test-plan_ref', 'idempotency_key': 'test-idempotency_key', 'steps_completed': 1, 'steps_total': 1, 'current_step': 'test-current_step', 'tool_trace': [], 'incidents_generated': [], 'telemetry_updates': [], 'execution_hash': 'test-execution_hash', 'rollback_available': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "execution_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w244_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/plan-execution", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w244_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/plan-execution", json={'plan_ref': 'test-plan_ref', 'idempotency_key': 'test-idempotency_key', 'steps_completed': 1, 'steps_total': 1, 'current_step': 'test-current_step', 'tool_trace': [], 'incidents_generated': [], 'telemetry_updates': [], 'execution_hash': 'test-execution_hash', 'rollback_available': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    assert r1.status_code == 201
    item_id = r1.json()["execution_id"]
    r2 = await client.get("/api/plan-execution")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/plan-execution/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["execution_id"] == item_id
