"""Tests for Wave 193: No-Floating-Claim Enforcement

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w193_claim_enforcement import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w193_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w193_create(client):
    r = await client.post("/api/claim-enforcement", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'dossier_id': 'test-dossier_id', 'has_dossier': True, 'claim_text': 'test-claim_text', 'blocked': True, 'block_reason': 'test-block_reason', 'export_allowed': True, 'enforcement_result': 'test-enforcement_result', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r.status_code == 201
    data = r.json()
    assert "enforcement_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w193_list(client):
    await client.post("/api/claim-enforcement", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'dossier_id': 'test-dossier_id', 'has_dossier': True, 'claim_text': 'test-claim_text', 'blocked': True, 'block_reason': 'test-block_reason', 'export_allowed': True, 'enforcement_result': 'test-enforcement_result', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    await client.post("/api/claim-enforcement", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'dossier_id': 'test-dossier_id', 'has_dossier': True, 'claim_text': 'test-claim_text', 'blocked': True, 'block_reason': 'test-block_reason', 'export_allowed': True, 'enforcement_result': 'test-enforcement_result', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    r = await client.get("/api/claim-enforcement")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w193_get_by_id(client):
    r = await client.post("/api/claim-enforcement", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'dossier_id': 'test-dossier_id', 'has_dossier': True, 'claim_text': 'test-claim_text', 'blocked': True, 'block_reason': 'test-block_reason', 'export_allowed': True, 'enforcement_result': 'test-enforcement_result', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["enforcement_id"]
    r2 = await client.get(f"/api/claim-enforcement/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["enforcement_id"] == item_id

@pytest.mark.asyncio
async def test_w193_get_not_found(client):
    r = await client.get("/api/claim-enforcement/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w193_block_export(client):
    r = await client.post("/api/claim-enforcement", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'dossier_id': 'test-dossier_id', 'has_dossier': True, 'claim_text': 'test-claim_text', 'blocked': True, 'block_reason': 'test-block_reason', 'export_allowed': True, 'enforcement_result': 'test-enforcement_result', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["enforcement_id"]
    r2 = await client.post(f"/api/claim-enforcement/{item_id}/block", json={})
    assert r2.status_code == 200
    assert r2.json()["enforcement_id"] == item_id

@pytest.mark.asyncio
async def test_w193_unblock_export(client):
    r = await client.post("/api/claim-enforcement", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'dossier_id': 'test-dossier_id', 'has_dossier': True, 'claim_text': 'test-claim_text', 'blocked': True, 'block_reason': 'test-block_reason', 'export_allowed': True, 'enforcement_result': 'test-enforcement_result', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["enforcement_id"]
    r2 = await client.post(f"/api/claim-enforcement/{item_id}/unblock", json={})
    assert r2.status_code == 200
    assert r2.json()["enforcement_id"] == item_id

@pytest.mark.asyncio
async def test_w193_block_export_not_found(client):
    r = await client.post("/api/claim-enforcement/nonexistent-id/block", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w193_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/claim-enforcement", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'dossier_id': 'test-dossier_id', 'has_dossier': True, 'claim_text': 'test-claim_text', 'blocked': True, 'block_reason': 'test-block_reason', 'export_allowed': True, 'enforcement_result': 'test-enforcement_result', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "claim_enforcement"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w193_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/claim-enforcement", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'dossier_id': 'test-dossier_id', 'has_dossier': True, 'claim_text': 'test-claim_text', 'blocked': True, 'block_reason': 'test-block_reason', 'export_allowed': True, 'enforcement_result': 'test-enforcement_result', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/claim-enforcement", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'dossier_id': 'test-dossier_id', 'has_dossier': True, 'claim_text': 'test-claim_text', 'blocked': True, 'block_reason': 'test-block_reason', 'export_allowed': True, 'enforcement_result': 'test-enforcement_result', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "enforcement_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w193_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/claim-enforcement", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w193_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/claim-enforcement", json={'entity_type': 'test-entity_type', 'entity_id': 'test-entity_id', 'dossier_id': 'test-dossier_id', 'has_dossier': True, 'claim_text': 'test-claim_text', 'blocked': True, 'block_reason': 'test-block_reason', 'export_allowed': True, 'enforcement_result': 'test-enforcement_result', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r1.status_code == 201
    item_id = r1.json()["enforcement_id"]
    r2 = await client.get("/api/claim-enforcement")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/claim-enforcement/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["enforcement_id"] == item_id
