"""Tests for Wave 337: Unified Why/Verify UX v4

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w337_unified_why_verify_v4 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w337_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w337_create(client):
    r = await client.post("/api/unified-why-verify-v4", json={'source_row_ref': 'test-source_row_ref', 'dossier_ref': 'test-dossier_ref', 'evidence_refs': [], 'policy_ref': 'test-policy_ref', 'verification_result': 'test-verification_result', 'confidence': 1.0, 'one_click_url': 'test-one_click_url', 'context_data': {}, 'deterministic': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert r.status_code == 201
    data = r.json()
    assert "verify_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w337_list(client):
    await client.post("/api/unified-why-verify-v4", json={'source_row_ref': 'test-source_row_ref', 'dossier_ref': 'test-dossier_ref', 'evidence_refs': [], 'policy_ref': 'test-policy_ref', 'verification_result': 'test-verification_result', 'confidence': 1.0, 'one_click_url': 'test-one_click_url', 'context_data': {}, 'deterministic': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    await client.post("/api/unified-why-verify-v4", json={'source_row_ref': 'test-source_row_ref', 'dossier_ref': 'test-dossier_ref', 'evidence_refs': [], 'policy_ref': 'test-policy_ref', 'verification_result': 'test-verification_result', 'confidence': 1.0, 'one_click_url': 'test-one_click_url', 'context_data': {}, 'deterministic': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    r = await client.get("/api/unified-why-verify-v4")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w337_get_by_id(client):
    r = await client.post("/api/unified-why-verify-v4", json={'source_row_ref': 'test-source_row_ref', 'dossier_ref': 'test-dossier_ref', 'evidence_refs': [], 'policy_ref': 'test-policy_ref', 'verification_result': 'test-verification_result', 'confidence': 1.0, 'one_click_url': 'test-one_click_url', 'context_data': {}, 'deterministic': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["verify_id"]
    r2 = await client.get(f"/api/unified-why-verify-v4/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["verify_id"] == item_id

@pytest.mark.asyncio
async def test_w337_get_not_found(client):
    r = await client.get("/api/unified-why-verify-v4/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w337_fetch_dossier(client):
    r = await client.post("/api/unified-why-verify-v4", json={'source_row_ref': 'test-source_row_ref', 'dossier_ref': 'test-dossier_ref', 'evidence_refs': [], 'policy_ref': 'test-policy_ref', 'verification_result': 'test-verification_result', 'confidence': 1.0, 'one_click_url': 'test-one_click_url', 'context_data': {}, 'deterministic': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["verify_id"]
    r2 = await client.post(f"/api/unified-why-verify-v4/{item_id}/dossier", json={})
    assert r2.status_code == 200
    assert r2.json()["verify_id"] == item_id

@pytest.mark.asyncio
async def test_w337_fetch_evidence(client):
    r = await client.post("/api/unified-why-verify-v4", json={'source_row_ref': 'test-source_row_ref', 'dossier_ref': 'test-dossier_ref', 'evidence_refs': [], 'policy_ref': 'test-policy_ref', 'verification_result': 'test-verification_result', 'confidence': 1.0, 'one_click_url': 'test-one_click_url', 'context_data': {}, 'deterministic': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["verify_id"]
    r2 = await client.post(f"/api/unified-why-verify-v4/{item_id}/evidence", json={})
    assert r2.status_code == 200
    assert r2.json()["verify_id"] == item_id

@pytest.mark.asyncio
async def test_w337_fetch_dossier_not_found(client):
    r = await client.post("/api/unified-why-verify-v4/nonexistent-id/dossier", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w337_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/unified-why-verify-v4", json={'source_row_ref': 'test-source_row_ref', 'dossier_ref': 'test-dossier_ref', 'evidence_refs': [], 'policy_ref': 'test-policy_ref', 'verification_result': 'test-verification_result', 'confidence': 1.0, 'one_click_url': 'test-one_click_url', 'context_data': {}, 'deterministic': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "unified_why_verify_v4"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w337_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/unified-why-verify-v4", json={'source_row_ref': 'test-source_row_ref', 'dossier_ref': 'test-dossier_ref', 'evidence_refs': [], 'policy_ref': 'test-policy_ref', 'verification_result': 'test-verification_result', 'confidence': 1.0, 'one_click_url': 'test-one_click_url', 'context_data': {}, 'deterministic': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/unified-why-verify-v4", json={'source_row_ref': 'test-source_row_ref', 'dossier_ref': 'test-dossier_ref', 'evidence_refs': [], 'policy_ref': 'test-policy_ref', 'verification_result': 'test-verification_result', 'confidence': 1.0, 'one_click_url': 'test-one_click_url', 'context_data': {}, 'deterministic': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "verify_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w337_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/unified-why-verify-v4", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w337_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/unified-why-verify-v4", json={'source_row_ref': 'test-source_row_ref', 'dossier_ref': 'test-dossier_ref', 'evidence_refs': [], 'policy_ref': 'test-policy_ref', 'verification_result': 'test-verification_result', 'confidence': 1.0, 'one_click_url': 'test-one_click_url', 'context_data': {}, 'deterministic': True, 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert r1.status_code == 201
    item_id = r1.json()["verify_id"]
    r2 = await client.get("/api/unified-why-verify-v4")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/unified-why-verify-v4/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["verify_id"] == item_id
