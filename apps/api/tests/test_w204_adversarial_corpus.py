"""Tests for Wave 204: Agent Policy Adversarial Corpus v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w204_adversarial_corpus import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w204_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w204_create(client):
    r = await client.post("/api/adversarial-corpus", json={'scenario_name': 'test-scenario_name', 'attack_type': 'test-attack_type', 'prompt_text': 'test-prompt_text', 'tool_call_attempted': 'test-tool_call_attempted', 'policy_result': 'test-policy_result', 'blocked': True, 'deny_reason': 'test-deny_reason', 'audit_deny_logged': True, 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert r.status_code == 201
    data = r.json()
    assert "corpus_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w204_list(client):
    await client.post("/api/adversarial-corpus", json={'scenario_name': 'test-scenario_name', 'attack_type': 'test-attack_type', 'prompt_text': 'test-prompt_text', 'tool_call_attempted': 'test-tool_call_attempted', 'policy_result': 'test-policy_result', 'blocked': True, 'deny_reason': 'test-deny_reason', 'audit_deny_logged': True, 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    await client.post("/api/adversarial-corpus", json={'scenario_name': 'test-scenario_name', 'attack_type': 'test-attack_type', 'prompt_text': 'test-prompt_text', 'tool_call_attempted': 'test-tool_call_attempted', 'policy_result': 'test-policy_result', 'blocked': True, 'deny_reason': 'test-deny_reason', 'audit_deny_logged': True, 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    r = await client.get("/api/adversarial-corpus")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w204_get_by_id(client):
    r = await client.post("/api/adversarial-corpus", json={'scenario_name': 'test-scenario_name', 'attack_type': 'test-attack_type', 'prompt_text': 'test-prompt_text', 'tool_call_attempted': 'test-tool_call_attempted', 'policy_result': 'test-policy_result', 'blocked': True, 'deny_reason': 'test-deny_reason', 'audit_deny_logged': True, 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    item_id = r.json()["corpus_id"]
    r2 = await client.get(f"/api/adversarial-corpus/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["corpus_id"] == item_id

@pytest.mark.asyncio
async def test_w204_get_not_found(client):
    r = await client.get("/api/adversarial-corpus/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w204_run_scenario(client):
    r = await client.post("/api/adversarial-corpus", json={'scenario_name': 'test-scenario_name', 'attack_type': 'test-attack_type', 'prompt_text': 'test-prompt_text', 'tool_call_attempted': 'test-tool_call_attempted', 'policy_result': 'test-policy_result', 'blocked': True, 'deny_reason': 'test-deny_reason', 'audit_deny_logged': True, 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    item_id = r.json()["corpus_id"]
    r2 = await client.post(f"/api/adversarial-corpus/{item_id}/run", json={})
    assert r2.status_code == 200
    assert r2.json()["corpus_id"] == item_id

@pytest.mark.asyncio
async def test_w204_verify_blocked(client):
    r = await client.post("/api/adversarial-corpus", json={'scenario_name': 'test-scenario_name', 'attack_type': 'test-attack_type', 'prompt_text': 'test-prompt_text', 'tool_call_attempted': 'test-tool_call_attempted', 'policy_result': 'test-policy_result', 'blocked': True, 'deny_reason': 'test-deny_reason', 'audit_deny_logged': True, 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    item_id = r.json()["corpus_id"]
    r2 = await client.post(f"/api/adversarial-corpus/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["corpus_id"] == item_id

@pytest.mark.asyncio
async def test_w204_run_scenario_not_found(client):
    r = await client.post("/api/adversarial-corpus/nonexistent-id/run", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w204_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/adversarial-corpus", json={'scenario_name': 'test-scenario_name', 'attack_type': 'test-attack_type', 'prompt_text': 'test-prompt_text', 'tool_call_attempted': 'test-tool_call_attempted', 'policy_result': 'test-policy_result', 'blocked': True, 'deny_reason': 'test-deny_reason', 'audit_deny_logged': True, 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "adversarial_corpus"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w204_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/adversarial-corpus", json={'scenario_name': 'test-scenario_name', 'attack_type': 'test-attack_type', 'prompt_text': 'test-prompt_text', 'tool_call_attempted': 'test-tool_call_attempted', 'policy_result': 'test-policy_result', 'blocked': True, 'deny_reason': 'test-deny_reason', 'audit_deny_logged': True, 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/adversarial-corpus", json={'scenario_name': 'test-scenario_name', 'attack_type': 'test-attack_type', 'prompt_text': 'test-prompt_text', 'tool_call_attempted': 'test-tool_call_attempted', 'policy_result': 'test-policy_result', 'blocked': True, 'deny_reason': 'test-deny_reason', 'audit_deny_logged': True, 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "corpus_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w204_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/adversarial-corpus", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w204_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/adversarial-corpus", json={'scenario_name': 'test-scenario_name', 'attack_type': 'test-attack_type', 'prompt_text': 'test-prompt_text', 'tool_call_attempted': 'test-tool_call_attempted', 'policy_result': 'test-policy_result', 'blocked': True, 'deny_reason': 'test-deny_reason', 'audit_deny_logged': True, 'deterministic': True, 'status': 'test-status', 'tested_at': 'test-tested_at'})
    assert r1.status_code == 201
    item_id = r1.json()["corpus_id"]
    r2 = await client.get("/api/adversarial-corpus")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/adversarial-corpus/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["corpus_id"] == item_id
