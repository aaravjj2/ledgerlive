"""Tests for Wave 241: Next Actions Engine v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w241_next_actions_engine import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w241_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w241_create(client):
    r = await client.post("/api/next-actions", json={'dag_ref': 'test-dag_ref', 'blocker_refs': [], 'sla_ref': 'test-sla_ref', 'incident_refs': [], 'priority_score': 1.0, 'action_type': 'test-action_type', 'description': 'test-description', 'dossier_link': 'test-dossier_link', 'evidence_refs': [], 'estimated_minutes': 1, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "action_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w241_list(client):
    await client.post("/api/next-actions", json={'dag_ref': 'test-dag_ref', 'blocker_refs': [], 'sla_ref': 'test-sla_ref', 'incident_refs': [], 'priority_score': 1.0, 'action_type': 'test-action_type', 'description': 'test-description', 'dossier_link': 'test-dossier_link', 'evidence_refs': [], 'estimated_minutes': 1, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/next-actions", json={'dag_ref': 'test-dag_ref', 'blocker_refs': [], 'sla_ref': 'test-sla_ref', 'incident_refs': [], 'priority_score': 1.0, 'action_type': 'test-action_type', 'description': 'test-description', 'dossier_link': 'test-dossier_link', 'evidence_refs': [], 'estimated_minutes': 1, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/next-actions")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w241_get_by_id(client):
    r = await client.post("/api/next-actions", json={'dag_ref': 'test-dag_ref', 'blocker_refs': [], 'sla_ref': 'test-sla_ref', 'incident_refs': [], 'priority_score': 1.0, 'action_type': 'test-action_type', 'description': 'test-description', 'dossier_link': 'test-dossier_link', 'evidence_refs': [], 'estimated_minutes': 1, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["action_id"]
    r2 = await client.get(f"/api/next-actions/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["action_id"] == item_id

@pytest.mark.asyncio
async def test_w241_get_not_found(client):
    r = await client.get("/api/next-actions/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w241_reprioritize(client):
    r = await client.post("/api/next-actions", json={'dag_ref': 'test-dag_ref', 'blocker_refs': [], 'sla_ref': 'test-sla_ref', 'incident_refs': [], 'priority_score': 1.0, 'action_type': 'test-action_type', 'description': 'test-description', 'dossier_link': 'test-dossier_link', 'evidence_refs': [], 'estimated_minutes': 1, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["action_id"]
    r2 = await client.post(f"/api/next-actions/{item_id}/reprioritize", json={})
    assert r2.status_code == 200
    assert r2.json()["action_id"] == item_id

@pytest.mark.asyncio
async def test_w241_link_dossier(client):
    r = await client.post("/api/next-actions", json={'dag_ref': 'test-dag_ref', 'blocker_refs': [], 'sla_ref': 'test-sla_ref', 'incident_refs': [], 'priority_score': 1.0, 'action_type': 'test-action_type', 'description': 'test-description', 'dossier_link': 'test-dossier_link', 'evidence_refs': [], 'estimated_minutes': 1, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["action_id"]
    r2 = await client.post(f"/api/next-actions/{item_id}/link-dossier", json={})
    assert r2.status_code == 200
    assert r2.json()["action_id"] == item_id

@pytest.mark.asyncio
async def test_w241_dismiss_action(client):
    r = await client.post("/api/next-actions", json={'dag_ref': 'test-dag_ref', 'blocker_refs': [], 'sla_ref': 'test-sla_ref', 'incident_refs': [], 'priority_score': 1.0, 'action_type': 'test-action_type', 'description': 'test-description', 'dossier_link': 'test-dossier_link', 'evidence_refs': [], 'estimated_minutes': 1, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["action_id"]
    r2 = await client.post(f"/api/next-actions/{item_id}/dismiss", json={})
    assert r2.status_code == 200
    assert r2.json()["action_id"] == item_id

@pytest.mark.asyncio
async def test_w241_reprioritize_not_found(client):
    r = await client.post("/api/next-actions/nonexistent-id/reprioritize", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w241_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/next-actions", json={'dag_ref': 'test-dag_ref', 'blocker_refs': [], 'sla_ref': 'test-sla_ref', 'incident_refs': [], 'priority_score': 1.0, 'action_type': 'test-action_type', 'description': 'test-description', 'dossier_link': 'test-dossier_link', 'evidence_refs': [], 'estimated_minutes': 1, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "next_actions_engine"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w241_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/next-actions", json={'dag_ref': 'test-dag_ref', 'blocker_refs': [], 'sla_ref': 'test-sla_ref', 'incident_refs': [], 'priority_score': 1.0, 'action_type': 'test-action_type', 'description': 'test-description', 'dossier_link': 'test-dossier_link', 'evidence_refs': [], 'estimated_minutes': 1, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/next-actions", json={'dag_ref': 'test-dag_ref', 'blocker_refs': [], 'sla_ref': 'test-sla_ref', 'incident_refs': [], 'priority_score': 1.0, 'action_type': 'test-action_type', 'description': 'test-description', 'dossier_link': 'test-dossier_link', 'evidence_refs': [], 'estimated_minutes': 1, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "action_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w241_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/next-actions", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w241_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/next-actions", json={'dag_ref': 'test-dag_ref', 'blocker_refs': [], 'sla_ref': 'test-sla_ref', 'incident_refs': [], 'priority_score': 1.0, 'action_type': 'test-action_type', 'description': 'test-description', 'dossier_link': 'test-dossier_link', 'evidence_refs': [], 'estimated_minutes': 1, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["action_id"]
    r2 = await client.get("/api/next-actions")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/next-actions/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["action_id"] == item_id
