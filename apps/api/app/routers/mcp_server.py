"""MCP Server Router — exposes LedgerLive tool registry via HTTP for Airia MCP Gateway.

Endpoints:
  GET  /api/mcp/health  → health check
  GET  /api/mcp/tools   → list all MCP tools (deterministic)
  POST /api/mcp/call    → call a tool (deterministic DEMO)
  GET  /api/mcp/config  → Airia MCP Gateway config snippet

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.mcp_server import (
    call_tool,
    generate_airia_config,
    get_server_health,
    list_tools,
)

router = APIRouter(tags=["mcp"])


class ToolCallRequest(BaseModel):
    tool_name: str
    args: dict = {}


@router.get("/api/mcp/health")
def mcp_health():
    """MCP server health check."""
    return get_server_health()


@router.get("/api/mcp/tools")
def mcp_list_tools():
    """Return all MCP tools — deterministic.

    Airia MCP Gateway calls this to discover available tools.
    SHA-256 of tools list is stable across calls.
    """
    return list_tools()


@router.post("/api/mcp/call", status_code=200)
def mcp_call_tool(body: ToolCallRequest):
    """Invoke a LedgerLive tool via MCP protocol.

    Returns deterministic DEMO response + audit event signature.
    Unknown tool name → 404.
    """
    result = call_tool(body.tool_name, body.args)
    if result.get("error"):
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/api/mcp/config")
def mcp_airia_config():
    """Generate Airia MCP Gateway config snippet.

    Returns a deterministic, import-ready config block that tells Airia
    how to connect to this MCP server. SHA-256 stable across calls.
    """
    return generate_airia_config()
