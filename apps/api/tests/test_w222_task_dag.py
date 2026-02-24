"""Tests for Wave 222: Task DAG Builder v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w222_task_dag import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w222_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w222_create(client):
    r = await client.post("/api/task-dag", json={'dag_name': 'test-dag_name', 'period_id': 'test-period_id', 'nodes': [], 'edges': [], 'topological_order': [], 'is_valid_dag': True, 'total_nodes': 1, 'completed_nodes': 1, 'critical_path_length': 1, 'status': 'test-status', 'built_at': 'test-built_at'})
    assert r.status_code == 201
    data = r.json()
    assert "dag_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w222_list(client):
    await client.post("/api/task-dag", json={'dag_name': 'test-dag_name', 'period_id': 'test-period_id', 'nodes': [], 'edges': [], 'topological_order': [], 'is_valid_dag': True, 'total_nodes': 1, 'completed_nodes': 1, 'critical_path_length': 1, 'status': 'test-status', 'built_at': 'test-built_at'})
    await client.post("/api/task-dag", json={'dag_name': 'test-dag_name', 'period_id': 'test-period_id', 'nodes': [], 'edges': [], 'topological_order': [], 'is_valid_dag': True, 'total_nodes': 1, 'completed_nodes': 1, 'critical_path_length': 1, 'status': 'test-status', 'built_at': 'test-built_at'})
    r = await client.get("/api/task-dag")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w222_get_by_id(client):
    r = await client.post("/api/task-dag", json={'dag_name': 'test-dag_name', 'period_id': 'test-period_id', 'nodes': [], 'edges': [], 'topological_order': [], 'is_valid_dag': True, 'total_nodes': 1, 'completed_nodes': 1, 'critical_path_length': 1, 'status': 'test-status', 'built_at': 'test-built_at'})
    item_id = r.json()["dag_id"]
    r2 = await client.get(f"/api/task-dag/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["dag_id"] == item_id

@pytest.mark.asyncio
async def test_w222_get_not_found(client):
    r = await client.get("/api/task-dag/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w222_add_node(client):
    r = await client.post("/api/task-dag", json={'dag_name': 'test-dag_name', 'period_id': 'test-period_id', 'nodes': [], 'edges': [], 'topological_order': [], 'is_valid_dag': True, 'total_nodes': 1, 'completed_nodes': 1, 'critical_path_length': 1, 'status': 'test-status', 'built_at': 'test-built_at'})
    item_id = r.json()["dag_id"]
    r2 = await client.post(f"/api/task-dag/{item_id}/node", json={})
    assert r2.status_code == 200
    assert r2.json()["dag_id"] == item_id

@pytest.mark.asyncio
async def test_w222_add_edge(client):
    r = await client.post("/api/task-dag", json={'dag_name': 'test-dag_name', 'period_id': 'test-period_id', 'nodes': [], 'edges': [], 'topological_order': [], 'is_valid_dag': True, 'total_nodes': 1, 'completed_nodes': 1, 'critical_path_length': 1, 'status': 'test-status', 'built_at': 'test-built_at'})
    item_id = r.json()["dag_id"]
    r2 = await client.post(f"/api/task-dag/{item_id}/edge", json={})
    assert r2.status_code == 200
    assert r2.json()["dag_id"] == item_id

@pytest.mark.asyncio
async def test_w222_validate_dag(client):
    r = await client.post("/api/task-dag", json={'dag_name': 'test-dag_name', 'period_id': 'test-period_id', 'nodes': [], 'edges': [], 'topological_order': [], 'is_valid_dag': True, 'total_nodes': 1, 'completed_nodes': 1, 'critical_path_length': 1, 'status': 'test-status', 'built_at': 'test-built_at'})
    item_id = r.json()["dag_id"]
    r2 = await client.post(f"/api/task-dag/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["dag_id"] == item_id

@pytest.mark.asyncio
async def test_w222_add_node_not_found(client):
    r = await client.post("/api/task-dag/nonexistent-id/node", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w222_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/task-dag", json={'dag_name': 'test-dag_name', 'period_id': 'test-period_id', 'nodes': [], 'edges': [], 'topological_order': [], 'is_valid_dag': True, 'total_nodes': 1, 'completed_nodes': 1, 'critical_path_length': 1, 'status': 'test-status', 'built_at': 'test-built_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "task_dag"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w222_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/task-dag", json={'dag_name': 'test-dag_name', 'period_id': 'test-period_id', 'nodes': [], 'edges': [], 'topological_order': [], 'is_valid_dag': True, 'total_nodes': 1, 'completed_nodes': 1, 'critical_path_length': 1, 'status': 'test-status', 'built_at': 'test-built_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/task-dag", json={'dag_name': 'test-dag_name', 'period_id': 'test-period_id', 'nodes': [], 'edges': [], 'topological_order': [], 'is_valid_dag': True, 'total_nodes': 1, 'completed_nodes': 1, 'critical_path_length': 1, 'status': 'test-status', 'built_at': 'test-built_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "dag_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w222_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/task-dag", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w222_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/task-dag", json={'dag_name': 'test-dag_name', 'period_id': 'test-period_id', 'nodes': [], 'edges': [], 'topological_order': [], 'is_valid_dag': True, 'total_nodes': 1, 'completed_nodes': 1, 'critical_path_length': 1, 'status': 'test-status', 'built_at': 'test-built_at'})
    assert r1.status_code == 201
    item_id = r1.json()["dag_id"]
    r2 = await client.get("/api/task-dag")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/task-dag/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["dag_id"] == item_id
