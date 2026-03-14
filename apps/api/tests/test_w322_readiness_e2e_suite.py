"""Tests for Wave 322: Readiness E2E Suite v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w322_readiness_e2e_suite import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w322_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w322_create(client):
    r = await client.post("/api/readiness-e2e-suite", json={'test_name': 'test-test_name', 'bundle_generated': True, 'validation_passed': True, 'verification_passed': True, 'badge_shown': True, 'all_passed': True, 'steps_executed': [], 'execution_log': [], 'deterministic': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    assert r.status_code == 201
    data = r.json()
    assert "suite_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w322_list(client):
    await client.post("/api/readiness-e2e-suite", json={'test_name': 'test-test_name', 'bundle_generated': True, 'validation_passed': True, 'verification_passed': True, 'badge_shown': True, 'all_passed': True, 'steps_executed': [], 'execution_log': [], 'deterministic': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    await client.post("/api/readiness-e2e-suite", json={'test_name': 'test-test_name', 'bundle_generated': True, 'validation_passed': True, 'verification_passed': True, 'badge_shown': True, 'all_passed': True, 'steps_executed': [], 'execution_log': [], 'deterministic': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    r = await client.get("/api/readiness-e2e-suite")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w322_get_by_id(client):
    r = await client.post("/api/readiness-e2e-suite", json={'test_name': 'test-test_name', 'bundle_generated': True, 'validation_passed': True, 'verification_passed': True, 'badge_shown': True, 'all_passed': True, 'steps_executed': [], 'execution_log': [], 'deterministic': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    item_id = r.json()["suite_id"]
    r2 = await client.get(f"/api/readiness-e2e-suite/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["suite_id"] == item_id

@pytest.mark.asyncio
async def test_w322_get_not_found(client):
    r = await client.get("/api/readiness-e2e-suite/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w322_rerun_suite(client):
    r = await client.post("/api/readiness-e2e-suite", json={'test_name': 'test-test_name', 'bundle_generated': True, 'validation_passed': True, 'verification_passed': True, 'badge_shown': True, 'all_passed': True, 'steps_executed': [], 'execution_log': [], 'deterministic': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    item_id = r.json()["suite_id"]
    r2 = await client.post(f"/api/readiness-e2e-suite/{item_id}/rerun", json={})
    assert r2.status_code == 200
    assert r2.json()["suite_id"] == item_id

@pytest.mark.asyncio
async def test_w322_export_badge(client):
    r = await client.post("/api/readiness-e2e-suite", json={'test_name': 'test-test_name', 'bundle_generated': True, 'validation_passed': True, 'verification_passed': True, 'badge_shown': True, 'all_passed': True, 'steps_executed': [], 'execution_log': [], 'deterministic': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    item_id = r.json()["suite_id"]
    r2 = await client.post(f"/api/readiness-e2e-suite/{item_id}/badge", json={})
    assert r2.status_code == 200
    assert r2.json()["suite_id"] == item_id

@pytest.mark.asyncio
async def test_w322_rerun_suite_not_found(client):
    r = await client.post("/api/readiness-e2e-suite/nonexistent-id/rerun", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w322_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/readiness-e2e-suite", json={'test_name': 'test-test_name', 'bundle_generated': True, 'validation_passed': True, 'verification_passed': True, 'badge_shown': True, 'all_passed': True, 'steps_executed': [], 'execution_log': [], 'deterministic': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "readiness_e2e_suite"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w322_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/readiness-e2e-suite", json={'test_name': 'test-test_name', 'bundle_generated': True, 'validation_passed': True, 'verification_passed': True, 'badge_shown': True, 'all_passed': True, 'steps_executed': [], 'execution_log': [], 'deterministic': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/readiness-e2e-suite", json={'test_name': 'test-test_name', 'bundle_generated': True, 'validation_passed': True, 'verification_passed': True, 'badge_shown': True, 'all_passed': True, 'steps_executed': [], 'execution_log': [], 'deterministic': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "suite_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w322_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/readiness-e2e-suite", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w322_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/readiness-e2e-suite", json={'test_name': 'test-test_name', 'bundle_generated': True, 'validation_passed': True, 'verification_passed': True, 'badge_shown': True, 'all_passed': True, 'steps_executed': [], 'execution_log': [], 'deterministic': True, 'status': 'test-status', 'executed_at': 'test-executed_at'})
    assert r1.status_code == 201
    item_id = r1.json()["suite_id"]
    r2 = await client.get("/api/readiness-e2e-suite")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/readiness-e2e-suite/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["suite_id"] == item_id
