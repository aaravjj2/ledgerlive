"""Tests for Wave 53: Driver-based Planning

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w53_driver_planning import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w53_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w53_create(client):
    r = await client.post("/api/drivers", json={'name': 'test-name', 'driver_type': 'test-driver_type', 'value': 1.0, 'unit': 'test-unit', 'depends_on': [], 'propagates_to': [], 'cycle_detected': True, 'version': 1, 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "driver_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w53_list(client):
    await client.post("/api/drivers", json={'name': 'test-name', 'driver_type': 'test-driver_type', 'value': 1.0, 'unit': 'test-unit', 'depends_on': [], 'propagates_to': [], 'cycle_detected': True, 'version': 1, 'created_at': 'test-created_at'})
    await client.post("/api/drivers", json={'name': 'test-name', 'driver_type': 'test-driver_type', 'value': 1.0, 'unit': 'test-unit', 'depends_on': [], 'propagates_to': [], 'cycle_detected': True, 'version': 1, 'created_at': 'test-created_at'})
    r = await client.get("/api/drivers")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w53_get_by_id(client):
    r = await client.post("/api/drivers", json={'name': 'test-name', 'driver_type': 'test-driver_type', 'value': 1.0, 'unit': 'test-unit', 'depends_on': [], 'propagates_to': [], 'cycle_detected': True, 'version': 1, 'created_at': 'test-created_at'})
    item_id = r.json()["driver_id"]
    r2 = await client.get(f"/api/drivers/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["driver_id"] == item_id

@pytest.mark.asyncio
async def test_w53_get_not_found(client):
    r = await client.get("/api/drivers/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w53_update_value(client):
    r = await client.post("/api/drivers", json={'name': 'test-name', 'driver_type': 'test-driver_type', 'value': 1.0, 'unit': 'test-unit', 'depends_on': [], 'propagates_to': [], 'cycle_detected': True, 'version': 1, 'created_at': 'test-created_at'})
    item_id = r.json()["driver_id"]
    r2 = await client.post(f"/api/drivers/{item_id}/update-value", json={})
    assert r2.status_code == 200
    assert r2.json()["driver_id"] == item_id

@pytest.mark.asyncio
async def test_w53_propagate(client):
    r = await client.post("/api/drivers", json={'name': 'test-name', 'driver_type': 'test-driver_type', 'value': 1.0, 'unit': 'test-unit', 'depends_on': [], 'propagates_to': [], 'cycle_detected': True, 'version': 1, 'created_at': 'test-created_at'})
    item_id = r.json()["driver_id"]
    r2 = await client.post(f"/api/drivers/{item_id}/propagate", json={})
    assert r2.status_code == 200
    assert r2.json()["driver_id"] == item_id

@pytest.mark.asyncio
async def test_w53_check_cycles(client):
    r = await client.post("/api/drivers", json={'name': 'test-name', 'driver_type': 'test-driver_type', 'value': 1.0, 'unit': 'test-unit', 'depends_on': [], 'propagates_to': [], 'cycle_detected': True, 'version': 1, 'created_at': 'test-created_at'})
    item_id = r.json()["driver_id"]
    r2 = await client.post(f"/api/drivers/{item_id}/check-cycles", json={})
    assert r2.status_code == 200
    assert r2.json()["driver_id"] == item_id

@pytest.mark.asyncio
async def test_w53_update_value_not_found(client):
    r = await client.post("/api/drivers/nonexistent-id/update-value", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w53_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/drivers", json={'name': 'test-name', 'driver_type': 'test-driver_type', 'value': 1.0, 'unit': 'test-unit', 'depends_on': [], 'propagates_to': [], 'cycle_detected': True, 'version': 1, 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "driver_planning"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w53_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/drivers", json={'name': 'test-name', 'driver_type': 'test-driver_type', 'value': 1.0, 'unit': 'test-unit', 'depends_on': [], 'propagates_to': [], 'cycle_detected': True, 'version': 1, 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/drivers", json={'name': 'test-name', 'driver_type': 'test-driver_type', 'value': 1.0, 'unit': 'test-unit', 'depends_on': [], 'propagates_to': [], 'cycle_detected': True, 'version': 1, 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "driver_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w53_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/drivers", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w53_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/drivers", json={'name': 'test-name', 'driver_type': 'test-driver_type', 'value': 1.0, 'unit': 'test-unit', 'depends_on': [], 'propagates_to': [], 'cycle_detected': True, 'version': 1, 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["driver_id"]
    r2 = await client.get("/api/drivers")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/drivers/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["driver_id"] == item_id
