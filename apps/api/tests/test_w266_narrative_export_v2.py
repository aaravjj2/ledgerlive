"""Tests for Wave 266: Narrative Export v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w266_narrative_export_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w266_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w266_create(client):
    r = await client.post("/api/narrative-export-v2", json={'period_ref': 'test-period_ref', 'sections': [], 'dossier_citations': [], 'evidence_citations': [], 'policy_event_citations': [], 'word_count': 1, 'format_version': 'test-format_version', 'render_hash': 'test-render_hash', 'stable_ordering': True, 'export_format': 'test-export_format', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "narrative_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w266_list(client):
    await client.post("/api/narrative-export-v2", json={'period_ref': 'test-period_ref', 'sections': [], 'dossier_citations': [], 'evidence_citations': [], 'policy_event_citations': [], 'word_count': 1, 'format_version': 'test-format_version', 'render_hash': 'test-render_hash', 'stable_ordering': True, 'export_format': 'test-export_format', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    await client.post("/api/narrative-export-v2", json={'period_ref': 'test-period_ref', 'sections': [], 'dossier_citations': [], 'evidence_citations': [], 'policy_event_citations': [], 'word_count': 1, 'format_version': 'test-format_version', 'render_hash': 'test-render_hash', 'stable_ordering': True, 'export_format': 'test-export_format', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    r = await client.get("/api/narrative-export-v2")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w266_get_by_id(client):
    r = await client.post("/api/narrative-export-v2", json={'period_ref': 'test-period_ref', 'sections': [], 'dossier_citations': [], 'evidence_citations': [], 'policy_event_citations': [], 'word_count': 1, 'format_version': 'test-format_version', 'render_hash': 'test-render_hash', 'stable_ordering': True, 'export_format': 'test-export_format', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["narrative_id"]
    r2 = await client.get(f"/api/narrative-export-v2/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["narrative_id"] == item_id

@pytest.mark.asyncio
async def test_w266_get_not_found(client):
    r = await client.get("/api/narrative-export-v2/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w266_add_citation(client):
    r = await client.post("/api/narrative-export-v2", json={'period_ref': 'test-period_ref', 'sections': [], 'dossier_citations': [], 'evidence_citations': [], 'policy_event_citations': [], 'word_count': 1, 'format_version': 'test-format_version', 'render_hash': 'test-render_hash', 'stable_ordering': True, 'export_format': 'test-export_format', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["narrative_id"]
    r2 = await client.post(f"/api/narrative-export-v2/{item_id}/citation", json={})
    assert r2.status_code == 200
    assert r2.json()["narrative_id"] == item_id

@pytest.mark.asyncio
async def test_w266_render_narrative(client):
    r = await client.post("/api/narrative-export-v2", json={'period_ref': 'test-period_ref', 'sections': [], 'dossier_citations': [], 'evidence_citations': [], 'policy_event_citations': [], 'word_count': 1, 'format_version': 'test-format_version', 'render_hash': 'test-render_hash', 'stable_ordering': True, 'export_format': 'test-export_format', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    item_id = r.json()["narrative_id"]
    r2 = await client.post(f"/api/narrative-export-v2/{item_id}/render", json={})
    assert r2.status_code == 200
    assert r2.json()["narrative_id"] == item_id

@pytest.mark.asyncio
async def test_w266_add_citation_not_found(client):
    r = await client.post("/api/narrative-export-v2/nonexistent-id/citation", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w266_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/narrative-export-v2", json={'period_ref': 'test-period_ref', 'sections': [], 'dossier_citations': [], 'evidence_citations': [], 'policy_event_citations': [], 'word_count': 1, 'format_version': 'test-format_version', 'render_hash': 'test-render_hash', 'stable_ordering': True, 'export_format': 'test-export_format', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "narrative_export_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w266_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/narrative-export-v2", json={'period_ref': 'test-period_ref', 'sections': [], 'dossier_citations': [], 'evidence_citations': [], 'policy_event_citations': [], 'word_count': 1, 'format_version': 'test-format_version', 'render_hash': 'test-render_hash', 'stable_ordering': True, 'export_format': 'test-export_format', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/narrative-export-v2", json={'period_ref': 'test-period_ref', 'sections': [], 'dossier_citations': [], 'evidence_citations': [], 'policy_event_citations': [], 'word_count': 1, 'format_version': 'test-format_version', 'render_hash': 'test-render_hash', 'stable_ordering': True, 'export_format': 'test-export_format', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "narrative_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w266_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/narrative-export-v2", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w266_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/narrative-export-v2", json={'period_ref': 'test-period_ref', 'sections': [], 'dossier_citations': [], 'evidence_citations': [], 'policy_event_citations': [], 'word_count': 1, 'format_version': 'test-format_version', 'render_hash': 'test-render_hash', 'stable_ordering': True, 'export_format': 'test-export_format', 'status': 'test-status', 'generated_at': 'test-generated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["narrative_id"]
    r2 = await client.get("/api/narrative-export-v2")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/narrative-export-v2/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["narrative_id"] == item_id
