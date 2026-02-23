"""Tests for Wave 175: Evidence Graph Search v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w175_evidence_search import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w175_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w175_create(client):
    r = await client.post("/api/evidence-search", json={'query_text': 'test-query_text', 'index_scope': 'test-index_scope', 'result_count': 1, 'results': [], 'order_hash': 'test-order_hash', 'saved': True, 'deterministic': True, 'status': 'test-status', 'searched_at': 'test-searched_at'})
    assert r.status_code == 201
    data = r.json()
    assert "search_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w175_list(client):
    await client.post("/api/evidence-search", json={'query_text': 'test-query_text', 'index_scope': 'test-index_scope', 'result_count': 1, 'results': [], 'order_hash': 'test-order_hash', 'saved': True, 'deterministic': True, 'status': 'test-status', 'searched_at': 'test-searched_at'})
    await client.post("/api/evidence-search", json={'query_text': 'test-query_text', 'index_scope': 'test-index_scope', 'result_count': 1, 'results': [], 'order_hash': 'test-order_hash', 'saved': True, 'deterministic': True, 'status': 'test-status', 'searched_at': 'test-searched_at'})
    r = await client.get("/api/evidence-search")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w175_get_by_id(client):
    r = await client.post("/api/evidence-search", json={'query_text': 'test-query_text', 'index_scope': 'test-index_scope', 'result_count': 1, 'results': [], 'order_hash': 'test-order_hash', 'saved': True, 'deterministic': True, 'status': 'test-status', 'searched_at': 'test-searched_at'})
    item_id = r.json()["search_id"]
    r2 = await client.get(f"/api/evidence-search/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["search_id"] == item_id

@pytest.mark.asyncio
async def test_w175_get_not_found(client):
    r = await client.get("/api/evidence-search/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w175_save_search(client):
    r = await client.post("/api/evidence-search", json={'query_text': 'test-query_text', 'index_scope': 'test-index_scope', 'result_count': 1, 'results': [], 'order_hash': 'test-order_hash', 'saved': True, 'deterministic': True, 'status': 'test-status', 'searched_at': 'test-searched_at'})
    item_id = r.json()["search_id"]
    r2 = await client.post(f"/api/evidence-search/{item_id}/save", json={})
    assert r2.status_code == 200
    assert r2.json()["search_id"] == item_id

@pytest.mark.asyncio
async def test_w175_open_evidence(client):
    r = await client.post("/api/evidence-search", json={'query_text': 'test-query_text', 'index_scope': 'test-index_scope', 'result_count': 1, 'results': [], 'order_hash': 'test-order_hash', 'saved': True, 'deterministic': True, 'status': 'test-status', 'searched_at': 'test-searched_at'})
    item_id = r.json()["search_id"]
    r2 = await client.post(f"/api/evidence-search/{item_id}/open", json={})
    assert r2.status_code == 200
    assert r2.json()["search_id"] == item_id

@pytest.mark.asyncio
async def test_w175_save_search_not_found(client):
    r = await client.post("/api/evidence-search/nonexistent-id/save", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w175_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/evidence-search", json={'query_text': 'test-query_text', 'index_scope': 'test-index_scope', 'result_count': 1, 'results': [], 'order_hash': 'test-order_hash', 'saved': True, 'deterministic': True, 'status': 'test-status', 'searched_at': 'test-searched_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "evidence_search"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w175_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/evidence-search", json={'query_text': 'test-query_text', 'index_scope': 'test-index_scope', 'result_count': 1, 'results': [], 'order_hash': 'test-order_hash', 'saved': True, 'deterministic': True, 'status': 'test-status', 'searched_at': 'test-searched_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/evidence-search", json={'query_text': 'test-query_text', 'index_scope': 'test-index_scope', 'result_count': 1, 'results': [], 'order_hash': 'test-order_hash', 'saved': True, 'deterministic': True, 'status': 'test-status', 'searched_at': 'test-searched_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "search_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w175_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/evidence-search", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w175_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/evidence-search", json={'query_text': 'test-query_text', 'index_scope': 'test-index_scope', 'result_count': 1, 'results': [], 'order_hash': 'test-order_hash', 'saved': True, 'deterministic': True, 'status': 'test-status', 'searched_at': 'test-searched_at'})
    assert r1.status_code == 201
    item_id = r1.json()["search_id"]
    r2 = await client.get("/api/evidence-search")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/evidence-search/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["search_id"] == item_id
