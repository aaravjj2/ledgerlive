"""Tests for Wave 267: Audit Q&A Pack v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w267_audit_qa_pack import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w267_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w267_create(client):
    r = await client.post("/api/audit-qa-pack", json={'period_ref': 'test-period_ref', 'questions': [], 'answers': [], 'evidence_links': {}, 'template_version': 'test-template_version', 'completeness_pct': 1.0, 'reviewed_by': 'test-reviewed_by', 'review_status': 'test-review_status', 'content_hash': 'test-content_hash', 'portal_compatible': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "qa_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w267_list(client):
    await client.post("/api/audit-qa-pack", json={'period_ref': 'test-period_ref', 'questions': [], 'answers': [], 'evidence_links': {}, 'template_version': 'test-template_version', 'completeness_pct': 1.0, 'reviewed_by': 'test-reviewed_by', 'review_status': 'test-review_status', 'content_hash': 'test-content_hash', 'portal_compatible': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/audit-qa-pack", json={'period_ref': 'test-period_ref', 'questions': [], 'answers': [], 'evidence_links': {}, 'template_version': 'test-template_version', 'completeness_pct': 1.0, 'reviewed_by': 'test-reviewed_by', 'review_status': 'test-review_status', 'content_hash': 'test-content_hash', 'portal_compatible': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/audit-qa-pack")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w267_get_by_id(client):
    r = await client.post("/api/audit-qa-pack", json={'period_ref': 'test-period_ref', 'questions': [], 'answers': [], 'evidence_links': {}, 'template_version': 'test-template_version', 'completeness_pct': 1.0, 'reviewed_by': 'test-reviewed_by', 'review_status': 'test-review_status', 'content_hash': 'test-content_hash', 'portal_compatible': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["qa_id"]
    r2 = await client.get(f"/api/audit-qa-pack/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["qa_id"] == item_id

@pytest.mark.asyncio
async def test_w267_get_not_found(client):
    r = await client.get("/api/audit-qa-pack/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w267_add_question(client):
    r = await client.post("/api/audit-qa-pack", json={'period_ref': 'test-period_ref', 'questions': [], 'answers': [], 'evidence_links': {}, 'template_version': 'test-template_version', 'completeness_pct': 1.0, 'reviewed_by': 'test-reviewed_by', 'review_status': 'test-review_status', 'content_hash': 'test-content_hash', 'portal_compatible': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["qa_id"]
    r2 = await client.post(f"/api/audit-qa-pack/{item_id}/question", json={})
    assert r2.status_code == 200
    assert r2.json()["qa_id"] == item_id

@pytest.mark.asyncio
async def test_w267_link_evidence(client):
    r = await client.post("/api/audit-qa-pack", json={'period_ref': 'test-period_ref', 'questions': [], 'answers': [], 'evidence_links': {}, 'template_version': 'test-template_version', 'completeness_pct': 1.0, 'reviewed_by': 'test-reviewed_by', 'review_status': 'test-review_status', 'content_hash': 'test-content_hash', 'portal_compatible': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["qa_id"]
    r2 = await client.post(f"/api/audit-qa-pack/{item_id}/evidence", json={})
    assert r2.status_code == 200
    assert r2.json()["qa_id"] == item_id

@pytest.mark.asyncio
async def test_w267_add_question_not_found(client):
    r = await client.post("/api/audit-qa-pack/nonexistent-id/question", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w267_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/audit-qa-pack", json={'period_ref': 'test-period_ref', 'questions': [], 'answers': [], 'evidence_links': {}, 'template_version': 'test-template_version', 'completeness_pct': 1.0, 'reviewed_by': 'test-reviewed_by', 'review_status': 'test-review_status', 'content_hash': 'test-content_hash', 'portal_compatible': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "audit_qa_pack"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w267_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/audit-qa-pack", json={'period_ref': 'test-period_ref', 'questions': [], 'answers': [], 'evidence_links': {}, 'template_version': 'test-template_version', 'completeness_pct': 1.0, 'reviewed_by': 'test-reviewed_by', 'review_status': 'test-review_status', 'content_hash': 'test-content_hash', 'portal_compatible': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/audit-qa-pack", json={'period_ref': 'test-period_ref', 'questions': [], 'answers': [], 'evidence_links': {}, 'template_version': 'test-template_version', 'completeness_pct': 1.0, 'reviewed_by': 'test-reviewed_by', 'review_status': 'test-review_status', 'content_hash': 'test-content_hash', 'portal_compatible': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "qa_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w267_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/audit-qa-pack", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w267_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/audit-qa-pack", json={'period_ref': 'test-period_ref', 'questions': [], 'answers': [], 'evidence_links': {}, 'template_version': 'test-template_version', 'completeness_pct': 1.0, 'reviewed_by': 'test-reviewed_by', 'review_status': 'test-review_status', 'content_hash': 'test-content_hash', 'portal_compatible': True, 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["qa_id"]
    r2 = await client.get("/api/audit-qa-pack")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/audit-qa-pack/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["qa_id"] == item_id
