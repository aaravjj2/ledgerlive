# Nuclear Loop Runner — tools/nuclear_loop/run.ps1
# Runs up to MAX_ITERS of: evaluate → apply → evaluate until 20/20
# Usage: powershell -File tools/nuclear_loop/run.ps1 [-MaxIters 25]

param(
    [int]$MaxIters = 25
)

$ErrorActionPreference = "Stop"
$REPO = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$PYTHON = "$REPO\apps\api\.venv\Scripts\python.exe"
$JUDGE  = "$REPO\evaluate_ledgerlive_strict.py"
$APPLY  = "$REPO\tools\nuclear_loop\apply.py"
$REPORT = "$REPO\nuclear_gate_report.json"

Write-Host "`n==> NUCLEAR LOOP START  (max $MaxIters iterations)`n" -ForegroundColor Cyan
Write-Host "Repo  : $REPO"
Write-Host "Python: $PYTHON"
Write-Host "Judge : $JUDGE"

if (-not (Test-Path $PYTHON)) {
    Write-Host "ERROR: Python venv not found at $PYTHON" -ForegroundColor Red
    exit 1
}

for ($i = 1; $i -le $MaxIters; $i++) {
    Write-Host "`n── ITER $i / $MaxIters ────────────────────────────────" -ForegroundColor Yellow

    # Step 1: Refresh demo_start_report.json before judge runs
    & $PYTHON $APPLY 2>&1 | ForEach-Object { Write-Host "  [apply] $_" }

    # Step 2: Run judge
    Write-Host "`n  [judge] Running evaluate_ledgerlive_strict.py ..." -ForegroundColor Cyan
    & $PYTHON $JUDGE
    if (-not $?) {
        Write-Host "  [judge] Exited with error — continuing" -ForegroundColor Red
    }

    # Step 3: Read report
    if (-not (Test-Path $REPORT)) {
        Write-Host "  [judge] No report generated — skipping iter" -ForegroundColor Red
        continue
    }

    $report = Get-Content $REPORT | ConvertFrom-Json
    $score  = $report.score
    $passed = $report.gates_passed
    $total  = $report.total_gates

    Write-Host "`n  SCORE: $score / 10   ($passed / $total gates)" -ForegroundColor $(if ($passed -eq $total) { "Green" } else { "Yellow" })

    if ($passed -eq $total) {
        Write-Host "`n==> NUCLEAR LOOP COMPLETE — 20/20 GATES PASS! SCORE: 10.0/10`n" -ForegroundColor Green
        Write-Host "  Completed in $i iteration(s). Ready to submit." -ForegroundColor Green
        exit 0
    }

    $failing = $report.gates.PSObject.Properties | Where-Object { -not $_.Value.pass } | Select-Object -ExpandProperty Name
    Write-Host "  Failing gates: $($failing -join ', ')" -ForegroundColor Red
}

Write-Host "`n==> NUCLEAR LOOP EXHAUSTED after $MaxIters iters" -ForegroundColor Red
$report = Get-Content $REPORT | ConvertFrom-Json
Write-Host "  Final score: $($report.score)/10  ($($report.gates_passed)/$($report.total_gates) gates)" -ForegroundColor Yellow
exit 1
