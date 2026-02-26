# Deploying LedgerLive MCP Remote Server to Heroku

This guide deploys the **Airia-compatible MCP Remote Server** (SSE transport) to Heroku so Airia can reach `https://<your-app>.herokuapp.com/mcp/sse`.

---

## Prerequisites

| Tool | Version |
|------|---------|
| [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) | latest |
| Git | ≥ 2.x |
| Python (local dev) | 3.12 or 3.14 |

---

## 1 — One-time Heroku app creation

```bash
# Log in
heroku login

# Create app (choose a unique name or let Heroku generate one)
heroku create ledgerlive-mcp

# Use the heroku-24 stack (Python 3.12 supported)
heroku stack:set heroku-24 --app ledgerlive-mcp

# Set a minimal environment variable (add others as needed)
heroku config:set ENVIRONMENT=production --app ledgerlive-mcp
```

---

## 2 — Deploy

```bash
# From the repo root (branch: waves → Heroku main)
git push heroku waves:main
```

Heroku will:
1. Detect Python via `requirements.txt` at the repo root
2. Install all pinned dependencies
3. Run the `Procfile` command: `cd apps/api && uvicorn app.main:app --host=0.0.0.0 --port=$PORT`

---

## 3 — Verify the deploy

```bash
heroku open --app ledgerlive-mcp
# Should open: https://ledgerlive-mcp.herokuapp.com/docs
```

Or check logs live:
```bash
heroku logs --tail --app ledgerlive-mcp
```

---

## 4 — Smoke-test the MCP endpoints

```bash
# Run smoke tests against Heroku
python tools/deploy/smoke_mcp.py --url https://ledgerlive-mcp.herokuapp.com --verbose
```

Expected output:
```
======================================================
  LedgerLive MCP Remote — smoke test
  Target: https://ledgerlive-mcp.herokuapp.com
======================================================

[ /mcp/info ]
  [PASS] status 200
  [PASS] name field
  [PASS] protocol_version
  [PASS] tool_count == 7
...
  Results: 17/17 passed  (0 failed)
======================================================

All checks passed. ✓
```

---

## 5 — Connect to Airia

1. Log into the **Airia platform** → **Tools Library**
2. Click **Add Remote MCP Server**
3. Paste the SSE URL:
   ```
   https://ledgerlive-mcp.herokuapp.com/mcp/sse
   ```
4. Airia will send `GET /mcp/sse`, receive the `event: endpoint` handshake pointing to `/mcp/message`, then call `tools/list` to discover all 7 LedgerLive tools.
5. Agents can now invoke any tool via `POST /mcp/message` in JSON-RPC 2.0 format.

---

## Available MCP Tools

| Tool name | Description |
|-----------|-------------|
| `ledgerlive.cfo_story_run` | Run a CFO narrative report for a fiscal period |
| `ledgerlive.cfo_cockpit` | Return live CFO cockpit KPI snapshot |
| `ledgerlive.ask_race_engineer` | Query the AI Race Engineer for strategy advice |
| `ledgerlive.race_control_status` | Fetch current Race Control / safety-car status |
| `ledgerlive.court_pack_verify` | Verify a Court Pack document bundle hash |
| `ledgerlive.telemetry_pack_verify` | Verify a Telemetry Pack bundle hash |
| `ledgerlive.agent_cycle` | Trigger an explicit perceive→decide→act agent cycle |

---

## MCP Endpoint Reference

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/mcp/sse` | SSE stream — emits `event: endpoint` with POST URL |
| `POST` | `/mcp/message` | JSON-RPC 2.0 — `initialize`, `tools/list`, `tools/call` |
| `GET` | `/mcp/info` | Server metadata + tool list (human-readable) |

### Example: `tools/list`

```bash
curl -s -X POST https://ledgerlive-mcp.herokuapp.com/mcp/message \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python -m json.tool
```

### Example: `tools/call`

```bash
curl -s -X POST https://ledgerlive-mcp.herokuapp.com/mcp/message \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "ledgerlive.cfo_cockpit",
      "arguments": {}
    }
  }' | python -m json.tool
```

---

## Scaling

```bash
# Scale web dynos
heroku ps:scale web=1 --app ledgerlive-mcp

# Upgrade to Standard-1X for production load
heroku dyno:type web=standard-1x --app ledgerlive-mcp
```

---

## Redeployment

```bash
git add .
git commit -m "update: <description>"
git push heroku waves:main
```

---

## Environment Variables

| Variable | Default | Notes |
|----------|---------|-------|
| `PORT` | set by Heroku | uvicorn listens on this |
| `ENVIRONMENT` | `production` | Controls logging verbosity |
| `OPENAI_API_KEY` | *(none)* | Required for AI agent features |

Set via:
```bash
heroku config:set OPENAI_API_KEY=sk-... --app ledgerlive-mcp
```
