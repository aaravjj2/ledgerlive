"""Tests for Wave 101: SOC2 Evidence Automation 2.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w101_soc2_evidence import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w101_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w101_create(client):
    r = await client.post("/api/soc2-evidence", json={'control_objective': 'test-control_objective', 'evidence_type': 'test-evidence_type', 'artifact_path': 'test-artifact_path', 'collected_at': 'test-collected_at', 'verified': True, 'coverage_pct': 1.0, 'status': 'test-status', 'collector_run_id': 'test-collector_run_id'})
    assert r.status_code == 201
    data = r.json()
    assert "evidence_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w101_list(client):
    await client.post("/api/soc2-evidence", json={'control_objective': 'test-control_objective', 'evidence_type': 'test-evidence_type', 'artifact_path': 'test-artifact_path', 'collected_at': 'test-collected_at', 'verified': True, 'coverage_pct': 1.0, 'status': 'test-status', 'collector_run_id': 'test-collector_run_id'})
    await client.post("/api/soc2-evidence", json={'control_objective': 'test-control_objective', 'evidence_type': 'test-evidence_type', 'artifact_path': 'test-artifact_path', 'collected_at': 'test-collected_at', 'verified': True, 'coverage_pct': 1.0, 'status': 'test-status', 'collector_run_id': 'test-collector_run_id'})
    r = await client.get("/api/soc2-evidence")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w101_get_by_id(client):
    r = await client.post("/api/soc2-evidence", json={'control_objective': 'test-control_objective', 'evidence_type': 'test-evidence_type', 'artifact_path': 'test-artifact_path', 'collected_at': 'test-collected_at', 'verified': True, 'coverage_pct': 1.0, 'status': 'test-status', 'collector_run_id': 'test-collector_run_id'})
    item_id = r.json()["evidence_id"]
    r2 = await client.get(f"/api/soc2-evidence/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["evidence_id"] == item_id

@pytest.mark.asyncio
async def test_w101_get_not_found(client):
    r = await client.get("/api/soc2-evidence/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w101_verify_evidence(client):
    r = await client.post("/api/soc2-evidence", json={'control_objective': 'test-control_objective', 'evidence_type': 'test-evidence_type', 'artifact_path': 'test-artifact_path', 'collected_at': 'test-collected_at', 'verified': True, 'coverage_pct': 1.0, 'status': 'test-status', 'collector_run_id': 'test-collector_run_id'})
    item_id = r.json()["evidence_id"]
    r2 = await client.post(f"/api/soc2-evidence/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["evidence_id"] == item_id

@pytest.mark.asyncio
async def test_w101_verify_evidence_not_found(client):
    r = await client.post("/api/soc2-evidence/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w101_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/soc2-evidence", json={'control_objective': 'test-control_objective', 'evidence_type': 'test-evidence_type', 'artifact_path': 'test-artifact_path', 'collected_at': 'test-collected_at', 'verified': True, 'coverage_pct': 1.0, 'status': 'test-status', 'collector_run_id': 'test-collector_run_id'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "soc2_evidence"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w101_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/soc2-evidence", json={'control_objective': 'test-control_objective', 'evidence_type': 'test-evidence_type', 'artifact_path': 'test-artifact_path', 'collected_at': 'test-collected_at', 'verified': True, 'coverage_pct': 1.0, 'status': 'test-status', 'collector_run_id': 'test-collector_run_id'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/soc2-evidence", json={'control_objective': 'test-control_objective', 'evidence_type': 'test-evidence_type', 'artifact_path': 'test-artifact_path', 'collected_at': 'test-collected_at', 'verified': True, 'coverage_pct': 1.0, 'status': 'test-status', 'collector_run_id': 'test-collector_run_id'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "evidence_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w101_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/soc2-evidence", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w101_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/soc2-evidence", json={'control_objective': 'test-control_objective', 'evidence_type': 'test-evidence_type', 'artifact_path': 'test-artifact_path', 'collected_at': 'test-collected_at', 'verified': True, 'coverage_pct': 1.0, 'status': 'test-status', 'collector_run_id': 'test-collector_run_id'})
    assert r1.status_code == 201
    item_id = r1.json()["evidence_id"]
    r2 = await client.get("/api/soc2-evidence")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/soc2-evidence/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["evidence_id"] == item_id
