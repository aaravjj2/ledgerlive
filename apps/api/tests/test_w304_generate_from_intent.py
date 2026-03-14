"""Tests for Wave 304: Generate from Intent v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w304_generate_from_intent import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w304_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w304_create(client):
    r = await client.post("/api/generate-from-intent", json={'intent_text': 'test-intent_text', 'matched_rules': [], 'generated_steps': [], 'confidence_score': 1.0, 'blueprint_ref': 'test-blueprint_ref', 'rule_engine_version': 'test-rule_engine_version', 'ambiguity_flags': [], 'fallback_used': True, 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "intent_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w304_list(client):
    await client.post("/api/generate-from-intent", json={'intent_text': 'test-intent_text', 'matched_rules': [], 'generated_steps': [], 'confidence_score': 1.0, 'blueprint_ref': 'test-blueprint_ref', 'rule_engine_version': 'test-rule_engine_version', 'ambiguity_flags': [], 'fallback_used': True, 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/generate-from-intent", json={'intent_text': 'test-intent_text', 'matched_rules': [], 'generated_steps': [], 'confidence_score': 1.0, 'blueprint_ref': 'test-blueprint_ref', 'rule_engine_version': 'test-rule_engine_version', 'ambiguity_flags': [], 'fallback_used': True, 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/generate-from-intent")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w304_get_by_id(client):
    r = await client.post("/api/generate-from-intent", json={'intent_text': 'test-intent_text', 'matched_rules': [], 'generated_steps': [], 'confidence_score': 1.0, 'blueprint_ref': 'test-blueprint_ref', 'rule_engine_version': 'test-rule_engine_version', 'ambiguity_flags': [], 'fallback_used': True, 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["intent_id"]
    r2 = await client.get(f"/api/generate-from-intent/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["intent_id"] == item_id

@pytest.mark.asyncio
async def test_w304_get_not_found(client):
    r = await client.get("/api/generate-from-intent/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w304_refine_intent(client):
    r = await client.post("/api/generate-from-intent", json={'intent_text': 'test-intent_text', 'matched_rules': [], 'generated_steps': [], 'confidence_score': 1.0, 'blueprint_ref': 'test-blueprint_ref', 'rule_engine_version': 'test-rule_engine_version', 'ambiguity_flags': [], 'fallback_used': True, 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["intent_id"]
    r2 = await client.post(f"/api/generate-from-intent/{item_id}/refine", json={})
    assert r2.status_code == 200
    assert r2.json()["intent_id"] == item_id

@pytest.mark.asyncio
async def test_w304_preview_intent(client):
    r = await client.post("/api/generate-from-intent", json={'intent_text': 'test-intent_text', 'matched_rules': [], 'generated_steps': [], 'confidence_score': 1.0, 'blueprint_ref': 'test-blueprint_ref', 'rule_engine_version': 'test-rule_engine_version', 'ambiguity_flags': [], 'fallback_used': True, 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["intent_id"]
    r2 = await client.post(f"/api/generate-from-intent/{item_id}/preview", json={})
    assert r2.status_code == 200
    assert r2.json()["intent_id"] == item_id

@pytest.mark.asyncio
async def test_w304_refine_intent_not_found(client):
    r = await client.post("/api/generate-from-intent/nonexistent-id/refine", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w304_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/generate-from-intent", json={'intent_text': 'test-intent_text', 'matched_rules': [], 'generated_steps': [], 'confidence_score': 1.0, 'blueprint_ref': 'test-blueprint_ref', 'rule_engine_version': 'test-rule_engine_version', 'ambiguity_flags': [], 'fallback_used': True, 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "generate_from_intent"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w304_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/generate-from-intent", json={'intent_text': 'test-intent_text', 'matched_rules': [], 'generated_steps': [], 'confidence_score': 1.0, 'blueprint_ref': 'test-blueprint_ref', 'rule_engine_version': 'test-rule_engine_version', 'ambiguity_flags': [], 'fallback_used': True, 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/generate-from-intent", json={'intent_text': 'test-intent_text', 'matched_rules': [], 'generated_steps': [], 'confidence_score': 1.0, 'blueprint_ref': 'test-blueprint_ref', 'rule_engine_version': 'test-rule_engine_version', 'ambiguity_flags': [], 'fallback_used': True, 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "intent_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w304_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/generate-from-intent", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w304_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/generate-from-intent", json={'intent_text': 'test-intent_text', 'matched_rules': [], 'generated_steps': [], 'confidence_score': 1.0, 'blueprint_ref': 'test-blueprint_ref', 'rule_engine_version': 'test-rule_engine_version', 'ambiguity_flags': [], 'fallback_used': True, 'deterministic': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["intent_id"]
    r2 = await client.get("/api/generate-from-intent")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/generate-from-intent/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["intent_id"] == item_id
