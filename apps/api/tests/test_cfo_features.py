"""Tests for CFO Cockpit, Scenario, Story Mode, and Agent Ask endpoints.

PROJECT_ID: LEDGERLIVE
"""
import pytest


@pytest.mark.asyncio
async def test_cfo_cockpit_returns_metrics(client):
    """GET /api/cfo/cockpit returns live finance metrics."""
    r = await client.get("/api/cfo/cockpit")
    assert r.status_code == 200
    data = r.json()

    assert "cost_cap" in data
    assert data["cost_cap"]["runway_usd"] > 0
    assert data["cost_cap"]["limit_usd"] == 135_000_000

    assert "exception_impact" in data
    assert data["exception_impact"]["saved_usd"] > 0

    assert "close_velocity" in data
    assert data["close_velocity"]["speedup_x"] > 1

    assert "cfo_summary" in data
    assert len(data["cfo_summary"]) > 20


@pytest.mark.asyncio
async def test_cfo_scenario_pack(client):
    """GET /api/cfo/scenario returns full Williams Q1 2026 pack."""
    r = await client.get("/api/cfo/scenario")
    assert r.status_code == 200
    data = r.json()

    assert data["scenario_id"] == "WILLIAMS_Q1_2026"
    assert data["team"] == "Williams Racing"
    assert len(data["invoices"]) >= 5
    assert len(data["exceptions_before"]) >= 2
    assert len(data["close_stages"]) >= 5
    assert "checksum" in data


@pytest.mark.asyncio
async def test_cfo_story_mode(client):
    """GET /api/cfo/story-mode returns guided walkthrough steps."""
    r = await client.get("/api/cfo/story-mode")
    assert r.status_code == 200
    data = r.json()

    assert data["enabled"] is True
    assert len(data["steps"]) >= 5

    # Each step has required fields
    for step in data["steps"]:
        assert "title" in step
        assert "description" in step
        assert "route" in step
        assert "testid" in step


@pytest.mark.asyncio
async def test_agent_ask_blocking(client):
    """POST /api/agent/ask returns grounded answer with citations."""
    r = await client.post("/api/agent/ask", json={
        "question": "What's blocking the close?"
    })
    assert r.status_code == 200
    data = r.json()

    assert data["intent"] == "what_is_blocking"
    assert len(data["answer"]) > 20
    assert len(data["citations"]) > 0
    assert data["model"] == "deterministic-intent-v1"


@pytest.mark.asyncio
async def test_agent_ask_cost_cap(client):
    """Agent answers cost cap questions with scenario data."""
    r = await client.post("/api/agent/ask", json={
        "question": "What is our cost cap runway?"
    })
    assert r.status_code == 200
    data = r.json()

    assert data["intent"] == "cost_cap_runway"
    assert "$3,800,000" in data["answer"]
    assert "WILLIAMS_Q1_2026" in data["citations"]


@pytest.mark.asyncio
async def test_agent_ask_intents(client):
    """GET /api/agent/ask/intents lists all supported intents."""
    r = await client.get("/api/agent/ask/intents")
    assert r.status_code == 200
    data = r.json()

    assert data["total"] >= 6
    assert len(data["intents"]) >= 6
    intent_ids = [i["id"] for i in data["intents"]]
    assert "blocking" in intent_ids
    assert "cost_cap" in intent_ids


@pytest.mark.asyncio
async def test_race_control_has_cfo_cockpit(client):
    """GET /api/race-control includes cfo_cockpit section."""
    r = await client.get("/api/race-control")
    assert r.status_code == 200
    data = r.json()

    assert "cfo_cockpit" in data
    cfo = data["cfo_cockpit"]
    assert cfo["cost_cap_runway_usd"] > 0
    assert cfo["close_speedup_x"] > 1
    assert len(cfo["cfo_summary"]) > 20
