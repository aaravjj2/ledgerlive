"""Tests for Wave 254: Exfil Detector v2

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w254_exfil_detector_v2 import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w254_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w254_create(client):
    r = await client.post("/api/exfil-detector-v2", json={'content_source': 'test-content_source', 'content_type': 'test-content_type', 'scan_result': 'test-scan_result', 'threat_type': 'test-threat_type', 'confidence': 1.0, 'classification_reason': 'test-classification_reason', 'evidence_refs': [], 'blocked': True, 'remediation_steps': [], 'scan_hash': 'test-scan_hash', 'status': 'test-status', 'scanned_at': 'test-scanned_at'})
    assert r.status_code == 201
    data = r.json()
    assert "detection_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w254_list(client):
    await client.post("/api/exfil-detector-v2", json={'content_source': 'test-content_source', 'content_type': 'test-content_type', 'scan_result': 'test-scan_result', 'threat_type': 'test-threat_type', 'confidence': 1.0, 'classification_reason': 'test-classification_reason', 'evidence_refs': [], 'blocked': True, 'remediation_steps': [], 'scan_hash': 'test-scan_hash', 'status': 'test-status', 'scanned_at': 'test-scanned_at'})
    await client.post("/api/exfil-detector-v2", json={'content_source': 'test-content_source', 'content_type': 'test-content_type', 'scan_result': 'test-scan_result', 'threat_type': 'test-threat_type', 'confidence': 1.0, 'classification_reason': 'test-classification_reason', 'evidence_refs': [], 'blocked': True, 'remediation_steps': [], 'scan_hash': 'test-scan_hash', 'status': 'test-status', 'scanned_at': 'test-scanned_at'})
    r = await client.get("/api/exfil-detector-v2")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w254_get_by_id(client):
    r = await client.post("/api/exfil-detector-v2", json={'content_source': 'test-content_source', 'content_type': 'test-content_type', 'scan_result': 'test-scan_result', 'threat_type': 'test-threat_type', 'confidence': 1.0, 'classification_reason': 'test-classification_reason', 'evidence_refs': [], 'blocked': True, 'remediation_steps': [], 'scan_hash': 'test-scan_hash', 'status': 'test-status', 'scanned_at': 'test-scanned_at'})
    item_id = r.json()["detection_id"]
    r2 = await client.get(f"/api/exfil-detector-v2/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["detection_id"] == item_id

@pytest.mark.asyncio
async def test_w254_get_not_found(client):
    r = await client.get("/api/exfil-detector-v2/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w254_classify_threat(client):
    r = await client.post("/api/exfil-detector-v2", json={'content_source': 'test-content_source', 'content_type': 'test-content_type', 'scan_result': 'test-scan_result', 'threat_type': 'test-threat_type', 'confidence': 1.0, 'classification_reason': 'test-classification_reason', 'evidence_refs': [], 'blocked': True, 'remediation_steps': [], 'scan_hash': 'test-scan_hash', 'status': 'test-status', 'scanned_at': 'test-scanned_at'})
    item_id = r.json()["detection_id"]
    r2 = await client.post(f"/api/exfil-detector-v2/{item_id}/classify", json={})
    assert r2.status_code == 200
    assert r2.json()["detection_id"] == item_id

@pytest.mark.asyncio
async def test_w254_block_content(client):
    r = await client.post("/api/exfil-detector-v2", json={'content_source': 'test-content_source', 'content_type': 'test-content_type', 'scan_result': 'test-scan_result', 'threat_type': 'test-threat_type', 'confidence': 1.0, 'classification_reason': 'test-classification_reason', 'evidence_refs': [], 'blocked': True, 'remediation_steps': [], 'scan_hash': 'test-scan_hash', 'status': 'test-status', 'scanned_at': 'test-scanned_at'})
    item_id = r.json()["detection_id"]
    r2 = await client.post(f"/api/exfil-detector-v2/{item_id}/block", json={})
    assert r2.status_code == 200
    assert r2.json()["detection_id"] == item_id

@pytest.mark.asyncio
async def test_w254_classify_threat_not_found(client):
    r = await client.post("/api/exfil-detector-v2/nonexistent-id/classify", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w254_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/exfil-detector-v2", json={'content_source': 'test-content_source', 'content_type': 'test-content_type', 'scan_result': 'test-scan_result', 'threat_type': 'test-threat_type', 'confidence': 1.0, 'classification_reason': 'test-classification_reason', 'evidence_refs': [], 'blocked': True, 'remediation_steps': [], 'scan_hash': 'test-scan_hash', 'status': 'test-status', 'scanned_at': 'test-scanned_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "exfil_detector_v2"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w254_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/exfil-detector-v2", json={'content_source': 'test-content_source', 'content_type': 'test-content_type', 'scan_result': 'test-scan_result', 'threat_type': 'test-threat_type', 'confidence': 1.0, 'classification_reason': 'test-classification_reason', 'evidence_refs': [], 'blocked': True, 'remediation_steps': [], 'scan_hash': 'test-scan_hash', 'status': 'test-status', 'scanned_at': 'test-scanned_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/exfil-detector-v2", json={'content_source': 'test-content_source', 'content_type': 'test-content_type', 'scan_result': 'test-scan_result', 'threat_type': 'test-threat_type', 'confidence': 1.0, 'classification_reason': 'test-classification_reason', 'evidence_refs': [], 'blocked': True, 'remediation_steps': [], 'scan_hash': 'test-scan_hash', 'status': 'test-status', 'scanned_at': 'test-scanned_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "detection_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w254_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/exfil-detector-v2", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w254_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/exfil-detector-v2", json={'content_source': 'test-content_source', 'content_type': 'test-content_type', 'scan_result': 'test-scan_result', 'threat_type': 'test-threat_type', 'confidence': 1.0, 'classification_reason': 'test-classification_reason', 'evidence_refs': [], 'blocked': True, 'remediation_steps': [], 'scan_hash': 'test-scan_hash', 'status': 'test-status', 'scanned_at': 'test-scanned_at'})
    assert r1.status_code == 201
    item_id = r1.json()["detection_id"]
    r2 = await client.get("/api/exfil-detector-v2")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/exfil-detector-v2/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["detection_id"] == item_id
