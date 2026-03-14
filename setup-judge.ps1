<#
setup-judge.ps1
One-shot setup for: OpenClaw + Ollama (devstral:latest) + a locked-down "judge" agent + runner script.

Safe defaults: NO shell/exec tools for the agent. Browser + web_fetch allowed for research.

Designed for Windows PowerShell 5.1 (uses only compatible constructs).
#>
[CmdletBinding()]
param(
  [string]$OllamaModel = "devstral:latest",
  [string]$BraveApiKey = ""  # optional; enables web_search tool if provided (Brave key required)
)

$ErrorActionPreference = "Stop"
try { Set-StrictMode -Version 2.0 } catch {}

function Write-Section([string]$msg) {
  Write-Host ""
  Write-Host "=== $msg ===" -ForegroundColor Cyan
}

function Test-Command([string]$name) {
  $c = Get-Command $name -ErrorAction SilentlyContinue
  if ($null -ne $c) { return $true } else { return $false }
}

function Ensure-WinGet() {
  if (-not (Test-Command "winget")) {
    throw "winget not found. Install App Installer from Microsoft Store, then re-run."
  }
}

function Ensure-Node22() {
  if (-not (Test-Command "node")) {
    Write-Section "Installing Node.js 22 (required by OpenClaw)"
    Start-Process -FilePath "winget" -ArgumentList "install -e --id OpenJS.NodeJS.22" -NoNewWindow -Wait
    return
  }

  $v = (node -v).Trim()
  $major = 0
  try { $major = [int]($v.TrimStart('v').Split('.')[0]) } catch { $major = 0 }
  if ($major -lt 22) {
    Write-Section "Upgrading Node.js to 22 (required by OpenClaw)"
    Start-Process -FilePath "winget" -ArgumentList "install -e --id OpenJS.NodeJS.22" -NoNewWindow -Wait
  } else {
    Write-Section "Node.js OK ($v)"
  }
}

function Ensure-Ollama() {
  if (-not (Test-Command "ollama")) {
    Write-Section "Installing Ollama"
    Start-Process -FilePath "winget" -ArgumentList "install -e --id Ollama.Ollama" -NoNewWindow -Wait
  } else {
    Write-Section "Ollama OK"
  }
}

function Ensure-Ollama-Running() {
  Write-Section "Checking Ollama API"
  $ok = $false
  try {
    Invoke-WebRequest -Uri "http://localhost:11434" -TimeoutSec 2 | Out-Null
    $ok = $true
  } catch { $ok = $false }

  if (-not $ok) {
    Write-Host "Ollama API not reachable; attempting to start 'ollama serve'..." -ForegroundColor Yellow
    try {
      Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden -NoNewWindow -PassThru | Out-Null
      Start-Sleep -Seconds 2
      Invoke-WebRequest -Uri "http://localhost:11434" -TimeoutSec 4 | Out-Null
      $ok = $true
    } catch { $ok = $false }
  }

  if (-not $ok) {
    throw "Could not reach Ollama at http://localhost:11434. Launch the Ollama app once, then re-run."
  }

  Write-Host "Ollama API OK" -ForegroundColor Green
}

function Pull-Ollama-Model([string]$model) {
  Write-Section "Ensuring Ollama model is present: $model"
  try {
    & ollama pull $model | Out-Host
  } catch {
    Write-Host "Warning: failed to pull model via ollama; ensure model is available: $model" -ForegroundColor Yellow
  }
}

function Ensure-OpenClaw() {
  if (Test-Command "openclaw") {
    Write-Section "OpenClaw already installed"
    try { openclaw --version | Out-Host } catch {}
    return
  }

  Write-Section "Installing OpenClaw (official installer, no onboarding wizard)"
  try {
    # Use WebClient to avoid Invoke-WebRequest interactive parsing warning on PS5.1
    $wc = New-Object System.Net.WebClient
    $code = $wc.DownloadString("https://openclaw.ai/install.ps1")
    $sb = [scriptblock]::Create($code)
    & $sb -NoOnboard
  } catch {
    throw "OpenClaw install failed: $($_.Exception.Message)"
  }

  if (-not (Test-Command "openclaw")) {
    throw "OpenClaw install finished but 'openclaw' is still not in PATH. Restart PowerShell and re-run."
  }

  openclaw --version | Out-Host
}

