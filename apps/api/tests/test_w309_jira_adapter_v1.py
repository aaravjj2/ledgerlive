"""Tests for Wave 309: Jira Adapter v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w309_jira_adapter_v1 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w309_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w309_create(client):
    r = await client.post("/api/jira-adapter", json={'issue_type': 'test-issue_type', 'summary': 'test-summary', 'description': 'test-description', 'priority': 'test-priority', 'blocker_ref': 'test-blocker_ref', 'incident_ref': 'test-incident_ref', 'approval_ref': 'test-approval_ref', 'idempotency_key': 'test-idempotency_key', 'deep_link': 'test-deep_link', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "issue_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w309_list(client):
    await client.post("/api/jira-adapter", json={'issue_type': 'test-issue_type', 'summary': 'test-summary', 'description': 'test-description', 'priority': 'test-priority', 'blocker_ref': 'test-blocker_ref', 'incident_ref': 'test-incident_ref', 'approval_ref': 'test-approval_ref', 'idempotency_key': 'test-idempotency_key', 'deep_link': 'test-deep_link', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/jira-adapter", json={'issue_type': 'test-issue_type', 'summary': 'test-summary', 'description': 'test-description', 'priority': 'test-priority', 'blocker_ref': 'test-blocker_ref', 'incident_ref': 'test-incident_ref', 'approval_ref': 'test-approval_ref', 'idempotency_key': 'test-idempotency_key', 'deep_link': 'test-deep_link', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/jira-adapter")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w309_get_by_id(client):
    r = await client.post("/api/jira-adapter", json={'issue_type': 'test-issue_type', 'summary': 'test-summary', 'description': 'test-description', 'priority': 'test-priority', 'blocker_ref': 'test-blocker_ref', 'incident_ref': 'test-incident_ref', 'approval_ref': 'test-approval_ref', 'idempotency_key': 'test-idempotency_key', 'deep_link': 'test-deep_link', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["issue_id"]
    r2 = await client.get(f"/api/jira-adapter/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["issue_id"] == item_id

@pytest.mark.asyncio
async def test_w309_get_not_found(client):
    r = await client.get("/api/jira-adapter/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w309_update_issue(client):
    r = await client.post("/api/jira-adapter", json={'issue_type': 'test-issue_type', 'summary': 'test-summary', 'description': 'test-description', 'priority': 'test-priority', 'blocker_ref': 'test-blocker_ref', 'incident_ref': 'test-incident_ref', 'approval_ref': 'test-approval_ref', 'idempotency_key': 'test-idempotency_key', 'deep_link': 'test-deep_link', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["issue_id"]
    r2 = await client.post(f"/api/jira-adapter/{item_id}/update", json={})
    assert r2.status_code == 200
    assert r2.json()["issue_id"] == item_id

@pytest.mark.asyncio
async def test_w309_transition_issue(client):
    r = await client.post("/api/jira-adapter", json={'issue_type': 'test-issue_type', 'summary': 'test-summary', 'description': 'test-description', 'priority': 'test-priority', 'blocker_ref': 'test-blocker_ref', 'incident_ref': 'test-incident_ref', 'approval_ref': 'test-approval_ref', 'idempotency_key': 'test-idempotency_key', 'deep_link': 'test-deep_link', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["issue_id"]
    r2 = await client.post(f"/api/jira-adapter/{item_id}/transition", json={})
    assert r2.status_code == 200
    assert r2.json()["issue_id"] == item_id

@pytest.mark.asyncio
async def test_w309_resolve_issue(client):
    r = await client.post("/api/jira-adapter", json={'issue_type': 'test-issue_type', 'summary': 'test-summary', 'description': 'test-description', 'priority': 'test-priority', 'blocker_ref': 'test-blocker_ref', 'incident_ref': 'test-incident_ref', 'approval_ref': 'test-approval_ref', 'idempotency_key': 'test-idempotency_key', 'deep_link': 'test-deep_link', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["issue_id"]
    r2 = await client.post(f"/api/jira-adapter/{item_id}/resolve", json={})
    assert r2.status_code == 200
    assert r2.json()["issue_id"] == item_id

@pytest.mark.asyncio
async def test_w309_update_issue_not_found(client):
    r = await client.post("/api/jira-adapter/nonexistent-id/update", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w309_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/jira-adapter", json={'issue_type': 'test-issue_type', 'summary': 'test-summary', 'description': 'test-description', 'priority': 'test-priority', 'blocker_ref': 'test-blocker_ref', 'incident_ref': 'test-incident_ref', 'approval_ref': 'test-approval_ref', 'idempotency_key': 'test-idempotency_key', 'deep_link': 'test-deep_link', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "jira_adapter_v1"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w309_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/jira-adapter", json={'issue_type': 'test-issue_type', 'summary': 'test-summary', 'description': 'test-description', 'priority': 'test-priority', 'blocker_ref': 'test-blocker_ref', 'incident_ref': 'test-incident_ref', 'approval_ref': 'test-approval_ref', 'idempotency_key': 'test-idempotency_key', 'deep_link': 'test-deep_link', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/jira-adapter", json={'issue_type': 'test-issue_type', 'summary': 'test-summary', 'description': 'test-description', 'priority': 'test-priority', 'blocker_ref': 'test-blocker_ref', 'incident_ref': 'test-incident_ref', 'approval_ref': 'test-approval_ref', 'idempotency_key': 'test-idempotency_key', 'deep_link': 'test-deep_link', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "issue_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w309_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/jira-adapter", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w309_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/jira-adapter", json={'issue_type': 'test-issue_type', 'summary': 'test-summary', 'description': 'test-description', 'priority': 'test-priority', 'blocker_ref': 'test-blocker_ref', 'incident_ref': 'test-incident_ref', 'approval_ref': 'test-approval_ref', 'idempotency_key': 'test-idempotency_key', 'deep_link': 'test-deep_link', 'deterministic': True, 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["issue_id"]
    r2 = await client.get("/api/jira-adapter")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/jira-adapter/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["issue_id"] == item_id
