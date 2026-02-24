"""Tests for Wave 296: Self-Healing Playbook v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w296_self_healing_playbook import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w296_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w296_create(client):
    r = await client.post("/api/self-healing-playbook", json={'trigger_condition': 'test-trigger_condition', 'recovery_steps': [], 'current_step': 1, 'total_steps': 1, 'approval_required_steps': [], 'approvals_received': [], 'audit_trail': [], 'auto_approved': True, 'outcome': 'test-outcome', 'deterministic': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    assert r.status_code == 201
    data = r.json()
    assert "playbook_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w296_list(client):
    await client.post("/api/self-healing-playbook", json={'trigger_condition': 'test-trigger_condition', 'recovery_steps': [], 'current_step': 1, 'total_steps': 1, 'approval_required_steps': [], 'approvals_received': [], 'audit_trail': [], 'auto_approved': True, 'outcome': 'test-outcome', 'deterministic': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    await client.post("/api/self-healing-playbook", json={'trigger_condition': 'test-trigger_condition', 'recovery_steps': [], 'current_step': 1, 'total_steps': 1, 'approval_required_steps': [], 'approvals_received': [], 'audit_trail': [], 'auto_approved': True, 'outcome': 'test-outcome', 'deterministic': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    r = await client.get("/api/self-healing-playbook")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w296_get_by_id(client):
    r = await client.post("/api/self-healing-playbook", json={'trigger_condition': 'test-trigger_condition', 'recovery_steps': [], 'current_step': 1, 'total_steps': 1, 'approval_required_steps': [], 'approvals_received': [], 'audit_trail': [], 'auto_approved': True, 'outcome': 'test-outcome', 'deterministic': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    item_id = r.json()["playbook_id"]
    r2 = await client.get(f"/api/self-healing-playbook/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["playbook_id"] == item_id

@pytest.mark.asyncio
async def test_w296_get_not_found(client):
    r = await client.get("/api/self-healing-playbook/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w296_advance_step(client):
    r = await client.post("/api/self-healing-playbook", json={'trigger_condition': 'test-trigger_condition', 'recovery_steps': [], 'current_step': 1, 'total_steps': 1, 'approval_required_steps': [], 'approvals_received': [], 'audit_trail': [], 'auto_approved': True, 'outcome': 'test-outcome', 'deterministic': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    item_id = r.json()["playbook_id"]
    r2 = await client.post(f"/api/self-healing-playbook/{item_id}/advance", json={})
    assert r2.status_code == 200
    assert r2.json()["playbook_id"] == item_id

@pytest.mark.asyncio
async def test_w296_approve_step(client):
    r = await client.post("/api/self-healing-playbook", json={'trigger_condition': 'test-trigger_condition', 'recovery_steps': [], 'current_step': 1, 'total_steps': 1, 'approval_required_steps': [], 'approvals_received': [], 'audit_trail': [], 'auto_approved': True, 'outcome': 'test-outcome', 'deterministic': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    item_id = r.json()["playbook_id"]
    r2 = await client.post(f"/api/self-healing-playbook/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["playbook_id"] == item_id

@pytest.mark.asyncio
async def test_w296_complete_playbook(client):
    r = await client.post("/api/self-healing-playbook", json={'trigger_condition': 'test-trigger_condition', 'recovery_steps': [], 'current_step': 1, 'total_steps': 1, 'approval_required_steps': [], 'approvals_received': [], 'audit_trail': [], 'auto_approved': True, 'outcome': 'test-outcome', 'deterministic': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    item_id = r.json()["playbook_id"]
    r2 = await client.post(f"/api/self-healing-playbook/{item_id}/complete", json={})
    assert r2.status_code == 200
    assert r2.json()["playbook_id"] == item_id

@pytest.mark.asyncio
async def test_w296_advance_step_not_found(client):
    r = await client.post("/api/self-healing-playbook/nonexistent-id/advance", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w296_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/self-healing-playbook", json={'trigger_condition': 'test-trigger_condition', 'recovery_steps': [], 'current_step': 1, 'total_steps': 1, 'approval_required_steps': [], 'approvals_received': [], 'audit_trail': [], 'auto_approved': True, 'outcome': 'test-outcome', 'deterministic': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "self_healing_playbook"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w296_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/self-healing-playbook", json={'trigger_condition': 'test-trigger_condition', 'recovery_steps': [], 'current_step': 1, 'total_steps': 1, 'approval_required_steps': [], 'approvals_received': [], 'audit_trail': [], 'auto_approved': True, 'outcome': 'test-outcome', 'deterministic': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/self-healing-playbook", json={'trigger_condition': 'test-trigger_condition', 'recovery_steps': [], 'current_step': 1, 'total_steps': 1, 'approval_required_steps': [], 'approvals_received': [], 'audit_trail': [], 'auto_approved': True, 'outcome': 'test-outcome', 'deterministic': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "playbook_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w296_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/self-healing-playbook", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w296_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/self-healing-playbook", json={'trigger_condition': 'test-trigger_condition', 'recovery_steps': [], 'current_step': 1, 'total_steps': 1, 'approval_required_steps': [], 'approvals_received': [], 'audit_trail': [], 'auto_approved': True, 'outcome': 'test-outcome', 'deterministic': True, 'status': 'test-status', 'started_at': 'test-started_at'})
    assert r1.status_code == 201
    item_id = r1.json()["playbook_id"]
    r2 = await client.get("/api/self-healing-playbook")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/self-healing-playbook/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["playbook_id"] == item_id
