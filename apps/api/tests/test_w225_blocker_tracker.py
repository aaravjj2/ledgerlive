"""Tests for Wave 225: Blocker Tracker v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w225_blocker_tracker import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w225_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w225_create(client):
    r = await client.post("/api/blocker-tracker", json={'task_id': 'test-task_id', 'blocker_type': 'test-blocker_type', 'description': 'test-description', 'severity': 'test-severity', 'owner': 'test-owner', 'raised_at': 'test-raised_at', 'resolved_at': 'test-resolved_at', 'resolution_notes': 'test-resolution_notes', 'impact_scope': [], 'days_open': 1, 'status': 'test-status'})
    assert r.status_code == 201
    data = r.json()
    assert "blocker_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w225_list(client):
    await client.post("/api/blocker-tracker", json={'task_id': 'test-task_id', 'blocker_type': 'test-blocker_type', 'description': 'test-description', 'severity': 'test-severity', 'owner': 'test-owner', 'raised_at': 'test-raised_at', 'resolved_at': 'test-resolved_at', 'resolution_notes': 'test-resolution_notes', 'impact_scope': [], 'days_open': 1, 'status': 'test-status'})
    await client.post("/api/blocker-tracker", json={'task_id': 'test-task_id', 'blocker_type': 'test-blocker_type', 'description': 'test-description', 'severity': 'test-severity', 'owner': 'test-owner', 'raised_at': 'test-raised_at', 'resolved_at': 'test-resolved_at', 'resolution_notes': 'test-resolution_notes', 'impact_scope': [], 'days_open': 1, 'status': 'test-status'})
    r = await client.get("/api/blocker-tracker")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w225_get_by_id(client):
    r = await client.post("/api/blocker-tracker", json={'task_id': 'test-task_id', 'blocker_type': 'test-blocker_type', 'description': 'test-description', 'severity': 'test-severity', 'owner': 'test-owner', 'raised_at': 'test-raised_at', 'resolved_at': 'test-resolved_at', 'resolution_notes': 'test-resolution_notes', 'impact_scope': [], 'days_open': 1, 'status': 'test-status'})
    item_id = r.json()["blocker_id"]
    r2 = await client.get(f"/api/blocker-tracker/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["blocker_id"] == item_id

@pytest.mark.asyncio
async def test_w225_get_not_found(client):
    r = await client.get("/api/blocker-tracker/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w225_resolve_blocker(client):
    r = await client.post("/api/blocker-tracker", json={'task_id': 'test-task_id', 'blocker_type': 'test-blocker_type', 'description': 'test-description', 'severity': 'test-severity', 'owner': 'test-owner', 'raised_at': 'test-raised_at', 'resolved_at': 'test-resolved_at', 'resolution_notes': 'test-resolution_notes', 'impact_scope': [], 'days_open': 1, 'status': 'test-status'})
    item_id = r.json()["blocker_id"]
    r2 = await client.post(f"/api/blocker-tracker/{item_id}/resolve", json={})
    assert r2.status_code == 200
    assert r2.json()["blocker_id"] == item_id

@pytest.mark.asyncio
async def test_w225_escalate_blocker(client):
    r = await client.post("/api/blocker-tracker", json={'task_id': 'test-task_id', 'blocker_type': 'test-blocker_type', 'description': 'test-description', 'severity': 'test-severity', 'owner': 'test-owner', 'raised_at': 'test-raised_at', 'resolved_at': 'test-resolved_at', 'resolution_notes': 'test-resolution_notes', 'impact_scope': [], 'days_open': 1, 'status': 'test-status'})
    item_id = r.json()["blocker_id"]
    r2 = await client.post(f"/api/blocker-tracker/{item_id}/escalate", json={})
    assert r2.status_code == 200
    assert r2.json()["blocker_id"] == item_id

@pytest.mark.asyncio
async def test_w225_resolve_blocker_not_found(client):
    r = await client.post("/api/blocker-tracker/nonexistent-id/resolve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w225_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/blocker-tracker", json={'task_id': 'test-task_id', 'blocker_type': 'test-blocker_type', 'description': 'test-description', 'severity': 'test-severity', 'owner': 'test-owner', 'raised_at': 'test-raised_at', 'resolved_at': 'test-resolved_at', 'resolution_notes': 'test-resolution_notes', 'impact_scope': [], 'days_open': 1, 'status': 'test-status'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "blocker_tracker"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w225_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/blocker-tracker", json={'task_id': 'test-task_id', 'blocker_type': 'test-blocker_type', 'description': 'test-description', 'severity': 'test-severity', 'owner': 'test-owner', 'raised_at': 'test-raised_at', 'resolved_at': 'test-resolved_at', 'resolution_notes': 'test-resolution_notes', 'impact_scope': [], 'days_open': 1, 'status': 'test-status'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/blocker-tracker", json={'task_id': 'test-task_id', 'blocker_type': 'test-blocker_type', 'description': 'test-description', 'severity': 'test-severity', 'owner': 'test-owner', 'raised_at': 'test-raised_at', 'resolved_at': 'test-resolved_at', 'resolution_notes': 'test-resolution_notes', 'impact_scope': [], 'days_open': 1, 'status': 'test-status'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "blocker_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w225_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/blocker-tracker", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w225_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/blocker-tracker", json={'task_id': 'test-task_id', 'blocker_type': 'test-blocker_type', 'description': 'test-description', 'severity': 'test-severity', 'owner': 'test-owner', 'raised_at': 'test-raised_at', 'resolved_at': 'test-resolved_at', 'resolution_notes': 'test-resolution_notes', 'impact_scope': [], 'days_open': 1, 'status': 'test-status'})
    assert r1.status_code == 201
    item_id = r1.json()["blocker_id"]
    r2 = await client.get("/api/blocker-tracker")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/blocker-tracker/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["blocker_id"] == item_id
