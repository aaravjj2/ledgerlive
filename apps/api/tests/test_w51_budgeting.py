"""Tests for Wave 51: Budgeting 1.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w51_budgeting import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w51_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w51_create(client):
    r = await client.post("/api/budgets", json={'name': 'test-name', 'version': 1, 'period_id': 'test-period_id', 'status': 'test-status', 'total_amount': 1.0, 'approved_by': 'test-approved_by', 'locked': True, 'variance_threshold_pct': 1.0, 'created_at': 'test-created_at', 'published_at': 'test-published_at'})
    assert r.status_code == 201
    data = r.json()
    assert "budget_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w51_list(client):
    await client.post("/api/budgets", json={'name': 'test-name', 'version': 1, 'period_id': 'test-period_id', 'status': 'test-status', 'total_amount': 1.0, 'approved_by': 'test-approved_by', 'locked': True, 'variance_threshold_pct': 1.0, 'created_at': 'test-created_at', 'published_at': 'test-published_at'})
    await client.post("/api/budgets", json={'name': 'test-name', 'version': 1, 'period_id': 'test-period_id', 'status': 'test-status', 'total_amount': 1.0, 'approved_by': 'test-approved_by', 'locked': True, 'variance_threshold_pct': 1.0, 'created_at': 'test-created_at', 'published_at': 'test-published_at'})
    r = await client.get("/api/budgets")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w51_get_by_id(client):
    r = await client.post("/api/budgets", json={'name': 'test-name', 'version': 1, 'period_id': 'test-period_id', 'status': 'test-status', 'total_amount': 1.0, 'approved_by': 'test-approved_by', 'locked': True, 'variance_threshold_pct': 1.0, 'created_at': 'test-created_at', 'published_at': 'test-published_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.get(f"/api/budgets/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w51_get_not_found(client):
    r = await client.get("/api/budgets/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w51_submit_budget(client):
    r = await client.post("/api/budgets", json={'name': 'test-name', 'version': 1, 'period_id': 'test-period_id', 'status': 'test-status', 'total_amount': 1.0, 'approved_by': 'test-approved_by', 'locked': True, 'variance_threshold_pct': 1.0, 'created_at': 'test-created_at', 'published_at': 'test-published_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.post(f"/api/budgets/{item_id}/submit", json={})
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w51_approve_budget(client):
    r = await client.post("/api/budgets", json={'name': 'test-name', 'version': 1, 'period_id': 'test-period_id', 'status': 'test-status', 'total_amount': 1.0, 'approved_by': 'test-approved_by', 'locked': True, 'variance_threshold_pct': 1.0, 'created_at': 'test-created_at', 'published_at': 'test-published_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.post(f"/api/budgets/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w51_lock_budget(client):
    r = await client.post("/api/budgets", json={'name': 'test-name', 'version': 1, 'period_id': 'test-period_id', 'status': 'test-status', 'total_amount': 1.0, 'approved_by': 'test-approved_by', 'locked': True, 'variance_threshold_pct': 1.0, 'created_at': 'test-created_at', 'published_at': 'test-published_at'})
    item_id = r.json()["budget_id"]
    r2 = await client.post(f"/api/budgets/{item_id}/lock", json={})
    assert r2.status_code == 200
    assert r2.json()["budget_id"] == item_id

@pytest.mark.asyncio
async def test_w51_submit_budget_not_found(client):
    r = await client.post("/api/budgets/nonexistent-id/submit", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w51_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/budgets", json={'name': 'test-name', 'version': 1, 'period_id': 'test-period_id', 'status': 'test-status', 'total_amount': 1.0, 'approved_by': 'test-approved_by', 'locked': True, 'variance_threshold_pct': 1.0, 'created_at': 'test-created_at', 'published_at': 'test-published_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "budgeting"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w51_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/budgets", json={'name': 'test-name', 'version': 1, 'period_id': 'test-period_id', 'status': 'test-status', 'total_amount': 1.0, 'approved_by': 'test-approved_by', 'locked': True, 'variance_threshold_pct': 1.0, 'created_at': 'test-created_at', 'published_at': 'test-published_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/budgets", json={'name': 'test-name', 'version': 1, 'period_id': 'test-period_id', 'status': 'test-status', 'total_amount': 1.0, 'approved_by': 'test-approved_by', 'locked': True, 'variance_threshold_pct': 1.0, 'created_at': 'test-created_at', 'published_at': 'test-published_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "budget_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w51_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/budgets", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w51_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/budgets", json={'name': 'test-name', 'version': 1, 'period_id': 'test-period_id', 'status': 'test-status', 'total_amount': 1.0, 'approved_by': 'test-approved_by', 'locked': True, 'variance_threshold_pct': 1.0, 'created_at': 'test-created_at', 'published_at': 'test-published_at'})
    assert r1.status_code == 201
    item_id = r1.json()["budget_id"]
    r2 = await client.get("/api/budgets")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/budgets/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["budget_id"] == item_id
