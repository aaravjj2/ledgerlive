"""Tests for Wave 302: Blueprint Builder v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w302_blueprint_builder_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w302_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w302_create(client):
    r = await client.post("/api/blueprint-graph", json={'blueprint_ref': 'test-blueprint_ref', 'nodes': [], 'edges': [], 'critical_path': [], 'is_valid': True, 'cycle_detected': True, 'depth': 1, 'parallelizable_steps': 1, 'validation_errors': [], 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "graph_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w302_list(client):
    await client.post("/api/blueprint-graph", json={'blueprint_ref': 'test-blueprint_ref', 'nodes': [], 'edges': [], 'critical_path': [], 'is_valid': True, 'cycle_detected': True, 'depth': 1, 'parallelizable_steps': 1, 'validation_errors': [], 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    await client.post("/api/blueprint-graph", json={'blueprint_ref': 'test-blueprint_ref', 'nodes': [], 'edges': [], 'critical_path': [], 'is_valid': True, 'cycle_detected': True, 'depth': 1, 'parallelizable_steps': 1, 'validation_errors': [], 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    r = await client.get("/api/blueprint-graph")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w302_get_by_id(client):
    r = await client.post("/api/blueprint-graph", json={'blueprint_ref': 'test-blueprint_ref', 'nodes': [], 'edges': [], 'critical_path': [], 'is_valid': True, 'cycle_detected': True, 'depth': 1, 'parallelizable_steps': 1, 'validation_errors': [], 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    item_id = r.json()["graph_id"]
    r2 = await client.get(f"/api/blueprint-graph/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["graph_id"] == item_id

@pytest.mark.asyncio
async def test_w302_get_not_found(client):
    r = await client.get("/api/blueprint-graph/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w302_validate_graph(client):
    r = await client.post("/api/blueprint-graph", json={'blueprint_ref': 'test-blueprint_ref', 'nodes': [], 'edges': [], 'critical_path': [], 'is_valid': True, 'cycle_detected': True, 'depth': 1, 'parallelizable_steps': 1, 'validation_errors': [], 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    item_id = r.json()["graph_id"]
    r2 = await client.post(f"/api/blueprint-graph/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["graph_id"] == item_id

@pytest.mark.asyncio
async def test_w302_critical_path(client):
    r = await client.post("/api/blueprint-graph", json={'blueprint_ref': 'test-blueprint_ref', 'nodes': [], 'edges': [], 'critical_path': [], 'is_valid': True, 'cycle_detected': True, 'depth': 1, 'parallelizable_steps': 1, 'validation_errors': [], 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    item_id = r.json()["graph_id"]
    r2 = await client.post(f"/api/blueprint-graph/{item_id}/critical-path", json={})
    assert r2.status_code == 200
    assert r2.json()["graph_id"] == item_id

@pytest.mark.asyncio
async def test_w302_validate_graph_not_found(client):
    r = await client.post("/api/blueprint-graph/nonexistent-id/validate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w302_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/blueprint-graph", json={'blueprint_ref': 'test-blueprint_ref', 'nodes': [], 'edges': [], 'critical_path': [], 'is_valid': True, 'cycle_detected': True, 'depth': 1, 'parallelizable_steps': 1, 'validation_errors': [], 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "blueprint_builder_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w302_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/blueprint-graph", json={'blueprint_ref': 'test-blueprint_ref', 'nodes': [], 'edges': [], 'critical_path': [], 'is_valid': True, 'cycle_detected': True, 'depth': 1, 'parallelizable_steps': 1, 'validation_errors': [], 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/blueprint-graph", json={'blueprint_ref': 'test-blueprint_ref', 'nodes': [], 'edges': [], 'critical_path': [], 'is_valid': True, 'cycle_detected': True, 'depth': 1, 'parallelizable_steps': 1, 'validation_errors': [], 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "graph_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w302_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/blueprint-graph", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w302_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/blueprint-graph", json={'blueprint_ref': 'test-blueprint_ref', 'nodes': [], 'edges': [], 'critical_path': [], 'is_valid': True, 'cycle_detected': True, 'depth': 1, 'parallelizable_steps': 1, 'validation_errors': [], 'deterministic': True, 'status': 'test-status', 'validated_at': 'test-validated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["graph_id"]
    r2 = await client.get("/api/blueprint-graph")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/blueprint-graph/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["graph_id"] == item_id
