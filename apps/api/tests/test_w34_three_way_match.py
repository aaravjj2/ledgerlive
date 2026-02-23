"""Tests for Wave 34: Three-Way Match

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w34_three_way_match import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w34_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w34_create(client):
    r = await client.post("/api/three-way-match", json={'po_id': 'test-po_id', 'receipt_id': 'test-receipt_id', 'invoice_id': 'test-invoice_id', 'po_amount': 1.0, 'receipt_amount': 1.0, 'invoice_amount': 1.0, 'variance_pct': 1.0, 'status': 'test-status', 'tolerance_pct': 1.0, 'approved_by': 'test-approved_by', 'matched_at': 'test-matched_at'})
    assert r.status_code == 201
    data = r.json()
    assert "match_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w34_list(client):
    await client.post("/api/three-way-match", json={'po_id': 'test-po_id', 'receipt_id': 'test-receipt_id', 'invoice_id': 'test-invoice_id', 'po_amount': 1.0, 'receipt_amount': 1.0, 'invoice_amount': 1.0, 'variance_pct': 1.0, 'status': 'test-status', 'tolerance_pct': 1.0, 'approved_by': 'test-approved_by', 'matched_at': 'test-matched_at'})
    await client.post("/api/three-way-match", json={'po_id': 'test-po_id', 'receipt_id': 'test-receipt_id', 'invoice_id': 'test-invoice_id', 'po_amount': 1.0, 'receipt_amount': 1.0, 'invoice_amount': 1.0, 'variance_pct': 1.0, 'status': 'test-status', 'tolerance_pct': 1.0, 'approved_by': 'test-approved_by', 'matched_at': 'test-matched_at'})
    r = await client.get("/api/three-way-match")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w34_get_by_id(client):
    r = await client.post("/api/three-way-match", json={'po_id': 'test-po_id', 'receipt_id': 'test-receipt_id', 'invoice_id': 'test-invoice_id', 'po_amount': 1.0, 'receipt_amount': 1.0, 'invoice_amount': 1.0, 'variance_pct': 1.0, 'status': 'test-status', 'tolerance_pct': 1.0, 'approved_by': 'test-approved_by', 'matched_at': 'test-matched_at'})
    item_id = r.json()["match_id"]
    r2 = await client.get(f"/api/three-way-match/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["match_id"] == item_id

@pytest.mark.asyncio
async def test_w34_get_not_found(client):
    r = await client.get("/api/three-way-match/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w34_approve_variance(client):
    r = await client.post("/api/three-way-match", json={'po_id': 'test-po_id', 'receipt_id': 'test-receipt_id', 'invoice_id': 'test-invoice_id', 'po_amount': 1.0, 'receipt_amount': 1.0, 'invoice_amount': 1.0, 'variance_pct': 1.0, 'status': 'test-status', 'tolerance_pct': 1.0, 'approved_by': 'test-approved_by', 'matched_at': 'test-matched_at'})
    item_id = r.json()["match_id"]
    r2 = await client.post(f"/api/three-way-match/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["match_id"] == item_id

@pytest.mark.asyncio
async def test_w34_reject_match(client):
    r = await client.post("/api/three-way-match", json={'po_id': 'test-po_id', 'receipt_id': 'test-receipt_id', 'invoice_id': 'test-invoice_id', 'po_amount': 1.0, 'receipt_amount': 1.0, 'invoice_amount': 1.0, 'variance_pct': 1.0, 'status': 'test-status', 'tolerance_pct': 1.0, 'approved_by': 'test-approved_by', 'matched_at': 'test-matched_at'})
    item_id = r.json()["match_id"]
    r2 = await client.post(f"/api/three-way-match/{item_id}/reject", json={})
    assert r2.status_code == 200
    assert r2.json()["match_id"] == item_id

@pytest.mark.asyncio
async def test_w34_recalculate(client):
    r = await client.post("/api/three-way-match", json={'po_id': 'test-po_id', 'receipt_id': 'test-receipt_id', 'invoice_id': 'test-invoice_id', 'po_amount': 1.0, 'receipt_amount': 1.0, 'invoice_amount': 1.0, 'variance_pct': 1.0, 'status': 'test-status', 'tolerance_pct': 1.0, 'approved_by': 'test-approved_by', 'matched_at': 'test-matched_at'})
    item_id = r.json()["match_id"]
    r2 = await client.post(f"/api/three-way-match/{item_id}/recalculate", json={})
    assert r2.status_code == 200
    assert r2.json()["match_id"] == item_id

@pytest.mark.asyncio
async def test_w34_approve_variance_not_found(client):
    r = await client.post("/api/three-way-match/nonexistent-id/approve", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w34_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/three-way-match", json={'po_id': 'test-po_id', 'receipt_id': 'test-receipt_id', 'invoice_id': 'test-invoice_id', 'po_amount': 1.0, 'receipt_amount': 1.0, 'invoice_amount': 1.0, 'variance_pct': 1.0, 'status': 'test-status', 'tolerance_pct': 1.0, 'approved_by': 'test-approved_by', 'matched_at': 'test-matched_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "three_way_match"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w34_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/three-way-match", json={'po_id': 'test-po_id', 'receipt_id': 'test-receipt_id', 'invoice_id': 'test-invoice_id', 'po_amount': 1.0, 'receipt_amount': 1.0, 'invoice_amount': 1.0, 'variance_pct': 1.0, 'status': 'test-status', 'tolerance_pct': 1.0, 'approved_by': 'test-approved_by', 'matched_at': 'test-matched_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/three-way-match", json={'po_id': 'test-po_id', 'receipt_id': 'test-receipt_id', 'invoice_id': 'test-invoice_id', 'po_amount': 1.0, 'receipt_amount': 1.0, 'invoice_amount': 1.0, 'variance_pct': 1.0, 'status': 'test-status', 'tolerance_pct': 1.0, 'approved_by': 'test-approved_by', 'matched_at': 'test-matched_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "match_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w34_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/three-way-match", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w34_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/three-way-match", json={'po_id': 'test-po_id', 'receipt_id': 'test-receipt_id', 'invoice_id': 'test-invoice_id', 'po_amount': 1.0, 'receipt_amount': 1.0, 'invoice_amount': 1.0, 'variance_pct': 1.0, 'status': 'test-status', 'tolerance_pct': 1.0, 'approved_by': 'test-approved_by', 'matched_at': 'test-matched_at'})
    assert r1.status_code == 201
    item_id = r1.json()["match_id"]
    r2 = await client.get("/api/three-way-match")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/three-way-match/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["match_id"] == item_id
