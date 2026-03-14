"""Tests for Wave 113: Evidence Query Language 2.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w113_query_language import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w113_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w113_create(client):
    r = await client.post("/api/evidence-queries", json={'query_text': 'test-query_text', 'query_type': 'test-query_type', 'result_count': 1, 'execution_ms': 1.0, 'saved': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "query_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w113_list(client):
    await client.post("/api/evidence-queries", json={'query_text': 'test-query_text', 'query_type': 'test-query_type', 'result_count': 1, 'execution_ms': 1.0, 'saved': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    await client.post("/api/evidence-queries", json={'query_text': 'test-query_text', 'query_type': 'test-query_type', 'result_count': 1, 'execution_ms': 1.0, 'saved': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    r = await client.get("/api/evidence-queries")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w113_get_by_id(client):
    r = await client.post("/api/evidence-queries", json={'query_text': 'test-query_text', 'query_type': 'test-query_type', 'result_count': 1, 'execution_ms': 1.0, 'saved': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    item_id = r.json()["query_id"]
    r2 = await client.get(f"/api/evidence-queries/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["query_id"] == item_id

@pytest.mark.asyncio
async def test_w113_get_not_found(client):
    r = await client.get("/api/evidence-queries/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w113_save_query(client):
    r = await client.post("/api/evidence-queries", json={'query_text': 'test-query_text', 'query_type': 'test-query_type', 'result_count': 1, 'execution_ms': 1.0, 'saved': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    item_id = r.json()["query_id"]
    r2 = await client.post(f"/api/evidence-queries/{item_id}/save", json={})
    assert r2.status_code == 200
    assert r2.json()["query_id"] == item_id

@pytest.mark.asyncio
async def test_w113_save_query_not_found(client):
    r = await client.post("/api/evidence-queries/nonexistent-id/save", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w113_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/evidence-queries", json={'query_text': 'test-query_text', 'query_type': 'test-query_type', 'result_count': 1, 'execution_ms': 1.0, 'saved': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "query_language"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w113_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/evidence-queries", json={'query_text': 'test-query_text', 'query_type': 'test-query_type', 'result_count': 1, 'execution_ms': 1.0, 'saved': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/evidence-queries", json={'query_text': 'test-query_text', 'query_type': 'test-query_type', 'result_count': 1, 'execution_ms': 1.0, 'saved': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "query_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w113_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/evidence-queries", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w113_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/evidence-queries", json={'query_text': 'test-query_text', 'query_type': 'test-query_type', 'result_count': 1, 'execution_ms': 1.0, 'saved': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["query_id"]
    r2 = await client.get("/api/evidence-queries")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/evidence-queries/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["query_id"] == item_id
