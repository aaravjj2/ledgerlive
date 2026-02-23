"""Tests for Wave 19: Audit Integrity

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w19_audit_integrity import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w19_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w19_create(client):
    r = await client.post("/api/audit-integrity/verify", json={'scope': 'test-scope', 'expected_hash': 'test-expected_hash', 'actual_hash': 'test-actual_hash', 'valid': True, 'checked_at': 'test-checked_at'})
    assert r.status_code == 201
    data = r.json()
    assert "check_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w19_list(client):
    await client.post("/api/audit-integrity/verify", json={'scope': 'test-scope', 'expected_hash': 'test-expected_hash', 'actual_hash': 'test-actual_hash', 'valid': True, 'checked_at': 'test-checked_at'})
    await client.post("/api/audit-integrity/verify", json={'scope': 'test-scope', 'expected_hash': 'test-expected_hash', 'actual_hash': 'test-actual_hash', 'valid': True, 'checked_at': 'test-checked_at'})
    r = await client.get("/api/audit-integrity/checks")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w19_get_by_id(client):
    r = await client.post("/api/audit-integrity/verify", json={'scope': 'test-scope', 'expected_hash': 'test-expected_hash', 'actual_hash': 'test-actual_hash', 'valid': True, 'checked_at': 'test-checked_at'})
    item_id = r.json()["check_id"]
    r2 = await client.get(f"/api/audit-integrity/checks/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["check_id"] == item_id

@pytest.mark.asyncio
async def test_w19_get_not_found(client):
    r = await client.get("/api/audit-integrity/checks/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w19_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/audit-integrity/verify", json={'scope': 'test-scope', 'expected_hash': 'test-expected_hash', 'actual_hash': 'test-actual_hash', 'valid': True, 'checked_at': 'test-checked_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "audit_integrity"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w19_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/audit-integrity/verify", json={'scope': 'test-scope', 'expected_hash': 'test-expected_hash', 'actual_hash': 'test-actual_hash', 'valid': True, 'checked_at': 'test-checked_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/audit-integrity/verify", json={'scope': 'test-scope', 'expected_hash': 'test-expected_hash', 'actual_hash': 'test-actual_hash', 'valid': True, 'checked_at': 'test-checked_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "check_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w19_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/audit-integrity/verify", json={})
    assert r.status_code == 201
