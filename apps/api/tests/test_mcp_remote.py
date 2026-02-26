"""Tests for MCP Remote Server (SSE + JSON-RPC 2.0).

Tests:
  - tools/list stability (deterministic SHA-256)
  - tools/list schema validity (every tool has required fields)
  - tools/call idempotency (same args → same trace_id)
  - tools/call audit trace_id present
  - MCP SSE endpoint emits `endpoint` event
  - JSON-RPC error handling (unknown method, bad body)
  - initialize handshake
  - all 7 named tools callable

Run: cd apps/api && .venv/Scripts/python -m pytest tests/test_mcp_remote.py -v
"""
from __future__ import annotations

import json
import hashlib

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.mcp.registry import (
    TOOLS,
    call_tool,
    list_tools,
    tools_sha256,
)

client = TestClient(app, raise_server_exceptions=True)


# ── Tool Registry Unit Tests ──────────────────────────────────────────────────


class TestToolRegistry:
    def test_list_tools_returns_all_seven(self):
        tools = list_tools()
        assert len(tools) == 7

    def test_tool_names_are_stable(self):
        names = {t["name"] for t in list_tools()}
        expected = {
            "ledgerlive.cfo_story_run",
            "ledgerlive.cfo_cockpit",
            "ledgerlive.ask_race_engineer",
            "ledgerlive.race_control_status",
            "ledgerlive.court_pack_verify",
            "ledgerlive.telemetry_pack_verify",
            "ledgerlive.agent_cycle",
        }
        assert names == expected

    def test_all_tools_have_required_fields(self):
        for tool in list_tools():
            assert "name" in tool,        f"{tool} missing name"
            assert "description" in tool, f"{tool} missing description"
            assert "inputSchema" in tool, f"{tool} missing inputSchema"
            schema = tool["inputSchema"]
            assert schema.get("type") == "object", f"{tool['name']} schema type != object"
            assert "properties" in schema, f"{tool['name']} schema missing properties"

    def test_tools_sha256_stable(self):
        """SHA-256 of tools list must be identical across calls."""
        sha1 = tools_sha256()
        sha2 = tools_sha256()
        assert sha1 == sha2
        assert len(sha1) == 64  # hex SHA-256

    def test_tools_sha256_changes_if_tools_change(self):
        """Verify SHA is actually computed from tool list content."""
        payload = json.dumps(TOOLS, sort_keys=True)
        expected = hashlib.sha256(payload.encode()).hexdigest()
        assert tools_sha256() == expected


class TestToolCallIdempotency:
    """Same args → same trace_id (deterministic)."""

    @pytest.mark.parametrize("tool_name,args", [
        ("ledgerlive.cfo_story_run",         {"period_id": "2026-Q1", "mode": "full"}),
        ("ledgerlive.cfo_cockpit",           {"period_id": "2026-Q1"}),
        ("ledgerlive.ask_race_engineer",     {"question": "What is the cost cap runway?"}),
        ("ledgerlive.race_control_status",   {"include_exceptions": True}),
        ("ledgerlive.court_pack_verify",     {"period_id": "2026-Q1"}),
        ("ledgerlive.telemetry_pack_verify", {"period_id": "2026-Q1"}),
        ("ledgerlive.agent_cycle",           {"dry_run": True}),
    ])
    def test_trace_id_idempotent(self, tool_name: str, args: dict):
        r1 = call_tool(tool_name, args)
        r2 = call_tool(tool_name, args)
        assert r1["trace_id"] == r2["trace_id"], (
            f"{tool_name}: trace_id changed between identical calls"
        )

    @pytest.mark.parametrize("tool_name,args", [
        ("ledgerlive.cfo_story_run",         {}),
        ("ledgerlive.cfo_cockpit",           {}),
        ("ledgerlive.race_control_status",   {}),
        ("ledgerlive.court_pack_verify",     {}),
        ("ledgerlive.telemetry_pack_verify", {}),
        ("ledgerlive.agent_cycle",           {}),
    ])
    def test_trace_id_present(self, tool_name: str, args: dict):
        result = call_tool(tool_name, args)
        assert "trace_id" in result
        assert result["trace_id"].startswith("trc-")

    def test_unknown_tool_raises_key_error(self):
        with pytest.raises(KeyError, match="Unknown tool"):
            call_tool("ledgerlive.nonexistent", {})


