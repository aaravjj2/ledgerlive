"""Tests for Wave 223: Dependency Resolver v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w223_dependency_resolver import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w223_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w223_create(client):
    r = await client.post("/api/dependency-resolver", json={'dag_id': 'test-dag_id', 'resolved_order': [], 'parallel_batches': [], 'unresolved_deps': [], 'circular_refs': [], 'ready_tasks': [], 'blocked_tasks': [], 'resolution_depth': 1, 'fully_resolved': True, 'status': 'test-status', 'resolved_at': 'test-resolved_at'})
    assert r.status_code == 201
    data = r.json()
    assert "resolver_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w223_list(client):
    await client.post("/api/dependency-resolver", json={'dag_id': 'test-dag_id', 'resolved_order': [], 'parallel_batches': [], 'unresolved_deps': [], 'circular_refs': [], 'ready_tasks': [], 'blocked_tasks': [], 'resolution_depth': 1, 'fully_resolved': True, 'status': 'test-status', 'resolved_at': 'test-resolved_at'})
    await client.post("/api/dependency-resolver", json={'dag_id': 'test-dag_id', 'resolved_order': [], 'parallel_batches': [], 'unresolved_deps': [], 'circular_refs': [], 'ready_tasks': [], 'blocked_tasks': [], 'resolution_depth': 1, 'fully_resolved': True, 'status': 'test-status', 'resolved_at': 'test-resolved_at'})
    r = await client.get("/api/dependency-resolver")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w223_get_by_id(client):
    r = await client.post("/api/dependency-resolver", json={'dag_id': 'test-dag_id', 'resolved_order': [], 'parallel_batches': [], 'unresolved_deps': [], 'circular_refs': [], 'ready_tasks': [], 'blocked_tasks': [], 'resolution_depth': 1, 'fully_resolved': True, 'status': 'test-status', 'resolved_at': 'test-resolved_at'})
    item_id = r.json()["resolver_id"]
    r2 = await client.get(f"/api/dependency-resolver/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["resolver_id"] == item_id

@pytest.mark.asyncio
async def test_w223_get_not_found(client):
    r = await client.get("/api/dependency-resolver/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w223_check_ready(client):
    r = await client.post("/api/dependency-resolver", json={'dag_id': 'test-dag_id', 'resolved_order': [], 'parallel_batches': [], 'unresolved_deps': [], 'circular_refs': [], 'ready_tasks': [], 'blocked_tasks': [], 'resolution_depth': 1, 'fully_resolved': True, 'status': 'test-status', 'resolved_at': 'test-resolved_at'})
    item_id = r.json()["resolver_id"]
    r2 = await client.post(f"/api/dependency-resolver/{item_id}/ready", json={})
    assert r2.status_code == 200
    assert r2.json()["resolver_id"] == item_id

@pytest.mark.asyncio
async def test_w223_detect_circular(client):
    r = await client.post("/api/dependency-resolver", json={'dag_id': 'test-dag_id', 'resolved_order': [], 'parallel_batches': [], 'unresolved_deps': [], 'circular_refs': [], 'ready_tasks': [], 'blocked_tasks': [], 'resolution_depth': 1, 'fully_resolved': True, 'status': 'test-status', 'resolved_at': 'test-resolved_at'})
    item_id = r.json()["resolver_id"]
    r2 = await client.post(f"/api/dependency-resolver/{item_id}/circular", json={})
    assert r2.status_code == 200
    assert r2.json()["resolver_id"] == item_id

@pytest.mark.asyncio
async def test_w223_check_ready_not_found(client):
    r = await client.post("/api/dependency-resolver/nonexistent-id/ready", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w223_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/dependency-resolver", json={'dag_id': 'test-dag_id', 'resolved_order': [], 'parallel_batches': [], 'unresolved_deps': [], 'circular_refs': [], 'ready_tasks': [], 'blocked_tasks': [], 'resolution_depth': 1, 'fully_resolved': True, 'status': 'test-status', 'resolved_at': 'test-resolved_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "dependency_resolver"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w223_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/dependency-resolver", json={'dag_id': 'test-dag_id', 'resolved_order': [], 'parallel_batches': [], 'unresolved_deps': [], 'circular_refs': [], 'ready_tasks': [], 'blocked_tasks': [], 'resolution_depth': 1, 'fully_resolved': True, 'status': 'test-status', 'resolved_at': 'test-resolved_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/dependency-resolver", json={'dag_id': 'test-dag_id', 'resolved_order': [], 'parallel_batches': [], 'unresolved_deps': [], 'circular_refs': [], 'ready_tasks': [], 'blocked_tasks': [], 'resolution_depth': 1, 'fully_resolved': True, 'status': 'test-status', 'resolved_at': 'test-resolved_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "resolver_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w223_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/dependency-resolver", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w223_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/dependency-resolver", json={'dag_id': 'test-dag_id', 'resolved_order': [], 'parallel_batches': [], 'unresolved_deps': [], 'circular_refs': [], 'ready_tasks': [], 'blocked_tasks': [], 'resolution_depth': 1, 'fully_resolved': True, 'status': 'test-status', 'resolved_at': 'test-resolved_at'})
    assert r1.status_code == 201
    item_id = r1.json()["resolver_id"]
    r2 = await client.get("/api/dependency-resolver")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/dependency-resolver/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["resolver_id"] == item_id
