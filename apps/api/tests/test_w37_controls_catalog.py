"""Tests for Wave 37: Controls Catalog

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w37_controls_catalog import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w37_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w37_create(client):
    r = await client.post("/api/controls", json={'name': 'test-name', 'description': 'test-description', 'control_type': 'test-control_type', 'frequency': 'test-frequency', 'owner': 'test-owner', 'mapped_workflows': [], 'required_evidence': [], 'status': 'test-status', 'last_tested': 'test-last_tested', 'coverage_pct': 1.0})
    assert r.status_code == 201
    data = r.json()
    assert "control_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w37_list(client):
    await client.post("/api/controls", json={'name': 'test-name', 'description': 'test-description', 'control_type': 'test-control_type', 'frequency': 'test-frequency', 'owner': 'test-owner', 'mapped_workflows': [], 'required_evidence': [], 'status': 'test-status', 'last_tested': 'test-last_tested', 'coverage_pct': 1.0})
    await client.post("/api/controls", json={'name': 'test-name', 'description': 'test-description', 'control_type': 'test-control_type', 'frequency': 'test-frequency', 'owner': 'test-owner', 'mapped_workflows': [], 'required_evidence': [], 'status': 'test-status', 'last_tested': 'test-last_tested', 'coverage_pct': 1.0})
    r = await client.get("/api/controls")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w37_get_by_id(client):
    r = await client.post("/api/controls", json={'name': 'test-name', 'description': 'test-description', 'control_type': 'test-control_type', 'frequency': 'test-frequency', 'owner': 'test-owner', 'mapped_workflows': [], 'required_evidence': [], 'status': 'test-status', 'last_tested': 'test-last_tested', 'coverage_pct': 1.0})
    item_id = r.json()["control_id"]
    r2 = await client.get(f"/api/controls/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["control_id"] == item_id

@pytest.mark.asyncio
async def test_w37_get_not_found(client):
    r = await client.get("/api/controls/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w37_map_evidence(client):
    r = await client.post("/api/controls", json={'name': 'test-name', 'description': 'test-description', 'control_type': 'test-control_type', 'frequency': 'test-frequency', 'owner': 'test-owner', 'mapped_workflows': [], 'required_evidence': [], 'status': 'test-status', 'last_tested': 'test-last_tested', 'coverage_pct': 1.0})
    item_id = r.json()["control_id"]
    r2 = await client.post(f"/api/controls/{item_id}/evidence", json={})
    assert r2.status_code == 200
    assert r2.json()["control_id"] == item_id

@pytest.mark.asyncio
async def test_w37_test_control(client):
    r = await client.post("/api/controls", json={'name': 'test-name', 'description': 'test-description', 'control_type': 'test-control_type', 'frequency': 'test-frequency', 'owner': 'test-owner', 'mapped_workflows': [], 'required_evidence': [], 'status': 'test-status', 'last_tested': 'test-last_tested', 'coverage_pct': 1.0})
    item_id = r.json()["control_id"]
    r2 = await client.post(f"/api/controls/{item_id}/test", json={})
    assert r2.status_code == 200
    assert r2.json()["control_id"] == item_id

@pytest.mark.asyncio
async def test_w37_map_evidence_not_found(client):
    r = await client.post("/api/controls/nonexistent-id/evidence", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w37_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/controls", json={'name': 'test-name', 'description': 'test-description', 'control_type': 'test-control_type', 'frequency': 'test-frequency', 'owner': 'test-owner', 'mapped_workflows': [], 'required_evidence': [], 'status': 'test-status', 'last_tested': 'test-last_tested', 'coverage_pct': 1.0})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "controls_catalog"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w37_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/controls", json={'name': 'test-name', 'description': 'test-description', 'control_type': 'test-control_type', 'frequency': 'test-frequency', 'owner': 'test-owner', 'mapped_workflows': [], 'required_evidence': [], 'status': 'test-status', 'last_tested': 'test-last_tested', 'coverage_pct': 1.0})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/controls", json={'name': 'test-name', 'description': 'test-description', 'control_type': 'test-control_type', 'frequency': 'test-frequency', 'owner': 'test-owner', 'mapped_workflows': [], 'required_evidence': [], 'status': 'test-status', 'last_tested': 'test-last_tested', 'coverage_pct': 1.0})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "control_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w37_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/controls", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w37_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/controls", json={'name': 'test-name', 'description': 'test-description', 'control_type': 'test-control_type', 'frequency': 'test-frequency', 'owner': 'test-owner', 'mapped_workflows': [], 'required_evidence': [], 'status': 'test-status', 'last_tested': 'test-last_tested', 'coverage_pct': 1.0})
    assert r1.status_code == 201
    item_id = r1.json()["control_id"]
    r2 = await client.get("/api/controls")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/controls/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["control_id"] == item_id