function Ensure-OpenClaw-Home() {
  # Use a safe user home path (prefer %USERPROFILE%); avoid assigning to $HOME (read-only on some shells)
  $userRoot = $env:USERPROFILE
  if (-not $userRoot) { $userRoot = $env:HOME }
  if (-not $userRoot) { $userRoot = $HOME }
  $ocHome = Join-Path $userRoot ".openclaw"
  if (-not (Test-Path $ocHome)) { New-Item -ItemType Directory -Force -Path $ocHome | Out-Null }
  return $ocHome
}

function Backup-If-Exists([string]$path) {
  if (Test-Path $path) {
    $ts = Get-Date -Format "yyyyMMdd-HHmmss"
    $bak = "$path.bak.$ts"
    Copy-Item -Force $path $bak
    Write-Host "Backed up existing file to: $bak" -ForegroundColor Yellow
  }
}

function Write-TextFile([string]$path, [string]$content) {
  $dir = Split-Path -Parent $path
  if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
  $content | Out-File -FilePath $path -Encoding utf8 -Force
}

function Configure-JudgeAgent([string]$openclawHome, [string]$ollamaModel, [string]$braveKey) {
  Write-Section "Configuring Judge agent workspace + strict rubric"

  $env:OLLAMA_API_KEY = "ollama-local"
  [Environment]::SetEnvironmentVariable("OLLAMA_API_KEY", "ollama-local", "User")

  $ws = Join-Path $openclawHome "workspace-judge"
  New-Item -ItemType Directory -Force -Path $ws | Out-Null

  # Persona + rubric files
  Write-TextFile (Join-Path $ws "SOUL.md") @"
You are JUDGE.

You are harsh, evidence-driven, and allergic to hand-waving.
If a claim is not backed by a link, repo, demo, screenshot, or reproducible steps, it is UNPROVEN.

No hype. No compliments unless directly earned by proof.
Never guess missing details. Never fill gaps.

You must follow the SCORING.md rubric exactly.
"@

  Write-TextFile (Join-Path $ws "AGENTS.md") @"
JUDGE workflow (always):

1) Intake
- List every artifact/link provided.
- List what is missing that prevents verification.

2) Rules-first
- Open the hackathon page(s).
- Extract judging criteria, scoring weights, track constraints, submission rules.
- If rules can't be found, say so and score conservatively.

3) Verification
For each claim:
- Mark: PROVEN / UNPROVEN / CONTRADICTED.
- Attach evidence links (URL + where it was found).

4) Competitive context (internet)
- Find similar hackathons and winners.
- Pull patterns (what winners consistently have).
- Cite sources (URLs).

5) Score
Apply hard gates first, then rubric.

6) Output
- Scorecard
- Hard-gate results
- Evidence map (Claim -> Proof)
- Fatal issues (top 3)
- Prioritized fix plan (top 5)
- JSON block at the end
"@

  Write-TextFile (Join-Path $ws "SCORING.md") @"
Hard Gates (apply first):
G0 Evidence Gate: unproven claims treated as false.
G1 Repro Gate: cannot run/verify from artifacts -> max 40/100.
G2 Integrity Gate: misleading demo/claims -> max 20/100.
G3 Rules Gate: violates hackathon rules/track -> 0 for that track.

Rubric (100):
- Problem clarity: 10
- Novelty: 15
- Technical difficulty: 20
- Execution quality: 20
- Proof/reproducibility: 20
- Security/privacy basics: 10
- Polish (demo/story): 5

