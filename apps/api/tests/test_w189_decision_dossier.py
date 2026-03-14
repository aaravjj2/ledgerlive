"""Tests for Wave 189: Decision Dossier Model API

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w189_decision_dossier import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w189_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w189_create(client):
    r = await client.post("/api/decision-dossiers", json={'close_period_id': 'test-close_period_id', 'exception_id': 'test-exception_id', 'evidence_spans': [], 'recon_scoring': {}, 'ml_confidence': 1.0, 'feature_contributions': {}, 'approvals_chain': [], 'export_verification': {}, 'resolution_type': 'test-resolution_type', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "dossier_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w189_list(client):
    await client.post("/api/decision-dossiers", json={'close_period_id': 'test-close_period_id', 'exception_id': 'test-exception_id', 'evidence_spans': [], 'recon_scoring': {}, 'ml_confidence': 1.0, 'feature_contributions': {}, 'approvals_chain': [], 'export_verification': {}, 'resolution_type': 'test-resolution_type', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/decision-dossiers", json={'close_period_id': 'test-close_period_id', 'exception_id': 'test-exception_id', 'evidence_spans': [], 'recon_scoring': {}, 'ml_confidence': 1.0, 'feature_contributions': {}, 'approvals_chain': [], 'export_verification': {}, 'resolution_type': 'test-resolution_type', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/decision-dossiers")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w189_get_by_id(client):
    r = await client.post("/api/decision-dossiers", json={'close_period_id': 'test-close_period_id', 'exception_id': 'test-exception_id', 'evidence_spans': [], 'recon_scoring': {}, 'ml_confidence': 1.0, 'feature_contributions': {}, 'approvals_chain': [], 'export_verification': {}, 'resolution_type': 'test-resolution_type', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["dossier_id"]
    r2 = await client.get(f"/api/decision-dossiers/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["dossier_id"] == item_id

@pytest.mark.asyncio
async def test_w189_get_not_found(client):
    r = await client.get("/api/decision-dossiers/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w189_add_evidence(client):
    r = await client.post("/api/decision-dossiers", json={'close_period_id': 'test-close_period_id', 'exception_id': 'test-exception_id', 'evidence_spans': [], 'recon_scoring': {}, 'ml_confidence': 1.0, 'feature_contributions': {}, 'approvals_chain': [], 'export_verification': {}, 'resolution_type': 'test-resolution_type', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["dossier_id"]
    r2 = await client.post(f"/api/decision-dossiers/{item_id}/evidence", json={})
    assert r2.status_code == 200
    assert r2.json()["dossier_id"] == item_id

@pytest.mark.asyncio
async def test_w189_add_approval(client):
    r = await client.post("/api/decision-dossiers", json={'close_period_id': 'test-close_period_id', 'exception_id': 'test-exception_id', 'evidence_spans': [], 'recon_scoring': {}, 'ml_confidence': 1.0, 'feature_contributions': {}, 'approvals_chain': [], 'export_verification': {}, 'resolution_type': 'test-resolution_type', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["dossier_id"]
    r2 = await client.post(f"/api/decision-dossiers/{item_id}/approval", json={})
    assert r2.status_code == 200
    assert r2.json()["dossier_id"] == item_id

@pytest.mark.asyncio
async def test_w189_verify_dossier(client):
    r = await client.post("/api/decision-dossiers", json={'close_period_id': 'test-close_period_id', 'exception_id': 'test-exception_id', 'evidence_spans': [], 'recon_scoring': {}, 'ml_confidence': 1.0, 'feature_contributions': {}, 'approvals_chain': [], 'export_verification': {}, 'resolution_type': 'test-resolution_type', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["dossier_id"]
    r2 = await client.post(f"/api/decision-dossiers/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["dossier_id"] == item_id

@pytest.mark.asyncio
async def test_w189_add_evidence_not_found(client):
    r = await client.post("/api/decision-dossiers/nonexistent-id/evidence", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w189_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/decision-dossiers", json={'close_period_id': 'test-close_period_id', 'exception_id': 'test-exception_id', 'evidence_spans': [], 'recon_scoring': {}, 'ml_confidence': 1.0, 'feature_contributions': {}, 'approvals_chain': [], 'export_verification': {}, 'resolution_type': 'test-resolution_type', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "decision_dossier"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w189_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/decision-dossiers", json={'close_period_id': 'test-close_period_id', 'exception_id': 'test-exception_id', 'evidence_spans': [], 'recon_scoring': {}, 'ml_confidence': 1.0, 'feature_contributions': {}, 'approvals_chain': [], 'export_verification': {}, 'resolution_type': 'test-resolution_type', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/decision-dossiers", json={'close_period_id': 'test-close_period_id', 'exception_id': 'test-exception_id', 'evidence_spans': [], 'recon_scoring': {}, 'ml_confidence': 1.0, 'feature_contributions': {}, 'approvals_chain': [], 'export_verification': {}, 'resolution_type': 'test-resolution_type', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "dossier_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w189_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/decision-dossiers", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w189_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/decision-dossiers", json={'close_period_id': 'test-close_period_id', 'exception_id': 'test-exception_id', 'evidence_spans': [], 'recon_scoring': {}, 'ml_confidence': 1.0, 'feature_contributions': {}, 'approvals_chain': [], 'export_verification': {}, 'resolution_type': 'test-resolution_type', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["dossier_id"]
    r2 = await client.get("/api/decision-dossiers")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/decision-dossiers/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["dossier_id"] == item_id
