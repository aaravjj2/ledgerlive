"""Tests for Wave 76: Reconciliation Explainability

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w076_recon_explain import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w076_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w076_create(client):
    r = await client.post("/api/recon-explain", json={'recon_id': 'test-recon_id', 'reason_dag': {}, 'evidence_pointers': [], 'confidence': 1.0, 'explanation_text': 'test-explanation_text', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r.status_code == 201
    data = r.json()
    assert "explain_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w076_list(client):
    await client.post("/api/recon-explain", json={'recon_id': 'test-recon_id', 'reason_dag': {}, 'evidence_pointers': [], 'confidence': 1.0, 'explanation_text': 'test-explanation_text', 'status': 'test-status', 'created_at': 'test-created_at'})
    await client.post("/api/recon-explain", json={'recon_id': 'test-recon_id', 'reason_dag': {}, 'evidence_pointers': [], 'confidence': 1.0, 'explanation_text': 'test-explanation_text', 'status': 'test-status', 'created_at': 'test-created_at'})
    r = await client.get("/api/recon-explain")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w076_get_by_id(client):
    r = await client.post("/api/recon-explain", json={'recon_id': 'test-recon_id', 'reason_dag': {}, 'evidence_pointers': [], 'confidence': 1.0, 'explanation_text': 'test-explanation_text', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["explain_id"]
    r2 = await client.get(f"/api/recon-explain/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["explain_id"] == item_id

@pytest.mark.asyncio
async def test_w076_get_not_found(client):
    r = await client.get("/api/recon-explain/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w076_add_evidence(client):
    r = await client.post("/api/recon-explain", json={'recon_id': 'test-recon_id', 'reason_dag': {}, 'evidence_pointers': [], 'confidence': 1.0, 'explanation_text': 'test-explanation_text', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["explain_id"]
    r2 = await client.post(f"/api/recon-explain/{item_id}/evidence", json={})
    assert r2.status_code == 200
    assert r2.json()["explain_id"] == item_id

@pytest.mark.asyncio
async def test_w076_verify_dag(client):
    r = await client.post("/api/recon-explain", json={'recon_id': 'test-recon_id', 'reason_dag': {}, 'evidence_pointers': [], 'confidence': 1.0, 'explanation_text': 'test-explanation_text', 'status': 'test-status', 'created_at': 'test-created_at'})
    item_id = r.json()["explain_id"]
    r2 = await client.post(f"/api/recon-explain/{item_id}/verify", json={})
    assert r2.status_code == 200
    assert r2.json()["explain_id"] == item_id

@pytest.mark.asyncio
async def test_w076_add_evidence_not_found(client):
    r = await client.post("/api/recon-explain/nonexistent-id/evidence", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w076_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/recon-explain", json={'recon_id': 'test-recon_id', 'reason_dag': {}, 'evidence_pointers': [], 'confidence': 1.0, 'explanation_text': 'test-explanation_text', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "recon_explain"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w076_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/recon-explain", json={'recon_id': 'test-recon_id', 'reason_dag': {}, 'evidence_pointers': [], 'confidence': 1.0, 'explanation_text': 'test-explanation_text', 'status': 'test-status', 'created_at': 'test-created_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/recon-explain", json={'recon_id': 'test-recon_id', 'reason_dag': {}, 'evidence_pointers': [], 'confidence': 1.0, 'explanation_text': 'test-explanation_text', 'status': 'test-status', 'created_at': 'test-created_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "explain_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w076_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/recon-explain", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w076_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/recon-explain", json={'recon_id': 'test-recon_id', 'reason_dag': {}, 'evidence_pointers': [], 'confidence': 1.0, 'explanation_text': 'test-explanation_text', 'status': 'test-status', 'created_at': 'test-created_at'})
    assert r1.status_code == 201
    item_id = r1.json()["explain_id"]
    r2 = await client.get("/api/recon-explain")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/recon-explain/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["explain_id"] == item_id
