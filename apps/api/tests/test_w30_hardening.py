"""Tests for Wave 30: Ultra-Hardening

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w30_hardening import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w30_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w30_create(client):
    r = await client.post("/api/hardening/rules", json={'rule_type': 'test-rule_type', 'name': 'test-name', 'config': {}, 'enabled': True, 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "rule_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w30_list(client):
    await client.post("/api/hardening/rules", json={'rule_type': 'test-rule_type', 'name': 'test-name', 'config': {}, 'enabled': True, 'created_at': 'test-created_at'})
    await client.post("/api/hardening/rules", json={'rule_type': 'test-rule_type', 'name': 'test-name', 'config': {}, 'enabled': True, 'created_at': 'test-created_at'})
    r = await client.get("/api/hardening/rules")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w30_get_by_id(client):
    r = await client.post("/api/hardening/rules", json={'rule_type': 'test-rule_type', 'name': 'test-name', 'config': {}, 'enabled': True, 'created_at': 'test-created_at'})
    item_id = r.json()["rule_id"]
    r2 = await client.get(f"/api/hardening/rules/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["rule_id"] == item_id

@pytest.mark.asyncio
async def test_w30_get_not_found(client):
    r = await client.get("/api/hardening/rules/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w30_toggle(client):
    r = await client.post("/api/hardening/rules", json={'rule_type': 'test-rule_type', 'name': 'test-name', 'config': {}, 'enabled': True, 'created_at': 'test-created_at'})
    item_id = r.json()["rule_id"]
    r2 = await client.post(f"/api/hardening/rules/{item_id}/toggle", json={})
    assert r2.status_code == 200
    assert r2.json()["rule_id"] == item_id

@pytest.mark.asyncio
async def test_w30_toggle_not_found(client):
    r = await client.post("/api/hardening/rules/nonexistent-id/toggle", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w30_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/hardening/rules", json={'rule_type': 'test-rule_type', 'name': 'test-name', 'config': {}, 'enabled': True, 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "hardening"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w30_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/hardening/rules", json={'rule_type': 'test-rule_type', 'name': 'test-name', 'config': {}, 'enabled': True, 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/hardening/rules", json={'rule_type': 'test-rule_type', 'name': 'test-name', 'config': {}, 'enabled': True, 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "rule_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w30_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/hardening/rules", json={})
    assert r.status_code == 201