Standard deductions:
- No repo OR private repo without access: -25
- No demo video: -10
- No setup instructions: -10
- Secrets committed: -25
- "Coming soon" described as done: -15
"@

  # OpenClaw config
  $configPath = Join-Path $openclawHome "openclaw.json"
  Backup-If-Exists $configPath

  $openclawModelId = "ollama/$ollamaModel"

  # Enable web search by default; if no Brave API key provided, pass empty string
  $searchEnabled = $true
  if (-not [string]::IsNullOrWhiteSpace($braveKey)) {
    $searchApiKey = $braveKey
  } else {
    $searchApiKey = ""
  }

  $cfg = @{
    agents = @{
      defaults = @{
        userTimezone = "America/New_York"
        model = @{
          primary = $openclawModelId
        }
      }
      list = @(
        @{
          id = "judge"
          default = $true
          name = "Hackathon Judge"
          workspace = $ws
          model = @{
            primary = $openclawModelId
          }
          sandbox = @{
            mode = "all"
            scope = "agent"
            workspaceAccess = "rw"
          }
          tools = @{
            profile = "minimal"
            allow = @("read","write","edit","web_fetch","browser")
            deny  = @("group:runtime","apply_patch","canvas","cron","gateway")
            elevated = @{
              enabled = $false
            }
          }
        }
      )
    }
    tools = @{
      web = @{
        fetch = @{
          enabled = $true
        }
        search = @{
          enabled = $searchEnabled
          apiKey  = $searchApiKey
          maxResults = 5
          timeoutSeconds = 30
          cacheTtlMinutes = 15
        }
      }
    }
  }

  ($cfg | ConvertTo-Json -Depth 32) | Out-File -FilePath $configPath -Encoding utf8 -Force
  Write-Host "Wrote config: $configPath" -ForegroundColor Green

  return $ws
}

function Ensure-Gateway-Service() {
  Write-Section "Installing + starting OpenClaw Gateway service"
  # Ensure gateway.mode=config and gateway auth token are set for the service
  try {
    $token = [guid]::NewGuid().ToString('N')
    [Environment]::SetEnvironmentVariable('OPENCLAW_GATEWAY_TOKEN', $token, 'User')
    $env:OPENCLAW_GATEWAY_TOKEN = $token
    try { & openclaw config set gateway.mode local | Out-Host } catch {}
    try { & openclaw config set gateway.auth.token $token | Out-Host } catch {}
  } catch {}
  try {
    Start-Process -FilePath "openclaw" -ArgumentList "gateway install --force" -NoNewWindow -Wait | Out-Null
  } catch {}
  # Attempt to fix configuration issues automatically and start gateway
  try { openclaw doctor --fix | Out-Host } catch {}

  try { Start-Process -FilePath "openclaw" -ArgumentList "gateway start" -NoNewWindow -Wait | Out-Null } catch {}
  Start-Sleep -Seconds 2
  try {
    openclaw gateway status | Out-Host
  } catch {
    Write-Host "Gateway status check failed; attempting to start service again..." -ForegroundColor Yellow
    try { Start-Process -FilePath "openclaw" -ArgumentList "gateway start" -NoNewWindow -Wait | Out-Null } catch {}
    Start-Sleep -Seconds 2
    try { openclaw gateway status | Out-Host } catch {}
  }
}

