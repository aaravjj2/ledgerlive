"""Tests for Wave 73: Accrual Suggestion Engine

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w073_accrual_suggest import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w073_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w073_create(client):
    r = await client.post("/api/accrual-suggestions", json={'pattern_id': 'test-pattern_id', 'accrual_type': 'test-accrual_type', 'amount': 1.0, 'account_id': 'test-account_id', 'period_id': 'test-period_id', 'confidence': 1.0, 'status': 'test-status', 'approved_by': 'test-approved_by', 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "suggestion_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w073_list(client):
    await client.post("/api/accrual-suggestions", json={'pattern_id': 'test-pattern_id', 'accrual_type': 'test-accrual_type', 'amount': 1.0, 'account_id': 'test-account_id', 'period_id': 'test-period_id', 'confidence': 1.0, 'status': 'test-status', 'approved_by': 'test-approved_by', 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    await client.post("/api/accrual-suggestions", json={'pattern_id': 'test-pattern_id', 'accrual_type': 'test-accrual_type', 'amount': 1.0, 'account_id': 'test-account_id', 'period_id': 'test-period_id', 'confidence': 1.0, 'status': 'test-status', 'approved_by': 'test-approved_by', 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    r = await client.get("/api/accrual-suggestions")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w073_get_by_id(client):
    r = await client.post("/api/accrual-suggestions", json={'pattern_id': 'test-pattern_id', 'accrual_type': 'test-accrual_type', 'amount': 1.0, 'account_id': 'test-account_id', 'period_id': 'test-period_id', 'confidence': 1.0, 'status': 'test-status', 'approved_by': 'test-approved_by', 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    item_id = r.json()["suggestion_id"]
    r2 = await client.get(f"/api/accrual-suggestions/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["suggestion_id"] == item_id

@pytest.mark.asyncio
async def test_w073_get_not_found(client):
    r = await client.get("/api/accrual-suggestions/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w073_approve(client):
    r = await client.post("/api/accrual-suggestions", json={'pattern_id': 'test-pattern_id', 'accrual_type': 'test-accrual_type', 'amount': 1.0, 'account_id': 'test-account_id', 'period_id': 'test-period_id', 'confidence': 1.0, 'status': 'test-status', 'approved_by': 'test-approved_by', 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    item_id = r.json()["suggestion_id"]
    r2 = await client.post(f"/api/accrual-suggestions/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["suggestion_id"] == item_id

@pytest.mark.asyncio
async def test_w073_post_accrual(client):
    r = await client.post("/api/accrual-suggestions", json={'pattern_id': 'test-pattern_id', 'accrual_type': 'test-accrual_type', 'amount': 1.0, 'account_id': 'test-account_id', 'period_id': 'test-period_id', 'confidence': 1.0, 'status': 'test-status', 'approved_by': 'test-approved_by', 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    item_id = r.json()["suggestion_id"]
    r2 = await client.post(f"/api/accrual-suggestions/{item_id}/post", json={})
    assert r2.status_code == 200
    assert r2.json()["suggestion_id"] == item_id

@pytest.mark.asyncio
async def test_w073_reject(client):
    r = await client.post("/api/accrual-suggestions", json={'pattern_id': 'test-pattern_id', 'accrual_type': 'test-accrual_type', 'amount': 1.0, 'account_id': 'test-account_id', 'period_id': 'test-period_id', 'confidence': 1.0, 'status': 'test-status', 'approved_by': 'test-approved_by', 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    item_id = r.json()["suggestion_id"]
    r2 = await client.post(f"/api/accrual-suggestions/{item_id}/reject", json={})
    assert r2.status_code == 200
    assert r2.json()["suggestion_id"] == item_id

@pytest.mark.asyncio
async def test_w073_approve_not_found(client):
    r = await client.post("/api/accrual-suggestions/nonexistent-id/approve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w073_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/accrual-suggestions", json={'pattern_id': 'test-pattern_id', 'accrual_type': 'test-accrual_type', 'amount': 1.0, 'account_id': 'test-account_id', 'period_id': 'test-period_id', 'confidence': 1.0, 'status': 'test-status', 'approved_by': 'test-approved_by', 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "accrual_suggest"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w073_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/accrual-suggestions", json={'pattern_id': 'test-pattern_id', 'accrual_type': 'test-accrual_type', 'amount': 1.0, 'account_id': 'test-account_id', 'period_id': 'test-period_id', 'confidence': 1.0, 'status': 'test-status', 'approved_by': 'test-approved_by', 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/accrual-suggestions", json={'pattern_id': 'test-pattern_id', 'accrual_type': 'test-accrual_type', 'amount': 1.0, 'account_id': 'test-account_id', 'period_id': 'test-period_id', 'confidence': 1.0, 'status': 'test-status', 'approved_by': 'test-approved_by', 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "suggestion_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w073_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/accrual-suggestions", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w073_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/accrual-suggestions", json={'pattern_id': 'test-pattern_id', 'accrual_type': 'test-accrual_type', 'amount': 1.0, 'account_id': 'test-account_id', 'period_id': 'test-period_id', 'confidence': 1.0, 'status': 'test-status', 'approved_by': 'test-approved_by', 'posted_at': 'test-posted_at', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["suggestion_id"]
    r2 = await client.get("/api/accrual-suggestions")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/accrual-suggestions/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["suggestion_id"] == item_id
