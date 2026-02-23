"""Tests for Wave 104: GDPR Redaction 2.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w104_gdpr_redaction import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w104_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w104_create(client):
    r = await client.post("/api/gdpr-redactions", json={'subject_id': 'test-subject_id', 'data_categories': [], 'redaction_scope': {}, 'merkle_before': 'test-merkle_before', 'merkle_after': 'test-merkle_after', 'integrity_preserved': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    assert r.status_code == 201
    data = r.json()
    assert "redaction_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w104_list(client):
    await client.post("/api/gdpr-redactions", json={'subject_id': 'test-subject_id', 'data_categories': [], 'redaction_scope': {}, 'merkle_before': 'test-merkle_before', 'merkle_after': 'test-merkle_after', 'integrity_preserved': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    await client.post("/api/gdpr-redactions", json={'subject_id': 'test-subject_id', 'data_categories': [], 'redaction_scope': {}, 'merkle_before': 'test-merkle_before', 'merkle_after': 'test-merkle_after', 'integrity_preserved': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    r = await client.get("/api/gdpr-redactions")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w104_get_by_id(client):
    r = await client.post("/api/gdpr-redactions", json={'subject_id': 'test-subject_id', 'data_categories': [], 'redaction_scope': {}, 'merkle_before': 'test-merkle_before', 'merkle_after': 'test-merkle_after', 'integrity_preserved': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    item_id = r.json()["redaction_id"]
    r2 = await client.get(f"/api/gdpr-redactions/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["redaction_id"] == item_id

@pytest.mark.asyncio
async def test_w104_get_not_found(client):
    r = await client.get("/api/gdpr-redactions/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w104_execute_redaction(client):
    r = await client.post("/api/gdpr-redactions", json={'subject_id': 'test-subject_id', 'data_categories': [], 'redaction_scope': {}, 'merkle_before': 'test-merkle_before', 'merkle_after': 'test-merkle_after', 'integrity_preserved': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    item_id = r.json()["redaction_id"]
    r2 = await client.post(f"/api/gdpr-redactions/{item_id}/execute", json={})
    assert r2.status_code == 200
    assert r2.json()["redaction_id"] == item_id

@pytest.mark.asyncio
async def test_w104_verify_integrity(client):
    r = await client.post("/api/gdpr-redactions", json={'subject_id': 'test-subject_id', 'data_categories': [], 'redaction_scope': {}, 'merkle_before': 'test-merkle_before', 'merkle_after': 'test-merkle_after', 'integrity_preserved': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    item_id = r.json()["redaction_id"]
    r2 = await client.post(f"/api/gdpr-redactions/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["redaction_id"] == item_id

@pytest.mark.asyncio
async def test_w104_execute_redaction_not_found(client):
    r = await client.post("/api/gdpr-redactions/nonexistent-id/execute", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w104_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/gdpr-redactions", json={'subject_id': 'test-subject_id', 'data_categories': [], 'redaction_scope': {}, 'merkle_before': 'test-merkle_before', 'merkle_after': 'test-merkle_after', 'integrity_preserved': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "gdpr_redaction"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w104_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/gdpr-redactions", json={'subject_id': 'test-subject_id', 'data_categories': [], 'redaction_scope': {}, 'merkle_before': 'test-merkle_before', 'merkle_after': 'test-merkle_after', 'integrity_preserved': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/gdpr-redactions", json={'subject_id': 'test-subject_id', 'data_categories': [], 'redaction_scope': {}, 'merkle_before': 'test-merkle_before', 'merkle_after': 'test-merkle_after', 'integrity_preserved': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "redaction_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w104_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/gdpr-redactions", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w104_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/gdpr-redactions", json={'subject_id': 'test-subject_id', 'data_categories': [], 'redaction_scope': {}, 'merkle_before': 'test-merkle_before', 'merkle_after': 'test-merkle_after', 'integrity_preserved': True, 'status': 'test-status', 'redacted_at': 'test-redacted_at'})
    assert r1.status_code == 201
    item_id = r1.json()["redaction_id"]
    r2 = await client.get("/api/gdpr-redactions")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/gdpr-redactions/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["redaction_id"] == item_id
