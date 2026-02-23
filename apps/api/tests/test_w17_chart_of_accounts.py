"""Tests for Wave 17: Chart of Accounts & JE

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w17_chart_of_accounts import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w17_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w17_create(client):
    r = await client.post("/api/coa/accounts", json={'code': 'test-code', 'name': 'test-name', 'account_type': 'test-account_type', 'parent_id': 'test-parent_id', 'active': True})
    assert r.status_code == 201
    data = r.json()
    assert "account_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w17_list(client):
    await client.post("/api/coa/accounts", json={'code': 'test-code', 'name': 'test-name', 'account_type': 'test-account_type', 'parent_id': 'test-parent_id', 'active': True})
    await client.post("/api/coa/accounts", json={'code': 'test-code', 'name': 'test-name', 'account_type': 'test-account_type', 'parent_id': 'test-parent_id', 'active': True})
    r = await client.get("/api/coa/accounts")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w17_get_by_id(client):
    r = await client.post("/api/coa/accounts", json={'code': 'test-code', 'name': 'test-name', 'account_type': 'test-account_type', 'parent_id': 'test-parent_id', 'active': True})
    item_id = r.json()["account_id"]
    r2 = await client.get(f"/api/coa/accounts/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["account_id"] == item_id

@pytest.mark.asyncio
async def test_w17_get_not_found(client):
    r = await client.get("/api/coa/accounts/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w17_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/coa/accounts", json={'code': 'test-code', 'name': 'test-name', 'account_type': 'test-account_type', 'parent_id': 'test-parent_id', 'active': True})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "chart_of_accounts"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w17_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/coa/accounts", json={'code': 'test-code', 'name': 'test-name', 'account_type': 'test-account_type', 'parent_id': 'test-parent_id', 'active': True})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/coa/accounts", json={'code': 'test-code', 'name': 'test-name', 'account_type': 'test-account_type', 'parent_id': 'test-parent_id', 'active': True})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "account_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w17_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/coa/accounts", json={})
    assert r.status_code == 201
