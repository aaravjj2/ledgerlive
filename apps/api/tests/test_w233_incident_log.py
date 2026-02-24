"""Tests for Wave 233: Incident Log v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w233_incident_log import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w233_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w233_create(client):
    r = await client.post("/api/incident-log", json={'incident_title': 'test-incident_title', 'severity': 'test-severity', 'category': 'test-category', 'description': 'test-description', 'impact_assessment': 'test-impact_assessment', 'affected_tasks': [], 'reported_by': 'test-reported_by', 'reported_at': 'test-reported_at', 'resolved_at': 'test-resolved_at', 'root_cause': 'test-root_cause', 'resolution_summary': 'test-resolution_summary', 'status': 'test-status'})
    assert r.status_code == 201
    data = r.json()
    assert "incident_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w233_list(client):
    await client.post("/api/incident-log", json={'incident_title': 'test-incident_title', 'severity': 'test-severity', 'category': 'test-category', 'description': 'test-description', 'impact_assessment': 'test-impact_assessment', 'affected_tasks': [], 'reported_by': 'test-reported_by', 'reported_at': 'test-reported_at', 'resolved_at': 'test-resolved_at', 'root_cause': 'test-root_cause', 'resolution_summary': 'test-resolution_summary', 'status': 'test-status'})
    await client.post("/api/incident-log", json={'incident_title': 'test-incident_title', 'severity': 'test-severity', 'category': 'test-category', 'description': 'test-description', 'impact_assessment': 'test-impact_assessment', 'affected_tasks': [], 'reported_by': 'test-reported_by', 'reported_at': 'test-reported_at', 'resolved_at': 'test-resolved_at', 'root_cause': 'test-root_cause', 'resolution_summary': 'test-resolution_summary', 'status': 'test-status'})
    r = await client.get("/api/incident-log")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w233_get_by_id(client):
    r = await client.post("/api/incident-log", json={'incident_title': 'test-incident_title', 'severity': 'test-severity', 'category': 'test-category', 'description': 'test-description', 'impact_assessment': 'test-impact_assessment', 'affected_tasks': [], 'reported_by': 'test-reported_by', 'reported_at': 'test-reported_at', 'resolved_at': 'test-resolved_at', 'root_cause': 'test-root_cause', 'resolution_summary': 'test-resolution_summary', 'status': 'test-status'})
    item_id = r.json()["incident_id"]
    r2 = await client.get(f"/api/incident-log/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["incident_id"] == item_id

@pytest.mark.asyncio
async def test_w233_get_not_found(client):
    r = await client.get("/api/incident-log/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w233_resolve_incident(client):
    r = await client.post("/api/incident-log", json={'incident_title': 'test-incident_title', 'severity': 'test-severity', 'category': 'test-category', 'description': 'test-description', 'impact_assessment': 'test-impact_assessment', 'affected_tasks': [], 'reported_by': 'test-reported_by', 'reported_at': 'test-reported_at', 'resolved_at': 'test-resolved_at', 'root_cause': 'test-root_cause', 'resolution_summary': 'test-resolution_summary', 'status': 'test-status'})
    item_id = r.json()["incident_id"]
    r2 = await client.post(f"/api/incident-log/{item_id}/resolve", json={})
    assert r2.status_code == 200
    assert r2.json()["incident_id"] == item_id

@pytest.mark.asyncio
async def test_w233_assess_impact(client):
    r = await client.post("/api/incident-log", json={'incident_title': 'test-incident_title', 'severity': 'test-severity', 'category': 'test-category', 'description': 'test-description', 'impact_assessment': 'test-impact_assessment', 'affected_tasks': [], 'reported_by': 'test-reported_by', 'reported_at': 'test-reported_at', 'resolved_at': 'test-resolved_at', 'root_cause': 'test-root_cause', 'resolution_summary': 'test-resolution_summary', 'status': 'test-status'})
    item_id = r.json()["incident_id"]
    r2 = await client.post(f"/api/incident-log/{item_id}/impact", json={})
    assert r2.status_code == 200
    assert r2.json()["incident_id"] == item_id

@pytest.mark.asyncio
async def test_w233_resolve_incident_not_found(client):
    r = await client.post("/api/incident-log/nonexistent-id/resolve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w233_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/incident-log", json={'incident_title': 'test-incident_title', 'severity': 'test-severity', 'category': 'test-category', 'description': 'test-description', 'impact_assessment': 'test-impact_assessment', 'affected_tasks': [], 'reported_by': 'test-reported_by', 'reported_at': 'test-reported_at', 'resolved_at': 'test-resolved_at', 'root_cause': 'test-root_cause', 'resolution_summary': 'test-resolution_summary', 'status': 'test-status'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "incident_log"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w233_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/incident-log", json={'incident_title': 'test-incident_title', 'severity': 'test-severity', 'category': 'test-category', 'description': 'test-description', 'impact_assessment': 'test-impact_assessment', 'affected_tasks': [], 'reported_by': 'test-reported_by', 'reported_at': 'test-reported_at', 'resolved_at': 'test-resolved_at', 'root_cause': 'test-root_cause', 'resolution_summary': 'test-resolution_summary', 'status': 'test-status'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/incident-log", json={'incident_title': 'test-incident_title', 'severity': 'test-severity', 'category': 'test-category', 'description': 'test-description', 'impact_assessment': 'test-impact_assessment', 'affected_tasks': [], 'reported_by': 'test-reported_by', 'reported_at': 'test-reported_at', 'resolved_at': 'test-resolved_at', 'root_cause': 'test-root_cause', 'resolution_summary': 'test-resolution_summary', 'status': 'test-status'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "incident_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w233_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/incident-log", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w233_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/incident-log", json={'incident_title': 'test-incident_title', 'severity': 'test-severity', 'category': 'test-category', 'description': 'test-description', 'impact_assessment': 'test-impact_assessment', 'affected_tasks': [], 'reported_by': 'test-reported_by', 'reported_at': 'test-reported_at', 'resolved_at': 'test-resolved_at', 'root_cause': 'test-root_cause', 'resolution_summary': 'test-resolution_summary', 'status': 'test-status'})
    assert r1.status_code == 201
    item_id = r1.json()["incident_id"]
    r2 = await client.get("/api/incident-log")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/incident-log/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["incident_id"] == item_id
