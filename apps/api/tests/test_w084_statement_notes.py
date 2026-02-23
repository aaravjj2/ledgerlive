"""Tests for Wave 84: Statement Notes & Footnotes

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w084_statement_notes import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w084_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w084_create(client):
    r = await client.post("/api/statement-notes", json={'statement_id': 'test-statement_id', 'note_type': 'test-note_type', 'title': 'test-title', 'content': 'test-content', 'evidence_pack': [], 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "note_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w084_list(client):
    await client.post("/api/statement-notes", json={'statement_id': 'test-statement_id', 'note_type': 'test-note_type', 'title': 'test-title', 'content': 'test-content', 'evidence_pack': [], 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    await client.post("/api/statement-notes", json={'statement_id': 'test-statement_id', 'note_type': 'test-note_type', 'title': 'test-title', 'content': 'test-content', 'evidence_pack': [], 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    r = await client.get("/api/statement-notes")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w084_get_by_id(client):
    r = await client.post("/api/statement-notes", json={'statement_id': 'test-statement_id', 'note_type': 'test-note_type', 'title': 'test-title', 'content': 'test-content', 'evidence_pack': [], 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    item_id = r.json()["note_id"]
    r2 = await client.get(f"/api/statement-notes/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["note_id"] == item_id

@pytest.mark.asyncio
async def test_w084_get_not_found(client):
    r = await client.get("/api/statement-notes/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w084_attach_evidence(client):
    r = await client.post("/api/statement-notes", json={'statement_id': 'test-statement_id', 'note_type': 'test-note_type', 'title': 'test-title', 'content': 'test-content', 'evidence_pack': [], 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    item_id = r.json()["note_id"]
    r2 = await client.post(f"/api/statement-notes/{item_id}/evidence", json={})
    assert r2.status_code == 200
    assert r2.json()["note_id"] == item_id

@pytest.mark.asyncio
async def test_w084_approve_note(client):
    r = await client.post("/api/statement-notes", json={'statement_id': 'test-statement_id', 'note_type': 'test-note_type', 'title': 'test-title', 'content': 'test-content', 'evidence_pack': [], 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    item_id = r.json()["note_id"]
    r2 = await client.post(f"/api/statement-notes/{item_id}/approve", json={})
    assert r2.status_code == 200
    assert r2.json()["note_id"] == item_id

@pytest.mark.asyncio
async def test_w084_attach_evidence_not_found(client):
    r = await client.post("/api/statement-notes/nonexistent-id/evidence", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w084_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/statement-notes", json={'statement_id': 'test-statement_id', 'note_type': 'test-note_type', 'title': 'test-title', 'content': 'test-content', 'evidence_pack': [], 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "statement_notes"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w084_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/statement-notes", json={'statement_id': 'test-statement_id', 'note_type': 'test-note_type', 'title': 'test-title', 'content': 'test-content', 'evidence_pack': [], 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/statement-notes", json={'statement_id': 'test-statement_id', 'note_type': 'test-note_type', 'title': 'test-title', 'content': 'test-content', 'evidence_pack': [], 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "note_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w084_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/statement-notes", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w084_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/statement-notes", json={'statement_id': 'test-statement_id', 'note_type': 'test-note_type', 'title': 'test-title', 'content': 'test-content', 'evidence_pack': [], 'approved_by': 'test-approved_by', 'status': 'test-status', 'created_at': 'test-created_at', 'updated_at': 'test-updated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["note_id"]
    r2 = await client.get("/api/statement-notes")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/statement-notes/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["note_id"] == item_id
