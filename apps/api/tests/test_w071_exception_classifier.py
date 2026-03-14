"""Tests for Wave 71: Exception Classifier

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w071_exception_classifier import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w071_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w071_create(client):
    r = await client.post("/api/exception-classifier", json={'exception_id': 'test-exception_id', 'exception_type': 'test-exception_type', 'severity': 'test-severity', 'suggested_resolution': 'test-suggested_resolution', 'evidence_links': [], 'confidence': 1.0, 'classified_at': 'test-classified_at'})
    assert r.status_code == 201
    data = r.json()
    assert "classification_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w071_list(client):
    await client.post("/api/exception-classifier", json={'exception_id': 'test-exception_id', 'exception_type': 'test-exception_type', 'severity': 'test-severity', 'suggested_resolution': 'test-suggested_resolution', 'evidence_links': [], 'confidence': 1.0, 'classified_at': 'test-classified_at'})
    await client.post("/api/exception-classifier", json={'exception_id': 'test-exception_id', 'exception_type': 'test-exception_type', 'severity': 'test-severity', 'suggested_resolution': 'test-suggested_resolution', 'evidence_links': [], 'confidence': 1.0, 'classified_at': 'test-classified_at'})
    r = await client.get("/api/exception-classifier")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w071_get_by_id(client):
    r = await client.post("/api/exception-classifier", json={'exception_id': 'test-exception_id', 'exception_type': 'test-exception_type', 'severity': 'test-severity', 'suggested_resolution': 'test-suggested_resolution', 'evidence_links': [], 'confidence': 1.0, 'classified_at': 'test-classified_at'})
    item_id = r.json()["classification_id"]
    r2 = await client.get(f"/api/exception-classifier/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["classification_id"] == item_id

@pytest.mark.asyncio
async def test_w071_get_not_found(client):
    r = await client.get("/api/exception-classifier/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w071_suggest_fix(client):
    r = await client.post("/api/exception-classifier", json={'exception_id': 'test-exception_id', 'exception_type': 'test-exception_type', 'severity': 'test-severity', 'suggested_resolution': 'test-suggested_resolution', 'evidence_links': [], 'confidence': 1.0, 'classified_at': 'test-classified_at'})
    item_id = r.json()["classification_id"]
    r2 = await client.post(f"/api/exception-classifier/{item_id}/suggest", json={})
    assert r2.status_code == 200
    assert r2.json()["classification_id"] == item_id

@pytest.mark.asyncio
async def test_w071_apply_suggestion(client):
    r = await client.post("/api/exception-classifier", json={'exception_id': 'test-exception_id', 'exception_type': 'test-exception_type', 'severity': 'test-severity', 'suggested_resolution': 'test-suggested_resolution', 'evidence_links': [], 'confidence': 1.0, 'classified_at': 'test-classified_at'})
    item_id = r.json()["classification_id"]
    r2 = await client.post(f"/api/exception-classifier/{item_id}/apply", json={})
    assert r2.status_code == 200
    assert r2.json()["classification_id"] == item_id

@pytest.mark.asyncio
async def test_w071_suggest_fix_not_found(client):
    r = await client.post("/api/exception-classifier/nonexistent-id/suggest", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w071_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/exception-classifier", json={'exception_id': 'test-exception_id', 'exception_type': 'test-exception_type', 'severity': 'test-severity', 'suggested_resolution': 'test-suggested_resolution', 'evidence_links': [], 'confidence': 1.0, 'classified_at': 'test-classified_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "exception_classifier"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w071_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/exception-classifier", json={'exception_id': 'test-exception_id', 'exception_type': 'test-exception_type', 'severity': 'test-severity', 'suggested_resolution': 'test-suggested_resolution', 'evidence_links': [], 'confidence': 1.0, 'classified_at': 'test-classified_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/exception-classifier", json={'exception_id': 'test-exception_id', 'exception_type': 'test-exception_type', 'severity': 'test-severity', 'suggested_resolution': 'test-suggested_resolution', 'evidence_links': [], 'confidence': 1.0, 'classified_at': 'test-classified_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "classification_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w071_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/exception-classifier", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w071_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/exception-classifier", json={'exception_id': 'test-exception_id', 'exception_type': 'test-exception_type', 'severity': 'test-severity', 'suggested_resolution': 'test-suggested_resolution', 'evidence_links': [], 'confidence': 1.0, 'classified_at': 'test-classified_at'})
    assert r1.status_code == 201
    item_id = r1.json()["classification_id"]
    r2 = await client.get("/api/exception-classifier")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/exception-classifier/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["classification_id"] == item_id
