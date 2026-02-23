"""Tests for Wave 55: Treasury 2.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w55_treasury import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w55_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w55_create(client):
    r = await client.post("/api/treasury/instruments", json={'name': 'test-name', 'instrument_type': 'test-instrument_type', 'principal': 1.0, 'rate_pct': 1.0, 'maturity_date': 'test-maturity_date', 'interest_accrued': 1.0, 'status': 'test-status', 'liquidity_bucket': 'test-liquidity_bucket', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "instrument_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w55_list(client):
    await client.post("/api/treasury/instruments", json={'name': 'test-name', 'instrument_type': 'test-instrument_type', 'principal': 1.0, 'rate_pct': 1.0, 'maturity_date': 'test-maturity_date', 'interest_accrued': 1.0, 'status': 'test-status', 'liquidity_bucket': 'test-liquidity_bucket', 'created_at': 'test-created_at'})
    await client.post("/api/treasury/instruments", json={'name': 'test-name', 'instrument_type': 'test-instrument_type', 'principal': 1.0, 'rate_pct': 1.0, 'maturity_date': 'test-maturity_date', 'interest_accrued': 1.0, 'status': 'test-status', 'liquidity_bucket': 'test-liquidity_bucket', 'created_at': 'test-created_at'})
    r = await client.get("/api/treasury/instruments")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w55_get_by_id(client):
    r = await client.post("/api/treasury/instruments", json={'name': 'test-name', 'instrument_type': 'test-instrument_type', 'principal': 1.0, 'rate_pct': 1.0, 'maturity_date': 'test-maturity_date', 'interest_accrued': 1.0, 'status': 'test-status', 'liquidity_bucket': 'test-liquidity_bucket', 'created_at': 'test-created_at'})
    item_id = r.json()["instrument_id"]
    r2 = await client.get(f"/api/treasury/instruments/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["instrument_id"] == item_id

@pytest.mark.asyncio
async def test_w55_get_not_found(client):
    r = await client.get("/api/treasury/instruments/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w55_project_interest(client):
    r = await client.post("/api/treasury/instruments", json={'name': 'test-name', 'instrument_type': 'test-instrument_type', 'principal': 1.0, 'rate_pct': 1.0, 'maturity_date': 'test-maturity_date', 'interest_accrued': 1.0, 'status': 'test-status', 'liquidity_bucket': 'test-liquidity_bucket', 'created_at': 'test-created_at'})
    item_id = r.json()["instrument_id"]
    r2 = await client.post(f"/api/treasury/instruments/{item_id}/project", json={})
    assert r2.status_code == 200
    assert r2.json()["instrument_id"] == item_id

@pytest.mark.asyncio
async def test_w55_project_interest_not_found(client):
    r = await client.post("/api/treasury/instruments/nonexistent-id/project", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w55_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/treasury/instruments", json={'name': 'test-name', 'instrument_type': 'test-instrument_type', 'principal': 1.0, 'rate_pct': 1.0, 'maturity_date': 'test-maturity_date', 'interest_accrued': 1.0, 'status': 'test-status', 'liquidity_bucket': 'test-liquidity_bucket', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "treasury"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w55_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/treasury/instruments", json={'name': 'test-name', 'instrument_type': 'test-instrument_type', 'principal': 1.0, 'rate_pct': 1.0, 'maturity_date': 'test-maturity_date', 'interest_accrued': 1.0, 'status': 'test-status', 'liquidity_bucket': 'test-liquidity_bucket', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/treasury/instruments", json={'name': 'test-name', 'instrument_type': 'test-instrument_type', 'principal': 1.0, 'rate_pct': 1.0, 'maturity_date': 'test-maturity_date', 'interest_accrued': 1.0, 'status': 'test-status', 'liquidity_bucket': 'test-liquidity_bucket', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "instrument_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w55_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/treasury/instruments", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w55_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/treasury/instruments", json={'name': 'test-name', 'instrument_type': 'test-instrument_type', 'principal': 1.0, 'rate_pct': 1.0, 'maturity_date': 'test-maturity_date', 'interest_accrued': 1.0, 'status': 'test-status', 'liquidity_bucket': 'test-liquidity_bucket', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["instrument_id"]
    r2 = await client.get("/api/treasury/instruments")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/treasury/instruments/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["instrument_id"] == item_id
