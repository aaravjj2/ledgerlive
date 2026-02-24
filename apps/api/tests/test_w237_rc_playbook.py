"""Tests for Wave 237: RC Playbook Engine v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w237_rc_playbook import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w237_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w237_create(client):
    r = await client.post("/api/rc-playbook", json={'playbook_name': 'test-playbook_name', 'scenario_type': 'test-scenario_type', 'steps': [], 'current_step': 1, 'total_steps': 1, 'decision_points': [], 'rollback_procedures': [], 'execution_log': [], 'completed': True, 'success': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    assert r.status_code == 201
    data = r.json()
    assert "playbook_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w237_list(client):
    await client.post("/api/rc-playbook", json={'playbook_name': 'test-playbook_name', 'scenario_type': 'test-scenario_type', 'steps': [], 'current_step': 1, 'total_steps': 1, 'decision_points': [], 'rollback_procedures': [], 'execution_log': [], 'completed': True, 'success': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    await client.post("/api/rc-playbook", json={'playbook_name': 'test-playbook_name', 'scenario_type': 'test-scenario_type', 'steps': [], 'current_step': 1, 'total_steps': 1, 'decision_points': [], 'rollback_procedures': [], 'execution_log': [], 'completed': True, 'success': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    r = await client.get("/api/rc-playbook")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w237_get_by_id(client):
    r = await client.post("/api/rc-playbook", json={'playbook_name': 'test-playbook_name', 'scenario_type': 'test-scenario_type', 'steps': [], 'current_step': 1, 'total_steps': 1, 'decision_points': [], 'rollback_procedures': [], 'execution_log': [], 'completed': True, 'success': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    item_id = r.json()["playbook_id"]
    r2 = await client.get(f"/api/rc-playbook/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["playbook_id"] == item_id

@pytest.mark.asyncio
async def test_w237_get_not_found(client):
    r = await client.get("/api/rc-playbook/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w237_advance_step(client):
    r = await client.post("/api/rc-playbook", json={'playbook_name': 'test-playbook_name', 'scenario_type': 'test-scenario_type', 'steps': [], 'current_step': 1, 'total_steps': 1, 'decision_points': [], 'rollback_procedures': [], 'execution_log': [], 'completed': True, 'success': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    item_id = r.json()["playbook_id"]
    r2 = await client.post(f"/api/rc-playbook/{item_id}/advance", json={})
    assert r2.status_code == 200
    assert r2.json()["playbook_id"] == item_id

@pytest.mark.asyncio
async def test_w237_rollback_step(client):
    r = await client.post("/api/rc-playbook", json={'playbook_name': 'test-playbook_name', 'scenario_type': 'test-scenario_type', 'steps': [], 'current_step': 1, 'total_steps': 1, 'decision_points': [], 'rollback_procedures': [], 'execution_log': [], 'completed': True, 'success': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    item_id = r.json()["playbook_id"]
    r2 = await client.post(f"/api/rc-playbook/{item_id}/rollback", json={})
    assert r2.status_code == 200
    assert r2.json()["playbook_id"] == item_id

@pytest.mark.asyncio
async def test_w237_advance_step_not_found(client):
    r = await client.post("/api/rc-playbook/nonexistent-id/advance", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w237_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/rc-playbook", json={'playbook_name': 'test-playbook_name', 'scenario_type': 'test-scenario_type', 'steps': [], 'current_step': 1, 'total_steps': 1, 'decision_points': [], 'rollback_procedures': [], 'execution_log': [], 'completed': True, 'success': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "rc_playbook"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w237_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/rc-playbook", json={'playbook_name': 'test-playbook_name', 'scenario_type': 'test-scenario_type', 'steps': [], 'current_step': 1, 'total_steps': 1, 'decision_points': [], 'rollback_procedures': [], 'execution_log': [], 'completed': True, 'success': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/rc-playbook", json={'playbook_name': 'test-playbook_name', 'scenario_type': 'test-scenario_type', 'steps': [], 'current_step': 1, 'total_steps': 1, 'decision_points': [], 'rollback_procedures': [], 'execution_log': [], 'completed': True, 'success': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "playbook_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w237_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/rc-playbook", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w237_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/rc-playbook", json={'playbook_name': 'test-playbook_name', 'scenario_type': 'test-scenario_type', 'steps': [], 'current_step': 1, 'total_steps': 1, 'decision_points': [], 'rollback_procedures': [], 'execution_log': [], 'completed': True, 'success': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    assert r1.status_code == 201
    item_id = r1.json()["playbook_id"]
    r2 = await client.get("/api/rc-playbook")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/rc-playbook/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["playbook_id"] == item_id
