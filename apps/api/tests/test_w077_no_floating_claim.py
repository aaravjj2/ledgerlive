"""Tests for Wave 77: No Floating Claim Guard

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w077_no_floating_claim import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w077_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w077_create(client):
    r = await client.post("/api/no-floating-claims", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'claim_field': 'test-claim_field', 'has_evidence': True, 'evidence_ref': 'test-evidence_ref', 'violation': True, 'scanned_at': 'test-scanned_at'})
    assert r.status_code == 201
    data = r.json()
    assert "guard_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w077_list(client):
    await client.post("/api/no-floating-claims", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'claim_field': 'test-claim_field', 'has_evidence': True, 'evidence_ref': 'test-evidence_ref', 'violation': True, 'scanned_at': 'test-scanned_at'})
    await client.post("/api/no-floating-claims", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'claim_field': 'test-claim_field', 'has_evidence': True, 'evidence_ref': 'test-evidence_ref', 'violation': True, 'scanned_at': 'test-scanned_at'})
    r = await client.get("/api/no-floating-claims")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w077_get_by_id(client):
    r = await client.post("/api/no-floating-claims", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'claim_field': 'test-claim_field', 'has_evidence': True, 'evidence_ref': 'test-evidence_ref', 'violation': True, 'scanned_at': 'test-scanned_at'})
    item_id = r.json()["guard_id"]
    r2 = await client.get(f"/api/no-floating-claims/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["guard_id"] == item_id

@pytest.mark.asyncio
async def test_w077_get_not_found(client):
    r = await client.get("/api/no-floating-claims/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w077_fix_violation(client):
    r = await client.post("/api/no-floating-claims", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'claim_field': 'test-claim_field', 'has_evidence': True, 'evidence_ref': 'test-evidence_ref', 'violation': True, 'scanned_at': 'test-scanned_at'})
    item_id = r.json()["guard_id"]
    r2 = await client.post(f"/api/no-floating-claims/{item_id}/fix", json={})
    assert r2.status_code == 200
    assert r2.json()["guard_id"] == item_id

@pytest.mark.asyncio
async def test_w077_fix_violation_not_found(client):
    r = await client.post("/api/no-floating-claims/nonexistent-id/fix", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w077_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/no-floating-claims", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'claim_field': 'test-claim_field', 'has_evidence': True, 'evidence_ref': 'test-evidence_ref', 'violation': True, 'scanned_at': 'test-scanned_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "no_floating_claim"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w077_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/no-floating-claims", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'claim_field': 'test-claim_field', 'has_evidence': True, 'evidence_ref': 'test-evidence_ref', 'violation': True, 'scanned_at': 'test-scanned_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/no-floating-claims", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'claim_field': 'test-claim_field', 'has_evidence': True, 'evidence_ref': 'test-evidence_ref', 'violation': True, 'scanned_at': 'test-scanned_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "guard_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w077_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/no-floating-claims", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w077_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/no-floating-claims", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'claim_field': 'test-claim_field', 'has_evidence': True, 'evidence_ref': 'test-evidence_ref', 'violation': True, 'scanned_at': 'test-scanned_at'})
    assert r1.status_code == 201
    item_id = r1.json()["guard_id"]
    r2 = await client.get("/api/no-floating-claims")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/no-floating-claims/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["guard_id"] == item_id
