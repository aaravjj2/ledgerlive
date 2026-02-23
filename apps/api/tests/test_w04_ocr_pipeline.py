"""Tests for Wave 4: OCR Pipeline

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w04_ocr_pipeline import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w04_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w04_create(client):
    r = await client.post("/api/ocr-jobs", json={'doc_id': 'test-doc_id', 'status': 'test-status', 'extracted_text': 'test-extracted_text', 'confidence': 1.0, 'processed_at': 'test-processed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "ocr_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w04_list(client):
    await client.post("/api/ocr-jobs", json={'doc_id': 'test-doc_id', 'status': 'test-status', 'extracted_text': 'test-extracted_text', 'confidence': 1.0, 'processed_at': 'test-processed_at'})
    await client.post("/api/ocr-jobs", json={'doc_id': 'test-doc_id', 'status': 'test-status', 'extracted_text': 'test-extracted_text', 'confidence': 1.0, 'processed_at': 'test-processed_at'})
    r = await client.get("/api/ocr-jobs")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w04_get_by_id(client):
    r = await client.post("/api/ocr-jobs", json={'doc_id': 'test-doc_id', 'status': 'test-status', 'extracted_text': 'test-extracted_text', 'confidence': 1.0, 'processed_at': 'test-processed_at'})
    item_id = r.json()["ocr_id"]
    r2 = await client.get(f"/api/ocr-jobs/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["ocr_id"] == item_id

@pytest.mark.asyncio
async def test_w04_get_not_found(client):
    r = await client.get("/api/ocr-jobs/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w04_retry(client):
    r = await client.post("/api/ocr-jobs", json={'doc_id': 'test-doc_id', 'status': 'test-status', 'extracted_text': 'test-extracted_text', 'confidence': 1.0, 'processed_at': 'test-processed_at'})
    item_id = r.json()["ocr_id"]
    r2 = await client.post(f"/api/ocr-jobs/{item_id}/retry", json={})
    assert r2.status_code == 200
    assert r2.json()["ocr_id"] == item_id

@pytest.mark.asyncio
async def test_w04_retry_not_found(client):
    r = await client.post("/api/ocr-jobs/nonexistent-id/retry", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w04_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/ocr-jobs", json={'doc_id': 'test-doc_id', 'status': 'test-status', 'extracted_text': 'test-extracted_text', 'confidence': 1.0, 'processed_at': 'test-processed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "ocr_pipeline"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w04_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/ocr-jobs", json={'doc_id': 'test-doc_id', 'status': 'test-status', 'extracted_text': 'test-extracted_text', 'confidence': 1.0, 'processed_at': 'test-processed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/ocr-jobs", json={'doc_id': 'test-doc_id', 'status': 'test-status', 'extracted_text': 'test-extracted_text', 'confidence': 1.0, 'processed_at': 'test-processed_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "ocr_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w04_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/ocr-jobs", json={})
    assert r.status_code == 201
