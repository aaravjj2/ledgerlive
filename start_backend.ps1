# start_backend.ps1 — Start LedgerLive backend on port 8090
# Works on PowerShell 5.1 (no &&, uses ; instead)

$PORT = 8090
$API_DIR = "C:\Aarav\ledgerlive\apps\api"
$PYTHON  = "$API_DIR\.venv\Scripts\python.exe"
$BASE    = "http://127.0.0.1:$PORT"

# Check if already running
try {
    $r = Invoke-WebRequest "$BASE/healthz" -UseBasicParsing -TimeoutSec 2
    Write-Host "Backend already running on :$PORT (status $($r.StatusCode))"
    exit 0
} catch {}

# Kill anything on the port
Write-Host "Starting backend on :$PORT ..."
Get-NetTCPConnection -LocalPort $PORT -ErrorAction SilentlyContinue |
    ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
Start-Sleep 1

# Start with DEMO env vars
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $PYTHON
$psi.Arguments = "-m uvicorn app.main:app --host 127.0.0.1 --port $PORT"
$psi.WorkingDirectory = $API_DIR
$psi.UseShellExecute = $false
$psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
$psi.EnvironmentVariables["APP_MODE"]     = "DEMO"
$psi.EnvironmentVariables["E2E_MODE"]     = "1"
$psi.EnvironmentVariables["LLM_PROVIDER"] = "DEMO"
$psi.EnvironmentVariables["SECRET_KEY"]   = "demo-secret"

$proc = [System.Diagnostics.Process]::Start($psi)
Write-Host "PID: $($proc.Id)"

# Poll until ready (30s max)
$ready = $false
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep 1
    try {
        $r = Invoke-WebRequest "$BASE/healthz" -UseBasicParsing -TimeoutSec 2
        if ($r.StatusCode -eq 200) { $ready = $true; break }
    } catch {}
}

if ($ready) {
    Write-Host "READY: $BASE/healthz"
    Write-Host "  Agent cycle : POST $BASE/api/agent/cycle"
    Write-Host "  Airia webhook: POST $BASE/api/webhook/airia"
    Write-Host "  MCP info     : GET  $BASE/mcp/info"
    Write-Host "  Docs         : GET  $BASE/docs"
    exit 0
} else {
    Write-Host "ERROR: Backend did not start within 30 seconds"
    exit 1
}
