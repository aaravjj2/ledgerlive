"""Tests for Wave 247: Pit Crew Routing v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w247_pit_crew_routing import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w247_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w247_create(client):
    r = await client.post("/api/pit-crew", json={'action_ref': 'test-action_ref', 'agent_assignments': [], 'required_skills': [], 'quorum_required': 1, 'quorum_achieved': True, 'veto_agents': [], 'veto_active': True, 'routing_strategy': 'test-routing_strategy', 'assignment_hash': 'test-assignment_hash', 'completion_pct': 1.0, 'status': 'test-status', 'routed_at': 'test-routed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "routing_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w247_list(client):
    await client.post("/api/pit-crew", json={'action_ref': 'test-action_ref', 'agent_assignments': [], 'required_skills': [], 'quorum_required': 1, 'quorum_achieved': True, 'veto_agents': [], 'veto_active': True, 'routing_strategy': 'test-routing_strategy', 'assignment_hash': 'test-assignment_hash', 'completion_pct': 1.0, 'status': 'test-status', 'routed_at': 'test-routed_at'})
    await client.post("/api/pit-crew", json={'action_ref': 'test-action_ref', 'agent_assignments': [], 'required_skills': [], 'quorum_required': 1, 'quorum_achieved': True, 'veto_agents': [], 'veto_active': True, 'routing_strategy': 'test-routing_strategy', 'assignment_hash': 'test-assignment_hash', 'completion_pct': 1.0, 'status': 'test-status', 'routed_at': 'test-routed_at'})
    r = await client.get("/api/pit-crew")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w247_get_by_id(client):
    r = await client.post("/api/pit-crew", json={'action_ref': 'test-action_ref', 'agent_assignments': [], 'required_skills': [], 'quorum_required': 1, 'quorum_achieved': True, 'veto_agents': [], 'veto_active': True, 'routing_strategy': 'test-routing_strategy', 'assignment_hash': 'test-assignment_hash', 'completion_pct': 1.0, 'status': 'test-status', 'routed_at': 'test-routed_at'})
    item_id = r.json()["routing_id"]
    r2 = await client.get(f"/api/pit-crew/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["routing_id"] == item_id

@pytest.mark.asyncio
async def test_w247_get_not_found(client):
    r = await client.get("/api/pit-crew/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w247_assign_agent(client):
    r = await client.post("/api/pit-crew", json={'action_ref': 'test-action_ref', 'agent_assignments': [], 'required_skills': [], 'quorum_required': 1, 'quorum_achieved': True, 'veto_agents': [], 'veto_active': True, 'routing_strategy': 'test-routing_strategy', 'assignment_hash': 'test-assignment_hash', 'completion_pct': 1.0, 'status': 'test-status', 'routed_at': 'test-routed_at'})
    item_id = r.json()["routing_id"]
    r2 = await client.post(f"/api/pit-crew/{item_id}/assign", json={})
    assert r2.status_code == 200
    assert r2.json()["routing_id"] == item_id

@pytest.mark.asyncio
async def test_w247_record_veto(client):
    r = await client.post("/api/pit-crew", json={'action_ref': 'test-action_ref', 'agent_assignments': [], 'required_skills': [], 'quorum_required': 1, 'quorum_achieved': True, 'veto_agents': [], 'veto_active': True, 'routing_strategy': 'test-routing_strategy', 'assignment_hash': 'test-assignment_hash', 'completion_pct': 1.0, 'status': 'test-status', 'routed_at': 'test-routed_at'})
    item_id = r.json()["routing_id"]
    r2 = await client.post(f"/api/pit-crew/{item_id}/veto", json={})
    assert r2.status_code == 200
    assert r2.json()["routing_id"] == item_id

@pytest.mark.asyncio
async def test_w247_check_quorum(client):
    r = await client.post("/api/pit-crew", json={'action_ref': 'test-action_ref', 'agent_assignments': [], 'required_skills': [], 'quorum_required': 1, 'quorum_achieved': True, 'veto_agents': [], 'veto_active': True, 'routing_strategy': 'test-routing_strategy', 'assignment_hash': 'test-assignment_hash', 'completion_pct': 1.0, 'status': 'test-status', 'routed_at': 'test-routed_at'})
    item_id = r.json()["routing_id"]
    r2 = await client.post(f"/api/pit-crew/{item_id}/quorum", json={})
    assert r2.status_code == 200
    assert r2.json()["routing_id"] == item_id

@pytest.mark.asyncio
async def test_w247_assign_agent_not_found(client):
    r = await client.post("/api/pit-crew/nonexistent-id/assign", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w247_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/pit-crew", json={'action_ref': 'test-action_ref', 'agent_assignments': [], 'required_skills': [], 'quorum_required': 1, 'quorum_achieved': True, 'veto_agents': [], 'veto_active': True, 'routing_strategy': 'test-routing_strategy', 'assignment_hash': 'test-assignment_hash', 'completion_pct': 1.0, 'status': 'test-status', 'routed_at': 'test-routed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "pit_crew_routing"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w247_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/pit-crew", json={'action_ref': 'test-action_ref', 'agent_assignments': [], 'required_skills': [], 'quorum_required': 1, 'quorum_achieved': True, 'veto_agents': [], 'veto_active': True, 'routing_strategy': 'test-routing_strategy', 'assignment_hash': 'test-assignment_hash', 'completion_pct': 1.0, 'status': 'test-status', 'routed_at': 'test-routed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/pit-crew", json={'action_ref': 'test-action_ref', 'agent_assignments': [], 'required_skills': [], 'quorum_required': 1, 'quorum_achieved': True, 'veto_agents': [], 'veto_active': True, 'routing_strategy': 'test-routing_strategy', 'assignment_hash': 'test-assignment_hash', 'completion_pct': 1.0, 'status': 'test-status', 'routed_at': 'test-routed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "routing_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w247_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/pit-crew", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w247_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/pit-crew", json={'action_ref': 'test-action_ref', 'agent_assignments': [], 'required_skills': [], 'quorum_required': 1, 'quorum_achieved': True, 'veto_agents': [], 'veto_active': True, 'routing_strategy': 'test-routing_strategy', 'assignment_hash': 'test-assignment_hash', 'completion_pct': 1.0, 'status': 'test-status', 'routed_at': 'test-routed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["routing_id"]
    r2 = await client.get("/api/pit-crew")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/pit-crew/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["routing_id"] == item_id
