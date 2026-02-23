"""Tests for Wave 187: Connector Runbooks Anti-CI Guard

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w187_connector_runbooks import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w187_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w187_create(client):
    r = await client.post("/api/connector-runbooks", json={'provider': 'test-provider', 'enable_flag': 'test-enable_flag', 'ci_guard_active': True, 'ci_env_detected': True, 'flag_value': True, 'guard_result': 'test-guard_result', 'runbook_content': 'test-runbook_content', 'validation_errors': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r.status_code == 201
    data = r.json()
    assert "runbook_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w187_list(client):
    await client.post("/api/connector-runbooks", json={'provider': 'test-provider', 'enable_flag': 'test-enable_flag', 'ci_guard_active': True, 'ci_env_detected': True, 'flag_value': True, 'guard_result': 'test-guard_result', 'runbook_content': 'test-runbook_content', 'validation_errors': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    await client.post("/api/connector-runbooks", json={'provider': 'test-provider', 'enable_flag': 'test-enable_flag', 'ci_guard_active': True, 'ci_env_detected': True, 'flag_value': True, 'guard_result': 'test-guard_result', 'runbook_content': 'test-runbook_content', 'validation_errors': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    r = await client.get("/api/connector-runbooks")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w187_get_by_id(client):
    r = await client.post("/api/connector-runbooks", json={'provider': 'test-provider', 'enable_flag': 'test-enable_flag', 'ci_guard_active': True, 'ci_env_detected': True, 'flag_value': True, 'guard_result': 'test-guard_result', 'runbook_content': 'test-runbook_content', 'validation_errors': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["runbook_id"]
    r2 = await client.get(f"/api/connector-runbooks/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["runbook_id"] == item_id

@pytest.mark.asyncio
async def test_w187_get_not_found(client):
    r = await client.get("/api/connector-runbooks/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w187_check_ci_guard(client):
    r = await client.post("/api/connector-runbooks", json={'provider': 'test-provider', 'enable_flag': 'test-enable_flag', 'ci_guard_active': True, 'ci_env_detected': True, 'flag_value': True, 'guard_result': 'test-guard_result', 'runbook_content': 'test-runbook_content', 'validation_errors': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["runbook_id"]
    r2 = await client.post(f"/api/connector-runbooks/{item_id}/ci-guard", json={})
    assert r2.status_code == 200
    assert r2.json()["runbook_id"] == item_id

@pytest.mark.asyncio
async def test_w187_validate_flags(client):
    r = await client.post("/api/connector-runbooks", json={'provider': 'test-provider', 'enable_flag': 'test-enable_flag', 'ci_guard_active': True, 'ci_env_detected': True, 'flag_value': True, 'guard_result': 'test-guard_result', 'runbook_content': 'test-runbook_content', 'validation_errors': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["runbook_id"]
    r2 = await client.post(f"/api/connector-runbooks/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["runbook_id"] == item_id

@pytest.mark.asyncio
async def test_w187_check_ci_guard_not_found(client):
    r = await client.post("/api/connector-runbooks/nonexistent-id/ci-guard", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w187_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/connector-runbooks", json={'provider': 'test-provider', 'enable_flag': 'test-enable_flag', 'ci_guard_active': True, 'ci_env_detected': True, 'flag_value': True, 'guard_result': 'test-guard_result', 'runbook_content': 'test-runbook_content', 'validation_errors': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "connector_runbooks"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w187_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/connector-runbooks", json={'provider': 'test-provider', 'enable_flag': 'test-enable_flag', 'ci_guard_active': True, 'ci_env_detected': True, 'flag_value': True, 'guard_result': 'test-guard_result', 'runbook_content': 'test-runbook_content', 'validation_errors': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/connector-runbooks", json={'provider': 'test-provider', 'enable_flag': 'test-enable_flag', 'ci_guard_active': True, 'ci_env_detected': True, 'flag_value': True, 'guard_result': 'test-guard_result', 'runbook_content': 'test-runbook_content', 'validation_errors': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "runbook_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w187_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/connector-runbooks", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w187_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/connector-runbooks", json={'provider': 'test-provider', 'enable_flag': 'test-enable_flag', 'ci_guard_active': True, 'ci_env_detected': True, 'flag_value': True, 'guard_result': 'test-guard_result', 'runbook_content': 'test-runbook_content', 'validation_errors': [], 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r1.status_code == 201
    item_id = r1.json()["runbook_id"]
    r2 = await client.get("/api/connector-runbooks")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/connector-runbooks/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["runbook_id"] == item_id