function Write-Runner([string]$openclawHome) {
  Write-Section "Writing judge runner script"

  $runnerPath = Join-Path $openclawHome "judge-run.ps1"
  $runnerContent = @'
param(
  [Parameter(Mandatory=$true)][string]$HackathonUrl,
  [Parameter(Mandatory=$true)][string]$ProjectUrl,
  [string]$RepoUrl = "",
  [string]$DemoUrl = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version 2.0

$ts = Get-Date -Format "yyyyMMdd-HHmmss"
$root = Join-Path (Get-Location) ("artifacts\proof\{0}-judge" -f $ts)
New-Item -ItemType Directory -Force -Path $root | Out-Null

$prompt = @"
You are JUDGE. Use SOUL.md / AGENTS.md / SCORING.md in your workspace.

Hackathon: $HackathonUrl
Project page: $ProjectUrl
Repo: $RepoUrl
Demo: $DemoUrl

Requirements:
- Use the hackathon rules as the source of truth.
- Verify claims using browser + web_fetch.
- If you cannot verify, mark UNPROVEN and penalize.
- Produce: scorecard + hard gates + evidence map + fatal issues + prioritized fixes.
- End with a JSON object containing: score_total, hard_gates, category_scores, proven_claims, unproven_claims, contradictions.
"@

$inPath = Join-Path $root "INPUT.txt"
$prompt | Out-File -Encoding utf8 $inPath

$out1 = Join-Path $root "judge_run1.json"
openclaw agent --agent judge --message $prompt --json | Out-File -Encoding utf8 $out1

$out2 = Join-Path $root "judge_run2.json"
openclaw agent --agent judge --message $prompt --json | Out-File -Encoding utf8 $out2

$h1 = (Get-FileHash $out1 -Algorithm SHA256).Hash
$h2 = (Get-FileHash $out2 -Algorithm SHA256).Hash

$manifest = Join-Path $root "MANIFEST.md"
@"
# Judge Proof Pack

## Objective
Strict evaluation of a hackathon submission, with evidence + repeat-run determinism check.

## Commands run
openclaw agent --agent judge --message <prompt> --json  (twice)

## Determinism
Run1 SHA256: $h1
Run2 SHA256: $h2
Deterministic: $([bool]($h1 -eq $h2))

## Files
- INPUT.txt
- judge_run1.json
- judge_run2.json
"@ | Out-File -Encoding utf8 $manifest

if ($h1 -ne $h2) {
  Write-Error "NON-DETERMINISTIC OUTPUT: hashes differ. See $root"
  exit 1
}

Write-Host "OK: proof pack at $root"
'@

  Write-TextFile $runnerPath $runnerContent
  Write-Host "Runner written: $runnerPath" -ForegroundColor Green
  return $runnerPath
}

# -------------------------
# Main (wrapped to surface errors clearly)
# -------------------------

try {
  Write-Section "Preflight"
  Ensure-WinGet

  Ensure-Ollama
  Ensure-Node22

  Ensure-Ollama-Running
  Pull-Ollama-Model $OllamaModel

  Ensure-OpenClaw

  # Ensure OpenClaw has its home folder
  $openclawHome = Ensure-OpenClaw-Home

  # Create baseline config/workspace if user has never run OpenClaw
  if (-not (Test-Path (Join-Path $openclawHome "openclaw.json"))) {
    Write-Section "Initializing OpenClaw home (openclaw setup)"
    try { openclaw setup | Out-Host } catch { Write-Host "openclaw setup skipped or failed" -ForegroundColor Yellow }
  }

  $ws = Configure-JudgeAgent -openclawHome $openclawHome -ollamaModel $OllamaModel -braveKey $BraveApiKey

  Ensure-Gateway-Service

  $runner = Write-Runner $openclawHome

  Write-Section "Done"
  Write-Host "Judge agent id: judge"
  Write-Host "Workspace: $ws"
  Write-Host "Config: $(Join-Path $openclawHome 'openclaw.json')"
  Write-Host ""
  Write-Host "Try a quick run:"
  Write-Host "  openclaw agent --agent judge --message 'Score this: https://devpost.com/... (add repo/demo links)' --json"
  Write-Host ""
  Write-Host "Or use the runner (creates artifacts/proof/*):"
  Write-Host "  & '$runner' -HackathonUrl 'https://...' -ProjectUrl 'https://...' -RepoUrl 'https://github.com/...' -DemoUrl 'https://...'"
} catch {
  Write-Host "ERROR during setup: $($_.Exception.Message)" -ForegroundColor Red
  if ($_.InvocationInfo) {
    Write-Host "At: $($_.InvocationInfo.ScriptLineNumber)" -ForegroundColor Yellow
  }
  if ($_.ScriptStackTrace) { Write-Host $_.ScriptStackTrace -ForegroundColor Yellow }
  throw
}
