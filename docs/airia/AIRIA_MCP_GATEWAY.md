# LedgerLive × Airia MCP Gateway

## Overview

[Airia](https://airia.com) supports connecting to external AI tools and agents via the
**Model Context Protocol (MCP)**. LedgerLive exposes its entire finance-close tool registry
as an MCP server at `http://127.0.0.1:8090/api/mcp`.

This means an Airia workflow can invoke any LedgerLive tool — document ingest, reconciliation,
triage, HITL approval gate, audit trail, evidence binder — without custom code, using Airia's
no-code MCP Gateway connector.

---

## MCP Server Details

| Property | Value |
|----------|-------|
| Protocol | MCP/1.0 |
| Transport | HTTP |
| Base URL | `http://127.0.0.1:8090/api/mcp` |
| Tools endpoint | `GET /api/mcp/tools` |
| Call endpoint | `POST /api/mcp/call` |
| Config endpoint | `GET /api/mcp/config` |
| Tool count | 8 |
| Auth (DEMO) | None |
| Auth (production) | API key header |

---

## Available Tools

| Tool Name | F1 Metaphor | Approval Required | Fail-Closed |
|-----------|-------------|-------------------|-------------|
| `ledgerlive.ingest` | Sensor data arrives | No | Yes |
| `ledgerlive.reconcile` | Lap delta check | No | Yes |
| `ledgerlive.triage` | Marshal flags | No | No |
| `ledgerlive.hitl_review` | Pit stop gate | **Yes** | **Yes** |
| `ledgerlive.audit_trail` | Race telemetry | No | No |
| `ledgerlive.evidence_binder` | Court pack seal | **Yes** | **Yes** |
| `ledgerlive.race_control` | Pit wall display | No | No |
| `ledgerlive.blueprint_builder` | Race strategy | No | No |

---

## How Airia MCP Gateway Connects

```bash
# 1. Start LedgerLive API
cd apps/api
APP_MODE=DEMO uvicorn app.main:app --port 8090

# 2. Fetch the gateway config
curl http://127.0.0.1:8090/api/mcp/config

# 3. Import config into Airia MCP Gateway (copy the JSON block)
# Airia → Connectors → MCP Gateway → Import JSON
```

### Airia Gateway Config Snippet

```json
{
  "mcp_gateway_connection": {
    "name": "LedgerLive Finance Close Agent",
    "version": "1.0.0",
    "transport": "http",
    "base_url": "http://127.0.0.1:8090/api/mcp",
    "tools_endpoint": "/tools",
    "call_endpoint": "/call",
    "auth_mode": "none",
    "tool_count": 8,
    "airia_platform_compatible": true
  }
}
```

> **Note:** The config SHA-256 is deterministic — it does not change unless the tool registry
> changes. This makes config validation idempotent.

---

## Example: Invoking a Tool via MCP

```bash
# List all available tools
curl http://127.0.0.1:8090/api/mcp/tools | jq '.tools[].name'

# Call the reconcile tool
curl -X POST http://127.0.0.1:8090/api/mcp/call \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "ledgerlive.reconcile", "args": {"period_id": "GRC-DEMO"}}'
```

Response includes a `call_signature` (SHA-256 of tool + args) for audit trail linkage.

---

## F1 Metaphor ↔ Airia Tool Mapping

```
Qualifying lap     → ledgerlive.ingest         (collect all documents)
Formation lap      → ledgerlive.reconcile       (verify alignment before race)
Pit Stop 1         → ledgerlive.triage          (classify exceptions, deploy flags)
Safety Car 🚗     → ledgerlive.hitl_review     (approval required, fail-closed)
Pit Stop 2         → ledgerlive.audit_trail     (seal lap records)
Checkered Flag 🏁 → ledgerlive.evidence_binder (sealed court pack for stewards)
```

---

## Compatibility Report

Run the Airia compatibility report to verify MCP integration status:

```bash
curl http://127.0.0.1:8090/api/airia/compat_report | jq '.overall'
# → "PASS"
```

The report checks:
- `bundle_structure_completeness` — community bundle files present
- `tool_schemas_version_pinned` — all tools version-pinned
- `workflow_dag_valid` — workflow DAG is acyclic
- `approval_steps_present` — HITL approval gates defined
- `fail_closed_rules_present` — on_error=halt configured
- `required_outputs_present` — telemetry/court/replay/narrative documented
- `deterministic_checksums` — SHA-256 stable across runs
- `mcp_server_present` — MCP server module + router found
- `mcp_tools_match_registry` — MCP tools match bundle registry
- `mcp_config_generated` — Airia MCP Gateway config is deterministic

All 10 checks must pass for `overall: PASS`.
