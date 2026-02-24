"""Tests for Wave 290: Finance Proof Wave v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w290_finance_proof import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w290_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w290_create(client):
    r = await client.post("/api/finance-proof", json={'close_run_ref': 'test-close_run_ref', 'tie_out_ref': 'test-tie_out_ref', 'variance_incident_ref': 'test-variance_incident_ref', 'approval_ref': 'test-approval_ref', 'export_verified': True, 'all_verified': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'content_hash': 'test-content_hash', 'evidence_bundle': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert r.status_code == 201
    data = r.json()
    assert "proof_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w290_list(client):
    await client.post("/api/finance-proof", json={'close_run_ref': 'test-close_run_ref', 'tie_out_ref': 'test-tie_out_ref', 'variance_incident_ref': 'test-variance_incident_ref', 'approval_ref': 'test-approval_ref', 'export_verified': True, 'all_verified': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'content_hash': 'test-content_hash', 'evidence_bundle': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    await client.post("/api/finance-proof", json={'close_run_ref': 'test-close_run_ref', 'tie_out_ref': 'test-tie_out_ref', 'variance_incident_ref': 'test-variance_incident_ref', 'approval_ref': 'test-approval_ref', 'export_verified': True, 'all_verified': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'content_hash': 'test-content_hash', 'evidence_bundle': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    r = await client.get("/api/finance-proof")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w290_get_by_id(client):
    r = await client.post("/api/finance-proof", json={'close_run_ref': 'test-close_run_ref', 'tie_out_ref': 'test-tie_out_ref', 'variance_incident_ref': 'test-variance_incident_ref', 'approval_ref': 'test-approval_ref', 'export_verified': True, 'all_verified': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'content_hash': 'test-content_hash', 'evidence_bundle': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["proof_id"]
    r2 = await client.get(f"/api/finance-proof/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["proof_id"] == item_id

@pytest.mark.asyncio
async def test_w290_get_not_found(client):
    r = await client.get("/api/finance-proof/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w290_verify_proof(client):
    r = await client.post("/api/finance-proof", json={'close_run_ref': 'test-close_run_ref', 'tie_out_ref': 'test-tie_out_ref', 'variance_incident_ref': 'test-variance_incident_ref', 'approval_ref': 'test-approval_ref', 'export_verified': True, 'all_verified': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'content_hash': 'test-content_hash', 'evidence_bundle': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["proof_id"]
    r2 = await client.post(f"/api/finance-proof/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["proof_id"] == item_id

@pytest.mark.asyncio
async def test_w290_seal_proof(client):
    r = await client.post("/api/finance-proof", json={'close_run_ref': 'test-close_run_ref', 'tie_out_ref': 'test-tie_out_ref', 'variance_incident_ref': 'test-variance_incident_ref', 'approval_ref': 'test-approval_ref', 'export_verified': True, 'all_verified': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'content_hash': 'test-content_hash', 'evidence_bundle': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    item_id = r.json()["proof_id"]
    r2 = await client.post(f"/api/finance-proof/{item_id}/seal", json={})
    assert r2.status_code == 200
    assert r2.json()["proof_id"] == item_id

@pytest.mark.asyncio
async def test_w290_verify_proof_not_found(client):
    r = await client.post("/api/finance-proof/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w290_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/finance-proof", json={'close_run_ref': 'test-close_run_ref', 'tie_out_ref': 'test-tie_out_ref', 'variance_incident_ref': 'test-variance_incident_ref', 'approval_ref': 'test-approval_ref', 'export_verified': True, 'all_verified': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'content_hash': 'test-content_hash', 'evidence_bundle': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "finance_proof"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w290_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/finance-proof", json={'close_run_ref': 'test-close_run_ref', 'tie_out_ref': 'test-tie_out_ref', 'variance_incident_ref': 'test-variance_incident_ref', 'approval_ref': 'test-approval_ref', 'export_verified': True, 'all_verified': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'content_hash': 'test-content_hash', 'evidence_bundle': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/finance-proof", json={'close_run_ref': 'test-close_run_ref', 'tie_out_ref': 'test-tie_out_ref', 'variance_incident_ref': 'test-variance_incident_ref', 'approval_ref': 'test-approval_ref', 'export_verified': True, 'all_verified': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'content_hash': 'test-content_hash', 'evidence_bundle': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "proof_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w290_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/finance-proof", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w290_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/finance-proof", json={'close_run_ref': 'test-close_run_ref', 'tie_out_ref': 'test-tie_out_ref', 'variance_incident_ref': 'test-variance_incident_ref', 'approval_ref': 'test-approval_ref', 'export_verified': True, 'all_verified': True, 'determinism_hash': 'test-determinism_hash', 'twice_run_match': True, 'content_hash': 'test-content_hash', 'evidence_bundle': [], 'status': 'test-status', 'verified_at': 'test-verified_at'})
    assert r1.status_code == 201
    item_id = r1.json()["proof_id"]
    r2 = await client.get("/api/finance-proof")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/finance-proof/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["proof_id"] == item_id
