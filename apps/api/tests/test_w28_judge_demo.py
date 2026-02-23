"""Tests for Wave 28: Judge Demo Harness

PROJECT_ID: LEDGERLIVE
"""
import pytest
from app.services.w28_judge_demo import service


@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()

def test_w28_service_starts_empty():
    assert service.count == 0

@pytest.mark.asyncio
async def test_w28_create(client):
    r = await client.post("/api/judge/evaluate", json={'input_text': 'test-input_text', 'expected': {}, 'predicted': {}, 'score': 1.0, 'verdict': 'test-verdict', 'judged_at': 'test-judged_at'})
    assert r.status_code == 201
    data = r.json()
    assert "judge_id" in data
    assert service.count == 1

@pytest.mark.asyncio
async def test_w28_list(client):
    await client.post("/api/judge/evaluate", json={'input_text': 'test-input_text', 'expected': {}, 'predicted': {}, 'score': 1.0, 'verdict': 'test-verdict', 'judged_at': 'test-judged_at'})
    await client.post("/api/judge/evaluate", json={'input_text': 'test-input_text', 'expected': {}, 'predicted': {}, 'score': 1.0, 'verdict': 'test-verdict', 'judged_at': 'test-judged_at'})
    r = await client.get("/api/judge/runs")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2

@pytest.mark.asyncio
async def test_w28_get_by_id(client):
    r = await client.post("/api/judge/evaluate", json={'input_text': 'test-input_text', 'expected': {}, 'predicted': {}, 'score': 1.0, 'verdict': 'test-verdict', 'judged_at': 'test-judged_at'})
    item_id = r.json()["judge_id"]
    r2 = await client.get(f"/api/judge/runs/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["judge_id"] == item_id

@pytest.mark.asyncio
async def test_w28_get_not_found(client):
    r = await client.get("/api/judge/runs/nonexistent-id")
    assert r.status_code == 404

@pytest.mark.asyncio
async def test_w28_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("/api/judge/evaluate", json={'input_text': 'test-input_text', 'expected': {}, 'predicted': {}, 'score': 1.0, 'verdict': 'test-verdict', 'judged_at': 'test-judged_at'})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "judge_demo"
    assert "trace_id" in event

@pytest.mark.asyncio
async def test_w28_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("/api/judge/evaluate", json={'input_text': 'test-input_text', 'expected': {}, 'predicted': {}, 'score': 1.0, 'verdict': 'test-verdict', 'judged_at': 'test-judged_at'})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("/api/judge/evaluate", json={'input_text': 'test-input_text', 'expected': {}, 'predicted': {}, 'score': 1.0, 'verdict': 'test-verdict', 'judged_at': 'test-judged_at'})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "judge_id":
            assert type(d1[k]) == type(d2[k])

@pytest.mark.asyncio
async def test_w28_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("/api/judge/evaluate", json={})
    assert r.status_code == 201