# ── HTTP Endpoint Tests ───────────────────────────────────────────────────────


class TestMcpMessageEndpoint:
    BASE = "/mcp/message"

    def _post(self, body: dict):
        return client.post(self.BASE, json=body)

    # initialize
    def test_initialize_returns_protocol_version(self):
        resp = self._post({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2024-11-05", "clientInfo": {}},
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 1
        result = data["result"]
        assert result["protocolVersion"] == "2024-11-05"
        assert "capabilities" in result
        assert "serverInfo" in result
        assert result["serverInfo"]["name"] == "LedgerLive Finance Close Agent"

    # tools/list
    def test_tools_list_returns_seven_tools(self):
        resp = self._post({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {},
        })
        assert resp.status_code == 200
        result = resp.json()["result"]
        assert len(result["tools"]) == 7

    def test_tools_list_is_stable(self):
        """Two calls must return identical JSON (deterministic)."""
        def _call():
            return self._post({
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/list",
                "params": {},
            }).json()

        r1 = _call()
        r2 = _call()
        # Compare sha256 reported by server
        assert r1["result"]["_meta"]["tools_sha256"] == r2["result"]["_meta"]["tools_sha256"]
        # Compare tool list directly
        assert r1["result"]["tools"] == r2["result"]["tools"]

    # tools/call
    @pytest.mark.parametrize("tool_name", [
        "ledgerlive.cfo_story_run",
        "ledgerlive.cfo_cockpit",
        "ledgerlive.ask_race_engineer",
        "ledgerlive.race_control_status",
        "ledgerlive.court_pack_verify",
        "ledgerlive.telemetry_pack_verify",
        "ledgerlive.agent_cycle",
    ])
    def test_tools_call_all_tools_succeed(self, tool_name: str):
        args = {}
        if tool_name == "ledgerlive.ask_race_engineer":
            args = {"question": "What is the runway?"}
        resp = self._post({
            "jsonrpc": "2.0",
            "id": 10,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": args},
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "result" in data, f"No result for {tool_name}: {data}"
        result = data["result"]
        assert result["isError"] is False
        assert len(result["content"]) >= 1
        assert result["content"][0]["type"] == "text"
        # Verify result payload has trace_id
        payload = json.loads(result["content"][0]["text"])
        assert "trace_id" in payload

    def test_tools_call_audit_trace_id_stable(self):
        """Same args → same trace_id in content response."""
        body = {
            "jsonrpc": "2.0",
            "id": 20,
            "method": "tools/call",
            "params": {"name": "ledgerlive.cfo_cockpit", "arguments": {"period_id": "2026-Q1"}},
        }
        r1 = self._post(body).json()
        r2 = self._post(body).json()
        t1 = r1["result"]["_meta"]["trace_id"]
        t2 = r2["result"]["_meta"]["trace_id"]
        assert t1 == t2 == r1["result"]["_meta"]["trace_id"]

    def test_tools_call_unknown_tool_returns_error(self):
        resp = self._post({
            "jsonrpc": "2.0",
            "id": 30,
            "method": "tools/call",
            "params": {"name": "ledgerlive.ghost_tool", "arguments": {}},
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "error" in data
        assert data["error"]["code"] == -32602

    def test_unknown_method_returns_method_not_found(self):
        resp = self._post({
            "jsonrpc": "2.0",
            "id": 40,
            "method": "tools/nonexistent",
            "params": {},
        })
        assert resp.status_code == 200
        assert resp.json()["error"]["code"] == -32601

    def test_bad_jsonrpc_version_returns_invalid_request(self):
        resp = self._post({
            "jsonrpc": "1.0",
            "id": 50,
            "method": "tools/list",
            "params": {},
        })
        assert resp.status_code == 200
        assert resp.json()["error"]["code"] == -32600

    def test_invalid_json_body_returns_400(self):
        resp = client.post(self.BASE, content=b"not-json", headers={"content-type": "application/json"})
        assert resp.status_code == 400

    def test_notification_returns_202(self):
        """JSON-RPC notifications have no response per spec."""
        resp = self._post({
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {},
            # No "id" field → notification
        })
        assert resp.status_code == 202

    def test_ping_method(self):
        resp = self._post({"jsonrpc": "2.0", "id": 99, "method": "ping", "params": {}})
        assert resp.status_code == 200
        assert resp.json()["result"] == {}


class TestMcpSseEndpoint:
    """SSE endpoint tests.

    The Starlette TestClient buffers the full response body before returning,
    so we cannot use it against a non-terminating SSE generator.
    Instead we test the generator directly as an async function (fast, precise)
    and check the HTTP headers via a capped read.
    """

    # ── generator unit tests (no HTTP round-trip) ─────────────────────────

    async def test_sse_generator_first_event_is_endpoint(self):
        """The very first yielded event must be {event: endpoint}."""
        from unittest.mock import AsyncMock, MagicMock
        from starlette.datastructures import URL
        from app.routers.mcp_remote import _sse_generator

        mock_req = MagicMock()
        mock_req.base_url = URL("http://testserver/")
        mock_req.is_disconnected = AsyncMock(return_value=False)

        events: list[dict] = []
        async for ev in _sse_generator(mock_req):
            events.append(ev)
            break  # only need the first event; aclose() is called automatically

        assert events, "Generator yielded no events"
        assert events[0]["event"] == "endpoint", f"First event was not 'endpoint': {events[0]}"

    async def test_sse_generator_endpoint_data_contains_message_url(self):
        """The endpoint event data must contain /mcp/message."""
        from unittest.mock import AsyncMock, MagicMock
        from starlette.datastructures import URL
        from app.routers.mcp_remote import _sse_generator

        mock_req = MagicMock()
        mock_req.base_url = URL("http://testserver/")
        mock_req.is_disconnected = AsyncMock(return_value=False)

        async for ev in _sse_generator(mock_req):
            assert "/mcp/message" in ev["data"], (
                f"endpoint event data does not contain /mcp/message: {ev['data']}"
            )
            break

    # ── HTTP-level header test ─────────────────────────────────────────────

    def test_sse_content_type_is_event_stream(self):
        """The /mcp/sse endpoint must be declared with EventSourceResponse
        (text/event-stream).  We check the route registration directly rather
        than making a live streaming request, which would block on the
        infinite keep-alive loop inside the TestClient.
        """
        from sse_starlette.sse import EventSourceResponse
        from app.routers.mcp_remote import router

        sse_route = next(
            (r for r in router.routes
             if getattr(r, "path", None) == "/mcp/sse"),
            None,
        )
        assert sse_route is not None, "GET /mcp/sse route not found in router"
        assert sse_route.response_class is EventSourceResponse, (
            f"Expected EventSourceResponse, got {sse_route.response_class}"
        )


class TestMcpInfoEndpoint:
    def test_mcp_info_returns_server_metadata(self):
        resp = client.get("/mcp/info")
        assert resp.status_code == 200
        data = resp.json()
        assert data["serverInfo"]["name"] == "LedgerLive Finance Close Agent"
        assert data["tool_count"] == 7
        assert data["sse_endpoint"] == "/mcp/sse"
        assert data["message_endpoint"] == "/mcp/message"
        assert len(data["tools"]) == 7
