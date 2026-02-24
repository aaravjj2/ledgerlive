"""Tests for Wave 259: Adversarial Corpus v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w259_adversarial_corpus_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w259_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w259_create(client):
    r = await client.post("/api/adversarial-corpus-v2", json={'scenario_count': 1, 'scenarios': [], 'blocked_count': 1, 'approval_required_count': 1, 'passed_count': 1, 'failed_count': 1, 'coverage_pct': 1.0, 'deterministic_results': True, 'evidence_per_scenario': {}, 'corpus_hash': 'test-corpus_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "corpus_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w259_list(client):
    await client.post("/api/adversarial-corpus-v2", json={'scenario_count': 1, 'scenarios': [], 'blocked_count': 1, 'approval_required_count': 1, 'passed_count': 1, 'failed_count': 1, 'coverage_pct': 1.0, 'deterministic_results': True, 'evidence_per_scenario': {}, 'corpus_hash': 'test-corpus_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    await client.post("/api/adversarial-corpus-v2", json={'scenario_count': 1, 'scenarios': [], 'blocked_count': 1, 'approval_required_count': 1, 'passed_count': 1, 'failed_count': 1, 'coverage_pct': 1.0, 'deterministic_results': True, 'evidence_per_scenario': {}, 'corpus_hash': 'test-corpus_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    r = await client.get("/api/adversarial-corpus-v2")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w259_get_by_id(client):
    r = await client.post("/api/adversarial-corpus-v2", json={'scenario_count': 1, 'scenarios': [], 'blocked_count': 1, 'approval_required_count': 1, 'passed_count': 1, 'failed_count': 1, 'coverage_pct': 1.0, 'deterministic_results': True, 'evidence_per_scenario': {}, 'corpus_hash': 'test-corpus_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["corpus_id"]
    r2 = await client.get(f"/api/adversarial-corpus-v2/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["corpus_id"] == item_id

@pytest.mark.asyncio
async def test_w259_get_not_found(client):
    r = await client.get("/api/adversarial-corpus-v2/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w259_run_scenarios(client):
    r = await client.post("/api/adversarial-corpus-v2", json={'scenario_count': 1, 'scenarios': [], 'blocked_count': 1, 'approval_required_count': 1, 'passed_count': 1, 'failed_count': 1, 'coverage_pct': 1.0, 'deterministic_results': True, 'evidence_per_scenario': {}, 'corpus_hash': 'test-corpus_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["corpus_id"]
    r2 = await client.post(f"/api/adversarial-corpus-v2/{item_id}/run", json={})
    assert r2.status_code == 200
    assert r2.json()["corpus_id"] == item_id

@pytest.mark.asyncio
async def test_w259_verify_determinism(client):
    r = await client.post("/api/adversarial-corpus-v2", json={'scenario_count': 1, 'scenarios': [], 'blocked_count': 1, 'approval_required_count': 1, 'passed_count': 1, 'failed_count': 1, 'coverage_pct': 1.0, 'deterministic_results': True, 'evidence_per_scenario': {}, 'corpus_hash': 'test-corpus_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    item_id = r.json()["corpus_id"]
    r2 = await client.post(f"/api/adversarial-corpus-v2/{item_id}/verify-determinism", json={})
    assert r2.status_code == 200
    assert r2.json()["corpus_id"] == item_id

@pytest.mark.asyncio
async def test_w259_run_scenarios_not_found(client):
    r = await client.post("/api/adversarial-corpus-v2/nonexistent-id/run", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w259_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/adversarial-corpus-v2", json={'scenario_count': 1, 'scenarios': [], 'blocked_count': 1, 'approval_required_count': 1, 'passed_count': 1, 'failed_count': 1, 'coverage_pct': 1.0, 'deterministic_results': True, 'evidence_per_scenario': {}, 'corpus_hash': 'test-corpus_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "adversarial_corpus_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w259_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/adversarial-corpus-v2", json={'scenario_count': 1, 'scenarios': [], 'blocked_count': 1, 'approval_required_count': 1, 'passed_count': 1, 'failed_count': 1, 'coverage_pct': 1.0, 'deterministic_results': True, 'evidence_per_scenario': {}, 'corpus_hash': 'test-corpus_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/adversarial-corpus-v2", json={'scenario_count': 1, 'scenarios': [], 'blocked_count': 1, 'approval_required_count': 1, 'passed_count': 1, 'failed_count': 1, 'coverage_pct': 1.0, 'deterministic_results': True, 'evidence_per_scenario': {}, 'corpus_hash': 'test-corpus_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "corpus_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w259_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/adversarial-corpus-v2", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w259_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/adversarial-corpus-v2", json={'scenario_count': 1, 'scenarios': [], 'blocked_count': 1, 'approval_required_count': 1, 'passed_count': 1, 'failed_count': 1, 'coverage_pct': 1.0, 'deterministic_results': True, 'evidence_per_scenario': {}, 'corpus_hash': 'test-corpus_hash', 'status': 'test-status', 'evaluated_at': 'test-evaluated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["corpus_id"]
    r2 = await client.get("/api/adversarial-corpus-v2")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/adversarial-corpus-v2/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["corpus_id"] == item_id
