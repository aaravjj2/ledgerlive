"""Tests for Wave 238: RC Dry Run Simulation v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w238_rc_dry_run import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w238_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w238_create(client):
    r = await client.post("/api/rc-dry-run", json={'playbook_id': 'test-playbook_id', 'period_id': 'test-period_id', 'simulated_steps': [], 'rules_evaluated': 1, 'sla_predictions': {}, 'predicted_blockers': [], 'predicted_duration_min': 1, 'risk_score': 1.0, 'outcome_prediction': 'test-outcome_prediction', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "dry_run_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w238_list(client):
    await client.post("/api/rc-dry-run", json={'playbook_id': 'test-playbook_id', 'period_id': 'test-period_id', 'simulated_steps': [], 'rules_evaluated': 1, 'sla_predictions': {}, 'predicted_blockers': [], 'predicted_duration_min': 1, 'risk_score': 1.0, 'outcome_prediction': 'test-outcome_prediction', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    await client.post("/api/rc-dry-run", json={'playbook_id': 'test-playbook_id', 'period_id': 'test-period_id', 'simulated_steps': [], 'rules_evaluated': 1, 'sla_predictions': {}, 'predicted_blockers': [], 'predicted_duration_min': 1, 'risk_score': 1.0, 'outcome_prediction': 'test-outcome_prediction', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    r = await client.get("/api/rc-dry-run")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w238_get_by_id(client):
    r = await client.post("/api/rc-dry-run", json={'playbook_id': 'test-playbook_id', 'period_id': 'test-period_id', 'simulated_steps': [], 'rules_evaluated': 1, 'sla_predictions': {}, 'predicted_blockers': [], 'predicted_duration_min': 1, 'risk_score': 1.0, 'outcome_prediction': 'test-outcome_prediction', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    item_id = r.json()["dry_run_id"]
    r2 = await client.get(f"/api/rc-dry-run/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["dry_run_id"] == item_id

@pytest.mark.asyncio
async def test_w238_get_not_found(client):
    r = await client.get("/api/rc-dry-run/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w238_predict_blockers(client):
    r = await client.post("/api/rc-dry-run", json={'playbook_id': 'test-playbook_id', 'period_id': 'test-period_id', 'simulated_steps': [], 'rules_evaluated': 1, 'sla_predictions': {}, 'predicted_blockers': [], 'predicted_duration_min': 1, 'risk_score': 1.0, 'outcome_prediction': 'test-outcome_prediction', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    item_id = r.json()["dry_run_id"]
    r2 = await client.post(f"/api/rc-dry-run/{item_id}/predict", json={})
    assert r2.status_code == 200
    assert r2.json()["dry_run_id"] == item_id

@pytest.mark.asyncio
async def test_w238_evaluate_risk(client):
    r = await client.post("/api/rc-dry-run", json={'playbook_id': 'test-playbook_id', 'period_id': 'test-period_id', 'simulated_steps': [], 'rules_evaluated': 1, 'sla_predictions': {}, 'predicted_blockers': [], 'predicted_duration_min': 1, 'risk_score': 1.0, 'outcome_prediction': 'test-outcome_prediction', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    item_id = r.json()["dry_run_id"]
    r2 = await client.post(f"/api/rc-dry-run/{item_id}/risk", json={})
    assert r2.status_code == 200
    assert r2.json()["dry_run_id"] == item_id

@pytest.mark.asyncio
async def test_w238_predict_blockers_not_found(client):
    r = await client.post("/api/rc-dry-run/nonexistent-id/predict", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w238_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/rc-dry-run", json={'playbook_id': 'test-playbook_id', 'period_id': 'test-period_id', 'simulated_steps': [], 'rules_evaluated': 1, 'sla_predictions': {}, 'predicted_blockers': [], 'predicted_duration_min': 1, 'risk_score': 1.0, 'outcome_prediction': 'test-outcome_prediction', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "rc_dry_run"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w238_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/rc-dry-run", json={'playbook_id': 'test-playbook_id', 'period_id': 'test-period_id', 'simulated_steps': [], 'rules_evaluated': 1, 'sla_predictions': {}, 'predicted_blockers': [], 'predicted_duration_min': 1, 'risk_score': 1.0, 'outcome_prediction': 'test-outcome_prediction', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/rc-dry-run", json={'playbook_id': 'test-playbook_id', 'period_id': 'test-period_id', 'simulated_steps': [], 'rules_evaluated': 1, 'sla_predictions': {}, 'predicted_blockers': [], 'predicted_duration_min': 1, 'risk_score': 1.0, 'outcome_prediction': 'test-outcome_prediction', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "dry_run_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w238_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/rc-dry-run", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w238_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/rc-dry-run", json={'playbook_id': 'test-playbook_id', 'period_id': 'test-period_id', 'simulated_steps': [], 'rules_evaluated': 1, 'sla_predictions': {}, 'predicted_blockers': [], 'predicted_duration_min': 1, 'risk_score': 1.0, 'outcome_prediction': 'test-outcome_prediction', 'simulation_hash': 'test-simulation_hash', 'status': 'test-status', 'simulated_at': 'test-simulated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["dry_run_id"]
    r2 = await client.get("/api/rc-dry-run")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/rc-dry-run/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["dry_run_id"] == item_id
