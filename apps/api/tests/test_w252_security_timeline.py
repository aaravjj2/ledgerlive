"""Tests for Wave 252: Security Timeline v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w252_security_timeline import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w252_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w252_create(client):
    r = await client.post("/api/security-timeline", json={'entries': [], 'filter_criteria': {}, 'date_range_start': 'test-date_range_start', 'date_range_end': 'test-date_range_end', 'entry_count': 1, 'severity_distribution': {}, 'export_format': 'test-export_format', 'render_hash': 'test-render_hash', 'includes_incidents': True, 'includes_policy_events': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "timeline_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w252_list(client):
    await client.post("/api/security-timeline", json={'entries': [], 'filter_criteria': {}, 'date_range_start': 'test-date_range_start', 'date_range_end': 'test-date_range_end', 'entry_count': 1, 'severity_distribution': {}, 'export_format': 'test-export_format', 'render_hash': 'test-render_hash', 'includes_incidents': True, 'includes_policy_events': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/security-timeline", json={'entries': [], 'filter_criteria': {}, 'date_range_start': 'test-date_range_start', 'date_range_end': 'test-date_range_end', 'entry_count': 1, 'severity_distribution': {}, 'export_format': 'test-export_format', 'render_hash': 'test-render_hash', 'includes_incidents': True, 'includes_policy_events': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/security-timeline")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w252_get_by_id(client):
    r = await client.post("/api/security-timeline", json={'entries': [], 'filter_criteria': {}, 'date_range_start': 'test-date_range_start', 'date_range_end': 'test-date_range_end', 'entry_count': 1, 'severity_distribution': {}, 'export_format': 'test-export_format', 'render_hash': 'test-render_hash', 'includes_incidents': True, 'includes_policy_events': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["timeline_id"]
    r2 = await client.get(f"/api/security-timeline/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["timeline_id"] == item_id

@pytest.mark.asyncio
async def test_w252_get_not_found(client):
    r = await client.get("/api/security-timeline/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w252_filter_timeline(client):
    r = await client.post("/api/security-timeline", json={'entries': [], 'filter_criteria': {}, 'date_range_start': 'test-date_range_start', 'date_range_end': 'test-date_range_end', 'entry_count': 1, 'severity_distribution': {}, 'export_format': 'test-export_format', 'render_hash': 'test-render_hash', 'includes_incidents': True, 'includes_policy_events': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["timeline_id"]
    r2 = await client.post(f"/api/security-timeline/{item_id}/filter", json={})
    assert r2.status_code == 200
    assert r2.json()["timeline_id"] == item_id

@pytest.mark.asyncio
async def test_w252_export_timeline(client):
    r = await client.post("/api/security-timeline", json={'entries': [], 'filter_criteria': {}, 'date_range_start': 'test-date_range_start', 'date_range_end': 'test-date_range_end', 'entry_count': 1, 'severity_distribution': {}, 'export_format': 'test-export_format', 'render_hash': 'test-render_hash', 'includes_incidents': True, 'includes_policy_events': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["timeline_id"]
    r2 = await client.post(f"/api/security-timeline/{item_id}/export", json={})
    assert r2.status_code == 200
    assert r2.json()["timeline_id"] == item_id

@pytest.mark.asyncio
async def test_w252_filter_timeline_not_found(client):
    r = await client.post("/api/security-timeline/nonexistent-id/filter", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w252_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/security-timeline", json={'entries': [], 'filter_criteria': {}, 'date_range_start': 'test-date_range_start', 'date_range_end': 'test-date_range_end', 'entry_count': 1, 'severity_distribution': {}, 'export_format': 'test-export_format', 'render_hash': 'test-render_hash', 'includes_incidents': True, 'includes_policy_events': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "security_timeline"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w252_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/security-timeline", json={'entries': [], 'filter_criteria': {}, 'date_range_start': 'test-date_range_start', 'date_range_end': 'test-date_range_end', 'entry_count': 1, 'severity_distribution': {}, 'export_format': 'test-export_format', 'render_hash': 'test-render_hash', 'includes_incidents': True, 'includes_policy_events': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/security-timeline", json={'entries': [], 'filter_criteria': {}, 'date_range_start': 'test-date_range_start', 'date_range_end': 'test-date_range_end', 'entry_count': 1, 'severity_distribution': {}, 'export_format': 'test-export_format', 'render_hash': 'test-render_hash', 'includes_incidents': True, 'includes_policy_events': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "timeline_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w252_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/security-timeline", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w252_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/security-timeline", json={'entries': [], 'filter_criteria': {}, 'date_range_start': 'test-date_range_start', 'date_range_end': 'test-date_range_end', 'entry_count': 1, 'severity_distribution': {}, 'export_format': 'test-export_format', 'render_hash': 'test-render_hash', 'includes_incidents': True, 'includes_policy_events': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["timeline_id"]
    r2 = await client.get("/api/security-timeline")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/security-timeline/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["timeline_id"] == item_id
