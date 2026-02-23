"""Tests for Wave 81: Intercompany 2.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w081_intercompany_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w081_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w081_create(client):
    r = await client.post("/api/intercompany-v2", json={'source_entity': 'test-source_entity', 'target_entity': 'test-target_entity', 'amount': 1.0, 'currency': 'test-currency', 'settlement_status': 'test-settlement_status', 'aging_days': 1, 'dispute_reason': 'test-dispute_reason', 'elimination_id': 'test-elimination_id', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "ic_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w081_list(client):
    await client.post("/api/intercompany-v2", json={'source_entity': 'test-source_entity', 'target_entity': 'test-target_entity', 'amount': 1.0, 'currency': 'test-currency', 'settlement_status': 'test-settlement_status', 'aging_days': 1, 'dispute_reason': 'test-dispute_reason', 'elimination_id': 'test-elimination_id', 'created_at': 'test-created_at'})
    await client.post("/api/intercompany-v2", json={'source_entity': 'test-source_entity', 'target_entity': 'test-target_entity', 'amount': 1.0, 'currency': 'test-currency', 'settlement_status': 'test-settlement_status', 'aging_days': 1, 'dispute_reason': 'test-dispute_reason', 'elimination_id': 'test-elimination_id', 'created_at': 'test-created_at'})
    r = await client.get("/api/intercompany-v2")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w081_get_by_id(client):
    r = await client.post("/api/intercompany-v2", json={'source_entity': 'test-source_entity', 'target_entity': 'test-target_entity', 'amount': 1.0, 'currency': 'test-currency', 'settlement_status': 'test-settlement_status', 'aging_days': 1, 'dispute_reason': 'test-dispute_reason', 'elimination_id': 'test-elimination_id', 'created_at': 'test-created_at'})
    item_id = r.json()["ic_id"]
    r2 = await client.get(f"/api/intercompany-v2/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["ic_id"] == item_id

@pytest.mark.asyncio
async def test_w081_get_not_found(client):
    r = await client.get("/api/intercompany-v2/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w081_settle(client):
    r = await client.post("/api/intercompany-v2", json={'source_entity': 'test-source_entity', 'target_entity': 'test-target_entity', 'amount': 1.0, 'currency': 'test-currency', 'settlement_status': 'test-settlement_status', 'aging_days': 1, 'dispute_reason': 'test-dispute_reason', 'elimination_id': 'test-elimination_id', 'created_at': 'test-created_at'})
    item_id = r.json()["ic_id"]
    r2 = await client.post(f"/api/intercompany-v2/{item_id}/settle", json={})
    assert r2.status_code == 200
    assert r2.json()["ic_id"] == item_id

@pytest.mark.asyncio
async def test_w081_dispute(client):
    r = await client.post("/api/intercompany-v2", json={'source_entity': 'test-source_entity', 'target_entity': 'test-target_entity', 'amount': 1.0, 'currency': 'test-currency', 'settlement_status': 'test-settlement_status', 'aging_days': 1, 'dispute_reason': 'test-dispute_reason', 'elimination_id': 'test-elimination_id', 'created_at': 'test-created_at'})
    item_id = r.json()["ic_id"]
    r2 = await client.post(f"/api/intercompany-v2/{item_id}/dispute", json={})
    assert r2.status_code == 200
    assert r2.json()["ic_id"] == item_id

@pytest.mark.asyncio
async def test_w081_eliminate(client):
    r = await client.post("/api/intercompany-v2", json={'source_entity': 'test-source_entity', 'target_entity': 'test-target_entity', 'amount': 1.0, 'currency': 'test-currency', 'settlement_status': 'test-settlement_status', 'aging_days': 1, 'dispute_reason': 'test-dispute_reason', 'elimination_id': 'test-elimination_id', 'created_at': 'test-created_at'})
    item_id = r.json()["ic_id"]
    r2 = await client.post(f"/api/intercompany-v2/{item_id}/eliminate", json={})
    assert r2.status_code == 200
    assert r2.json()["ic_id"] == item_id

@pytest.mark.asyncio
async def test_w081_settle_not_found(client):
    r = await client.post("/api/intercompany-v2/nonexistent-id/settle", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w081_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/intercompany-v2", json={'source_entity': 'test-source_entity', 'target_entity': 'test-target_entity', 'amount': 1.0, 'currency': 'test-currency', 'settlement_status': 'test-settlement_status', 'aging_days': 1, 'dispute_reason': 'test-dispute_reason', 'elimination_id': 'test-elimination_id', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "intercompany_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w081_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/intercompany-v2", json={'source_entity': 'test-source_entity', 'target_entity': 'test-target_entity', 'amount': 1.0, 'currency': 'test-currency', 'settlement_status': 'test-settlement_status', 'aging_days': 1, 'dispute_reason': 'test-dispute_reason', 'elimination_id': 'test-elimination_id', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/intercompany-v2", json={'source_entity': 'test-source_entity', 'target_entity': 'test-target_entity', 'amount': 1.0, 'currency': 'test-currency', 'settlement_status': 'test-settlement_status', 'aging_days': 1, 'dispute_reason': 'test-dispute_reason', 'elimination_id': 'test-elimination_id', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "ic_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w081_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/intercompany-v2", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w081_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/intercompany-v2", json={'source_entity': 'test-source_entity', 'target_entity': 'test-target_entity', 'amount': 1.0, 'currency': 'test-currency', 'settlement_status': 'test-settlement_status', 'aging_days': 1, 'dispute_reason': 'test-dispute_reason', 'elimination_id': 'test-elimination_id', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["ic_id"]
    r2 = await client.get("/api/intercompany-v2")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/intercompany-v2/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["ic_id"] == item_id
