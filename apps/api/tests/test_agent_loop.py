"""Tests for Agent Loop — perceive→decide→act autonomous cycle.

Verifies that the agent loop:
- PERCEIVE: reads current state from live services
- DECIDE: produces actions with reasoning and confidence scores
- ACT: executes actions against live stores
- Full cycle returns structured trace with all three phases

PROJECT_ID: LEDGERLIVE
"""
import pytest


@pytest.mark.asyncio
async def test_agent_perceive_returns_state(client):
    """PERCEIVE phase returns structured state from all services."""
    r = await client.get("/api/agent/perceive")
    assert r.status_code == 200
    data = r.json()

    # Must have all perception sections
    assert "documents" in data
    assert "ocr" in data
    assert "reconciliations" in data
    assert "exceptions" in data
    assert "reviews" in data
    assert "workflows" in data
    assert "ts" in data

    # Each section has expected structure
    assert "total" in data["documents"]
    assert "completed" in data["ocr"]
    assert "open" in data["exceptions"]
    assert "active" in data["workflows"]


@pytest.mark.asyncio
async def test_agent_cycle_runs_full_loop(client):
    """POST /api/agent/cycle runs a full perceive→decide→act cycle."""
    r = await client.post("/api/agent/cycle")
    assert r.status_code == 201
    data = r.json()

    # Must have cycle structure
    assert "cycle_id" in data
    assert "elapsed_ms" in data
    assert "phases" in data
    assert "summary" in data
    assert "checkpoint_hash" in data

    # All three phases present
    phases = data["phases"]
    assert "perceive" in phases
    assert "decide" in phases
    assert "act" in phases

    # Decide phase has actions and reasoning
    decide = phases["decide"]
    assert "actions" in decide
    assert "reasoning_trace" in decide
    assert "actions_planned" in decide
    assert isinstance(decide["actions"], list)

    # Act phase has results
    act_phase = phases["act"]
    assert "results" in act_phase
    assert "total_actions" in act_phase
    assert "successes" in act_phase

    # Airia webhook notification is always included
    airia_actions = [a for a in decide["actions"] if a["action"] == "notify_airia"]
    assert len(airia_actions) >= 1, "Cycle must always notify Airia"


@pytest.mark.asyncio
async def test_agent_cycle_with_open_exceptions(client):
    """Agent resolves or escalates open exceptions during a cycle."""
    # Seed an open exception first
    exc_r = await client.post("/api/exceptions", json={
        "category": "timing",
        "severity": "low",
        "description": "Test timing exception for agent loop",
        "status": "open",
    })
    assert exc_r.status_code in [200, 201]

    # Run cycle — agent should plan to auto-resolve the low-severity exception
    r = await client.post("/api/agent/cycle")
    assert r.status_code == 201
    data = r.json()

    decide = data["phases"]["decide"]
    resolve_actions = [a for a in decide["actions"] if a["action"] == "auto_resolve"]

    # Should have at least one auto-resolve action
    assert len(resolve_actions) >= 1, "Agent should auto-resolve low-severity exceptions"

    # The resolve action should have reasoning and confidence
    action = resolve_actions[0]
    assert action["confidence"] >= 0.7, "Auto-resolve confidence should be >= 0.7"
    assert len(action["reasoning"]) > 10, "Must have meaningful reasoning"
    assert len(action["citations"]) > 0, "Must cite the exception ID"


@pytest.mark.asyncio
async def test_agent_cycle_history(client):
    """GET /api/agent/cycles returns cycle history."""
    # Run a cycle first
    await client.post("/api/agent/cycle")

    r = await client.get("/api/agent/cycles")
    assert r.status_code == 200
    data = r.json()
    assert "cycles" in data
    assert "total" in data
    assert data["total"] >= 1


@pytest.mark.asyncio
async def test_agent_cycle_by_id(client):
    """GET /api/agent/cycle/{id} returns specific cycle."""
    # Run a cycle
    cycle_r = await client.post("/api/agent/cycle")
    cycle_id = cycle_r.json()["cycle_id"]

    r = await client.get(f"/api/agent/cycle/{cycle_id}")
    assert r.status_code == 200
    assert r.json()["cycle_id"] == cycle_id


@pytest.mark.asyncio
async def test_agent_cycle_not_found(client):
    """GET /api/agent/cycle/{bad_id} returns 404."""
    r = await client.get("/api/agent/cycle/nonexistent-id")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_decide_escalates_high_severity(client):
    """Agent escalates high-severity exceptions instead of auto-resolving."""
    # Seed a high-severity exception
    await client.post("/api/exceptions", json={
        "category": "cost_cap_breach",
        "severity": "high",
        "description": "FX variance exceeds cost cap threshold",
        "status": "open",
    })

    r = await client.post("/api/agent/cycle")
    data = r.json()

    decide = data["phases"]["decide"]
    escalate_actions = [a for a in decide["actions"] if a["action"] == "escalate"]

    assert len(escalate_actions) >= 1, "High-severity exceptions must be escalated"
    assert escalate_actions[0]["confidence"] >= 0.85


@pytest.mark.asyncio
async def test_cycle_emits_audit_event(client):
    """Agent cycle emits an audit event."""
    await client.post("/api/agent/cycle")

    r = await client.get("/api/audit")
    data = r.json()
    events = data["events"]

    cycle_events = [e for e in events if e["action"] == "agent_cycle"]
    assert len(cycle_events) >= 1, "Agent cycle must produce audit event"
    assert "elapsed_ms" in cycle_events[0]["detail"]
