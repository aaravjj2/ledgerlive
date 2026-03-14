#!/usr/bin/env bash
# ============================================================
# LedgerLive — Cloudflare Tunnel Demo (Linux / WSL)
# ============================================================
# Starts the backend in DEMO mode, opens a trycloudflare tunnel,
# runs the MCP smoke test, and prints the Airia paste URL.
#
# MANUAL ONLY — never called from pytest / playwright / CI.
#
# Requirements:
#   - cloudflared installed (apt / brew / manual)
#   - Python venv at /home/$USER/.venv  (or the active venv in PATH)
#
# Usage:
#   bash tools/cloudflare_tunnel_demo.sh
#   bash tools/cloudflare_tunnel_demo.sh --skip-backend   (if already running)
# ============================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API_DIR="$REPO_ROOT/apps/api"
SMOKE="$REPO_ROOT/tools/deploy/smoke_mcp.py"
BACKEND_PORT=8090
CF_LOG="/tmp/ledgerlive_cf_tunnel.log"
BACKEND_LOG="/tmp/ledgerlive_backend.log"
SKIP_BACKEND=false

# Parse flags
for arg in "$@"; do
  [[ "$arg" == "--skip-backend" ]] && SKIP_BACKEND=true
done

# Resolve Python — prefer venv in repo, then ~/.venv, then PATH
if [[ -x "$API_DIR/.venv/bin/python" ]]; then
  PYTHON="$API_DIR/.venv/bin/python"
elif [[ -x "$HOME/.venv/bin/python" ]]; then
  PYTHON="$HOME/.venv/bin/python"
else
  PYTHON="$(command -v python3)"
fi

# ── Colors ───────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
ok()  { echo -e "${GREEN}  ✓ $*${NC}"; }
warn(){ echo -e "${YELLOW}  ⚠ $*${NC}"; }
err(){ echo -e "${RED}  ✗ $*${NC}"; }
hdr(){ echo -e "${CYAN}\n$*${NC}"; }

hdr "============================================================"
hdr "  LedgerLive — Cloudflare Tunnel Demo"
hdr "============================================================"

# ── [1/5] cloudflared ────────────────────────────────────────────────────────
hdr "[1/5] cloudflared"
if ! command -v cloudflared &>/dev/null; then
  err "cloudflared not found."
  echo "  Install: sudo apt-get install cloudflared"
  echo "  Or:      brew install cloudflared"
  exit 1
fi
ok "$(cloudflared --version)"

# ── [2/5] Backend ────────────────────────────────────────────────────────────
hdr "[2/5] Backend (port $BACKEND_PORT)"
if curl -s --max-time 2 "http://127.0.0.1:$BACKEND_PORT/healthz" | grep -q '"status":"ok"'; then
  ok "Already running on :$BACKEND_PORT"
elif [[ "$SKIP_BACKEND" == "true" ]]; then
  warn "Backend not running but --skip-backend set; continuing..."
else
  echo "  Starting backend in DEMO mode..."
  cd "$API_DIR"
  APP_MODE=DEMO E2E_MODE=1 LLM_PROVIDER=DEMO SECRET_KEY=demo-secret \
    "$PYTHON" -m uvicorn app.main:app \
      --host 127.0.0.1 --port "$BACKEND_PORT" --log-level warning \
      > "$BACKEND_LOG" 2>&1 &
  BACKEND_PID=$!
  echo "  Waiting for backend (PID $BACKEND_PID)..."
  for i in $(seq 1 20); do
    sleep 1
    if curl -s --max-time 2 "http://127.0.0.1:$BACKEND_PORT/healthz" | grep -q '"status":"ok"'; then
      ok "/healthz → 200"
      break
    fi
    if [[ $i -eq 20 ]]; then
      err "Backend did not start within 20s. Check $BACKEND_LOG"
      cat "$BACKEND_LOG" | tail -20
      exit 1
    fi
  done
  cd "$REPO_ROOT"
fi

