"""MCP Remote Router — Airia-compatible SSE + JSON-RPC 2.0 transport.

Implements the Model Context Protocol (MCP) remote server spec:
  GET  /mcp/sse       → SSE stream, first event is `endpoint` with POST URL
  POST /mcp/message   → JSON-RPC 2.0 (initialize | tools/list | tools/call)

Protocol reference: https://modelcontextprotocol.io/docs/concepts/transports
Airia integration:  Tools Library → Add Remote MCP Server → paste <HOST>/mcp/sse

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, AsyncIterator

from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

from app.mcp.registry import call_tool, list_tools, tools_sha256

log = logging.getLogger(__name__)

router = APIRouter(tags=["MCP Remote"])

MCP_PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {
    "name": "LedgerLive Finance Close Agent",
    "version": "1.0.0",
}
CAPABILITIES: dict[str, Any] = {
    "tools": {},          # supports tools/list and tools/call
    "prompts": {},        # future
    "logging": {},        # future
}

# ── JSON-RPC 2.0 helpers ─────────────────────────────────────────────────────


def _ok(request_id: Any, result: Any) -> dict:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _err(request_id: Any, code: int, message: str, data: Any = None) -> dict:
    e: dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        e["data"] = data
    return {"jsonrpc": "2.0", "id": request_id, "error": e}


# ── Protocol handlers ─────────────────────────────────────────────────────────


def _handle_initialize(request_id: Any, params: dict) -> dict:
    """MCP initialize handshake."""
    return _ok(request_id, {
        "protocolVersion": MCP_PROTOCOL_VERSION,
        "capabilities": CAPABILITIES,
        "serverInfo": SERVER_INFO,
        "instructions": (
            "LedgerLive Finance Close Agent — 7 tools for F1 finance operations. "
            "Call ledgerlive.cfo_cockpit for a quick snapshot, "
            "ledgerlive.cfo_story_run for the full close pipeline."
        ),
    })


def _handle_tools_list(request_id: Any, params: dict) -> dict:
    """Return deterministic tool list for Airia discovery."""
    return _ok(request_id, {
        "tools": list_tools(),
        "_meta": {
            "tools_sha256": tools_sha256(),
            "count": len(list_tools()),
        },
    })


def _handle_tools_call(request_id: Any, params: dict) -> dict:
    """Invoke a registered tool and return MCP content response."""
    name = params.get("name", "")
    args = params.get("arguments", params.get("args", {}))
    if not name:
        return _err(request_id, -32602, "Missing required param: name")
    try:
        result = call_tool(name, args)
    except KeyError as e:
        return _err(request_id, -32602, str(e))
    except Exception as e:  # noqa: BLE001
        log.exception("Tool call failed: %s", name)
        return _err(request_id, -32603, f"Internal error: {e}")

    # Wrap result as MCP content array
    content_text = json.dumps(result, indent=2, default=str)
    return _ok(request_id, {
        "content": [{"type": "text", "text": content_text}],
        "isError": False,
        "_meta": {
            "trace_id": result.get("trace_id", ""),
            "tool": name,
        },
    })


def _dispatch(body: dict) -> dict:
    """Route a single JSON-RPC 2.0 request to the correct handler."""
    rpc_ver = body.get("jsonrpc", "")
    method  = body.get("method", "")
    req_id  = body.get("id")
    params  = body.get("params") or {}

    if rpc_ver != "2.0":
        return _err(req_id, -32600, "Invalid Request: jsonrpc must be '2.0'")

    if method == "initialize":
        return _handle_initialize(req_id, params)
    if method == "tools/list":
        return _handle_tools_list(req_id, params)
    if method == "tools/call":
        return _handle_tools_call(req_id, params)
    if method == "notifications/initialized":
        # Client acknowledgement — no response needed per MCP spec
        return None  # type: ignore[return-value]
    if method == "ping":
        return _ok(req_id, {})

    return _err(req_id, -32601, f"Method not found: {method}")


# ── SSE endpoint ─────────────────────────────────────────────────────────────


async def _sse_generator(request: Request) -> AsyncIterator[dict]:
    """Yield SSE events for the MCP SSE transport.

    First event: `endpoint` — tells the client where to POST messages.
    Then: periodic `ping` events to keep the connection alive.
    """
    # Build the base URL dynamically so it works on localhost and Heroku
    base = str(request.base_url).rstrip("/")
    message_url = f"{base}/mcp/message"

    # ── Required: endpoint event ──────────────────────────────
    yield {
        "event": "endpoint",
        "data": message_url,
    }

    # ── Keep-alive pings ──────────────────────────────────────
    # Check disconnect frequently (every 250 ms) so tests don't stall;
    # only yield a real ping every PING_INTERVAL seconds.
    PING_INTERVAL = 15.0
    CHECK_STEP = 0.25
    elapsed = 0.0
    while True:
        if await request.is_disconnected():
            break
        await asyncio.sleep(CHECK_STEP)
        elapsed += CHECK_STEP
        if elapsed >= PING_INTERVAL:
            elapsed = 0.0
            try:
                yield {
                    "event": "ping",
                    "data": json.dumps({"ts": asyncio.get_event_loop().time()}),
                }
            except Exception:
                break


@router.get(
    "/mcp/sse",
    summary="MCP SSE transport — endpoint discovery",
    description=(
        "Connect via SSE. First event is `endpoint` containing the POST URL "
        "for JSON-RPC 2.0 messages. Keep-alive pings follow every 15s."
    ),
    response_class=EventSourceResponse,
)
async def mcp_sse(request: Request):
    """Airia MCP Remote Server SSE transport.

    Airia: Tools Library → Add Remote MCP Server → paste <HOST>/mcp/sse
    """
    return EventSourceResponse(
        _sse_generator(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",        # Nginx proxy buffering off
            "Access-Control-Allow-Origin": "*",
        },
    )


# ── JSON-RPC message endpoint ─────────────────────────────────────────────────


@router.post(
    "/mcp/message",
    summary="MCP JSON-RPC 2.0 message endpoint",
    description="Accepts JSON-RPC 2.0 messages: initialize | tools/list | tools/call",
)
async def mcp_message(request: Request) -> JSONResponse:
    """Handle JSON-RPC 2.0 messages for the MCP remote server."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            _err(None, -32700, "Parse error: request body is not valid JSON"),
            status_code=400,
        )

    # Support JSON-RPC batch (array) — but Airia sends single objects
    if isinstance(body, list):
        results = [_dispatch(item) for item in body]
        results = [r for r in results if r is not None]
        return JSONResponse(results)

    result = _dispatch(body)
    if result is None:
        # Notification — no response per JSON-RPC spec
        return Response(status_code=202)

    return JSONResponse(result)


# ── Meta endpoint ─────────────────────────────────────────────────────────────


@router.get(
    "/mcp/info",
    summary="MCP server info and tool list",
)
async def mcp_info() -> dict:
    """Return server info and tool list — useful for Airia config page."""
    return {
        "protocolVersion":  MCP_PROTOCOL_VERSION,
        "serverInfo":       SERVER_INFO,
        "capabilities":     CAPABILITIES,
        "tools":            list_tools(),
        "tools_sha256":     tools_sha256(),
        "tool_count":       len(list_tools()),
        "sse_endpoint":     "/mcp/sse",
        "message_endpoint": "/mcp/message",
        "airia_integration": (
            "Tools Library → Add Remote MCP Server → paste <HOST>/mcp/sse"
        ),
    }
