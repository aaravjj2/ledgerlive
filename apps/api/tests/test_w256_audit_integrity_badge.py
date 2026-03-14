"""Tests for Wave 256: Audit Integrity Badge v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w256_audit_integrity_badge import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w256_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w256_create(client):
    r = await client.post("/api/audit-integrity-badge", json={'entity_type': 'test-entity_type', 'entity_ref': 'test-entity_ref', 'merkle_root': 'test-merkle_root', 'proof_chain': [], 'verification_result': 'test-verification_result', 'last_verified_at': 'test-last_verified_at', 'tamper_detected': True, 'badge_state': 'test-badge_state', 'display_color': 'test-display_color', 'proof_depth': 1, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "badge_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w256_list(client):
    await client.post("/api/audit-integrity-badge", json={'entity_type': 'test-entity_type', 'entity_ref': 'test-entity_ref', 'merkle_root': 'test-merkle_root', 'proof_chain': [], 'verification_result': 'test-verification_result', 'last_verified_at': 'test-last_verified_at', 'tamper_detected': True, 'badge_state': 'test-badge_state', 'display_color': 'test-display_color', 'proof_depth': 1, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    await client.post("/api/audit-integrity-badge", json={'entity_type': 'test-entity_type', 'entity_ref': 'test-entity_ref', 'merkle_root': 'test-merkle_root', 'proof_chain': [], 'verification_result': 'test-verification_result', 'last_verified_at': 'test-last_verified_at', 'tamper_detected': True, 'badge_state': 'test-badge_state', 'display_color': 'test-display_color', 'proof_depth': 1, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    r = await client.get("/api/audit-integrity-badge")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w256_get_by_id(client):
    r = await client.post("/api/audit-integrity-badge", json={'entity_type': 'test-entity_type', 'entity_ref': 'test-entity_ref', 'merkle_root': 'test-merkle_root', 'proof_chain': [], 'verification_result': 'test-verification_result', 'last_verified_at': 'test-last_verified_at', 'tamper_detected': True, 'badge_state': 'test-badge_state', 'display_color': 'test-display_color', 'proof_depth': 1, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    item_id = r.json()["badge_id"]
    r2 = await client.get(f"/api/audit-integrity-badge/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["badge_id"] == item_id

@pytest.mark.asyncio
async def test_w256_get_not_found(client):
    r = await client.get("/api/audit-integrity-badge/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w256_verify_badge(client):
    r = await client.post("/api/audit-integrity-badge", json={'entity_type': 'test-entity_type', 'entity_ref': 'test-entity_ref', 'merkle_root': 'test-merkle_root', 'proof_chain': [], 'verification_result': 'test-verification_result', 'last_verified_at': 'test-last_verified_at', 'tamper_detected': True, 'badge_state': 'test-badge_state', 'display_color': 'test-display_color', 'proof_depth': 1, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    item_id = r.json()["badge_id"]
    r2 = await client.post(f"/api/audit-integrity-badge/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["badge_id"] == item_id

@pytest.mark.asyncio
async def test_w256_recompute_badge(client):
    r = await client.post("/api/audit-integrity-badge", json={'entity_type': 'test-entity_type', 'entity_ref': 'test-entity_ref', 'merkle_root': 'test-merkle_root', 'proof_chain': [], 'verification_result': 'test-verification_result', 'last_verified_at': 'test-last_verified_at', 'tamper_detected': True, 'badge_state': 'test-badge_state', 'display_color': 'test-display_color', 'proof_depth': 1, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    item_id = r.json()["badge_id"]
    r2 = await client.post(f"/api/audit-integrity-badge/{item_id}/recompute", json={})
    assert r2.status_code == 200
    assert r2.json()["badge_id"] == item_id

@pytest.mark.asyncio
async def test_w256_verify_badge_not_found(client):
    r = await client.post("/api/audit-integrity-badge/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w256_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/audit-integrity-badge", json={'entity_type': 'test-entity_type', 'entity_ref': 'test-entity_ref', 'merkle_root': 'test-merkle_root', 'proof_chain': [], 'verification_result': 'test-verification_result', 'last_verified_at': 'test-last_verified_at', 'tamper_detected': True, 'badge_state': 'test-badge_state', 'display_color': 'test-display_color', 'proof_depth': 1, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "audit_integrity_badge"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w256_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/audit-integrity-badge", json={'entity_type': 'test-entity_type', 'entity_ref': 'test-entity_ref', 'merkle_root': 'test-merkle_root', 'proof_chain': [], 'verification_result': 'test-verification_result', 'last_verified_at': 'test-last_verified_at', 'tamper_detected': True, 'badge_state': 'test-badge_state', 'display_color': 'test-display_color', 'proof_depth': 1, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/audit-integrity-badge", json={'entity_type': 'test-entity_type', 'entity_ref': 'test-entity_ref', 'merkle_root': 'test-merkle_root', 'proof_chain': [], 'verification_result': 'test-verification_result', 'last_verified_at': 'test-last_verified_at', 'tamper_detected': True, 'badge_state': 'test-badge_state', 'display_color': 'test-display_color', 'proof_depth': 1, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "badge_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w256_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/audit-integrity-badge", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w256_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/audit-integrity-badge", json={'entity_type': 'test-entity_type', 'entity_ref': 'test-entity_ref', 'merkle_root': 'test-merkle_root', 'proof_chain': [], 'verification_result': 'test-verification_result', 'last_verified_at': 'test-last_verified_at', 'tamper_detected': True, 'badge_state': 'test-badge_state', 'display_color': 'test-display_color', 'proof_depth': 1, 'status': 'test-status', 'computed_at': 'test-computed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["badge_id"]
    r2 = await client.get("/api/audit-integrity-badge")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/audit-integrity-badge/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["badge_id"] == item_id
