"""Tests for Wave 46: Data Quality Engine

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w46_data_quality import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w46_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w46_create(client):
    r = await client.post("/api/data-quality/checks", json={'rule_name': 'test-rule_name', 'rule_type': 'test-rule_type', 'target_entity': 'test-target_entity', 'severity': 'test-severity', 'violations_found': 1, 'quality_score': 1.0, 'blocks_export': True, 'approved_override': True, 'run_at': 'test-run_at'})
    assert r.status_code == 201
    data = r.json()
    assert "check_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w46_list(client):
    await client.post("/api/data-quality/checks", json={'rule_name': 'test-rule_name', 'rule_type': 'test-rule_type', 'target_entity': 'test-target_entity', 'severity': 'test-severity', 'violations_found': 1, 'quality_score': 1.0, 'blocks_export': True, 'approved_override': True, 'run_at': 'test-run_at'})
    await client.post("/api/data-quality/checks", json={'rule_name': 'test-rule_name', 'rule_type': 'test-rule_type', 'target_entity': 'test-target_entity', 'severity': 'test-severity', 'violations_found': 1, 'quality_score': 1.0, 'blocks_export': True, 'approved_override': True, 'run_at': 'test-run_at'})
    r = await client.get("/api/data-quality/checks")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w46_get_by_id(client):
    r = await client.post("/api/data-quality/checks", json={'rule_name': 'test-rule_name', 'rule_type': 'test-rule_type', 'target_entity': 'test-target_entity', 'severity': 'test-severity', 'violations_found': 1, 'quality_score': 1.0, 'blocks_export': True, 'approved_override': True, 'run_at': 'test-run_at'})
    item_id = r.json()["check_id"]
    r2 = await client.get(f"/api/data-quality/checks/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["check_id"] == item_id

@pytest.mark.asyncio
async def test_w46_get_not_found(client):
    r = await client.get("/api/data-quality/checks/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w46_approve_override(client):
    r = await client.post("/api/data-quality/checks", json={'rule_name': 'test-rule_name', 'rule_type': 'test-rule_type', 'target_entity': 'test-target_entity', 'severity': 'test-severity', 'violations_found': 1, 'quality_score': 1.0, 'blocks_export': True, 'approved_override': True, 'run_at': 'test-run_at'})
    item_id = r.json()["check_id"]
    r2 = await client.post(f"/api/data-quality/checks/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["check_id"] == item_id

@pytest.mark.asyncio
async def test_w46_approve_override_not_found(client):
    r = await client.post("/api/data-quality/checks/nonexistent-id/approve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w46_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/data-quality/checks", json={'rule_name': 'test-rule_name', 'rule_type': 'test-rule_type', 'target_entity': 'test-target_entity', 'severity': 'test-severity', 'violations_found': 1, 'quality_score': 1.0, 'blocks_export': True, 'approved_override': True, 'run_at': 'test-run_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "data_quality"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w46_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/data-quality/checks", json={'rule_name': 'test-rule_name', 'rule_type': 'test-rule_type', 'target_entity': 'test-target_entity', 'severity': 'test-severity', 'violations_found': 1, 'quality_score': 1.0, 'blocks_export': True, 'approved_override': True, 'run_at': 'test-run_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/data-quality/checks", json={'rule_name': 'test-rule_name', 'rule_type': 'test-rule_type', 'target_entity': 'test-target_entity', 'severity': 'test-severity', 'violations_found': 1, 'quality_score': 1.0, 'blocks_export': True, 'approved_override': True, 'run_at': 'test-run_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "check_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w46_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/data-quality/checks", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w46_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/data-quality/checks", json={'rule_name': 'test-rule_name', 'rule_type': 'test-rule_type', 'target_entity': 'test-target_entity', 'severity': 'test-severity', 'violations_found': 1, 'quality_score': 1.0, 'blocks_export': True, 'approved_override': True, 'run_at': 'test-run_at'})
    assert r1.status_code == 201
    item_id = r1.json()["check_id"]
    r2 = await client.get("/api/data-quality/checks")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/data-quality/checks/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["check_id"] == item_id
