"""Tests for Wave 166: Agent Console UI

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w166_agent_console import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w166_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w166_create(client):
    r = await client.post("/api/agent-console", json={'session_id': 'test-session_id', 'transcript_items': [], 'tool_trace_items': [], 'verifier_items': [], 'approvals_pending': [], 'run_status': 'test-run_status', 'export_links': [], 'page_testid': 'test-page_testid', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "console_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w166_list(client):
    await client.post("/api/agent-console", json={'session_id': 'test-session_id', 'transcript_items': [], 'tool_trace_items': [], 'verifier_items': [], 'approvals_pending': [], 'run_status': 'test-run_status', 'export_links': [], 'page_testid': 'test-page_testid', 'created_at': 'test-created_at'})
    await client.post("/api/agent-console", json={'session_id': 'test-session_id', 'transcript_items': [], 'tool_trace_items': [], 'verifier_items': [], 'approvals_pending': [], 'run_status': 'test-run_status', 'export_links': [], 'page_testid': 'test-page_testid', 'created_at': 'test-created_at'})
    r = await client.get("/api/agent-console")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w166_get_by_id(client):
    r = await client.post("/api/agent-console", json={'session_id': 'test-session_id', 'transcript_items': [], 'tool_trace_items': [], 'verifier_items': [], 'approvals_pending': [], 'run_status': 'test-run_status', 'export_links': [], 'page_testid': 'test-page_testid', 'created_at': 'test-created_at'})
    item_id = r.json()["console_id"]
    r2 = await client.get(f"/api/agent-console/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["console_id"] == item_id

@pytest.mark.asyncio
async def test_w166_get_not_found(client):
    r = await client.get("/api/agent-console/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w166_refresh_console(client):
    r = await client.post("/api/agent-console", json={'session_id': 'test-session_id', 'transcript_items': [], 'tool_trace_items': [], 'verifier_items': [], 'approvals_pending': [], 'run_status': 'test-run_status', 'export_links': [], 'page_testid': 'test-page_testid', 'created_at': 'test-created_at'})
    item_id = r.json()["console_id"]
    r2 = await client.post(f"/api/agent-console/{item_id}/refresh", json={})
    assert r2.status_code == 200
    assert r2.json()["console_id"] == item_id

@pytest.mark.asyncio
async def test_w166_approve_item(client):
    r = await client.post("/api/agent-console", json={'session_id': 'test-session_id', 'transcript_items': [], 'tool_trace_items': [], 'verifier_items': [], 'approvals_pending': [], 'run_status': 'test-run_status', 'export_links': [], 'page_testid': 'test-page_testid', 'created_at': 'test-created_at'})
    item_id = r.json()["console_id"]
    r2 = await client.post(f"/api/agent-console/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["console_id"] == item_id

@pytest.mark.asyncio
async def test_w166_export_from_console(client):
    r = await client.post("/api/agent-console", json={'session_id': 'test-session_id', 'transcript_items': [], 'tool_trace_items': [], 'verifier_items': [], 'approvals_pending': [], 'run_status': 'test-run_status', 'export_links': [], 'page_testid': 'test-page_testid', 'created_at': 'test-created_at'})
    item_id = r.json()["console_id"]
    r2 = await client.post(f"/api/agent-console/{item_id}/export", json={})
    assert r2.status_code == 200
    assert r2.json()["console_id"] == item_id

@pytest.mark.asyncio
async def test_w166_refresh_console_not_found(client):
    r = await client.post("/api/agent-console/nonexistent-id/refresh", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w166_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/agent-console", json={'session_id': 'test-session_id', 'transcript_items': [], 'tool_trace_items': [], 'verifier_items': [], 'approvals_pending': [], 'run_status': 'test-run_status', 'export_links': [], 'page_testid': 'test-page_testid', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "agent_console"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w166_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/agent-console", json={'session_id': 'test-session_id', 'transcript_items': [], 'tool_trace_items': [], 'verifier_items': [], 'approvals_pending': [], 'run_status': 'test-run_status', 'export_links': [], 'page_testid': 'test-page_testid', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/agent-console", json={'session_id': 'test-session_id', 'transcript_items': [], 'tool_trace_items': [], 'verifier_items': [], 'approvals_pending': [], 'run_status': 'test-run_status', 'export_links': [], 'page_testid': 'test-page_testid', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "console_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w166_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/agent-console", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w166_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/agent-console", json={'session_id': 'test-session_id', 'transcript_items': [], 'tool_trace_items': [], 'verifier_items': [], 'approvals_pending': [], 'run_status': 'test-run_status', 'export_links': [], 'page_testid': 'test-page_testid', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["console_id"]
    r2 = await client.get("/api/agent-console")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/agent-console/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["console_id"] == item_id
