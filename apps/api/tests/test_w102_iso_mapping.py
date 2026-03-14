"""Tests for Wave 102: ISO Mapping 2.0

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w102_iso_mapping import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w102_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w102_create(client):
    r = await client.post("/api/iso-mappings", json={'iso_control': 'test-iso_control', 'mapped_control_id': 'test-mapped_control_id', 'coverage_status': 'test-coverage_status', 'evidence_count': 1, 'gap_identified': True, 'status': 'test-status', 'mapped_at': 'test-mapped_at'})
    assert r.status_code == 201
    data = r.json()
    assert "mapping_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w102_list(client):
    await client.post("/api/iso-mappings", json={'iso_control': 'test-iso_control', 'mapped_control_id': 'test-mapped_control_id', 'coverage_status': 'test-coverage_status', 'evidence_count': 1, 'gap_identified': True, 'status': 'test-status', 'mapped_at': 'test-mapped_at'})
    await client.post("/api/iso-mappings", json={'iso_control': 'test-iso_control', 'mapped_control_id': 'test-mapped_control_id', 'coverage_status': 'test-coverage_status', 'evidence_count': 1, 'gap_identified': True, 'status': 'test-status', 'mapped_at': 'test-mapped_at'})
    r = await client.get("/api/iso-mappings")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w102_get_by_id(client):
    r = await client.post("/api/iso-mappings", json={'iso_control': 'test-iso_control', 'mapped_control_id': 'test-mapped_control_id', 'coverage_status': 'test-coverage_status', 'evidence_count': 1, 'gap_identified': True, 'status': 'test-status', 'mapped_at': 'test-mapped_at'})
    item_id = r.json()["mapping_id"]
    r2 = await client.get(f"/api/iso-mappings/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["mapping_id"] == item_id

@pytest.mark.asyncio
async def test_w102_get_not_found(client):
    r = await client.get("/api/iso-mappings/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w102_assess_coverage(client):
    r = await client.post("/api/iso-mappings", json={'iso_control': 'test-iso_control', 'mapped_control_id': 'test-mapped_control_id', 'coverage_status': 'test-coverage_status', 'evidence_count': 1, 'gap_identified': True, 'status': 'test-status', 'mapped_at': 'test-mapped_at'})
    item_id = r.json()["mapping_id"]
    r2 = await client.post(f"/api/iso-mappings/{item_id}/assess", json={})
    assert r2.status_code == 200
    assert r2.json()["mapping_id"] == item_id

@pytest.mark.asyncio
async def test_w102_assess_coverage_not_found(client):
    r = await client.post("/api/iso-mappings/nonexistent-id/assess", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w102_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/iso-mappings", json={'iso_control': 'test-iso_control', 'mapped_control_id': 'test-mapped_control_id', 'coverage_status': 'test-coverage_status', 'evidence_count': 1, 'gap_identified': True, 'status': 'test-status', 'mapped_at': 'test-mapped_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "iso_mapping"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w102_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/iso-mappings", json={'iso_control': 'test-iso_control', 'mapped_control_id': 'test-mapped_control_id', 'coverage_status': 'test-coverage_status', 'evidence_count': 1, 'gap_identified': True, 'status': 'test-status', 'mapped_at': 'test-mapped_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/iso-mappings", json={'iso_control': 'test-iso_control', 'mapped_control_id': 'test-mapped_control_id', 'coverage_status': 'test-coverage_status', 'evidence_count': 1, 'gap_identified': True, 'status': 'test-status', 'mapped_at': 'test-mapped_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "mapping_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w102_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/iso-mappings", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w102_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("/api/iso-mappings", json={'iso_control': 'test-iso_control', 'mapped_control_id': 'test-mapped_control_id', 'coverage_status': 'test-coverage_status', 'evidence_count': 1, 'gap_identified': True, 'status': 'test-status', 'mapped_at': 'test-mapped_at'})
    assert r1.status_code == 201
    item_id = r1.json()["mapping_id"]
    r2 = await client.get("/api/iso-mappings")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/iso-mappings/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["mapping_id"] == item_id
