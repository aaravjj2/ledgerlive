"""Tests for Wave 142: DB Partitioning & Indexes

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w142_db_partitioning import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w142_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w142_create(client):
    r = await client.post("/api/db-partitioning", json={'table_name': 'test-table_name', 'partition_key': 'test-partition_key', 'index_name': 'test-index_name', 'explain_plan': {}, 'plan_shape_match': True, 'query_time_ms': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "partition_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w142_list(client):
    await client.post("/api/db-partitioning", json={'table_name': 'test-table_name', 'partition_key': 'test-partition_key', 'index_name': 'test-index_name', 'explain_plan': {}, 'plan_shape_match': True, 'query_time_ms': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    await client.post("/api/db-partitioning", json={'table_name': 'test-table_name', 'partition_key': 'test-partition_key', 'index_name': 'test-index_name', 'explain_plan': {}, 'plan_shape_match': True, 'query_time_ms': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    r = await client.get("/api/db-partitioning")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w142_get_by_id(client):
    r = await client.post("/api/db-partitioning", json={'table_name': 'test-table_name', 'partition_key': 'test-partition_key', 'index_name': 'test-index_name', 'explain_plan': {}, 'plan_shape_match': True, 'query_time_ms': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    item_id = r.json()["partition_id"]
    r2 = await client.get(f"/api/db-partitioning/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["partition_id"] == item_id

@pytest.mark.asyncio
async def test_w142_get_not_found(client):
    r = await client.get("/api/db-partitioning/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w142_analyze_plan(client):
    r = await client.post("/api/db-partitioning", json={'table_name': 'test-table_name', 'partition_key': 'test-partition_key', 'index_name': 'test-index_name', 'explain_plan': {}, 'plan_shape_match': True, 'query_time_ms': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    item_id = r.json()["partition_id"]
    r2 = await client.post(f"/api/db-partitioning/{item_id}/analyze", json={})
    assert r2.status_code == 200
    assert r2.json()["partition_id"] == item_id

@pytest.mark.asyncio
async def test_w142_verify_shape(client):
    r = await client.post("/api/db-partitioning", json={'table_name': 'test-table_name', 'partition_key': 'test-partition_key', 'index_name': 'test-index_name', 'explain_plan': {}, 'plan_shape_match': True, 'query_time_ms': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    item_id = r.json()["partition_id"]
    r2 = await client.post(f"/api/db-partitioning/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["partition_id"] == item_id

@pytest.mark.asyncio
async def test_w142_analyze_plan_not_found(client):
    r = await client.post("/api/db-partitioning/nonexistent-id/analyze", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w142_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/db-partitioning", json={'table_name': 'test-table_name', 'partition_key': 'test-partition_key', 'index_name': 'test-index_name', 'explain_plan': {}, 'plan_shape_match': True, 'query_time_ms': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "db_partitioning"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w142_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/db-partitioning", json={'table_name': 'test-table_name', 'partition_key': 'test-partition_key', 'index_name': 'test-index_name', 'explain_plan': {}, 'plan_shape_match': True, 'query_time_ms': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/db-partitioning", json={'table_name': 'test-table_name', 'partition_key': 'test-partition_key', 'index_name': 'test-index_name', 'explain_plan': {}, 'plan_shape_match': True, 'query_time_ms': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "partition_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w142_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/db-partitioning", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w142_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/db-partitioning", json={'table_name': 'test-table_name', 'partition_key': 'test-partition_key', 'index_name': 'test-index_name', 'explain_plan': {}, 'plan_shape_match': True, 'query_time_ms': 1.0, 'status': 'test-status', 'analyzed_at': 'test-analyzed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["partition_id"]
    r2 = await client.get("/api/db-partitioning")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/db-partitioning/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["partition_id"] == item_id
