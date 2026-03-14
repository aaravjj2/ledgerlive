"""Tests for Wave 246: Fail-Closed Escalation v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w246_fail_closed_escalation import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w246_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w246_create(client):
    r = await client.post("/api/fail-closed-escalation", json={'step_ref': 'test-step_ref', 'risk_rule_results': {}, 'uncertainty_score': 1.0, 'escalation_type': 'test-escalation_type', 'approval_required': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'automation_paused': True, 'pause_reason': 'test-pause_reason', 'escalation_chain': [], 'status': 'test-status', 'escalated_at': 'test-escalated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "escalation_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w246_list(client):
    await client.post("/api/fail-closed-escalation", json={'step_ref': 'test-step_ref', 'risk_rule_results': {}, 'uncertainty_score': 1.0, 'escalation_type': 'test-escalation_type', 'approval_required': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'automation_paused': True, 'pause_reason': 'test-pause_reason', 'escalation_chain': [], 'status': 'test-status', 'escalated_at': 'test-escalated_at'})
    await client.post("/api/fail-closed-escalation", json={'step_ref': 'test-step_ref', 'risk_rule_results': {}, 'uncertainty_score': 1.0, 'escalation_type': 'test-escalation_type', 'approval_required': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'automation_paused': True, 'pause_reason': 'test-pause_reason', 'escalation_chain': [], 'status': 'test-status', 'escalated_at': 'test-escalated_at'})
    r = await client.get("/api/fail-closed-escalation")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w246_get_by_id(client):
    r = await client.post("/api/fail-closed-escalation", json={'step_ref': 'test-step_ref', 'risk_rule_results': {}, 'uncertainty_score': 1.0, 'escalation_type': 'test-escalation_type', 'approval_required': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'automation_paused': True, 'pause_reason': 'test-pause_reason', 'escalation_chain': [], 'status': 'test-status', 'escalated_at': 'test-escalated_at'})
    item_id = r.json()["escalation_id"]
    r2 = await client.get(f"/api/fail-closed-escalation/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["escalation_id"] == item_id

@pytest.mark.asyncio
async def test_w246_get_not_found(client):
    r = await client.get("/api/fail-closed-escalation/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w246_approve_escalation(client):
    r = await client.post("/api/fail-closed-escalation", json={'step_ref': 'test-step_ref', 'risk_rule_results': {}, 'uncertainty_score': 1.0, 'escalation_type': 'test-escalation_type', 'approval_required': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'automation_paused': True, 'pause_reason': 'test-pause_reason', 'escalation_chain': [], 'status': 'test-status', 'escalated_at': 'test-escalated_at'})
    item_id = r.json()["escalation_id"]
    r2 = await client.post(f"/api/fail-closed-escalation/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["escalation_id"] == item_id

@pytest.mark.asyncio
async def test_w246_create_incident(client):
    r = await client.post("/api/fail-closed-escalation", json={'step_ref': 'test-step_ref', 'risk_rule_results': {}, 'uncertainty_score': 1.0, 'escalation_type': 'test-escalation_type', 'approval_required': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'automation_paused': True, 'pause_reason': 'test-pause_reason', 'escalation_chain': [], 'status': 'test-status', 'escalated_at': 'test-escalated_at'})
    item_id = r.json()["escalation_id"]
    r2 = await client.post(f"/api/fail-closed-escalation/{item_id}/create-incident", json={})
    assert r2.status_code == 200
    assert r2.json()["escalation_id"] == item_id

@pytest.mark.asyncio
async def test_w246_resume_automation(client):
    r = await client.post("/api/fail-closed-escalation", json={'step_ref': 'test-step_ref', 'risk_rule_results': {}, 'uncertainty_score': 1.0, 'escalation_type': 'test-escalation_type', 'approval_required': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'automation_paused': True, 'pause_reason': 'test-pause_reason', 'escalation_chain': [], 'status': 'test-status', 'escalated_at': 'test-escalated_at'})
    item_id = r.json()["escalation_id"]
    r2 = await client.post(f"/api/fail-closed-escalation/{item_id}/resume", json={})
    assert r2.status_code == 200
    assert r2.json()["escalation_id"] == item_id

@pytest.mark.asyncio
async def test_w246_approve_escalation_not_found(client):
    r = await client.post("/api/fail-closed-escalation/nonexistent-id/approve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w246_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/fail-closed-escalation", json={'step_ref': 'test-step_ref', 'risk_rule_results': {}, 'uncertainty_score': 1.0, 'escalation_type': 'test-escalation_type', 'approval_required': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'automation_paused': True, 'pause_reason': 'test-pause_reason', 'escalation_chain': [], 'status': 'test-status', 'escalated_at': 'test-escalated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "fail_closed_escalation"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w246_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/fail-closed-escalation", json={'step_ref': 'test-step_ref', 'risk_rule_results': {}, 'uncertainty_score': 1.0, 'escalation_type': 'test-escalation_type', 'approval_required': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'automation_paused': True, 'pause_reason': 'test-pause_reason', 'escalation_chain': [], 'status': 'test-status', 'escalated_at': 'test-escalated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/fail-closed-escalation", json={'step_ref': 'test-step_ref', 'risk_rule_results': {}, 'uncertainty_score': 1.0, 'escalation_type': 'test-escalation_type', 'approval_required': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'automation_paused': True, 'pause_reason': 'test-pause_reason', 'escalation_chain': [], 'status': 'test-status', 'escalated_at': 'test-escalated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "escalation_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w246_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/fail-closed-escalation", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w246_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/fail-closed-escalation", json={'step_ref': 'test-step_ref', 'risk_rule_results': {}, 'uncertainty_score': 1.0, 'escalation_type': 'test-escalation_type', 'approval_required': True, 'incident_created': True, 'incident_ref': 'test-incident_ref', 'automation_paused': True, 'pause_reason': 'test-pause_reason', 'escalation_chain': [], 'status': 'test-status', 'escalated_at': 'test-escalated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["escalation_id"]
    r2 = await client.get("/api/fail-closed-escalation")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/fail-closed-escalation/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["escalation_id"] == item_id

