"""Tests for Wave 190: Evidence Span Highlighter v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w190_evidence_highlighter import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w190_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w190_create(client):
    r = await client.post("/api/evidence-highlights", json={'dossier_id': 'test-dossier_id', 'doc_id': 'test-doc_id', 'page_number': 1, 'field_name': 'test-field_name', 'offset_start': 1, 'offset_end': 1, 'highlight_text': 'test-highlight_text', 'confidence': 1.0, 'deep_link': 'test-deep_link', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "highlight_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w190_list(client):
    await client.post("/api/evidence-highlights", json={'dossier_id': 'test-dossier_id', 'doc_id': 'test-doc_id', 'page_number': 1, 'field_name': 'test-field_name', 'offset_start': 1, 'offset_end': 1, 'highlight_text': 'test-highlight_text', 'confidence': 1.0, 'deep_link': 'test-deep_link', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/evidence-highlights", json={'dossier_id': 'test-dossier_id', 'doc_id': 'test-doc_id', 'page_number': 1, 'field_name': 'test-field_name', 'offset_start': 1, 'offset_end': 1, 'highlight_text': 'test-highlight_text', 'confidence': 1.0, 'deep_link': 'test-deep_link', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/evidence-highlights")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w190_get_by_id(client):
    r = await client.post("/api/evidence-highlights", json={'dossier_id': 'test-dossier_id', 'doc_id': 'test-doc_id', 'page_number': 1, 'field_name': 'test-field_name', 'offset_start': 1, 'offset_end': 1, 'highlight_text': 'test-highlight_text', 'confidence': 1.0, 'deep_link': 'test-deep_link', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["highlight_id"]
    r2 = await client.get(f"/api/evidence-highlights/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["highlight_id"] == item_id

@pytest.mark.asyncio
async def test_w190_get_not_found(client):
    r = await client.get("/api/evidence-highlights/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w190_link_to_dossier(client):
    r = await client.post("/api/evidence-highlights", json={'dossier_id': 'test-dossier_id', 'doc_id': 'test-doc_id', 'page_number': 1, 'field_name': 'test-field_name', 'offset_start': 1, 'offset_end': 1, 'highlight_text': 'test-highlight_text', 'confidence': 1.0, 'deep_link': 'test-deep_link', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["highlight_id"]
    r2 = await client.post(f"/api/evidence-highlights/{item_id}/link", json={})
    assert r2.status_code == 200
    assert r2.json()["highlight_id"] == item_id

@pytest.mark.asyncio
async def test_w190_open_deep_link(client):
    r = await client.post("/api/evidence-highlights", json={'dossier_id': 'test-dossier_id', 'doc_id': 'test-doc_id', 'page_number': 1, 'field_name': 'test-field_name', 'offset_start': 1, 'offset_end': 1, 'highlight_text': 'test-highlight_text', 'confidence': 1.0, 'deep_link': 'test-deep_link', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["highlight_id"]
    r2 = await client.post(f"/api/evidence-highlights/{item_id}/open", json={})
    assert r2.status_code == 200
    assert r2.json()["highlight_id"] == item_id

@pytest.mark.asyncio
async def test_w190_link_to_dossier_not_found(client):
    r = await client.post("/api/evidence-highlights/nonexistent-id/link", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w190_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/evidence-highlights", json={'dossier_id': 'test-dossier_id', 'doc_id': 'test-doc_id', 'page_number': 1, 'field_name': 'test-field_name', 'offset_start': 1, 'offset_end': 1, 'highlight_text': 'test-highlight_text', 'confidence': 1.0, 'deep_link': 'test-deep_link', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "evidence_highlighter"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w190_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/evidence-highlights", json={'dossier_id': 'test-dossier_id', 'doc_id': 'test-doc_id', 'page_number': 1, 'field_name': 'test-field_name', 'offset_start': 1, 'offset_end': 1, 'highlight_text': 'test-highlight_text', 'confidence': 1.0, 'deep_link': 'test-deep_link', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/evidence-highlights", json={'dossier_id': 'test-dossier_id', 'doc_id': 'test-doc_id', 'page_number': 1, 'field_name': 'test-field_name', 'offset_start': 1, 'offset_end': 1, 'highlight_text': 'test-highlight_text', 'confidence': 1.0, 'deep_link': 'test-deep_link', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "highlight_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w190_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/evidence-highlights", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w190_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/evidence-highlights", json={'dossier_id': 'test-dossier_id', 'doc_id': 'test-doc_id', 'page_number': 1, 'field_name': 'test-field_name', 'offset_start': 1, 'offset_end': 1, 'highlight_text': 'test-highlight_text', 'confidence': 1.0, 'deep_link': 'test-deep_link', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["highlight_id"]
    r2 = await client.get("/api/evidence-highlights")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/evidence-highlights/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["highlight_id"] == item_id
