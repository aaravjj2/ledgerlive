"""Tests for Wave 1: Close Period Management

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w01_close_period import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w01_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w01_create(client):
    r = await client.post("/api/close-periods", json={'name': 'test-name', 'status': 'test-status', 'fiscal_year': 1, 'fiscal_month': 1, 'opened_at': 'test-opened_at', 'closed_at': 'test-closed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "period_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w01_list(client):
    await client.post("/api/close-periods", json={'name': 'test-name', 'status': 'test-status', 'fiscal_year': 1, 'fiscal_month': 1, 'opened_at': 'test-opened_at', 'closed_at': 'test-closed_at'})
    await client.post("/api/close-periods", json={'name': 'test-name', 'status': 'test-status', 'fiscal_year': 1, 'fiscal_month': 1, 'opened_at': 'test-opened_at', 'closed_at': 'test-closed_at'})
    r = await client.get("/api/close-periods")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w01_get_by_id(client):
    r = await client.post("/api/close-periods", json={'name': 'test-name', 'status': 'test-status', 'fiscal_year': 1, 'fiscal_month': 1, 'opened_at': 'test-opened_at', 'closed_at': 'test-closed_at'})
    item_id = r.json()["period_id"]
    r2 = await client.get(f"/api/close-periods/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["period_id"] == item_id

@pytest.mark.asyncio
async def test_w01_get_not_found(client):
    r = await client.get("/api/close-periods/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w01_close_period(client):
    r = await client.post("/api/close-periods", json={'name': 'test-name', 'status': 'test-status', 'fiscal_year': 1, 'fiscal_month': 1, 'opened_at': 'test-opened_at', 'closed_at': 'test-closed_at'})
    item_id = r.json()["period_id"]
    r2 = await client.post(f"/api/close-periods/{item_id}/close", json={})
    assert r2.status_code == 200
    assert r2.json()["period_id"] == item_id

@pytest.mark.asyncio
async def test_w01_lock_period(client):
    r = await client.post("/api/close-periods", json={'name': 'test-name', 'status': 'test-status', 'fiscal_year': 1, 'fiscal_month': 1, 'opened_at': 'test-opened_at', 'closed_at': 'test-closed_at'})
    item_id = r.json()["period_id"]
    r2 = await client.post(f"/api/close-periods/{item_id}/lock", json={})
    assert r2.status_code == 200
    assert r2.json()["period_id"] == item_id

@pytest.mark.asyncio
async def test_w01_close_period_not_found(client):
    r = await client.post("/api/close-periods/nonexistent-id/close", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w01_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/close-periods", json={'name': 'test-name', 'status': 'test-status', 'fiscal_year': 1, 'fiscal_month': 1, 'opened_at': 'test-opened_at', 'closed_at': 'test-closed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "close_period"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w01_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/close-periods", json={'name': 'test-name', 'status': 'test-status', 'fiscal_year': 1, 'fiscal_month': 1, 'opened_at': 'test-opened_at', 'closed_at': 'test-closed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/close-periods", json={'name': 'test-name', 'status': 'test-status', 'fiscal_year': 1, 'fiscal_month': 1, 'opened_at': 'test-opened_at', 'closed_at': 'test-closed_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "period_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w01_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/close-periods", json={})
    assert r.status_code == 201
