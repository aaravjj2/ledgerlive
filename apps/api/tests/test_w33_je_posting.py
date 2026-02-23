"""Tests for Wave 33: JE Posting Engine

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w33_je_posting import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w33_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w33_create(client):
    r = await client.post("/api/je-postings", json={'batch_id': 'test-batch_id', 'journal_entries': [], 'status': 'test-status', 'locked': True, 'approved_by': 'test-approved_by', 'reversal_of': 'test-reversal_of', 'total_debits': 1.0, 'total_credits': 1.0, 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "posting_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w33_list(client):
    await client.post("/api/je-postings", json={'batch_id': 'test-batch_id', 'journal_entries': [], 'status': 'test-status', 'locked': True, 'approved_by': 'test-approved_by', 'reversal_of': 'test-reversal_of', 'total_debits': 1.0, 'total_credits': 1.0, 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    await client.post("/api/je-postings", json={'batch_id': 'test-batch_id', 'journal_entries': [], 'status': 'test-status', 'locked': True, 'approved_by': 'test-approved_by', 'reversal_of': 'test-reversal_of', 'total_debits': 1.0, 'total_credits': 1.0, 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    r = await client.get("/api/je-postings")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w33_get_by_id(client):
    r = await client.post("/api/je-postings", json={'batch_id': 'test-batch_id', 'journal_entries': [], 'status': 'test-status', 'locked': True, 'approved_by': 'test-approved_by', 'reversal_of': 'test-reversal_of', 'total_debits': 1.0, 'total_credits': 1.0, 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    item_id = r.json()["posting_id"]
    r2 = await client.get(f"/api/je-postings/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["posting_id"] == item_id

@pytest.mark.asyncio
async def test_w33_get_not_found(client):
    r = await client.get("/api/je-postings/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w33_approve(client):
    r = await client.post("/api/je-postings", json={'batch_id': 'test-batch_id', 'journal_entries': [], 'status': 'test-status', 'locked': True, 'approved_by': 'test-approved_by', 'reversal_of': 'test-reversal_of', 'total_debits': 1.0, 'total_credits': 1.0, 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    item_id = r.json()["posting_id"]
    r2 = await client.post(f"/api/je-postings/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["posting_id"] == item_id

@pytest.mark.asyncio
async def test_w33_post(client):
    r = await client.post("/api/je-postings", json={'batch_id': 'test-batch_id', 'journal_entries': [], 'status': 'test-status', 'locked': True, 'approved_by': 'test-approved_by', 'reversal_of': 'test-reversal_of', 'total_debits': 1.0, 'total_credits': 1.0, 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    item_id = r.json()["posting_id"]
    r2 = await client.post(f"/api/je-postings/{item_id}/post", json={})
    assert r2.status_code == 200
    assert r2.json()["posting_id"] == item_id

@pytest.mark.asyncio
async def test_w33_reverse(client):
    r = await client.post("/api/je-postings", json={'batch_id': 'test-batch_id', 'journal_entries': [], 'status': 'test-status', 'locked': True, 'approved_by': 'test-approved_by', 'reversal_of': 'test-reversal_of', 'total_debits': 1.0, 'total_credits': 1.0, 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    item_id = r.json()["posting_id"]
    r2 = await client.post(f"/api/je-postings/{item_id}/reverse", json={})
    assert r2.status_code == 200
    assert r2.json()["posting_id"] == item_id

@pytest.mark.asyncio
async def test_w33_approve_not_found(client):
    r = await client.post("/api/je-postings/nonexistent-id/approve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w33_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/je-postings", json={'batch_id': 'test-batch_id', 'journal_entries': [], 'status': 'test-status', 'locked': True, 'approved_by': 'test-approved_by', 'reversal_of': 'test-reversal_of', 'total_debits': 1.0, 'total_credits': 1.0, 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "je_posting"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w33_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/je-postings", json={'batch_id': 'test-batch_id', 'journal_entries': [], 'status': 'test-status', 'locked': True, 'approved_by': 'test-approved_by', 'reversal_of': 'test-reversal_of', 'total_debits': 1.0, 'total_credits': 1.0, 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/je-postings", json={'batch_id': 'test-batch_id', 'journal_entries': [], 'status': 'test-status', 'locked': True, 'approved_by': 'test-approved_by', 'reversal_of': 'test-reversal_of', 'total_debits': 1.0, 'total_credits': 1.0, 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "posting_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w33_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/je-postings", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w33_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/je-postings", json={'batch_id': 'test-batch_id', 'journal_entries': [], 'status': 'test-status', 'locked': True, 'approved_by': 'test-approved_by', 'reversal_of': 'test-reversal_of', 'total_debits': 1.0, 'total_credits': 1.0, 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["posting_id"]
    r2 = await client.get("/api/je-postings")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/je-postings/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["posting_id"] == item_id
