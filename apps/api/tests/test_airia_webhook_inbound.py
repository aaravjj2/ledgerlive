"""Tests for Airia Webhook Inbound — real platform integration endpoints.

Verifies that:
- Airia can trigger agent cycles via webhook
- Webhook log and stats are maintained
- Export endpoint produces Airia-compatible format

PROJECT_ID: LEDGERLIVE
"""
import pytest


@pytest.mark.asyncio
async def test_airia_webhook_trigger_cycle(client):
    """POST /api/webhook/airia with trigger_cycle runs an agent cycle."""
    r = await client.post("/api/webhook/airia", json={
        "event_type": "trigger_cycle",
        "data": {"source": "airia_test"},
    })
    assert r.status_code == 200
    data = r.json()

    assert data["status"] == "cycle_complete"
    assert "cycle_id" in data
    assert "summary" in data
    assert "event_id" in data
    assert "actions_executed" in data
    assert "successes" in data


@pytest.mark.asyncio
async def test_airia_webhook_query_state(client):
    """POST /api/webhook/airia with query_state returns perception."""
    r = await client.post("/api/webhook/airia", json={
        "event_type": "query_state",
    })
    assert r.status_code == 200
    data = r.json()

    assert data["status"] == "state_returned"
    assert "perception" in data
    assert "documents" in data["perception"]
    assert "exceptions" in data["perception"]


@pytest.mark.asyncio
async def test_airia_webhook_ping(client):
    """POST /api/webhook/airia with ping returns pong."""
    r = await client.post("/api/webhook/airia", json={
        "event_type": "ping",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "pong"
    assert data["project"] == "LEDGERLIVE"


@pytest.mark.asyncio
async def test_airia_webhook_log(client):
    """GET /api/webhook/airia/log returns inbound event history."""
    # Trigger a webhook first
    await client.post("/api/webhook/airia", json={"event_type": "ping"})

    r = await client.get("/api/webhook/airia/log")
    assert r.status_code == 200
    data = r.json()
    assert "inbound" in data
    assert "outbound" in data
    assert data["total_inbound"] >= 1


@pytest.mark.asyncio
async def test_airia_webhook_stats(client):
    """GET /api/webhook/airia/stats returns delivery statistics."""
    r = await client.get("/api/webhook/airia/stats")
    assert r.status_code == 200
    data = r.json()
    assert "inbound_total" in data
    assert "outbound" in data
    assert "integration_status" in data


@pytest.mark.asyncio
async def test_airia_export(client):
    """POST /api/webhook/airia/export produces Airia-compatible bundle."""
    # Run a cycle first to have data
    await client.post("/api/agent/cycle")

    r = await client.post("/api/webhook/airia/export", json={
        "format": "airia_v1",
        "include_traces": True,
    })
    assert r.status_code == 200
    data = r.json()

    assert data["format"] == "airia_v1"
    assert data["project"] == "LEDGERLIVE"
    assert "agent_cycles" in data
    assert "cfo_metrics" in data
    assert "webhook_stats" in data
    assert "checksum" in data
    assert "exported_at" in data


@pytest.mark.asyncio
async def test_airia_export_without_traces(client):
    """Export with include_traces=False omits cycle details."""
    r = await client.post("/api/webhook/airia/export", json={
        "format": "airia_v1",
        "include_traces": False,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["agent_cycles"] == []


@pytest.mark.asyncio
async def test_airia_webhook_emits_audit(client):
    """Webhook triggers emit audit events."""
    await client.post("/api/webhook/airia", json={"event_type": "ping"})

    r = await client.get("/api/audit")
    events = r.json()["events"]
    webhook_events = [e for e in events if e["action"] == "webhook_received"]
    assert len(webhook_events) >= 1
