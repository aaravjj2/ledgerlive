"""Tests for Wave 83: Consolidated Cash Flow

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w083_cashflow_consol import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w083_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w083_create(client):
    r = await client.post("/api/cashflow-consol", json={'period_id': 'test-period_id', 'entity_ids': [], 'operating': 1.0, 'investing': 1.0, 'financing': 1.0, 'net_change': 1.0, 'tie_out_status': 'test-tie_out_status', 'source_refs': [], 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "cf_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w083_list(client):
    await client.post("/api/cashflow-consol", json={'period_id': 'test-period_id', 'entity_ids': [], 'operating': 1.0, 'investing': 1.0, 'financing': 1.0, 'net_change': 1.0, 'tie_out_status': 'test-tie_out_status', 'source_refs': [], 'created_at': 'test-created_at'})
    await client.post("/api/cashflow-consol", json={'period_id': 'test-period_id', 'entity_ids': [], 'operating': 1.0, 'investing': 1.0, 'financing': 1.0, 'net_change': 1.0, 'tie_out_status': 'test-tie_out_status', 'source_refs': [], 'created_at': 'test-created_at'})
    r = await client.get("/api/cashflow-consol")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w083_get_by_id(client):
    r = await client.post("/api/cashflow-consol", json={'period_id': 'test-period_id', 'entity_ids': [], 'operating': 1.0, 'investing': 1.0, 'financing': 1.0, 'net_change': 1.0, 'tie_out_status': 'test-tie_out_status', 'source_refs': [], 'created_at': 'test-created_at'})
    item_id = r.json()["cf_id"]
    r2 = await client.get(f"/api/cashflow-consol/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["cf_id"] == item_id

@pytest.mark.asyncio
async def test_w083_get_not_found(client):
    r = await client.get("/api/cashflow-consol/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w083_tie_out(client):
    r = await client.post("/api/cashflow-consol", json={'period_id': 'test-period_id', 'entity_ids': [], 'operating': 1.0, 'investing': 1.0, 'financing': 1.0, 'net_change': 1.0, 'tie_out_status': 'test-tie_out_status', 'source_refs': [], 'created_at': 'test-created_at'})
    item_id = r.json()["cf_id"]
    r2 = await client.post(f"/api/cashflow-consol/{item_id}/tie-out", json={})
    assert r2.status_code == 200
    assert r2.json()["cf_id"] == item_id

@pytest.mark.asyncio
async def test_w083_drill_down(client):
    r = await client.post("/api/cashflow-consol", json={'period_id': 'test-period_id', 'entity_ids': [], 'operating': 1.0, 'investing': 1.0, 'financing': 1.0, 'net_change': 1.0, 'tie_out_status': 'test-tie_out_status', 'source_refs': [], 'created_at': 'test-created_at'})
    item_id = r.json()["cf_id"]
    r2 = await client.post(f"/api/cashflow-consol/{item_id}/drilldown", json={})
    assert r2.status_code == 200
    assert r2.json()["cf_id"] == item_id

@pytest.mark.asyncio
async def test_w083_tie_out_not_found(client):
    r = await client.post("/api/cashflow-consol/nonexistent-id/tie-out", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w083_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/cashflow-consol", json={'period_id': 'test-period_id', 'entity_ids': [], 'operating': 1.0, 'investing': 1.0, 'financing': 1.0, 'net_change': 1.0, 'tie_out_status': 'test-tie_out_status', 'source_refs': [], 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "cashflow_consol"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w083_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/cashflow-consol", json={'period_id': 'test-period_id', 'entity_ids': [], 'operating': 1.0, 'investing': 1.0, 'financing': 1.0, 'net_change': 1.0, 'tie_out_status': 'test-tie_out_status', 'source_refs': [], 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/cashflow-consol", json={'period_id': 'test-period_id', 'entity_ids': [], 'operating': 1.0, 'investing': 1.0, 'financing': 1.0, 'net_change': 1.0, 'tie_out_status': 'test-tie_out_status', 'source_refs': [], 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "cf_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w083_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/cashflow-consol", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w083_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/cashflow-consol", json={'period_id': 'test-period_id', 'entity_ids': [], 'operating': 1.0, 'investing': 1.0, 'financing': 1.0, 'net_change': 1.0, 'tie_out_status': 'test-tie_out_status', 'source_refs': [], 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["cf_id"]
    r2 = await client.get("/api/cashflow-consol")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/cashflow-consol/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["cf_id"] == item_id
