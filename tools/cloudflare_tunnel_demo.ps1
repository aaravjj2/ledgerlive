#Requires -Version 5.1
<#
.SYNOPSIS
    LedgerLive — Cloudflare Tunnel Demo Script

.DESCRIPTION
    Starts the LedgerLive backend in DEMO mode, launches a Cloudflare trycloudflare
    tunnel to expose it publicly, runs the MCP smoke test, and prints the Airia paste
    URL. Designed for live hackathon demos — NOT for CI.

.EXAMPLE
    .\tools\cloudflare_tunnel_demo.ps1

.NOTES
    Requirements:
      - cloudflared installed (winget install -e --id Cloudflare.cloudflared)
      - apps\api\.venv must exist (python -m venv apps\api\.venv; pip install -r requirements.txt)
    
    This script is MANUAL ONLY — never import or call from pytest/playwright.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$REPO_ROOT = Split-Path $PSScriptRoot -Parent
$API_DIR   = Join-Path $REPO_ROOT "apps\api"
$PYTHON    = Join-Path $API_DIR ".venv\Scripts\python.exe"
$SMOKE     = Join-Path $REPO_ROOT "tools\deploy\smoke_mcp.py"
$BACKEND_PORT = 8090
$TUNNEL_LOG = Join-Path $REPO_ROOT "tunnel_log.txt"

# ─── ANSI helpers ────────────────────────────────────────────────────────────
function Write-Green($msg) { Write-Host $msg -ForegroundColor Green }
function Write-Yellow($msg) { Write-Host $msg -ForegroundColor Yellow }
function Write-Red($msg) { Write-Host $msg -ForegroundColor Red }
function Write-Cyan($msg) { Write-Host $msg -ForegroundColor Cyan }

Write-Cyan "`n============================================================"
Write-Cyan "  LedgerLive — Cloudflare Tunnel Demo"
Write-Cyan "============================================================`n"

# ─── Validate cloudflared ─────────────────────────────────────────────────────
Write-Host "[1/5] Checking cloudflared..."
try {
    $cfver = & cloudflared --version 2>&1 | Select-String "cloudflared"
    Write-Green "      $cfver"
} catch {
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" +
                [System.Environment]::GetEnvironmentVariable("PATH","User")
    try {
        $cfver = & cloudflared --version 2>&1 | Select-String "cloudflared"
        Write-Green "      $cfver"
    } catch {
        Write-Red "      cloudflared not found. Install with:"
        Write-Red "      winget install -e --id Cloudflare.cloudflared"
        exit 1
    }
}

# ─── Start backend (if not running) ──────────────────────────────────────────
Write-Host "`n[2/5] Backend..."
$backendRunning = $false
try {
    $r = Invoke-WebRequest "http://127.0.0.1:$BACKEND_PORT/healthz" -UseBasicParsing -TimeoutSec 2
    if ($r.StatusCode -eq 200) {
        Write-Green "      Already running on :$BACKEND_PORT"
        $backendRunning = $true
    }
} catch { }