# ── [3/5] Local smoke test ───────────────────────────────────────────────────
hdr "[3/5] Local MCP smoke test"
"$PYTHON" "$SMOKE" --url "http://127.0.0.1:$BACKEND_PORT" || {
  err "Local smoke FAILED — fix MCP endpoints before tunneling."
  exit 1
}

# ── [4/5] Cloudflare tunnel ──────────────────────────────────────────────────
hdr "[4/5] Cloudflare Tunnel"

# Kill any pre-existing tunnel
pkill -f "cloudflared tunnel" 2>/dev/null || true
rm -f "$CF_LOG"

echo "  Starting tunnel → http://127.0.0.1:$BACKEND_PORT ..."
cloudflared tunnel --url "http://127.0.0.1:$BACKEND_PORT" > "$CF_LOG" 2>&1 &
CF_PID=$!

# Wait for the trycloudflare URL to appear in the log (up to 30s)
PUBLIC_URL=""
for i in $(seq 1 30); do
  sleep 1
  PUBLIC_URL="$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' "$CF_LOG" 2>/dev/null | head -1)"
  if [[ -n "$PUBLIC_URL" ]]; then break; fi
done

if [[ -z "$PUBLIC_URL" ]]; then
  err "Tunnel URL not captured after 30s. Check $CF_LOG"
  cat "$CF_LOG" | tail -20
  exit 1
fi
ok "Tunnel URL: $PUBLIC_URL"

# Give tunnel a moment to warm up
sleep 3

# ── [5/5] Smoke test against public URL ─────────────────────────────────────
hdr "[5/5] Public URL smoke test"
"$PYTHON" "$SMOKE" --url "$PUBLIC_URL" || {
  err "Public smoke FAILED."
  exit 1
}

# ── Output ───────────────────────────────────────────────────────────────────
MCP_SSE_URL="$PUBLIC_URL/mcp/sse"

echo ""
echo -e "${CYAN}============================================================${NC}"
echo -e "${GREEN}  DEMO READY${NC}"
echo -e "${CYAN}============================================================${NC}"
echo ""
echo -e "  ${YELLOW}Backend:${NC}      http://127.0.0.1:$BACKEND_PORT"
echo -e "  ${YELLOW}Public URL:${NC}   $PUBLIC_URL"
echo -e "  ${YELLOW}MCP SSE URL:${NC}  ${GREEN}$MCP_SSE_URL${NC}"
echo ""
echo -e "${CYAN}  ── Airia UI Steps ──────────────────────────────────────────${NC}"
echo "  1. Open Airia → Tools Library"
echo "  2. Click \"Add Remote MCP Server\""
echo -e "  3. Paste: ${GREEN}$MCP_SSE_URL${NC}"
echo "  4. Click \"Connect / Discover Tools\""
echo "  5. Confirm 7 tools named  ledgerlive.*  appear"
echo "  6. Click Save"
echo ""
echo -e "${CYAN}  ── Agent Build (Williams CFO Race Control) ─────────────────${NC}"
echo "  In Agent Studio → New Agent → \"Williams CFO Race Control Agent\""
echo "  Add tool steps in order:"
echo "    a) ledgerlive.race_control_status"
echo "    b) ledgerlive.cfo_story_run"
echo "    c) ledgerlive.cfo_cockpit"
echo "    d) ledgerlive.court_pack_verify"
echo "    e) ledgerlive.telemetry_pack_verify"
echo "    f) ledgerlive.ask_race_engineer  (question: \"What's blocking the close and why?\")"
echo "  Run test → confirm all 6 tool calls succeed."
echo ""
echo -e "${CYAN}  ── Repeat anytime ──────────────────────────────────────────${NC}"
echo "  Start backend:  cd apps/api && APP_MODE=DEMO E2E_MODE=1 LLM_PROVIDER=DEMO SECRET_KEY=demo-secret \\"
echo "                  $PYTHON -m uvicorn app.main:app --host 127.0.0.1 --port 8090"
echo "  Start tunnel:   cloudflared tunnel --url http://127.0.0.1:8090"
echo "  Smoke test:     $PYTHON tools/deploy/smoke_mcp.py --url <PUBLIC_URL>"
echo "  Open docs:      http://127.0.0.1:8090/docs"
echo ""
