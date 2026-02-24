"""Tests for Wave 310: Jira Cards in Race Control v1

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w310_jira_cards_rc import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w310_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w310_create(client):
    r = await client.post("/api/jira-cards-rc", json={'jira_issue_ref': 'test-jira_issue_ref', 'blocker_ref': 'test-blocker_ref', 'deep_link_url': 'test-deep_link_url', 'display_order': 1, 'lane_ref': 'test-lane_ref', 'severity': 'test-severity', 'linked_at': 'test-linked_at', 'is_resolved': True, 'deterministic': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    assert r.status_code == 201
    data = r.json()
    assert "card_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w310_list(client):
    await client.post("/api/jira-cards-rc", json={'jira_issue_ref': 'test-jira_issue_ref', 'blocker_ref': 'test-blocker_ref', 'deep_link_url': 'test-deep_link_url', 'display_order': 1, 'lane_ref': 'test-lane_ref', 'severity': 'test-severity', 'linked_at': 'test-linked_at', 'is_resolved': True, 'deterministic': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    await client.post("/api/jira-cards-rc", json={'jira_issue_ref': 'test-jira_issue_ref', 'blocker_ref': 'test-blocker_ref', 'deep_link_url': 'test-deep_link_url', 'display_order': 1, 'lane_ref': 'test-lane_ref', 'severity': 'test-severity', 'linked_at': 'test-linked_at', 'is_resolved': True, 'deterministic': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    r = await client.get("/api/jira-cards-rc")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w310_get_by_id(client):
    r = await client.post("/api/jira-cards-rc", json={'jira_issue_ref': 'test-jira_issue_ref', 'blocker_ref': 'test-blocker_ref', 'deep_link_url': 'test-deep_link_url', 'display_order': 1, 'lane_ref': 'test-lane_ref', 'severity': 'test-severity', 'linked_at': 'test-linked_at', 'is_resolved': True, 'deterministic': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    item_id = r.json()["card_id"]
    r2 = await client.get(f"/api/jira-cards-rc/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["card_id"] == item_id

@pytest.mark.asyncio
async def test_w310_get_not_found(client):
    r = await client.get("/api/jira-cards-rc/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w310_reorder_cards(client):
    r = await client.post("/api/jira-cards-rc", json={'jira_issue_ref': 'test-jira_issue_ref', 'blocker_ref': 'test-blocker_ref', 'deep_link_url': 'test-deep_link_url', 'display_order': 1, 'lane_ref': 'test-lane_ref', 'severity': 'test-severity', 'linked_at': 'test-linked_at', 'is_resolved': True, 'deterministic': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    item_id = r.json()["card_id"]
    r2 = await client.post(f"/api/jira-cards-rc/{item_id}/reorder", json={})
    assert r2.status_code == 200
    assert r2.json()["card_id"] == item_id

@pytest.mark.asyncio
async def test_w310_resolve_card(client):
    r = await client.post("/api/jira-cards-rc", json={'jira_issue_ref': 'test-jira_issue_ref', 'blocker_ref': 'test-blocker_ref', 'deep_link_url': 'test-deep_link_url', 'display_order': 1, 'lane_ref': 'test-lane_ref', 'severity': 'test-severity', 'linked_at': 'test-linked_at', 'is_resolved': True, 'deterministic': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    item_id = r.json()["card_id"]
    r2 = await client.post(f"/api/jira-cards-rc/{item_id}/resolve", json={})
    assert r2.status_code == 200
    assert r2.json()["card_id"] == item_id

@pytest.mark.asyncio
async def test_w310_reorder_cards_not_found(client):
    r = await client.post("/api/jira-cards-rc/nonexistent-id/reorder", json={})
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w310_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/jira-cards-rc", json={'jira_issue_ref': 'test-jira_issue_ref', 'blocker_ref': 'test-blocker_ref', 'deep_link_url': 'test-deep_link_url', 'display_order': 1, 'lane_ref': 'test-lane_ref', 'severity': 'test-severity', 'linked_at': 'test-linked_at', 'is_resolved': True, 'deterministic': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "jira_cards_rc"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w310_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("/api/jira-cards-rc", json={'jira_issue_ref': 'test-jira_issue_ref', 'blocker_ref': 'test-blocker_ref', 'deep_link_url': 'test-deep_link_url', 'display_order': 1, 'lane_ref': 'test-lane_ref', 'severity': 'test-severity', 'linked_at': 'test-linked_at', 'is_resolved': True, 'deterministic': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/jira-cards-rc", json={'jira_issue_ref': 'test-jira_issue_ref', 'blocker_ref': 'test-blocker_ref', 'deep_link_url': 'test-deep_link_url', 'display_order': 1, 'lane_ref': 'test-lane_ref', 'severity': 'test-severity', 'linked_at': 'test-linked_at', 'is_resolved': True, 'deterministic': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "card_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w310_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("/api/jira-cards-rc", json={})
    assert r.status_code == 201

@pytest.mark.asyncio
async def test_w310_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("/api/jira-cards-rc", json={'jira_issue_ref': 'test-jira_issue_ref', 'blocker_ref': 'test-blocker_ref', 'deep_link_url': 'test-deep_link_url', 'display_order': 1, 'lane_ref': 'test-lane_ref', 'severity': 'test-severity', 'linked_at': 'test-linked_at', 'is_resolved': True, 'deterministic': True, 'status': 'test-status', 'updated_at': 'test-updated_at'})
    assert r1.status_code == 201
    item_id = r1.json()["card_id"]
    r2 = await client.get("/api/jira-cards-rc")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"/api/jira-cards-rc/{item_id}")
    assert r3.status_code == 200
    assert r3.json()["card_id"] == item_id