if (-not $backendRunning) {
    Write-Yellow "      Starting backend in DEMO mode..."
    $env:APP_MODE   = "DEMO"
    $env:E2E_MODE   = "1"
    $env:LLM_PROVIDER = "DEMO"
    $env:SECRET_KEY = "demo-secret"
    Start-Process -FilePath $PYTHON `
        -ArgumentList "-m","uvicorn","app.main:app","--host","127.0.0.1","--port",$BACKEND_PORT,"--log-level","warning" `
        -WorkingDirectory $API_DIR `
        -WindowStyle Hidden

    Write-Host "      Waiting for /healthz..."
    $ready = $false
    for ($i = 0; $i -lt 30; $i++) {
        Start-Sleep 1
        try {
            $r = Invoke-WebRequest "http://127.0.0.1:$BACKEND_PORT/healthz" -UseBasicParsing -TimeoutSec 2
            if ($r.StatusCode -eq 200) { $ready = $true; break }
        } catch { }
    }
    if (-not $ready) {
        Write-Red "      Backend did not start within 30 s. Check uvicorn logs."
        exit 1
    }
    Write-Green "      Backend ready on :$BACKEND_PORT"
}

# ─── Start Cloudflare Tunnel ──────────────────────────────────────────────────
Write-Host "`n[3/5] Starting Cloudflare Tunnel..."
if (Test-Path $TUNNEL_LOG) { Remove-Item $TUNNEL_LOG -Force }

Start-Process -FilePath "cloudflared" `
    -ArgumentList "tunnel","--url","http://127.0.0.1:$BACKEND_PORT","--no-autoupdate" `
    -RedirectStandardError $TUNNEL_LOG `
    -WindowStyle Hidden

Write-Host "      Waiting for trycloudflare URL (up to 20 s)..."
$PUBLIC_URL = $null
for ($i = 0; $i -lt 40; $i++) {
    Start-Sleep -Milliseconds 500
    if (Test-Path $TUNNEL_LOG) {
        $lines = Get-Content $TUNNEL_LOG -ErrorAction SilentlyContinue
        foreach ($line in $lines) {
            if ($line -match "https://[a-z0-9\-]+\.trycloudflare\.com") {
                $PUBLIC_URL = $Matches[0].Trim()
                break
            }
        }
    }
    if ($PUBLIC_URL) { break }
}

if (-not $PUBLIC_URL) {
    Write-Red "      Could not parse tunnel URL from cloudflared output."
    Write-Yellow "      Check: $TUNNEL_LOG"
    exit 1
}

Write-Green "      Tunnel active: $PUBLIC_URL"

# ─── Run smoke test ───────────────────────────────────────────────────────────
Write-Host "`n[4/5] Running smoke test against $PUBLIC_URL ..."
$smokeResult = & $PYTHON $SMOKE --url $PUBLIC_URL 2>&1
Write-Host $smokeResult
if ($LASTEXITCODE -ne 0) {
    Write-Red "`n      Smoke test FAILED. See output above."
    Write-Yellow "      The tunnel is still running at: $PUBLIC_URL"
} else {
    Write-Green "`n      Smoke test PASSED (0 failed)"
}

# ─── Print Airia instructions ─────────────────────────────────────────────────
Write-Cyan "`n[5/5] AIRIA INTEGRATION INSTRUCTIONS"
Write-Cyan "============================================================`n"

$MCP_SSE_URL = "$PUBLIC_URL/mcp/sse"

Write-Host @"
  ┌─── MCP Server URL (paste into Airia) ────────────────────────────┐
  │                                                                    │
  │    $MCP_SSE_URL
  │                                                                    │
  └──────────────────────────────────────────────────────────────────┘

  AIRIA UI STEPS:
  ──────────────────────────────────────────────────────────────────
  1. Open Airia → Tools Library
  2. Click "Add Remote MCP Server"
  3. Paste: $MCP_SSE_URL
  4. Click "Connect / Discover Tools"
  5. Confirm tool list shows 7 tools:
       • ledgerlive.cfo_story_run
       • ledgerlive.cfo_cockpit
       • ledgerlive.ask_race_engineer
       • ledgerlive.race_control_status
       • ledgerlive.court_pack_verify
       • ledgerlive.telemetry_pack_verify
       • ledgerlive.agent_cycle
  6. Click "Save"

  AGENT BUILD (Williams CFO Race Control Agent):
  ──────────────────────────────────────────────────────────────────
  In Agent Studio → New Agent: "Williams CFO Race Control Agent"
    Step 1: ledgerlive.race_control_status
    Step 2: ledgerlive.cfo_story_run
    Step 3: ledgerlive.cfo_cockpit
    Step 4: ledgerlive.court_pack_verify
    Step 5: ledgerlive.telemetry_pack_verify
    Step 6: ledgerlive.ask_race_engineer
              question: "What's blocking the close and why?"
  Run test → confirm all 6 tool calls succeed.

  DEMO COMMANDS (run anytime):
  ──────────────────────────────────────────────────────────────────
  # Start backend:
  cd C:\Aarav\ledgerlive\apps\api
  `$env:APP_MODE="DEMO"; `$env:LLM_PROVIDER="DEMO"; `$env:SECRET_KEY="demo-secret"
  .\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8090

  # Start tunnel (gives new URL each time):
  cloudflared tunnel --url http://127.0.0.1:8090

  # Run smoke against public URL:
  cd C:\Aarav\ledgerlive
  .venv\Scripts\python.exe tools\deploy\smoke_mcp.py --url <PUBLIC_URL>

  # Open API docs:
  Start-Process "http://127.0.0.1:8090/docs"
"@

Write-Cyan "`n============================================================"
Write-Green "  Ready to demo! Tunnel is running."
Write-Cyan "============================================================`n"
