"""Tests for Wave 32: Multi-Entity Consolidation

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w32_consolidation import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w32_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w32_create(client):
    r = await client.post("/api/consolidations", json={'period_id': 'test-period_id', 'parent_entity_id': 'test-parent_entity_id', 'child_entities': [], 'adjustments': [], 'eliminations': [], 'status': 'test-status', 'total_assets': 1.0, 'total_liabilities': 1.0, 'net_income': 1.0, 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    assert r.status_code == 201
    data = r.json()
    assert "consolidation_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w32_list(client):
    await client.post("/api/consolidations", json={'period_id': 'test-period_id', 'parent_entity_id': 'test-parent_entity_id', 'child_entities': [], 'adjustments': [], 'eliminations': [], 'status': 'test-status', 'total_assets': 1.0, 'total_liabilities': 1.0, 'net_income': 1.0, 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    await client.post("/api/consolidations", json={'period_id': 'test-period_id', 'parent_entity_id': 'test-parent_entity_id', 'child_entities': [], 'adjustments': [], 'eliminations': [], 'status': 'test-status', 'total_assets': 1.0, 'total_liabilities': 1.0, 'net_income': 1.0, 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    r = await client.get("/api/consolidations")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w32_get_by_id(client):
    r = await client.post("/api/consolidations", json={'period_id': 'test-period_id', 'parent_entity_id': 'test-parent_entity_id', 'child_entities': [], 'adjustments': [], 'eliminations': [], 'status': 'test-status', 'total_assets': 1.0, 'total_liabilities': 1.0, 'net_income': 1.0, 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    item_id = r.json()["consolidation_id"]
    r2 = await client.get(f"/api/consolidations/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["consolidation_id"] == item_id

@pytest.mark.asyncio
async def test_w32_get_not_found(client):
    r = await client.get("/api/consolidations/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w32_add_adjustment(client):
    r = await client.post("/api/consolidations", json={'period_id': 'test-period_id', 'parent_entity_id': 'test-parent_entity_id', 'child_entities': [], 'adjustments': [], 'eliminations': [], 'status': 'test-status', 'total_assets': 1.0, 'total_liabilities': 1.0, 'net_income': 1.0, 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    item_id = r.json()["consolidation_id"]
    r2 = await client.post(f"/api/consolidations/{item_id}/adjustments", json={})
    assert r2.status_code == 200
    assert r2.json()["consolidation_id"] == item_id

@pytest.mark.asyncio
async def test_w32_add_elimination(client):
    r = await client.post("/api/consolidations", json={'period_id': 'test-period_id', 'parent_entity_id': 'test-parent_entity_id', 'child_entities': [], 'adjustments': [], 'eliminations': [], 'status': 'test-status', 'total_assets': 1.0, 'total_liabilities': 1.0, 'net_income': 1.0, 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    item_id = r.json()["consolidation_id"]
    r2 = await client.post(f"/api/consolidations/{item_id}/eliminations", json={})
    assert r2.status_code == 200
    assert r2.json()["consolidation_id"] == item_id

@pytest.mark.asyncio
async def test_w32_finalize(client):
    r = await client.post("/api/consolidations", json={'period_id': 'test-period_id', 'parent_entity_id': 'test-parent_entity_id', 'child_entities': [], 'adjustments': [], 'eliminations': [], 'status': 'test-status', 'total_assets': 1.0, 'total_liabilities': 1.0, 'net_income': 1.0, 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    item_id = r.json()["consolidation_id"]
    r2 = await client.post(f"/api/consolidations/{item_id}/finalize", json={})
    assert r2.status_code == 200
    assert r2.json()["consolidation_id"] == item_id

@pytest.mark.asyncio
async def test_w32_add_adjustment_not_found(client):
    r = await client.post("/api/consolidations/nonexistent-id/adjustments", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w32_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/consolidations", json={'period_id': 'test-period_id', 'parent_entity_id': 'test-parent_entity_id', 'child_entities': [], 'adjustments': [], 'eliminations': [], 'status': 'test-status', 'total_assets': 1.0, 'total_liabilities': 1.0, 'net_income': 1.0, 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "consolidation"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w32_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/consolidations", json={'period_id': 'test-period_id', 'parent_entity_id': 'test-parent_entity_id', 'child_entities': [], 'adjustments': [], 'eliminations': [], 'status': 'test-status', 'total_assets': 1.0, 'total_liabilities': 1.0, 'net_income': 1.0, 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/consolidations", json={'period_id': 'test-period_id', 'parent_entity_id': 'test-parent_entity_id', 'child_entities': [], 'adjustments': [], 'eliminations': [], 'status': 'test-status', 'total_assets': 1.0, 'total_liabilities': 1.0, 'net_income': 1.0, 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "consolidation_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w32_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/consolidations", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w32_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/consolidations", json={'period_id': 'test-period_id', 'parent_entity_id': 'test-parent_entity_id', 'child_entities': [], 'adjustments': [], 'eliminations': [], 'status': 'test-status', 'total_assets': 1.0, 'total_liabilities': 1.0, 'net_income': 1.0, 'created_at': 'test-created_at', 'finalized_at': 'test-finalized_at'})
    assert r1.status_code == 201
    item_id = r1.json()["consolidation_id"]
    r2 = await client.get("/api/consolidations")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/consolidations/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["consolidation_id"] == item_id
