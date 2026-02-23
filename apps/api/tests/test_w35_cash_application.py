"""Tests for Wave 35: Cash Application

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w35_cash_application import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w35_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w35_create(client):
    r = await client.post("/api/cash-applications", json={'customer_id': 'test-customer_id', 'invoice_id': 'test-invoice_id', 'payment_amount': 1.0, 'applied_amount': 1.0, 'remaining': 1.0, 'status': 'test-status', 'dispute_reason': 'test-dispute_reason', 'resolved_at': 'test-resolved_at', 'applied_at': 'test-applied_at'})
    assert r.status_code == 201
    data = r.json()
    assert "application_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w35_list(client):
    await client.post("/api/cash-applications", json={'customer_id': 'test-customer_id', 'invoice_id': 'test-invoice_id', 'payment_amount': 1.0, 'applied_amount': 1.0, 'remaining': 1.0, 'status': 'test-status', 'dispute_reason': 'test-dispute_reason', 'resolved_at': 'test-resolved_at', 'applied_at': 'test-applied_at'})
    await client.post("/api/cash-applications", json={'customer_id': 'test-customer_id', 'invoice_id': 'test-invoice_id', 'payment_amount': 1.0, 'applied_amount': 1.0, 'remaining': 1.0, 'status': 'test-status', 'dispute_reason': 'test-dispute_reason', 'resolved_at': 'test-resolved_at', 'applied_at': 'test-applied_at'})
    r = await client.get("/api/cash-applications")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w35_get_by_id(client):
    r = await client.post("/api/cash-applications", json={'customer_id': 'test-customer_id', 'invoice_id': 'test-invoice_id', 'payment_amount': 1.0, 'applied_amount': 1.0, 'remaining': 1.0, 'status': 'test-status', 'dispute_reason': 'test-dispute_reason', 'resolved_at': 'test-resolved_at', 'applied_at': 'test-applied_at'})
    item_id = r.json()["application_id"]
    r2 = await client.get(f"/api/cash-applications/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["application_id"] == item_id

@pytest.mark.asyncio
async def test_w35_get_not_found(client):
    r = await client.get("/api/cash-applications/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w35_dispute(client):
    r = await client.post("/api/cash-applications", json={'customer_id': 'test-customer_id', 'invoice_id': 'test-invoice_id', 'payment_amount': 1.0, 'applied_amount': 1.0, 'remaining': 1.0, 'status': 'test-status', 'dispute_reason': 'test-dispute_reason', 'resolved_at': 'test-resolved_at', 'applied_at': 'test-applied_at'})
    item_id = r.json()["application_id"]
    r2 = await client.post(f"/api/cash-applications/{item_id}/dispute", json={})
    assert r2.status_code == 200
    assert r2.json()["application_id"] == item_id

@pytest.mark.asyncio
async def test_w35_resolve_dispute(client):
    r = await client.post("/api/cash-applications", json={'customer_id': 'test-customer_id', 'invoice_id': 'test-invoice_id', 'payment_amount': 1.0, 'applied_amount': 1.0, 'remaining': 1.0, 'status': 'test-status', 'dispute_reason': 'test-dispute_reason', 'resolved_at': 'test-resolved_at', 'applied_at': 'test-applied_at'})
    item_id = r.json()["application_id"]
    r2 = await client.post(f"/api/cash-applications/{item_id}/resolve", json={})
    assert r2.status_code == 200
    assert r2.json()["application_id"] == item_id

@pytest.mark.asyncio
async def test_w35_dispute_not_found(client):
    r = await client.post("/api/cash-applications/nonexistent-id/dispute", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w35_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/cash-applications", json={'customer_id': 'test-customer_id', 'invoice_id': 'test-invoice_id', 'payment_amount': 1.0, 'applied_amount': 1.0, 'remaining': 1.0, 'status': 'test-status', 'dispute_reason': 'test-dispute_reason', 'resolved_at': 'test-resolved_at', 'applied_at': 'test-applied_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "cash_application"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w35_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/cash-applications", json={'customer_id': 'test-customer_id', 'invoice_id': 'test-invoice_id', 'payment_amount': 1.0, 'applied_amount': 1.0, 'remaining': 1.0, 'status': 'test-status', 'dispute_reason': 'test-dispute_reason', 'resolved_at': 'test-resolved_at', 'applied_at': 'test-applied_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/cash-applications", json={'customer_id': 'test-customer_id', 'invoice_id': 'test-invoice_id', 'payment_amount': 1.0, 'applied_amount': 1.0, 'remaining': 1.0, 'status': 'test-status', 'dispute_reason': 'test-dispute_reason', 'resolved_at': 'test-resolved_at', 'applied_at': 'test-applied_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "application_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w35_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/cash-applications", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w35_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/cash-applications", json={'customer_id': 'test-customer_id', 'invoice_id': 'test-invoice_id', 'payment_amount': 1.0, 'applied_amount': 1.0, 'remaining': 1.0, 'status': 'test-status', 'dispute_reason': 'test-dispute_reason', 'resolved_at': 'test-resolved_at', 'applied_at': 'test-applied_at'})
    assert r1.status_code == 201
    item_id = r1.json()["application_id"]
    r2 = await client.get("/api/cash-applications")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/cash-applications/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["application_id"] == item_id
