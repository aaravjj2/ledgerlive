"""LedgerLive MCP Server — exposes the LedgerLive tool registry as MCP-compatible tools.

Airia MCP Gateway can connect to this server to invoke LedgerLive finance-close tools.
ALL operations are deterministic/offline (no external calls).

PROJECT_ID: LEDGERLIVE
MCP_VERSION: 1.0
"""
from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path
from typing import Any

# ── Tool registry ─────────────────────────────────────────────────────────────

MCP_TOOLS: list[dict] = [
    {
        "name": "ledgerlive.ingest",
        "description": "Ingest and OCR-extract sub-ledger documents for the close period. "
                       "F1: sensor data arriving from the car.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "period_id": {"type": "string", "description": "Close period identifier"},
                "source": {"type": "string", "enum": ["ap", "ar", "payroll", "ic"], "description": "Document source"},
            },
            "required": ["period_id"],
        },
        "outputSchema": {
            "type": "object",
            "properties": {
                "doc_count": {"type": "integer"},
                "queue_id": {"type": "string"},
                "trace_id": {"type": "string"},
            },
        },
        "idempotency": "period_id+source",
        "airia_type": "DocumentReader",
        "f1_metaphor": "Sensor data arrives — telemetry pipeline starts",
        "approval_required": False,
        "fail_closed": True,
    },
    {
        "name": "ledgerlive.reconcile",
        "description": "Match AP invoices against AR settlements. Items within drift_threshold "
                       "are auto-approved; outliers become exceptions. F1: computing lap delta.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "period_id": {"type": "string"},
                "drift_threshold_pct": {"type": "number", "default": 0.5},
            },
            "required": ["period_id"],
        },
        "outputSchema": {
            "type": "object",
            "properties": {
                "match_count": {"type": "integer"},
                "exception_count": {"type": "integer"},
                "trace_id": {"type": "string"},
            },
        },
        "idempotency": "period_id+drift_threshold_pct",
        "airia_type": "DataMatcher",
        "f1_metaphor": "Lap delta check — within tolerance or outlier",
        "approval_required": False,
        "fail_closed": True,
    },
    {
        "name": "ledgerlive.triage",
        "description": "Classify exceptions as P1/P2/P3 and route to queues. "
                       "F1: deploying marshal flags — yellow caution, red halt.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "period_id": {"type": "string"},
                "auto_resolve_p3": {"type": "boolean", "default": True},
            },
            "required": ["period_id"],
        },
        "outputSchema": {
            "type": "object",
            "properties": {
                "p1_count": {"type": "integer"},
                "p2_count": {"type": "integer"},
                "p3_count": {"type": "integer"},
                "trace_id": {"type": "string"},
            },
        },
        "idempotency": "period_id",
        "airia_type": "Classifier",
        "f1_metaphor": "Marshal flags — yellow/red severity routing",
        "approval_required": False,
        "fail_closed": False,
    },
    {
        "name": "ledgerlive.hitl_review",
        "description": "Gate: route P1/P2 items to approver chain. Block close until cleared. "
                       "F1: pit stop — pit wall must confirm before car re-joins.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "period_id": {"type": "string"},
                "approver_group": {"type": "string", "default": "close_managers"},
                "deadline_hours": {"type": "integer", "default": 4},
            },
            "required": ["period_id"],
        },
        "outputSchema": {
            "type": "object",
            "properties": {
                "pending_count": {"type": "integer"},
                "approved_count": {"type": "integer"},
                "trace_id": {"type": "string"},
            },
        },
        "idempotency": "period_id+approver_group",
        "airia_type": "HumanInTheLoop",
        "f1_metaphor": "Pit stop — pit wall confirms before re-joining",
        "approval_required": True,
        "fail_closed": True,
    },
    {
        "name": "ledgerlive.audit_trail",
        "description": "Append immutable audit event with actor, timestamp, payload sha256. "
                       "F1: on-board data recorder — every event logged.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "event_type": {"type": "string"},
                "actor": {"type": "string"},
                "payload": {"type": "object"},
            },
            "required": ["event_type", "actor"],
        },
        "outputSchema": {
            "type": "object",
            "properties": {
                "event_id": {"type": "string"},
                "sha256": {"type": "string"},
                "trace_id": {"type": "string"},
            },
        },
        "idempotency": "event_type+actor+payload_sha256",
        "airia_type": "EventLogger",
        "f1_metaphor": "Race telemetry — every data point recorded",
        "approval_required": False,
        "fail_closed": False,
    },
    {
        "name": "ledgerlive.evidence_binder",
        "description": "Compile approved items, audit entries, assertions into signed PDF with "
                       "sha256 manifest. F1: court pack sealed for the stewards.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "period_id": {"type": "string"},
                "sign": {"type": "boolean", "default": True},
            },
            "required": ["period_id"],
        },
        "outputSchema": {
            "type": "object",
            "properties": {
                "binder_id": {"type": "string"},
                "manifest_sha256": {"type": "string"},
                "assertion_count": {"type": "integer"},
                "trace_id": {"type": "string"},
            },
        },
        "idempotency": "period_id",
        "airia_type": "DocumentWriter",
        "f1_metaphor": "Court pack — sealed for stewards audit",
        "approval_required": True,
        "fail_closed": True,
    },
    {
        "name": "ledgerlive.race_control",
        "description": "Read-only Race Control dashboard data: current stage, lap times, "
                       "incident log, approval queue status. F1: pit-wall display.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "period_id": {"type": "string"},
                "include_telemetry": {"type": "boolean", "default": False},
            },
            "required": ["period_id"],
        },
        "outputSchema": {
            "type": "object",
            "properties": {
                "current_stage": {"type": "string"},
                "lap_count": {"type": "integer"},
                "incidents_open": {"type": "integer"},
                "approvals_pending": {"type": "integer"},
                "trace_id": {"type": "string"},
            },
        },
        "idempotency": "period_id",
        "airia_type": "Dashboard",
        "f1_metaphor": "Pit wall — live race metrics and decisions",
        "approval_required": False,
        "fail_closed": False,
    },
    {
        "name": "ledgerlive.blueprint_builder",
        "description": "Generate Airia workflow blueprint from LedgerLive close definition. "
                       "Outputs import-ready JSON for Airia no-code builder.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "template": {"type": "string", "enum": ["standard", "fast", "full"], "default": "standard"},
                "include_hitl": {"type": "boolean", "default": True},
            },
        },
        "outputSchema": {
            "type": "object",
            "properties": {
                "blueprint_id": {"type": "string"},
                "blueprint_sha256": {"type": "string"},
                "step_count": {"type": "integer"},
                "trace_id": {"type": "string"},
            },
        },
        "idempotency": "template+include_hitl",
        "airia_type": "WorkflowCompiler",
        "f1_metaphor": "Race strategy — pre-planned with contingency branches",
        "approval_required": False,
        "fail_closed": False,
    },
]

