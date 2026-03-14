"""Tests for Wave 253: Tool Scope Matrix UI v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w253_tool_scope_matrix import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w253_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w253_create(client):
    r = await client.post("/api/tool-scope-matrix", json={'roles': [], 'tools': [], 'scope_entries': [], 'data_tiers': {}, 'approval_requirements': {}, 'coverage_pct': 1.0, 'gaps_identified': [], 'render_hash': 'test-render_hash', 'last_reviewed_by': 'test-last_reviewed_by', 'review_status': 'test-review_status', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "matrix_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w253_list(client):
    await client.post("/api/tool-scope-matrix", json={'roles': [], 'tools': [], 'scope_entries': [], 'data_tiers': {}, 'approval_requirements': {}, 'coverage_pct': 1.0, 'gaps_identified': [], 'render_hash': 'test-render_hash', 'last_reviewed_by': 'test-last_reviewed_by', 'review_status': 'test-review_status', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/tool-scope-matrix", json={'roles': [], 'tools': [], 'scope_entries': [], 'data_tiers': {}, 'approval_requirements': {}, 'coverage_pct': 1.0, 'gaps_identified': [], 'render_hash': 'test-render_hash', 'last_reviewed_by': 'test-last_reviewed_by', 'review_status': 'test-review_status', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/tool-scope-matrix")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w253_get_by_id(client):
    r = await client.post("/api/tool-scope-matrix", json={'roles': [], 'tools': [], 'scope_entries': [], 'data_tiers': {}, 'approval_requirements': {}, 'coverage_pct': 1.0, 'gaps_identified': [], 'render_hash': 'test-render_hash', 'last_reviewed_by': 'test-last_reviewed_by', 'review_status': 'test-review_status', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["matrix_id"]
    r2 = await client.get(f"/api/tool-scope-matrix/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["matrix_id"] == item_id

@pytest.mark.asyncio
async def test_w253_get_not_found(client):
    r = await client.get("/api/tool-scope-matrix/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w253_evaluate_coverage(client):
    r = await client.post("/api/tool-scope-matrix", json={'roles': [], 'tools': [], 'scope_entries': [], 'data_tiers': {}, 'approval_requirements': {}, 'coverage_pct': 1.0, 'gaps_identified': [], 'render_hash': 'test-render_hash', 'last_reviewed_by': 'test-last_reviewed_by', 'review_status': 'test-review_status', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["matrix_id"]
    r2 = await client.post(f"/api/tool-scope-matrix/{item_id}/evaluate", json={})
    assert r2.status_code == 200
    assert r2.json()["matrix_id"] == item_id

@pytest.mark.asyncio
async def test_w253_identify_gaps(client):
    r = await client.post("/api/tool-scope-matrix", json={'roles': [], 'tools': [], 'scope_entries': [], 'data_tiers': {}, 'approval_requirements': {}, 'coverage_pct': 1.0, 'gaps_identified': [], 'render_hash': 'test-render_hash', 'last_reviewed_by': 'test-last_reviewed_by', 'review_status': 'test-review_status', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["matrix_id"]
    r2 = await client.post(f"/api/tool-scope-matrix/{item_id}/gaps", json={})
    assert r2.status_code == 200
    assert r2.json()["matrix_id"] == item_id

@pytest.mark.asyncio
async def test_w253_evaluate_coverage_not_found(client):
    r = await client.post("/api/tool-scope-matrix/nonexistent-id/evaluate", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w253_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/tool-scope-matrix", json={'roles': [], 'tools': [], 'scope_entries': [], 'data_tiers': {}, 'approval_requirements': {}, 'coverage_pct': 1.0, 'gaps_identified': [], 'render_hash': 'test-render_hash', 'last_reviewed_by': 'test-last_reviewed_by', 'review_status': 'test-review_status', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "tool_scope_matrix"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w253_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/tool-scope-matrix", json={'roles': [], 'tools': [], 'scope_entries': [], 'data_tiers': {}, 'approval_requirements': {}, 'coverage_pct': 1.0, 'gaps_identified': [], 'render_hash': 'test-render_hash', 'last_reviewed_by': 'test-last_reviewed_by', 'review_status': 'test-review_status', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/tool-scope-matrix", json={'roles': [], 'tools': [], 'scope_entries': [], 'data_tiers': {}, 'approval_requirements': {}, 'coverage_pct': 1.0, 'gaps_identified': [], 'render_hash': 'test-render_hash', 'last_reviewed_by': 'test-last_reviewed_by', 'review_status': 'test-review_status', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "matrix_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w253_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/tool-scope-matrix", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w253_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/tool-scope-matrix", json={'roles': [], 'tools': [], 'scope_entries': [], 'data_tiers': {}, 'approval_requirements': {}, 'coverage_pct': 1.0, 'gaps_identified': [], 'render_hash': 'test-render_hash', 'last_reviewed_by': 'test-last_reviewed_by', 'review_status': 'test-review_status', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["matrix_id"]
    r2 = await client.get("/api/tool-scope-matrix")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/tool-scope-matrix/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["matrix_id"] == item_id
