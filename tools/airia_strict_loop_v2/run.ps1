# ─── run.ps1 ──────────────────────────────────────────────────────
# Airia Strict Judge Loop v2 — CFO-Memorable edition.
#
# Stop condition:
#   cfo_remember == "YES"
#   AND submission_ready == "YES"
#   AND remaining_issues_count == 0
#   AND score >= 9.0
#
# Gates (enforced EVERY iteration before judge):
#   1. pytest 0 fail / 0 skip
#   2. no_apex PASS
#   3. no_network PASS
# ──────────────────────────────────────────────────────────────────

param(
    [int]$MaxIters = 10
)

$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot\..\..\

$PYTHON = "apps\api\.venv\Scripts\python.exe"
$env:OLLAMA_MODEL   = "devstral"
$env:APP_MODE       = "DEMO"
$env:E2E_MODE       = "1"
$env:PYTHONUTF8     = "1"
$env:LLM_PROVIDER   = "DEMO"
$env:SECRET_KEY     = "demo-secret"

# ── Helpers ──────────────────────────────────────────────────────

function Ensure-Backend {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:8090/healthz" -Method GET -UseBasicParsing -TimeoutSec 3
        Write-Host "[v2] Backend already running (healthz OK)" -ForegroundColor Green
    } catch {
        Write-Host "[v2] Starting backend on :8090 ..." -ForegroundColor Yellow
        Start-Process -FilePath $PYTHON `
            -ArgumentList "-m","uvicorn","app.main:app","--host","127.0.0.1","--port","8090" `
            -WorkingDirectory "apps\api" `
            -WindowStyle Hidden
        Start-Sleep 6
        # Verify
        try {
            Invoke-WebRequest -Uri "http://127.0.0.1:8090/healthz" -UseBasicParsing -TimeoutSec 5 | Out-Null
            Write-Host "[v2] Backend started OK" -ForegroundColor Green
        } catch {
            Write-Host "[v2] Backend FAILED to start!" -ForegroundColor Red
            exit 1
        }
    }
}

function Run-Gate-Pytest {
    Write-Host "[v2] Gate: pytest ..." -ForegroundColor Cyan
    Push-Location apps\api
    $output = & .venv\Scripts\python.exe -m pytest tests/ -q --tb=short 2>&1
    $result = $LASTEXITCODE
    $output | Select-Object -Last 5 | Write-Host
    Pop-Location
    if ($result -ne 0) {
        Write-Host "[v2] GATE FAIL: pytest returned exit code $result" -ForegroundColor Red
        return $false
    }
    # Check for skips
    $summary = ($output | Select-Object -Last 2) -join " "
    if ($summary -match "(\d+) skipped") {
        Write-Host "[v2] GATE FAIL: $($Matches[1]) tests skipped" -ForegroundColor Red
        return $false
    }
    Write-Host "[v2] Gate PASS: pytest" -ForegroundColor Green
    return $true
}

function Run-Gate-NoApex {
    Write-Host "[v2] Gate: no_apex ..." -ForegroundColor Cyan
    & $PYTHON tools/gates/no_apex_references.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[v2] GATE FAIL: no_apex" -ForegroundColor Red
        return $false
    }
    Write-Host "[v2] Gate PASS: no_apex" -ForegroundColor Green
    return $true
}

function Run-Gate-NoNetwork {
    Write-Host "[v2] Gate: no_network ..." -ForegroundColor Cyan
    & $PYTHON tools/gates/no_network_in_tests.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[v2] GATE FAIL: no_network" -ForegroundColor Red
        return $false
    }
    Write-Host "[v2] Gate PASS: no_network" -ForegroundColor Green
    return $true
}

function Check-StopCondition($evalData) {
    $score           = $evalData.computed_score
    $cfoRemember     = $evalData.cfo_remember
    $submReady       = $evalData.submission_ready
    $negCount        = ($evalData.negative_criticisms | Measure-Object).Count
    $remainingCount  = 0
    if ($evalData.llm_judgment -and $evalData.llm_judgment.remaining_issues) {
        $remainingCount = ($evalData.llm_judgment.remaining_issues | Where-Object { $_ -and $_.Trim() -ne "" } | Measure-Object).Count
    }

    Write-Host ""
    Write-Host "[v2] ── STOP CONDITION CHECK ──" -ForegroundColor Magenta
    Write-Host "     cfo_remember     = $cfoRemember  (need YES)"
    Write-Host "     submission_ready = $submReady  (need YES)"
    Write-Host "     score            = $score  (need >= 9.0)"
    Write-Host "     remaining_issues = $remainingCount  (need 0)"
    Write-Host "     negative_crits   = $negCount  (need 0)"

    if ($cfoRemember -eq "YES" -and $submReady -eq "YES" -and $score -ge 9.0 -and $remainingCount -eq 0) {
        Write-Host "[v2] ALL STOP CONDITIONS MET!" -ForegroundColor Green
        return $true
    }
    return $false
}

# ── MAIN ─────────────────────────────────────────────────────────

Write-Host ""
Write-Host "================================================================" -ForegroundColor Magenta
Write-Host "  AIRIA STRICT JUDGE LOOP v2 — CFO MEMORABLE EDITION" -ForegroundColor Magenta
Write-Host "  Max iterations: $MaxIters" -ForegroundColor Magenta
Write-Host "  Stop: cfo_remember=YES & submission_ready=YES & score>=9 & remaining=0" -ForegroundColor Magenta
Write-Host "================================================================" -ForegroundColor Magenta

Ensure-Backend

for ($iter = 1; $iter -le $MaxIters; $iter++) {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "  ITERATION $iter / $MaxIters" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan

    # ── Gates ──
    if (-not (Run-Gate-NoApex))    { Write-Host "[v2] Fix no_apex gate first." -ForegroundColor Red; exit 1 }
    if (-not (Run-Gate-NoNetwork)) { Write-Host "[v2] Fix no_network gate first." -ForegroundColor Red; exit 1 }

    # ── Run strict judge ──
    Write-Host "[v2] Running strict judge ..." -ForegroundColor Yellow
    & $PYTHON evaluate_ledgerlive_strict.py 2>&1 | Select-Object -Last 30

    # ── Parse result ──
    if (-not (Test-Path brutal_evaluation.json)) {
        Write-Host "[v2] brutal_evaluation.json not found!" -ForegroundColor Red
        continue
    }
    $eval = Get-Content brutal_evaluation.json -Raw | ConvertFrom-Json
    $score = $eval.computed_score

    Write-Host ""
    Write-Host "[v2] SCORE: $score / 10" -ForegroundColor $(if ($score -ge 9) { "Green" } elseif ($score -ge 6) { "Yellow" } else { "Red" })

    # Show breakdown
    if ($eval.breakdown) {
        Write-Host "[v2] Breakdown:" -ForegroundColor Gray
        $eval.breakdown.PSObject.Properties | ForEach-Object {
            Write-Host "       $($_.Name): $([math]::Round($_.Value, 2))" -ForegroundColor Gray
        }
    }

    # Show passed/failed checks
    Write-Host "[v2] Passed: $($eval.passed_checks -join ', ')" -ForegroundColor Green
    Write-Host "[v2] Failed: $($eval.failed_checks -join ', ')" -ForegroundColor Red

    # ── Check stop condition ──
    if (Check-StopCondition $eval) {
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host "  TARGET REACHED! cfo_remember=YES, submission_ready=YES" -ForegroundColor Green
        Write-Host "  Score: $score / 10" -ForegroundColor Green
        Write-Host "============================================================" -ForegroundColor Green

        # Final commit
        git add -A
        git commit -m "judge-loop-1: strict v2 score $score — CFO memorable YES"
        break
    }

    # ── Apply fixes ──
    Write-Host "[v2] Applying fixes ..." -ForegroundColor Yellow
    & $PYTHON tools/airia_strict_loop_v2/apply.py --from brutal_evaluation.json

    # ── Run pytest gate (after fixes) ──
    if (-not (Run-Gate-Pytest)) {
        Write-Host "[v2] Tests broke after fixes — reverting." -ForegroundColor Red
        git checkout -- .
        continue
    }

    # ── Commit iteration ──
    git add -A
    git commit -m "judge-loop-1: v2 iter $iter (score $score)"

    Write-Host "[v2] Iteration $iter complete." -ForegroundColor Cyan
}

if ($iter -gt $MaxIters) {
    Write-Host "[v2] Max iterations reached. Manual intervention needed." -ForegroundColor Red
    exit 1
}