MCP_SERVER_META = {
    "name": "ledgerlive-mcp",
    "version": "1.0.0",
    "protocol": "mcp/1.0",
    "description": "LedgerLive Finance-Close Agent — MCP tool server for Airia MCP Gateway",
    "transport": "http",
    "endpoint": "http://127.0.0.1:8090/api/mcp",
    "auth": "none (DEMO mode) / api-key (production)",
    "tool_count": len(MCP_TOOLS),
    "airia_compatible": True,
}

# ── Deterministic DEMO responses per tool ────────────────────────────────────

_DEMO_RESPONSES: dict[str, dict] = {
    "ledgerlive.ingest": {
        "doc_count": 42,
        "queue_id": "q-ingest-demo-0001",
        "trace_id": "tr-ingest-demo-0001",
        "status": "PASS",
        "audit_event": "mcp_tool_call",
    },
    "ledgerlive.reconcile": {
        "match_count": 38,
        "exception_count": 4,
        "trace_id": "tr-recon-demo-0001",
        "status": "PASS",
        "audit_event": "mcp_tool_call",
    },
    "ledgerlive.triage": {
        "p1_count": 1,
        "p2_count": 2,
        "p3_count": 1,
        "trace_id": "tr-triage-demo-0001",
        "status": "PASS",
        "audit_event": "mcp_tool_call",
    },
    "ledgerlive.hitl_review": {
        "pending_count": 3,
        "approved_count": 0,
        "trace_id": "tr-hitl-demo-0001",
        "status": "PENDING_APPROVAL",
        "approval_required": True,
        "audit_event": "mcp_tool_call",
    },
    "ledgerlive.audit_trail": {
        "event_id": "evt-mcp-demo-0001",
        "sha256": "a" * 64,
        "trace_id": "tr-audit-demo-0001",
        "status": "LOGGED",
        "audit_event": "mcp_tool_call",
    },
    "ledgerlive.evidence_binder": {
        "binder_id": "bind-demo-0001",
        "manifest_sha256": "b" * 64,
        "assertion_count": 12,
        "trace_id": "tr-binder-demo-0001",
        "status": "SEALED",
        "audit_event": "mcp_tool_call",
    },
    "ledgerlive.race_control": {
        "current_stage": "pit_stop_1",
        "lap_count": 3,
        "incidents_open": 1,
        "approvals_pending": 2,
        "trace_id": "tr-rc-demo-0001",
        "status": "PASS",
        "audit_event": "mcp_tool_call",
    },
    "ledgerlive.blueprint_builder": {
        "blueprint_id": "bp-demo-0001",
        "blueprint_sha256": "c" * 64,
        "step_count": 8,
        "trace_id": "tr-bp-demo-0001",
        "status": "GENERATED",
        "audit_event": "mcp_tool_call",
    },
}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


