"""Tests for Wave 3: Document Store

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w03_document_store import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w03_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w03_create(client):
    r = await client.post("/api/documents", json={'filename': 'test-filename', 'content_hash': 'test-content_hash', 'mime_type': 'test-mime_type', 'size_bytes': 1, 'uploaded_at': 'test-uploaded_at', 'entity_id': 'test-entity_id'})
    assert r.status_code == 201
    data = r.json()
    assert "doc_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w03_list(client):
    await client.post("/api/documents", json={'filename': 'test-filename', 'content_hash': 'test-content_hash', 'mime_type': 'test-mime_type', 'size_bytes': 1, 'uploaded_at': 'test-uploaded_at', 'entity_id': 'test-entity_id'})
    await client.post("/api/documents", json={'filename': 'test-filename', 'content_hash': 'test-content_hash', 'mime_type': 'test-mime_type', 'size_bytes': 1, 'uploaded_at': 'test-uploaded_at', 'entity_id': 'test-entity_id'})
    r = await client.get("/api/documents")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w03_get_by_id(client):
    r = await client.post("/api/documents", json={'filename': 'test-filename', 'content_hash': 'test-content_hash', 'mime_type': 'test-mime_type', 'size_bytes': 1, 'uploaded_at': 'test-uploaded_at', 'entity_id': 'test-entity_id'})
    item_id = r.json()["doc_id"]
    r2 = await client.get(f"/api/documents/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["doc_id"] == item_id

@pytest.mark.asyncio
async def test_w03_get_not_found(client):
    r = await client.get("/api/documents/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w03_delete(client):
    r = await client.post("/api/documents", json={'filename': 'test-filename', 'content_hash': 'test-content_hash', 'mime_type': 'test-mime_type', 'size_bytes': 1, 'uploaded_at': 'test-uploaded_at', 'entity_id': 'test-entity_id'})
    item_id = r.json()["doc_id"]
    r2 = await client.delete(f"/api/documents/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["deleted"] is True
    assert service.count == 0

@pytest.mark.asyncio
async def test_w03_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/documents", json={'filename': 'test-filename', 'content_hash': 'test-content_hash', 'mime_type': 'test-mime_type', 'size_bytes': 1, 'uploaded_at': 'test-uploaded_at', 'entity_id': 'test-entity_id'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "document_store"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w03_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/documents", json={'filename': 'test-filename', 'content_hash': 'test-content_hash', 'mime_type': 'test-mime_type', 'size_bytes': 1, 'uploaded_at': 'test-uploaded_at', 'entity_id': 'test-entity_id'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/documents", json={'filename': 'test-filename', 'content_hash': 'test-content_hash', 'mime_type': 'test-mime_type', 'size_bytes': 1, 'uploaded_at': 'test-uploaded_at', 'entity_id': 'test-entity_id'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "doc_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w03_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/documents", json={})
    assert r.status_code == 201
