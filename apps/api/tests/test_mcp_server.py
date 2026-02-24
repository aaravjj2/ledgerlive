"""Tests for MCP Server service — LedgerLive MCP tool registry.

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

import json
import pytest

from app.services.mcp_server import (
    MCP_TOOLS,
    MCP_SERVER_META,
    call_tool,
    generate_airia_config,
    get_server_health,
    list_tools,
    _sha256,
    _canonical_json,
)
from app.services.airia_bundle import BUNDLE_TOOLS


# ── Tool registry shape ────────────────────────────────────────────────────────

def test_mcp_tool_count():
    assert len(MCP_TOOLS) == 8, "MCP server must expose exactly 8 tools"


def test_mcp_tools_are_list_of_dicts():
    assert isinstance(MCP_TOOLS, list)
    for t in MCP_TOOLS:
        assert isinstance(t, dict), f"Expected dict, got {type(t)}"


def test_mcp_tool_required_fields():
    required = {"name", "description", "inputSchema", "outputSchema", "idempotency",
                "airia_type", "f1_metaphor", "approval_required", "fail_closed"}
    for t in MCP_TOOLS:
        missing = required - t.keys()
        assert not missing, f"Tool {t.get('name')} missing fields: {missing}"


def test_mcp_tool_names_start_with_ledgerlive():
    for t in MCP_TOOLS:
        assert t["name"].startswith("ledgerlive."), \
            f"Tool {t['name']} must start with 'ledgerlive.'"


def test_mcp_canonical_tool_names():
    """All expected tool names must be present."""
    names = {t["name"] for t in MCP_TOOLS}
    expected = {
        "ledgerlive.ingest", "ledgerlive.reconcile", "ledgerlive.triage",
        "ledgerlive.hitl_review", "ledgerlive.audit_trail", "ledgerlive.evidence_binder",
        "ledgerlive.race_control", "ledgerlive.blueprint_builder",
    }
    assert names == expected


def test_mcp_hitl_review_approval_required():
    """hitl_review must have approval_required=True and fail_closed=True."""
    t = next(x for x in MCP_TOOLS if x["name"] == "ledgerlive.hitl_review")
    assert t["approval_required"] is True
    assert t["fail_closed"] is True


def test_mcp_evidence_binder_fail_closed():
    t = next(x for x in MCP_TOOLS if x["name"] == "ledgerlive.evidence_binder")
    assert t["fail_closed"] is True
    assert t["approval_required"] is True


def test_mcp_tools_match_bundle_registry():
    """Every BUNDLE_TOOLS id should have a corresponding MCP tool."""
    mcp_ids = {t["name"] for t in MCP_TOOLS}
    for bt in BUNDLE_TOOLS:
        assert bt["id"] in mcp_ids, \
            f"Bundle tool {bt['id']} has no matching MCP tool"


def test_mcp_input_schemas_have_type():
    for t in MCP_TOOLS:
        schema = t.get("inputSchema", {})
        assert schema.get("type") == "object", \
            f"Tool {t['name']} inputSchema must be type=object"


def test_mcp_f1_metaphors_not_empty():
    for t in MCP_TOOLS:
        assert t.get("f1_metaphor"), f"Tool {t['name']} must have f1_metaphor"


# ── list_tools() ──────────────────────────────────────────────────────────────

def test_list_tools_returns_dict():
    result = list_tools()
    assert isinstance(result, dict)


def test_list_tools_has_required_keys():
    result = list_tools()
    for key in ("protocol", "server", "tools", "tool_count", "tools_sha256"):
        assert key in result, f"list_tools() missing key: {key}"


def test_list_tools_count():
    result = list_tools()
    assert result["tool_count"] == 8
    assert len(result["tools"]) == 8


def test_list_tools_sha256_is_64():
    result = list_tools()
    sha = result["tools_sha256"]
    assert len(sha) == 64, f"tools_sha256 must be 64-char hex, got {len(sha)}"


def test_list_tools_deterministic():
    """Two calls to list_tools() must return identical SHA-256."""
    r1 = list_tools()
    r2 = list_tools()
    assert r1["tools_sha256"] == r2["tools_sha256"]


def test_list_tools_protocol():
    result = list_tools()
    assert result["protocol"] == "mcp/1.0"


# ── call_tool() ───────────────────────────────────────────────────────────────

def test_call_tool_known_tool():
    result = call_tool("ledgerlive.ingest", {"period_id": "test"})
    assert result.get("status") == "PASS"
    assert "trace_id" in result


def test_call_tool_unknown_raises_error():
    result = call_tool("ledgerlive.nonexistent")
    assert result.get("error")
    assert "nonexistent" in result["error"]


def test_call_tool_reconcile():
    result = call_tool("ledgerlive.reconcile", {"period_id": "P1"})
    assert "match_count" in result
    assert "exception_count" in result


def test_call_tool_hitl_review_pending():
    """HITL review returns PENDING_APPROVAL (requires human action)."""
    result = call_tool("ledgerlive.hitl_review", {"period_id": "P1"})
    assert result.get("status") == "PENDING_APPROVAL"
    assert result.get("approval_required") is True


def test_call_tool_returns_call_signature():
    result = call_tool("ledgerlive.ingest", {"period_id": "test"})
    sig = result.get("call_signature")
    assert sig and len(sig) == 64, "call_signature must be 64-char sha256"


def test_call_tool_idempotent():
    """Same call args must return same call_signature."""
    a1 = call_tool("ledgerlive.reconcile", {"period_id": "P1"})
    a2 = call_tool("ledgerlive.reconcile", {"period_id": "P1"})
    assert a1["call_signature"] == a2["call_signature"]


def test_call_tool_evidence_binder_sealed():
    result = call_tool("ledgerlive.evidence_binder", {"period_id": "P1"})
    assert result.get("status") == "SEALED"
    assert "manifest_sha256" in result


def test_call_tool_audit_trail_logged():
    result = call_tool("ledgerlive.audit_trail", {
        "event_type": "test_event", "actor": "test_agent"
    })
    assert result.get("status") == "LOGGED"


def test_call_tool_all_tools_respond():
    for t in MCP_TOOLS:
        result = call_tool(t["name"], {"period_id": "P1"})
        assert "status" in result, f"Tool {t['name']} must return status"


# ── generate_airia_config() ───────────────────────────────────────────────────

def test_generate_airia_config_returns_dict():
    result = generate_airia_config()
    assert isinstance(result, dict)


def test_generate_airia_config_keys():
    result = generate_airia_config()
    for key in ("config", "config_sha256", "import_ready"):
        assert key in result, f"Missing key: {key}"


def test_generate_airia_config_sha256_64():
    result = generate_airia_config()
    assert len(result["config_sha256"]) == 64


def test_generate_airia_config_deterministic():
    r1 = generate_airia_config()
    r2 = generate_airia_config()
    assert r1["config_sha256"] == r2["config_sha256"]


def test_generate_airia_config_import_ready():
    result = generate_airia_config()
    assert result["import_ready"] is True


def test_generate_airia_config_has_tool_count():
    result = generate_airia_config()
    conn = result["config"].get("mcp_gateway_connection", {})
    assert conn.get("tool_count") == 8


def test_generate_airia_config_base_url():
    result = generate_airia_config()
    conn = result["config"].get("mcp_gateway_connection", {})
    assert "8090/api/mcp" in conn.get("base_url", "")


def test_generate_airia_config_is_airia_compatible():
    result = generate_airia_config()
    conn = result["config"].get("mcp_gateway_connection", {})
    assert conn.get("airia_platform_compatible") is True


# ── get_server_health() ───────────────────────────────────────────────────────

def test_server_health_ok():
    result = get_server_health()
    assert result["status"] == "ok"


def test_server_health_tool_count():
    result = get_server_health()
    assert result["tool_count"] == 8


def test_server_health_protocol():
    result = get_server_health()
    assert result["protocol"] == "mcp/1.0"


# ── Router-level HTTP tests ───────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_mcp_health_endpoint(client):
    r = await client.get("/api/mcp/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["tool_count"] == 8


@pytest.mark.asyncio
async def test_mcp_tools_endpoint(client):
    r = await client.get("/api/mcp/tools")
    assert r.status_code == 200
    data = r.json()
    assert data["tool_count"] == 8
    assert len(data["tools"]) == 8


@pytest.mark.asyncio
async def test_mcp_tools_deterministic(client):
    r1 = await client.get("/api/mcp/tools")
    r2 = await client.get("/api/mcp/tools")
    assert r1.json()["tools_sha256"] == r2.json()["tools_sha256"]


@pytest.mark.asyncio
async def test_mcp_call_ingest(client):
    r = await client.post("/api/mcp/call", json={"tool_name": "ledgerlive.ingest", "args": {"period_id": "P1"}})
    assert r.status_code == 200
    assert r.json()["status"] == "PASS"


@pytest.mark.asyncio
async def test_mcp_call_unknown_returns_404(client):
    r = await client.post("/api/mcp/call", json={"tool_name": "ledgerlive.bad_tool", "args": {}})
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_mcp_config_endpoint(client):
    r = await client.get("/api/mcp/config")
    assert r.status_code == 200
    data = r.json()
    assert data["import_ready"] is True
    assert len(data["config_sha256"]) == 64


@pytest.mark.asyncio
async def test_mcp_config_deterministic(client):
    r1 = await client.get("/api/mcp/config")
    r2 = await client.get("/api/mcp/config")
    assert r1.json()["config_sha256"] == r2.json()["config_sha256"]
