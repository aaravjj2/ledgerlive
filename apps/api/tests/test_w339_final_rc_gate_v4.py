"""Tests for Wave 339: Final RC Gate v4

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w339_final_rc_gate_v4 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w339_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w339_create(client):
    r = await client.post("/api/final-rc-gate-v4", json={'builder_coverage': True, 'atlassian_mocks_pass': True, 'airia_readiness': True, 'security_budgets_pass': True, 'golden_scenario_pass': True, 'all_pass': True, 'gate_score': 1.0, 'failure_details': [], 'evidence_refs': [], 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "gate_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w339_list(client):
    await client.post("/api/final-rc-gate-v4", json={'builder_coverage': True, 'atlassian_mocks_pass': True, 'airia_readiness': True, 'security_budgets_pass': True, 'golden_scenario_pass': True, 'all_pass': True, 'gate_score': 1.0, 'failure_details': [], 'evidence_refs': [], 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    await client.post("/api/final-rc-gate-v4", json={'builder_coverage': True, 'atlassian_mocks_pass': True, 'airia_readiness': True, 'security_budgets_pass': True, 'golden_scenario_pass': True, 'all_pass': True, 'gate_score': 1.0, 'failure_details': [], 'evidence_refs': [], 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    r = await client.get("/api/final-rc-gate-v4")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w339_get_by_id(client):
    r = await client.post("/api/final-rc-gate-v4", json={'builder_coverage': True, 'atlassian_mocks_pass': True, 'airia_readiness': True, 'security_budgets_pass': True, 'golden_scenario_pass': True, 'all_pass': True, 'gate_score': 1.0, 'failure_details': [], 'evidence_refs': [], 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["gate_id"]
    r2 = await client.get(f"/api/final-rc-gate-v4/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["gate_id"] == item_id

@pytest.mark.asyncio
async def test_w339_get_not_found(client):
    r = await client.get("/api/final-rc-gate-v4/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w339_verify_all(client):
    r = await client.post("/api/final-rc-gate-v4", json={'builder_coverage': True, 'atlassian_mocks_pass': True, 'airia_readiness': True, 'security_budgets_pass': True, 'golden_scenario_pass': True, 'all_pass': True, 'gate_score': 1.0, 'failure_details': [], 'evidence_refs': [], 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["gate_id"]
    r2 = await client.post(f"/api/final-rc-gate-v4/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["gate_id"] == item_id

@pytest.mark.asyncio
async def test_w339_export_gate_pack(client):
    r = await client.post("/api/final-rc-gate-v4", json={'builder_coverage': True, 'atlassian_mocks_pass': True, 'airia_readiness': True, 'security_budgets_pass': True, 'golden_scenario_pass': True, 'all_pass': True, 'gate_score': 1.0, 'failure_details': [], 'evidence_refs': [], 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["gate_id"]
    r2 = await client.post(f"/api/final-rc-gate-v4/{item_id}/export", json={})
    assert r2.status_code == 200
    assert r2.json()["gate_id"] == item_id

@pytest.mark.asyncio
async def test_w339_verify_all_not_found(client):
    r = await client.post("/api/final-rc-gate-v4/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w339_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/final-rc-gate-v4", json={'builder_coverage': True, 'atlassian_mocks_pass': True, 'airia_readiness': True, 'security_budgets_pass': True, 'golden_scenario_pass': True, 'all_pass': True, 'gate_score': 1.0, 'failure_details': [], 'evidence_refs': [], 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "final_rc_gate_v4"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w339_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/final-rc-gate-v4", json={'builder_coverage': True, 'atlassian_mocks_pass': True, 'airia_readiness': True, 'security_budgets_pass': True, 'golden_scenario_pass': True, 'all_pass': True, 'gate_score': 1.0, 'failure_details': [], 'evidence_refs': [], 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/final-rc-gate-v4", json={'builder_coverage': True, 'atlassian_mocks_pass': True, 'airia_readiness': True, 'security_budgets_pass': True, 'golden_scenario_pass': True, 'all_pass': True, 'gate_score': 1.0, 'failure_details': [], 'evidence_refs': [], 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "gate_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w339_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/final-rc-gate-v4", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w339_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/final-rc-gate-v4", json={'builder_coverage': True, 'atlassian_mocks_pass': True, 'airia_readiness': True, 'security_budgets_pass': True, 'golden_scenario_pass': True, 'all_pass': True, 'gate_score': 1.0, 'failure_details': [], 'evidence_refs': [], 'deterministic': True, 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["gate_id"]
    r2 = await client.get("/api/final-rc-gate-v4")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/final-rc-gate-v4/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["gate_id"] == item_id
