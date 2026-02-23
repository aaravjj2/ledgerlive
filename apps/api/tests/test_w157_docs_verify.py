"""Tests for Wave 157: Documentation & VERIFY.md

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w157_docs_verify import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w157_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w157_create(client):
    r = await client.post("/api/docs-verify", json={'doc_type': 'test-doc_type', 'title': 'test-title', 'content_hash': 'test-content_hash', 'sections': [], 'verified': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "doc_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w157_list(client):
    await client.post("/api/docs-verify", json={'doc_type': 'test-doc_type', 'title': 'test-title', 'content_hash': 'test-content_hash', 'sections': [], 'verified': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/docs-verify", json={'doc_type': 'test-doc_type', 'title': 'test-title', 'content_hash': 'test-content_hash', 'sections': [], 'verified': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/docs-verify")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w157_get_by_id(client):
    r = await client.post("/api/docs-verify", json={'doc_type': 'test-doc_type', 'title': 'test-title', 'content_hash': 'test-content_hash', 'sections': [], 'verified': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["doc_id"]
    r2 = await client.get(f"/api/docs-verify/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["doc_id"] == item_id

@pytest.mark.asyncio
async def test_w157_get_not_found(client):
    r = await client.get("/api/docs-verify/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w157_verify_doc(client):
    r = await client.post("/api/docs-verify", json={'doc_type': 'test-doc_type', 'title': 'test-title', 'content_hash': 'test-content_hash', 'sections': [], 'verified': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["doc_id"]
    r2 = await client.post(f"/api/docs-verify/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["doc_id"] == item_id

@pytest.mark.asyncio
async def test_w157_verify_doc_not_found(client):
    r = await client.post("/api/docs-verify/nonexistent-id/verify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w157_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/docs-verify", json={'doc_type': 'test-doc_type', 'title': 'test-title', 'content_hash': 'test-content_hash', 'sections': [], 'verified': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "docs_verify"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w157_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/docs-verify", json={'doc_type': 'test-doc_type', 'title': 'test-title', 'content_hash': 'test-content_hash', 'sections': [], 'verified': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/docs-verify", json={'doc_type': 'test-doc_type', 'title': 'test-title', 'content_hash': 'test-content_hash', 'sections': [], 'verified': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "doc_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w157_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/docs-verify", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w157_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/docs-verify", json={'doc_type': 'test-doc_type', 'title': 'test-title', 'content_hash': 'test-content_hash', 'sections': [], 'verified': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["doc_id"]
    r2 = await client.get("/api/docs-verify")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/docs-verify/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["doc_id"] == item_id
