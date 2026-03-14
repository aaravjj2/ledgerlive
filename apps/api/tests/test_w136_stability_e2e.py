"""Tests for Wave 136: MCP Stability E2E

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w136_stability_e2e import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w136_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w136_create(client):
    r = await client.post("/api/stability-e2e", json={'flow_name': 'test-flow_name', 'run_count': 1, 'all_consistent': True, 'inconsistencies': [], 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "test_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w136_list(client):
    await client.post("/api/stability-e2e", json={'flow_name': 'test-flow_name', 'run_count': 1, 'all_consistent': True, 'inconsistencies': [], 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    await client.post("/api/stability-e2e", json={'flow_name': 'test-flow_name', 'run_count': 1, 'all_consistent': True, 'inconsistencies': [], 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    r = await client.get("/api/stability-e2e")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w136_get_by_id(client):
    r = await client.post("/api/stability-e2e", json={'flow_name': 'test-flow_name', 'run_count': 1, 'all_consistent': True, 'inconsistencies': [], 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["test_id"]
    r2 = await client.get(f"/api/stability-e2e/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["test_id"] == item_id

@pytest.mark.asyncio
async def test_w136_get_not_found(client):
    r = await client.get("/api/stability-e2e/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w136_verify_consistency(client):
    r = await client.post("/api/stability-e2e", json={'flow_name': 'test-flow_name', 'run_count': 1, 'all_consistent': True, 'inconsistencies': [], 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    item_id = r.json()["test_id"]
    r2 = await client.post(f"/api/stability-e2e/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["test_id"] == item_id

@pytest.mark.asyncio
async def test_w136_verify_consistency_not_found(client):
    r = await client.post("/api/stability-e2e/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w136_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/stability-e2e", json={'flow_name': 'test-flow_name', 'run_count': 1, 'all_consistent': True, 'inconsistencies': [], 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "stability_e2e"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w136_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/stability-e2e", json={'flow_name': 'test-flow_name', 'run_count': 1, 'all_consistent': True, 'inconsistencies': [], 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/stability-e2e", json={'flow_name': 'test-flow_name', 'run_count': 1, 'all_consistent': True, 'inconsistencies': [], 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "test_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w136_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/stability-e2e", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w136_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/stability-e2e", json={'flow_name': 'test-flow_name', 'run_count': 1, 'all_consistent': True, 'inconsistencies': [], 'status': 'test-status', 'started_at': 'test-started_at', 'completed_at': 'test-completed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["test_id"]
    r2 = await client.get("/api/stability-e2e")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/stability-e2e/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["test_id"] == item_id
