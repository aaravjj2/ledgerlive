"""Tests for Wave 327: Redaction Events v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w327_redaction_events_v1 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w327_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w327_create(client):
    r = await client.post("/api/redaction-events-v1", json={'document_ref': 'test-document_ref', 'field_redacted': 'test-field_redacted', 'redaction_reason': 'test-redaction_reason', 'redacted_by': 'test-redacted_by', 'evidence_ref': 'test-evidence_ref', 'original_tier': 'test-original_tier', 'redaction_method': 'test-redaction_method', 'reversible': True, 'deterministic': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    assert r.status_code == 201
    data = r.json()
    assert "redaction_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w327_list(client):
    await client.post("/api/redaction-events-v1", json={'document_ref': 'test-document_ref', 'field_redacted': 'test-field_redacted', 'redaction_reason': 'test-redaction_reason', 'redacted_by': 'test-redacted_by', 'evidence_ref': 'test-evidence_ref', 'original_tier': 'test-original_tier', 'redaction_method': 'test-redaction_method', 'reversible': True, 'deterministic': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    await client.post("/api/redaction-events-v1", json={'document_ref': 'test-document_ref', 'field_redacted': 'test-field_redacted', 'redaction_reason': 'test-redaction_reason', 'redacted_by': 'test-redacted_by', 'evidence_ref': 'test-evidence_ref', 'original_tier': 'test-original_tier', 'redaction_method': 'test-redaction_method', 'reversible': True, 'deterministic': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    r = await client.get("/api/redaction-events-v1")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w327_get_by_id(client):
    r = await client.post("/api/redaction-events-v1", json={'document_ref': 'test-document_ref', 'field_redacted': 'test-field_redacted', 'redaction_reason': 'test-redaction_reason', 'redacted_by': 'test-redacted_by', 'evidence_ref': 'test-evidence_ref', 'original_tier': 'test-original_tier', 'redaction_method': 'test-redaction_method', 'reversible': True, 'deterministic': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    item_id = r.json()["redaction_id"]
    r2 = await client.get(f"/api/redaction-events-v1/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["redaction_id"] == item_id

@pytest.mark.asyncio
async def test_w327_get_not_found(client):
    r = await client.get("/api/redaction-events-v1/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w327_link_evidence(client):
    r = await client.post("/api/redaction-events-v1", json={'document_ref': 'test-document_ref', 'field_redacted': 'test-field_redacted', 'redaction_reason': 'test-redaction_reason', 'redacted_by': 'test-redacted_by', 'evidence_ref': 'test-evidence_ref', 'original_tier': 'test-original_tier', 'redaction_method': 'test-redaction_method', 'reversible': True, 'deterministic': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    item_id = r.json()["redaction_id"]
    r2 = await client.post(f"/api/redaction-events-v1/{item_id}/evidence", json={})
    assert r2.status_code == 200
    assert r2.json()["redaction_id"] == item_id

@pytest.mark.asyncio
async def test_w327_reverse_redaction(client):
    r = await client.post("/api/redaction-events-v1", json={'document_ref': 'test-document_ref', 'field_redacted': 'test-field_redacted', 'redaction_reason': 'test-redaction_reason', 'redacted_by': 'test-redacted_by', 'evidence_ref': 'test-evidence_ref', 'original_tier': 'test-original_tier', 'redaction_method': 'test-redaction_method', 'reversible': True, 'deterministic': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    item_id = r.json()["redaction_id"]
    r2 = await client.post(f"/api/redaction-events-v1/{item_id}/reverse", json={})
    assert r2.status_code == 200
    assert r2.json()["redaction_id"] == item_id

@pytest.mark.asyncio
async def test_w327_link_evidence_not_found(client):
    r = await client.post("/api/redaction-events-v1/nonexistent-id/evidence", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w327_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/redaction-events-v1", json={'document_ref': 'test-document_ref', 'field_redacted': 'test-field_redacted', 'redaction_reason': 'test-redaction_reason', 'redacted_by': 'test-redacted_by', 'evidence_ref': 'test-evidence_ref', 'original_tier': 'test-original_tier', 'redaction_method': 'test-redaction_method', 'reversible': True, 'deterministic': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "redaction_events_v1"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w327_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/redaction-events-v1", json={'document_ref': 'test-document_ref', 'field_redacted': 'test-field_redacted', 'redaction_reason': 'test-redaction_reason', 'redacted_by': 'test-redacted_by', 'evidence_ref': 'test-evidence_ref', 'original_tier': 'test-original_tier', 'redaction_method': 'test-redaction_method', 'reversible': True, 'deterministic': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/redaction-events-v1", json={'document_ref': 'test-document_ref', 'field_redacted': 'test-field_redacted', 'redaction_reason': 'test-redaction_reason', 'redacted_by': 'test-redacted_by', 'evidence_ref': 'test-evidence_ref', 'original_tier': 'test-original_tier', 'redaction_method': 'test-redaction_method', 'reversible': True, 'deterministic': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "redaction_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w327_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/redaction-events-v1", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w327_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/redaction-events-v1", json={'document_ref': 'test-document_ref', 'field_redacted': 'test-field_redacted', 'redaction_reason': 'test-redaction_reason', 'redacted_by': 'test-redacted_by', 'evidence_ref': 'test-evidence_ref', 'original_tier': 'test-original_tier', 'redaction_method': 'test-redaction_method', 'reversible': True, 'deterministic': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    assert r1.status_code == 201
    item_id = r1.json()["redaction_id"]
    r2 = await client.get("/api/redaction-events-v1")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/redaction-events-v1/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["redaction_id"] == item_id
