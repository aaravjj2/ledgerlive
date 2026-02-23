"""Tests for Wave 66: Phase2 Integration Flow E2E

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w066_integration_flow_e2e import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w066_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w066_create(client):
    r = await client.post("/api/integration-flow-e2e", json={'flow_name': 'test-flow_name', 'connector_steps': [], 'mapping_steps': [], 'quality_steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'all_passed': True, 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "flow_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w066_list(client):
    await client.post("/api/integration-flow-e2e", json={'flow_name': 'test-flow_name', 'connector_steps': [], 'mapping_steps': [], 'quality_steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'all_passed': True, 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    await client.post("/api/integration-flow-e2e", json={'flow_name': 'test-flow_name', 'connector_steps': [], 'mapping_steps': [], 'quality_steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'all_passed': True, 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    r = await client.get("/api/integration-flow-e2e")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w066_get_by_id(client):
    r = await client.post("/api/integration-flow-e2e", json={'flow_name': 'test-flow_name', 'connector_steps': [], 'mapping_steps': [], 'quality_steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'all_passed': True, 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["flow_id"]
    r2 = await client.get(f"/api/integration-flow-e2e/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["flow_id"] == item_id

@pytest.mark.asyncio
async def test_w066_get_not_found(client):
    r = await client.get("/api/integration-flow-e2e/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w066_advance(client):
    r = await client.post("/api/integration-flow-e2e", json={'flow_name': 'test-flow_name', 'connector_steps': [], 'mapping_steps': [], 'quality_steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'all_passed': True, 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["flow_id"]
    r2 = await client.post(f"/api/integration-flow-e2e/{item_id}/advance", json={})
    assert r2.status_code == 200
    assert r2.json()["flow_id"] == item_id

@pytest.mark.asyncio
async def test_w066_verify_flow(client):
    r = await client.post("/api/integration-flow-e2e", json={'flow_name': 'test-flow_name', 'connector_steps': [], 'mapping_steps': [], 'quality_steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'all_passed': True, 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["flow_id"]
    r2 = await client.post(f"/api/integration-flow-e2e/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["flow_id"] == item_id

@pytest.mark.asyncio
async def test_w066_advance_not_found(client):
    r = await client.post("/api/integration-flow-e2e/nonexistent-id/advance", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w066_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/integration-flow-e2e", json={'flow_name': 'test-flow_name', 'connector_steps': [], 'mapping_steps': [], 'quality_steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'all_passed': True, 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "integration_flow_e2e"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w066_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/integration-flow-e2e", json={'flow_name': 'test-flow_name', 'connector_steps': [], 'mapping_steps': [], 'quality_steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'all_passed': True, 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/integration-flow-e2e", json={'flow_name': 'test-flow_name', 'connector_steps': [], 'mapping_steps': [], 'quality_steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'all_passed': True, 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "flow_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w066_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/integration-flow-e2e", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w066_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/integration-flow-e2e", json={'flow_name': 'test-flow_name', 'connector_steps': [], 'mapping_steps': [], 'quality_steps': [], 'current_step': 1, 'total_steps': 1, 'status': 'test-status', 'all_passed': True, 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["flow_id"]
    r2 = await client.get("/api/integration-flow-e2e")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/integration-flow-e2e/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["flow_id"] == item_id
