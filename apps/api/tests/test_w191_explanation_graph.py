"""Tests for Wave 191: Explanation Graph v3

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w191_explanation_graph import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w191_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w191_create(client):
    r = await client.post("/api/explanation-graphs", json={'root_exception_id': 'test-root_exception_id', 'nodes': [], 'edges': [], 'citation_count': 1, 'uncited_nodes': [], 'dag_hash': 'test-dag_hash', 'serialization_stable': True, 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "graph_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w191_list(client):
    await client.post("/api/explanation-graphs", json={'root_exception_id': 'test-root_exception_id', 'nodes': [], 'edges': [], 'citation_count': 1, 'uncited_nodes': [], 'dag_hash': 'test-dag_hash', 'serialization_stable': True, 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/explanation-graphs", json={'root_exception_id': 'test-root_exception_id', 'nodes': [], 'edges': [], 'citation_count': 1, 'uncited_nodes': [], 'dag_hash': 'test-dag_hash', 'serialization_stable': True, 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/explanation-graphs")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w191_get_by_id(client):
    r = await client.post("/api/explanation-graphs", json={'root_exception_id': 'test-root_exception_id', 'nodes': [], 'edges': [], 'citation_count': 1, 'uncited_nodes': [], 'dag_hash': 'test-dag_hash', 'serialization_stable': True, 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["graph_id"]
    r2 = await client.get(f"/api/explanation-graphs/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["graph_id"] == item_id

@pytest.mark.asyncio
async def test_w191_get_not_found(client):
    r = await client.get("/api/explanation-graphs/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w191_add_node(client):
    r = await client.post("/api/explanation-graphs", json={'root_exception_id': 'test-root_exception_id', 'nodes': [], 'edges': [], 'citation_count': 1, 'uncited_nodes': [], 'dag_hash': 'test-dag_hash', 'serialization_stable': True, 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["graph_id"]
    r2 = await client.post(f"/api/explanation-graphs/{item_id}/node", json={})
    assert r2.status_code == 200
    assert r2.json()["graph_id"] == item_id

@pytest.mark.asyncio
async def test_w191_validate_citations(client):
    r = await client.post("/api/explanation-graphs", json={'root_exception_id': 'test-root_exception_id', 'nodes': [], 'edges': [], 'citation_count': 1, 'uncited_nodes': [], 'dag_hash': 'test-dag_hash', 'serialization_stable': True, 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["graph_id"]
    r2 = await client.post(f"/api/explanation-graphs/{item_id}/validate", json={})
    assert r2.status_code == 200
    assert r2.json()["graph_id"] == item_id

@pytest.mark.asyncio
async def test_w191_serialize_dag(client):
    r = await client.post("/api/explanation-graphs", json={'root_exception_id': 'test-root_exception_id', 'nodes': [], 'edges': [], 'citation_count': 1, 'uncited_nodes': [], 'dag_hash': 'test-dag_hash', 'serialization_stable': True, 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["graph_id"]
    r2 = await client.post(f"/api/explanation-graphs/{item_id}/serialize", json={})
    assert r2.status_code == 200
    assert r2.json()["graph_id"] == item_id

@pytest.mark.asyncio
async def test_w191_add_node_not_found(client):
    r = await client.post("/api/explanation-graphs/nonexistent-id/node", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w191_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/explanation-graphs", json={'root_exception_id': 'test-root_exception_id', 'nodes': [], 'edges': [], 'citation_count': 1, 'uncited_nodes': [], 'dag_hash': 'test-dag_hash', 'serialization_stable': True, 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "explanation_graph"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w191_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/explanation-graphs", json={'root_exception_id': 'test-root_exception_id', 'nodes': [], 'edges': [], 'citation_count': 1, 'uncited_nodes': [], 'dag_hash': 'test-dag_hash', 'serialization_stable': True, 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/explanation-graphs", json={'root_exception_id': 'test-root_exception_id', 'nodes': [], 'edges': [], 'citation_count': 1, 'uncited_nodes': [], 'dag_hash': 'test-dag_hash', 'serialization_stable': True, 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "graph_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w191_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/explanation-graphs", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w191_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/explanation-graphs", json={'root_exception_id': 'test-root_exception_id', 'nodes': [], 'edges': [], 'citation_count': 1, 'uncited_nodes': [], 'dag_hash': 'test-dag_hash', 'serialization_stable': True, 'validation_result': 'test-validation_result', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["graph_id"]
    r2 = await client.get("/api/explanation-graphs")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/explanation-graphs/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["graph_id"] == item_id
