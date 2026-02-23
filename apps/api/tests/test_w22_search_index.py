"""Tests for Wave 22: Search Index

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w22_search_index import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w22_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w22_create(client):
    r = await client.post("/api/search/reindex", json={'query': 'test-query', 'doc_type': 'test-doc_type', 'title': 'test-title', 'snippet': 'test-snippet', 'score': 1.0, 'matched_at': 'test-matched_at'})
    assert r.status_code == 201
    data = r.json()
    assert "result_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w22_list(client):
    await client.post("/api/search/reindex", json={'query': 'test-query', 'doc_type': 'test-doc_type', 'title': 'test-title', 'snippet': 'test-snippet', 'score': 1.0, 'matched_at': 'test-matched_at'})
    await client.post("/api/search/reindex", json={'query': 'test-query', 'doc_type': 'test-doc_type', 'title': 'test-title', 'snippet': 'test-snippet', 'score': 1.0, 'matched_at': 'test-matched_at'})
    r = await client.get("/api/search")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w22_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/search/reindex", json={'query': 'test-query', 'doc_type': 'test-doc_type', 'title': 'test-title', 'snippet': 'test-snippet', 'score': 1.0, 'matched_at': 'test-matched_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "search_index"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w22_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/search/reindex", json={'query': 'test-query', 'doc_type': 'test-doc_type', 'title': 'test-title', 'snippet': 'test-snippet', 'score': 1.0, 'matched_at': 'test-matched_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/search/reindex", json={'query': 'test-query', 'doc_type': 'test-doc_type', 'title': 'test-title', 'snippet': 'test-snippet', 'score': 1.0, 'matched_at': 'test-matched_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "result_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w22_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/search/reindex", json={})
    assert r.status_code == 201