# ── Public API ────────────────────────────────────────────────────────────────

def list_tools() -> dict:
    """Return the full MCP tool registry — deterministic."""
    tools_sha256 = _sha256(_canonical_json({"tools": MCP_TOOLS}))
    return {
        "protocol": "mcp/1.0",
        "server": MCP_SERVER_META,
        "tools": MCP_TOOLS,
        "tool_count": len(MCP_TOOLS),
        "tools_sha256": tools_sha256,
    }


def call_tool(tool_name: str, args: dict | None = None) -> dict:
    """Invoke a tool by name. Returns deterministic DEMO response + audit event."""
    known = {t["name"] for t in MCP_TOOLS}
    if tool_name not in known:
        return {
            "error": f"Unknown tool: {tool_name}",
            "available_tools": sorted(known),
            "status": "FAIL",
        }
    resp = dict(_DEMO_RESPONSES.get(tool_name, {"status": "PASS"}))
    # Make audit event deterministic with sha256 of call
    call_sig = _sha256(_canonical_json({"tool": tool_name, "args": args or {}}))
    resp["call_signature"] = call_sig
    resp["tool_name"] = tool_name
    return resp


def generate_airia_config() -> dict:
    """Generate a deterministic Airia MCP Gateway config snippet."""
    config = {
        "mcp_gateway_connection": {
            "name": "LedgerLive Finance Close Agent",
            "version": "1.0.0",
            "transport": "http",
            "base_url": "http://127.0.0.1:8090/api/mcp",
            "tools_endpoint": "/tools",
            "call_endpoint": "/call",
            "auth_mode": "none",
            "tool_count": len(MCP_TOOLS),
            "tool_names": [t["name"] for t in MCP_TOOLS],
            "airia_platform_compatible": True,
            "f1_theme": "Finance close as race: pit stops, telemetry, safety cars, checkered flag",
        }
    }
    config_sha256 = _sha256(_canonical_json(config))
    return {
        "config": config,
        "config_sha256": config_sha256,
        "import_ready": True,
    }


def get_server_health() -> dict:
    """Health check for the MCP server."""
    return {
        "status": "ok",
        "server": MCP_SERVER_META["name"],
        "version": MCP_SERVER_META["version"],
        "tool_count": len(MCP_TOOLS),
        "protocol": MCP_SERVER_META["protocol"],
    }
