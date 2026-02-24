# ─── run_strict_loop.ps1 ──────────────────────────────────────────
# Airia strict-judge loop runner.
# Sets up environment, runs evaluate_ledgerlive_strict.py in a loop,
# and applies fixes until score >= 9.0.
# ──────────────────────────────────────────────────────────────────

param(
    [int]$MaxIters = 12
)

$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot\..\..\

$PYTHON = "apps\api\.venv\Scripts\python.exe"
$env:OLLAMA_MODEL = "devstral"
$env:APP_MODE = "DEMO"
$env:E2E_MODE = "1"
$env:PYTHONUTF8 = "1"

function Ensure-Backend {
    $conn = Get-NetTCPConnection -LocalPort 8090 -ErrorAction SilentlyContinue
    if (-not $conn) {
        Write-Host "[loop] Starting backend on :8090 ..." -ForegroundColor Yellow
        Start-Process -FilePath $PYTHON -ArgumentList "-m","uvicorn","app.main:app","--host","127.0.0.1","--port","8090" -WorkingDirectory "apps\api" -WindowStyle Hidden
        Start-Sleep 5
    } else {
        Write-Host "[loop] Backend already running (PID $($conn.OwningProcess))"
    }
}

function Ensure-Frontend {
    $conn = Get-NetTCPConnection -LocalPort 4173 -ErrorAction SilentlyContinue
    if (-not $conn) {
        Write-Host "[loop] Building + starting frontend preview on :4173 ..." -ForegroundColor Yellow
        Push-Location apps\web
        npx vite build --outDir dist 2>$null
        Start-Process -FilePath "npx" -ArgumentList "vite","preview","--host","127.0.0.1","--port","4173" -WindowStyle Hidden
        Pop-Location
        Start-Sleep 5
    } else {
        Write-Host "[loop] Frontend already running (PID $($conn.OwningProcess))"
    }
}

function Run-Gates {
    Write-Host "[loop] Running gates ..." -ForegroundColor Cyan
    & $PYTHON tools/gates/no_apex_references.py
    if ($LASTEXITCODE -ne 0) { Write-Host "[loop] GATE FAIL: no_apex" -ForegroundColor Red; return $false }
    & $PYTHON tools/gates/no_network_in_tests.py
    if ($LASTEXITCODE -ne 0) { Write-Host "[loop] GATE FAIL: no_network" -ForegroundColor Red; return $false }
    return $true
}

function Run-Tests {
    Write-Host "[loop] Running pytest ..." -ForegroundColor Cyan
    Push-Location apps\api
    & .venv\Scripts\python.exe -m pytest tests/ -q --tb=short 2>&1 | Select-Object -Last 5
    $result = $LASTEXITCODE
    Pop-Location
    return ($result -eq 0)
}

# ─── MAIN LOOP ───────────────────────────────────────────────────
Ensure-Backend
Ensure-Frontend

for ($iter = 1; $iter -le $MaxIters; $iter++) {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "  STRICT JUDGE LOOP — ITERATION $iter / $MaxIters" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan

    # Run strict judge
    Write-Host "[loop] Running strict judge ..."
    & $PYTHON evaluate_ledgerlive_strict.py 2>&1 | Select-Object -Last 20

    # Parse score
    if (Test-Path brutal_evaluation.json) {
        $eval = Get-Content brutal_evaluation.json -Raw | ConvertFrom-Json
        $score = $eval.computed_score
        Write-Host ""
        Write-Host "[loop] SCORE: $score / 10" -ForegroundColor $(if ($score -ge 9) { "Green" } elseif ($score -ge 6) { "Yellow" } else { "Red" })
        Write-Host "[loop] Breakdown:" -ForegroundColor Gray
        $eval.breakdown | Format-List | Out-String | Write-Host

        if ($score -ge 9.0) {
            Write-Host "[loop] TARGET REACHED: $score >= 9.0!" -ForegroundColor Green
            # Final proof pack
            & $PYTHON tools/proof/generate_proof_pack.py --milestone=airia-9plus-strict
            git add -A
            git commit -m "airia-9plus: strict judge score $score"
            git tag v0.303.0-ledgerlive
            git push origin waves
            git push origin v0.303.0-ledgerlive
            Write-Host "[loop] DONE — v0.303.0-ledgerlive tagged and pushed." -ForegroundColor Green
            exit 0
        }
    } else {
        Write-Host "[loop] brutal_evaluation.json not found!" -ForegroundColor Red
    }

    # Apply fixes
    Write-Host "[loop] Applying fixes for iteration $iter ..."
    & $PYTHON tools/airia_loop/apply_fixes.py --from brutal_evaluation.json

    # Run gates
    if (-not (Run-Tests)) { Write-Host "[loop] Tests FAILED — stopping." -ForegroundColor Red; exit 1 }
    if (-not (Run-Gates)) { Write-Host "[loop] Gates FAILED — stopping." -ForegroundColor Red; exit 1 }

    # Proof pack
    $milestone = "airia-loop-iter-$iter"
    & $PYTHON tools/proof/generate_proof_pack.py --milestone=$milestone

    # Commit
    git add -A
    git commit -m "judge-loop-$iter`: strict judge iteration $iter (score $score)"
    $patchTag = "v0.302.$($iter + 10).0-ledgerlive"
    git tag $patchTag
    git push origin waves
    git push origin $patchTag

    Write-Host "[loop] Iteration $iter complete. Tag: $patchTag" -ForegroundColor Cyan
}

Write-Host "[loop] Max iterations reached without hitting 9.0 — manual intervention needed." -ForegroundColor Red
exit 1
