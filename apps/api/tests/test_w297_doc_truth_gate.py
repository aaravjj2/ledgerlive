"""Tests for Wave 297: Documentation Truth Gate v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w297_doc_truth_gate import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w297_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w297_create(client):
    r = await client.post("/api/doc-truth-gate", json={'readme_hash': 'test-readme_hash', 'verify_hash': 'test-verify_hash', 'route_registry_hash': 'test-route_registry_hash', 'make_targets': [], 'endpoint_count': 1, 'mismatches': [], 'all_match': True, 'coverage_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r.status_code == 201
    data = r.json()
    assert "truth_gate_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w297_list(client):
    await client.post("/api/doc-truth-gate", json={'readme_hash': 'test-readme_hash', 'verify_hash': 'test-verify_hash', 'route_registry_hash': 'test-route_registry_hash', 'make_targets': [], 'endpoint_count': 1, 'mismatches': [], 'all_match': True, 'coverage_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    await client.post("/api/doc-truth-gate", json={'readme_hash': 'test-readme_hash', 'verify_hash': 'test-verify_hash', 'route_registry_hash': 'test-route_registry_hash', 'make_targets': [], 'endpoint_count': 1, 'mismatches': [], 'all_match': True, 'coverage_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    r = await client.get("/api/doc-truth-gate")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w297_get_by_id(client):
    r = await client.post("/api/doc-truth-gate", json={'readme_hash': 'test-readme_hash', 'verify_hash': 'test-verify_hash', 'route_registry_hash': 'test-route_registry_hash', 'make_targets': [], 'endpoint_count': 1, 'mismatches': [], 'all_match': True, 'coverage_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["truth_gate_id"]
    r2 = await client.get(f"/api/doc-truth-gate/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["truth_gate_id"] == item_id

@pytest.mark.asyncio
async def test_w297_get_not_found(client):
    r = await client.get("/api/doc-truth-gate/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w297_check_readme(client):
    r = await client.post("/api/doc-truth-gate", json={'readme_hash': 'test-readme_hash', 'verify_hash': 'test-verify_hash', 'route_registry_hash': 'test-route_registry_hash', 'make_targets': [], 'endpoint_count': 1, 'mismatches': [], 'all_match': True, 'coverage_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["truth_gate_id"]
    r2 = await client.post(f"/api/doc-truth-gate/{item_id}/readme", json={})
    assert r2.status_code == 200
    assert r2.json()["truth_gate_id"] == item_id

@pytest.mark.asyncio
async def test_w297_check_routes(client):
    r = await client.post("/api/doc-truth-gate", json={'readme_hash': 'test-readme_hash', 'verify_hash': 'test-verify_hash', 'route_registry_hash': 'test-route_registry_hash', 'make_targets': [], 'endpoint_count': 1, 'mismatches': [], 'all_match': True, 'coverage_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    item_id = r.json()["truth_gate_id"]
    r2 = await client.post(f"/api/doc-truth-gate/{item_id}/routes", json={})
    assert r2.status_code == 200
    assert r2.json()["truth_gate_id"] == item_id

@pytest.mark.asyncio
async def test_w297_check_readme_not_found(client):
    r = await client.post("/api/doc-truth-gate/nonexistent-id/readme", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w297_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/doc-truth-gate", json={'readme_hash': 'test-readme_hash', 'verify_hash': 'test-verify_hash', 'route_registry_hash': 'test-route_registry_hash', 'make_targets': [], 'endpoint_count': 1, 'mismatches': [], 'all_match': True, 'coverage_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "doc_truth_gate"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w297_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/doc-truth-gate", json={'readme_hash': 'test-readme_hash', 'verify_hash': 'test-verify_hash', 'route_registry_hash': 'test-route_registry_hash', 'make_targets': [], 'endpoint_count': 1, 'mismatches': [], 'all_match': True, 'coverage_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/doc-truth-gate", json={'readme_hash': 'test-readme_hash', 'verify_hash': 'test-verify_hash', 'route_registry_hash': 'test-route_registry_hash', 'make_targets': [], 'endpoint_count': 1, 'mismatches': [], 'all_match': True, 'coverage_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "truth_gate_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w297_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/doc-truth-gate", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w297_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/doc-truth-gate", json={'readme_hash': 'test-readme_hash', 'verify_hash': 'test-verify_hash', 'route_registry_hash': 'test-route_registry_hash', 'make_targets': [], 'endpoint_count': 1, 'mismatches': [], 'all_match': True, 'coverage_pct': 1.0, 'deterministic': True, 'gate_hash': 'test-gate_hash', 'status': 'test-status', 'checked_at': 'test-checked_at'})
    assert r1.status_code == 201
    item_id = r1.json()["truth_gate_id"]
    r2 = await client.get("/api/doc-truth-gate")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/doc-truth-gate/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["truth_gate_id"] == item_id
