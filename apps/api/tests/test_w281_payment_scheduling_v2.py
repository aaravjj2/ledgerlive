"""Tests for Wave 281: Payment Scheduling v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w281_payment_scheduling_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w281_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w281_create(client):
    r = await client.post("/api/payment-scheduling-v2", json={'vendor_id': 'test-vendor_id', 'amount': 1.0, 'currency': 'test-currency', 'payment_date': 'test-payment_date', 'approval_gate': 'test-approval_gate', 'vendor_risk_score': 1.0, 'treasury_ladder_ref': 'test-treasury_ladder_ref', 'cash_available': 1.0, 'conflict_detected': True, 'approval_status': 'test-approval_status', 'deterministic': True, 'status': 'test-status', 'scheduled_at': 'test-scheduled_at'})
    assert r.status_code == 201
    data = r.json()
    assert "schedule_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w281_list(client):
    await client.post("/api/payment-scheduling-v2", json={'vendor_id': 'test-vendor_id', 'amount': 1.0, 'currency': 'test-currency', 'payment_date': 'test-payment_date', 'approval_gate': 'test-approval_gate', 'vendor_risk_score': 1.0, 'treasury_ladder_ref': 'test-treasury_ladder_ref', 'cash_available': 1.0, 'conflict_detected': True, 'approval_status': 'test-approval_status', 'deterministic': True, 'status': 'test-status', 'scheduled_at': 'test-scheduled_at'})
    await client.post("/api/payment-scheduling-v2", json={'vendor_id': 'test-vendor_id', 'amount': 1.0, 'currency': 'test-currency', 'payment_date': 'test-payment_date', 'approval_gate': 'test-approval_gate', 'vendor_risk_score': 1.0, 'treasury_ladder_ref': 'test-treasury_ladder_ref', 'cash_available': 1.0, 'conflict_detected': True, 'approval_status': 'test-approval_status', 'deterministic': True, 'status': 'test-status', 'scheduled_at': 'test-scheduled_at'})
    r = await client.get("/api/payment-scheduling-v2")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w281_get_by_id(client):
    r = await client.post("/api/payment-scheduling-v2", json={'vendor_id': 'test-vendor_id', 'amount': 1.0, 'currency': 'test-currency', 'payment_date': 'test-payment_date', 'approval_gate': 'test-approval_gate', 'vendor_risk_score': 1.0, 'treasury_ladder_ref': 'test-treasury_ladder_ref', 'cash_available': 1.0, 'conflict_detected': True, 'approval_status': 'test-approval_status', 'deterministic': True, 'status': 'test-status', 'scheduled_at': 'test-scheduled_at'})
    item_id = r.json()["schedule_id"]
    r2 = await client.get(f"/api/payment-scheduling-v2/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["schedule_id"] == item_id

@pytest.mark.asyncio
async def test_w281_get_not_found(client):
    r = await client.get("/api/payment-scheduling-v2/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w281_approve_payment(client):
    r = await client.post("/api/payment-scheduling-v2", json={'vendor_id': 'test-vendor_id', 'amount': 1.0, 'currency': 'test-currency', 'payment_date': 'test-payment_date', 'approval_gate': 'test-approval_gate', 'vendor_risk_score': 1.0, 'treasury_ladder_ref': 'test-treasury_ladder_ref', 'cash_available': 1.0, 'conflict_detected': True, 'approval_status': 'test-approval_status', 'deterministic': True, 'status': 'test-status', 'scheduled_at': 'test-scheduled_at'})
    item_id = r.json()["schedule_id"]
    r2 = await client.post(f"/api/payment-scheduling-v2/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["schedule_id"] == item_id

@pytest.mark.asyncio
async def test_w281_check_cash(client):
    r = await client.post("/api/payment-scheduling-v2", json={'vendor_id': 'test-vendor_id', 'amount': 1.0, 'currency': 'test-currency', 'payment_date': 'test-payment_date', 'approval_gate': 'test-approval_gate', 'vendor_risk_score': 1.0, 'treasury_ladder_ref': 'test-treasury_ladder_ref', 'cash_available': 1.0, 'conflict_detected': True, 'approval_status': 'test-approval_status', 'deterministic': True, 'status': 'test-status', 'scheduled_at': 'test-scheduled_at'})
    item_id = r.json()["schedule_id"]
    r2 = await client.post(f"/api/payment-scheduling-v2/{item_id}/cash-check", json={})
    assert r2.status_code == 200
    assert r2.json()["schedule_id"] == item_id

@pytest.mark.asyncio
async def test_w281_assess_vendor_risk(client):
    r = await client.post("/api/payment-scheduling-v2", json={'vendor_id': 'test-vendor_id', 'amount': 1.0, 'currency': 'test-currency', 'payment_date': 'test-payment_date', 'approval_gate': 'test-approval_gate', 'vendor_risk_score': 1.0, 'treasury_ladder_ref': 'test-treasury_ladder_ref', 'cash_available': 1.0, 'conflict_detected': True, 'approval_status': 'test-approval_status', 'deterministic': True, 'status': 'test-status', 'scheduled_at': 'test-scheduled_at'})
    item_id = r.json()["schedule_id"]
    r2 = await client.post(f"/api/payment-scheduling-v2/{item_id}/vendor-risk", json={})
    assert r2.status_code == 200
    assert r2.json()["schedule_id"] == item_id

@pytest.mark.asyncio
async def test_w281_approve_payment_not_found(client):
    r = await client.post("/api/payment-scheduling-v2/nonexistent-id/approve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w281_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/payment-scheduling-v2", json={'vendor_id': 'test-vendor_id', 'amount': 1.0, 'currency': 'test-currency', 'payment_date': 'test-payment_date', 'approval_gate': 'test-approval_gate', 'vendor_risk_score': 1.0, 'treasury_ladder_ref': 'test-treasury_ladder_ref', 'cash_available': 1.0, 'conflict_detected': True, 'approval_status': 'test-approval_status', 'deterministic': True, 'status': 'test-status', 'scheduled_at': 'test-scheduled_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "payment_scheduling_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w281_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/payment-scheduling-v2", json={'vendor_id': 'test-vendor_id', 'amount': 1.0, 'currency': 'test-currency', 'payment_date': 'test-payment_date', 'approval_gate': 'test-approval_gate', 'vendor_risk_score': 1.0, 'treasury_ladder_ref': 'test-treasury_ladder_ref', 'cash_available': 1.0, 'conflict_detected': True, 'approval_status': 'test-approval_status', 'deterministic': True, 'status': 'test-status', 'scheduled_at': 'test-scheduled_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/payment-scheduling-v2", json={'vendor_id': 'test-vendor_id', 'amount': 1.0, 'currency': 'test-currency', 'payment_date': 'test-payment_date', 'approval_gate': 'test-approval_gate', 'vendor_risk_score': 1.0, 'treasury_ladder_ref': 'test-treasury_ladder_ref', 'cash_available': 1.0, 'conflict_detected': True, 'approval_status': 'test-approval_status', 'deterministic': True, 'status': 'test-status', 'scheduled_at': 'test-scheduled_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "schedule_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w281_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/payment-scheduling-v2", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w281_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/payment-scheduling-v2", json={'vendor_id': 'test-vendor_id', 'amount': 1.0, 'currency': 'test-currency', 'payment_date': 'test-payment_date', 'approval_gate': 'test-approval_gate', 'vendor_risk_score': 1.0, 'treasury_ladder_ref': 'test-treasury_ladder_ref', 'cash_available': 1.0, 'conflict_detected': True, 'approval_status': 'test-approval_status', 'deterministic': True, 'status': 'test-status', 'scheduled_at': 'test-scheduled_at'})
    assert r1.status_code == 201
    item_id = r1.json()["schedule_id"]
    r2 = await client.get("/api/payment-scheduling-v2")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/payment-scheduling-v2/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["schedule_id"] == item_id
