"""Tests for Wave 8: HITL Review Queue

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w08_review_queue import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w08_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w08_create(client):
    r = await client.post("/api/reviews", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'reviewer': 'test-reviewer', 'status': 'test-status', 'decision': 'test-decision', 'notes': 'test-notes', 'queued_at': 'test-queued_at', 'decided_at': 'test-decided_at'})
    assert r.status_code == 201
    data = r.json()
    assert "review_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w08_list(client):
    await client.post("/api/reviews", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'reviewer': 'test-reviewer', 'status': 'test-status', 'decision': 'test-decision', 'notes': 'test-notes', 'queued_at': 'test-queued_at', 'decided_at': 'test-decided_at'})
    await client.post("/api/reviews", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'reviewer': 'test-reviewer', 'status': 'test-status', 'decision': 'test-decision', 'notes': 'test-notes', 'queued_at': 'test-queued_at', 'decided_at': 'test-decided_at'})
    r = await client.get("/api/reviews")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w08_get_by_id(client):
    r = await client.post("/api/reviews", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'reviewer': 'test-reviewer', 'status': 'test-status', 'decision': 'test-decision', 'notes': 'test-notes', 'queued_at': 'test-queued_at', 'decided_at': 'test-decided_at'})
    item_id = r.json()["review_id"]
    r2 = await client.get(f"/api/reviews/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["review_id"] == item_id

@pytest.mark.asyncio
async def test_w08_get_not_found(client):
    r = await client.get("/api/reviews/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w08_decide(client):
    r = await client.post("/api/reviews", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'reviewer': 'test-reviewer', 'status': 'test-status', 'decision': 'test-decision', 'notes': 'test-notes', 'queued_at': 'test-queued_at', 'decided_at': 'test-decided_at'})
    item_id = r.json()["review_id"]
    r2 = await client.post(f"/api/reviews/{item_id}/decide", json={})
    assert r2.status_code == 200
    assert r2.json()["review_id"] == item_id

@pytest.mark.asyncio
async def test_w08_decide_not_found(client):
    r = await client.post("/api/reviews/nonexistent-id/decide", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w08_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/reviews", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'reviewer': 'test-reviewer', 'status': 'test-status', 'decision': 'test-decision', 'notes': 'test-notes', 'queued_at': 'test-queued_at', 'decided_at': 'test-decided_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "review_queue"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w08_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/reviews", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'reviewer': 'test-reviewer', 'status': 'test-status', 'decision': 'test-decision', 'notes': 'test-notes', 'queued_at': 'test-queued_at', 'decided_at': 'test-decided_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/reviews", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'reviewer': 'test-reviewer', 'status': 'test-status', 'decision': 'test-decision', 'notes': 'test-notes', 'queued_at': 'test-queued_at', 'decided_at': 'test-decided_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "review_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w08_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/reviews", json={})
    assert r.status_code == 201
