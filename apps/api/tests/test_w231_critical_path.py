"""Tests for Wave 231: Critical Path Analyzer v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w231_critical_path import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w231_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w231_create(client):
    r = await client.post("/api/critical-path", json={'dag_id': 'test-dag_id', 'critical_nodes': [], 'critical_edges': [], 'total_duration': 1, 'earliest_start': {}, 'latest_finish': {}, 'float_values': {}, 'bottleneck_node': 'test-bottleneck_node', 'slack_available': 1, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "analysis_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w231_list(client):
    await client.post("/api/critical-path", json={'dag_id': 'test-dag_id', 'critical_nodes': [], 'critical_edges': [], 'total_duration': 1, 'earliest_start': {}, 'latest_finish': {}, 'float_values': {}, 'bottleneck_node': 'test-bottleneck_node', 'slack_available': 1, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    await client.post("/api/critical-path", json={'dag_id': 'test-dag_id', 'critical_nodes': [], 'critical_edges': [], 'total_duration': 1, 'earliest_start': {}, 'latest_finish': {}, 'float_values': {}, 'bottleneck_node': 'test-bottleneck_node', 'slack_available': 1, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    r = await client.get("/api/critical-path")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w231_get_by_id(client):
    r = await client.post("/api/critical-path", json={'dag_id': 'test-dag_id', 'critical_nodes': [], 'critical_edges': [], 'total_duration': 1, 'earliest_start': {}, 'latest_finish': {}, 'float_values': {}, 'bottleneck_node': 'test-bottleneck_node', 'slack_available': 1, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    item_id = r.json()["analysis_id"]
    r2 = await client.get(f"/api/critical-path/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["analysis_id"] == item_id

@pytest.mark.asyncio
async def test_w231_get_not_found(client):
    r = await client.get("/api/critical-path/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w231_find_bottleneck(client):
    r = await client.post("/api/critical-path", json={'dag_id': 'test-dag_id', 'critical_nodes': [], 'critical_edges': [], 'total_duration': 1, 'earliest_start': {}, 'latest_finish': {}, 'float_values': {}, 'bottleneck_node': 'test-bottleneck_node', 'slack_available': 1, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    item_id = r.json()["analysis_id"]
    r2 = await client.post(f"/api/critical-path/{item_id}/bottleneck", json={})
    assert r2.status_code == 200
    assert r2.json()["analysis_id"] == item_id

@pytest.mark.asyncio
async def test_w231_compute_float(client):
    r = await client.post("/api/critical-path", json={'dag_id': 'test-dag_id', 'critical_nodes': [], 'critical_edges': [], 'total_duration': 1, 'earliest_start': {}, 'latest_finish': {}, 'float_values': {}, 'bottleneck_node': 'test-bottleneck_node', 'slack_available': 1, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    item_id = r.json()["analysis_id"]
    r2 = await client.post(f"/api/critical-path/{item_id}/float", json={})
    assert r2.status_code == 200
    assert r2.json()["analysis_id"] == item_id

@pytest.mark.asyncio
async def test_w231_find_bottleneck_not_found(client):
    r = await client.post("/api/critical-path/nonexistent-id/bottleneck", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w231_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/critical-path", json={'dag_id': 'test-dag_id', 'critical_nodes': [], 'critical_edges': [], 'total_duration': 1, 'earliest_start': {}, 'latest_finish': {}, 'float_values': {}, 'bottleneck_node': 'test-bottleneck_node', 'slack_available': 1, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "critical_path"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w231_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/critical-path", json={'dag_id': 'test-dag_id', 'critical_nodes': [], 'critical_edges': [], 'total_duration': 1, 'earliest_start': {}, 'latest_finish': {}, 'float_values': {}, 'bottleneck_node': 'test-bottleneck_node', 'slack_available': 1, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/critical-path", json={'dag_id': 'test-dag_id', 'critical_nodes': [], 'critical_edges': [], 'total_duration': 1, 'earliest_start': {}, 'latest_finish': {}, 'float_values': {}, 'bottleneck_node': 'test-bottleneck_node', 'slack_available': 1, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "analysis_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w231_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/critical-path", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w231_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/critical-path", json={'dag_id': 'test-dag_id', 'critical_nodes': [], 'critical_edges': [], 'total_duration': 1, 'earliest_start': {}, 'latest_finish': {}, 'float_values': {}, 'bottleneck_node': 'test-bottleneck_node', 'slack_available': 1, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["analysis_id"]
    r2 = await client.get("/api/critical-path")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/critical-path/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["analysis_id"] == item_id
