# ============================================================
# evaluate_ledgerlive.py
# Hackathon Judge for LedgerLive
# Airia "Race Beyond the Track" Hackathon — Williams F1 / Atlassian
# Deadline: March 1, 2026 11:59 PM AEDT
# Prize pool: $20,000 USD
#
# Your stack:
#   Backend  → FastAPI on http://127.0.0.1:8090  (apps/api/)
#   Frontend → React/Vite on http://127.0.0.1:4174 (apps/web/)
#   DB       → SQLite (local)
#
# Usage:
#   cd C:\Aarav\ledgerlive
#   $env:OLLAMA_MODEL = "devstral"
#   python evaluate_ledgerlive.py
# ============================================================

import subprocess
import requests
import json
import time
import sys
import os
from pathlib import Path

try:
    from openai import OpenAI
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    print("Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "openai", "colorama", "requests"], check=True)
    from openai import OpenAI
    from colorama import Fore, Style, init
    init(autoreset=True)

# ── CONFIG ───────────────────────────────────────────────────
REPO_PATH    = Path(os.getenv("LEDGER_REPO_PATH", r"C:\Aarav\ledgerlive"))
BACKEND_URL  = "http://127.0.0.1:8090"
FRONTEND_URL = "http://127.0.0.1:4174"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "devstral")

# Start commands matching your README exactly
BACKEND_CMD  = f'cd "{REPO_PATH}\\apps\\api" && .venv\\Scripts\\python -m uvicorn app.main:app --port 8090 --reload'
FRONTEND_CMD = f'cd "{REPO_PATH}\\apps\\web" && npm run dev'

# ── Hackathon judging criteria (Airia / Williams F1) ────────
HACKATHON_CRITERIA = """
Airia "Race Beyond the Track" Hackathon — Judging Criteria:
Built by Airia (official Williams F1 partner). Platform: Airia's no-code AI agent builder.
Theme: Autonomous AI agents that EITHER:
  (a) Elevate the F1 fan experience, OR
  (b) Streamline racing operations / boost team productivity workflows

Judging dimensions (inferred from past Airia hackathon + Atlassian Williams context):
1. AGENT AUTONOMY (30%): Does the project use/simulate an autonomous AI agent?
   Real agentic loop: perceive → decide → act → report. Not just a chatbot or dashboard.
2. WORKFLOW IMPACT (25%): Does it meaningfully streamline a real workflow?
   Finance close automation, document triage, exception handling = strong fit.
3. F1 / RACING THEME ALIGNMENT (20%): Is the F1/racing theme genuine or forced?
   Race control dashboard, pit stop analogy for finance close, lap-by-lap audit trail = good.
4. AIRIA PLATFORM USE (15%): Built on or compatible with Airia's no-code agent platform?
   If not natively, does it demonstrate integration potential?
5. DEMO QUALITY & PRESENTATION (10%): Working demo, clear README, video-ready.

DEADLINE: March 1, 2026 11:59 PM AEDT (that's very soon — urgency is real).
PRIZE: Up to $20,000 USD. Must attend March 4 awards ceremony to be eligible.
"""

client = OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)

# ── HELPERS ──────────────────────────────────────────────────
def header(text):
    print(f"\n{Fore.CYAN}{'='*62}")
    print(f"  {text}")
    print(f"{'='*62}{Style.RESET_ALL}")

def ok(msg):   print(f"  {Fore.GREEN}✓ {msg}{Style.RESET_ALL}")
def fail(msg): print(f"  {Fore.RED}✗ {msg}{Style.RESET_ALL}")
def warn(msg): print(f"  {Fore.YELLOW}⚠ {msg}{Style.RESET_ALL}")

# ── START SERVICES ───────────────────────────────────────────
def start_services():
    header("STARTING SERVICES")
    procs = []

    warn("Starting backend (FastAPI :8090)...")
    p1 = subprocess.Popen(
        ["powershell", "-Command", BACKEND_CMD],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    procs.append(p1)
    time.sleep(7)

    try:
        r = requests.get(f"{BACKEND_URL}/docs", timeout=4)
        ok(f"Backend responding (status {r.status_code})")
    except:
        warn("Backend may still be starting...")

    warn("Starting frontend (React :4174)...")
    p2 = subprocess.Popen(
        ["powershell", "-Command", FRONTEND_CMD],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    procs.append(p2)
    time.sleep(10)

    try:
        r = requests.get(FRONTEND_URL, timeout=4)
        ok(f"Frontend responding (status {r.status_code})")
    except:
        warn("Frontend may still be building...")

    return procs

# ── TEST 1: Backend API ───────────────────────────────────────
def test_backend():
    header("TEST 1/6 — Backend API (FastAPI :8090)")
    results = {"running": False, "endpoints": [], "core_features": {}}

    try:
        r = requests.get(f"{BACKEND_URL}/docs", timeout=5)
        results["running"] = r.status_code == 200
        ok("FastAPI /docs accessible")
    except Exception as e:
        fail(f"Backend not reachable: {e}")
        return results

    # Read OpenAPI spec
    try:
        r2 = requests.get(f"{BACKEND_URL}/openapi.json", timeout=5)
        spec = r2.json()
        paths = list(spec.get("paths", {}).keys())
        results["endpoints"] = paths
        ok(f"Found {len(paths)} API endpoints")

        # Check for core LedgerLive features
        feature_map = {
            "document_ingestion": ["document", "upload", "ingest", "ocr"],
            "reconciliation":     ["reconcil", "match", "reconcile"],
            "exceptions":         ["exception", "triage", "flag", "anomal"],
            "review_queue":       ["review", "queue", "hitl", "human"],
            "audit_trail":        ["audit", "log", "trail", "history"],
            "race_control":       ["race", "f1", "lap", "pit"],
            "agent":              ["agent", "workflow", "automat", "pipeline"],
        }

        for feature, keywords in feature_map.items():
            found = any(
                any(kw in path.lower() for kw in keywords)
                for path in paths
            )
            results["core_features"][feature] = found
            icon = "✓" if found else "✗"
            color = Fore.GREEN if found else Fore.RED
            print(f"  {color}{icon} Feature '{feature}': {'present' if found else 'MISSING'}{Style.RESET_ALL}")

    except Exception as e:
        warn(f"Could not parse OpenAPI spec: {e}")

    return results

# ── TEST 2: Frontend ──────────────────────────────────────────
def test_frontend():
    header("TEST 2/6 — Frontend (React :4174)")
    results = {"running": False, "port": None}

    for port in [4174, 4173, 5173, 3000, 5100]:
        try:
            r = requests.get(f"http://127.0.0.1:{port}", timeout=3)
            if r.status_code == 200:
                results["running"] = True
                results["port"] = port
                ok(f"Frontend live on port {port}")
                return results
        except:
            pass

    fail("Frontend not detected on any port (4174, 4173, 5173, 3000, 5100)")
    warn("Run: cd apps/web && npm run dev")
    return results

# ── TEST 3: Core Workflow E2E ─────────────────────────────────
def test_core_workflow(backend_results):
    header("TEST 3/6 — Core Workflow Tests")
    results = {}

    if not backend_results.get("running"):
        warn("Backend not running — skipping workflow tests")
        return results

    endpoints = backend_results.get("endpoints", [])

    # Test document ingestion
    doc_endpoints = [e for e in endpoints if any(k in e.lower() for k in ["document", "upload", "ingest"])]
    if doc_endpoints:
        ep = doc_endpoints[0]
        try:
            r = requests.get(f"{BACKEND_URL}{ep}", timeout=5)
            results["documents_endpoint"] = r.status_code < 500
            ok(f"Document endpoint {ep} → status {r.status_code}")
        except Exception as e:
            results["documents_endpoint"] = False
            warn(f"Document endpoint failed: {e}")
    else:
        fail("No document ingestion endpoint found")
        results["documents_endpoint"] = False

    # Test reconciliation
    recon_endpoints = [e for e in endpoints if "reconcil" in e.lower()]
    if recon_endpoints:
        ep = recon_endpoints[0]
        try:
            r = requests.get(f"{BACKEND_URL}{ep}", timeout=5)
            results["reconciliation_endpoint"] = r.status_code < 500
            ok(f"Reconciliation endpoint {ep} → status {r.status_code}")
        except Exception as e:
            results["reconciliation_endpoint"] = False
    else:
        warn("No reconciliation endpoint found")
        results["reconciliation_endpoint"] = False

    # Test exceptions/triage
    exc_endpoints = [e for e in endpoints if any(k in e.lower() for k in ["exception", "triage", "flag"])]
    if exc_endpoints:
        ep = exc_endpoints[0]
        try:
            r = requests.get(f"{BACKEND_URL}{ep}", timeout=5)
            results["exceptions_endpoint"] = r.status_code < 500
            ok(f"Exceptions endpoint {ep} → status {r.status_code}")
        except Exception as e:
            results["exceptions_endpoint"] = False
    else:
        warn("No exceptions/triage endpoint found")

    # Test audit trail
    audit_endpoints = [e for e in endpoints if "audit" in e.lower()]
    if audit_endpoints:
        ep = audit_endpoints[0]
        try:
            r = requests.get(f"{BACKEND_URL}{ep}", timeout=5)
            results["audit_endpoint"] = r.status_code < 500
            ok(f"Audit trail endpoint {ep} → status {r.status_code}")
        except Exception as e:
            results["audit_endpoint"] = False
    else:
        warn("No audit trail endpoint found")

    # Test race control (F1 theming)
    race_endpoints = [e for e in endpoints if any(k in e.lower() for k in ["race", "f1", "lap"])]
    if race_endpoints:
        ok(f"Race control / F1 theme endpoints found: {race_endpoints[:3]}")
        results["f1_theming"] = True
    else:
        warn("No F1/race-themed endpoints — important for this hackathon's theme alignment")
        results["f1_theming"] = False

    return results

# ── TEST 4: Agent Autonomy Check ─────────────────────────────
def test_agent_autonomy(backend_results):
    header("TEST 4/6 — Agent Autonomy Check")
    results = {"has_agent_loop": False, "autonomy_score": 0}

    endpoints = backend_results.get("endpoints", [])

    # Look for agentic patterns
    agent_signals = {
        "pipeline/workflow trigger": [e for e in endpoints if any(k in e.lower() for k in ["pipeline", "workflow", "trigger", "run"])],
        "agent status/polling":      [e for e in endpoints if any(k in e.lower() for k in ["status", "progress", "poll", "job"])],
        "human-in-the-loop (HITL)":  [e for e in endpoints if any(k in e.lower() for k in ["review", "approve", "reject", "hitl"])],
        "automated decisions":       [e for e in endpoints if any(k in e.lower() for k in ["auto", "classify", "decide", "resolve"])],
    }

    score = 0
    for signal_name, matching_endpoints in agent_signals.items():
        if matching_endpoints:
            ok(f"{signal_name}: {matching_endpoints[:2]}")
            score += 1
        else:
            warn(f"{signal_name}: not detected")

    results["autonomy_score"] = score
    results["has_agent_loop"] = score >= 2
    results["agent_signals"] = {k: bool(v) for k, v in agent_signals.items()}

    if score >= 3:
        ok(f"Strong agent autonomy signals ({score}/4) — excellent for this hackathon!")
    elif score >= 2:
        warn(f"Moderate agent autonomy ({score}/4) — needs more agentic loop evidence")
    else:
        fail(f"Weak agent autonomy ({score}/4) — CRITICAL: judges want to see autonomous decision-making")
        warn("Add: POST /pipeline/run, GET /pipeline/status, POST /review/{id}/approve")

    return results

# ── TEST 5: Run Existing Tests ────────────────────────────────
def run_existing_tests():
    header("TEST 5/6 — Existing Test Suite")
    results = {"pytest_passed": False, "passed": 0, "failed": 0}

    api_path = REPO_PATH / "apps" / "api"
    if not api_path.exists():
        warn(f"apps/api not found at {api_path}")
        return results

    # Try to find python in .venv
    venv_python = api_path / ".venv" / "Scripts" / "python.exe"
    python_exe = str(venv_python) if venv_python.exists() else sys.executable

    try:
        r = subprocess.run(
            [python_exe, "-m", "pytest", "tests/", "-q", "--tb=no", "--no-header"],
            cwd=str(api_path),
            capture_output=True,
            text=True,
            timeout=60
        )
        output = r.stdout + r.stderr

        import re
        passed_match = re.search(r"(\d+) passed", output)
        failed_match = re.search(r"(\d+) failed", output)

        if passed_match:
            results["passed"] = int(passed_match.group(1))
        if failed_match:
            results["failed"] = int(failed_match.group(1))
        results["pytest_passed"] = results["failed"] == 0 and results["passed"] > 0

        if results["pytest_passed"]:
            ok(f"pytest: {results['passed']} passed, 0 failed ✓")
        elif results["passed"] > 0:
            warn(f"pytest: {results['passed']} passed, {results['failed']} failed")
        else:
            warn(f"pytest output: {output[:300]}")

    except subprocess.TimeoutExpired:
        warn("pytest timed out after 60s")
    except Exception as e:
        warn(f"Could not run pytest: {e}")

    return results

# ── TEST 6: Code & Docs Analysis ─────────────────────────────
def analyze_code_and_docs():
    header("TEST 6/6 — Code & Documentation Analysis")
    data = {}

    # README
    readme_path = REPO_PATH / "README.md"
    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8", errors="ignore")
        data["readme"] = content[:5000]
        ok(f"README.md found ({len(content)} chars)")

        # Check for F1/racing theme in README
        f1_keywords = ["f1", "formula", "race", "racing", "williams", "pit", "lap", "sprint", "grand prix"]
        f1_mentions = sum(1 for kw in f1_keywords if kw in content.lower())
        data["f1_in_readme"] = f1_mentions
        if f1_mentions >= 3:
            ok(f"Strong F1 theme in README ({f1_mentions} racing references)")
        elif f1_mentions > 0:
            warn(f"Light F1 theme in README ({f1_mentions} mentions) — strengthen this for judges")
        else:
            fail("No F1/racing theme in README — CRITICAL for this hackathon")
    else:
        data["readme"] = "No README found"
        fail("No README.md — required for submission")

    # Check for Airia integration
    airia_files = []
    for pattern in ["**/*.py", "**/*.ts", "**/*.tsx", "**/*.json", "**/*.yaml", "**/*.md"]:
        for f in REPO_PATH.rglob(pattern):
            skip = any(s in str(f) for s in ["node_modules", ".venv", ".git", "__pycache__"])
            if skip:
                continue
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                if "airia" in content.lower():
                    airia_files.append(str(f.relative_to(REPO_PATH)))
            except:
                pass
    data["airia_integration_files"] = airia_files[:5]
    if airia_files:
        ok(f"Airia references found in {len(airia_files)} file(s)")
    else:
        warn("No Airia platform references found")
        warn("IMPORTANT: This hackathon is specifically about building on Airia's platform")
        warn("At minimum, mention Airia integration in README and add an export/webhook endpoint")

    # Key source files for context
    key_files = [
        "apps/api/app/main.py",
        "apps/api/app/routers",
        "apps/web/src/App.tsx",
        "docs",
    ]
    snippets = []
    for rel in key_files:
        p = REPO_PATH / rel
        if p.is_file():
            snippets.append(f"--- {rel} ---\n" + p.read_text(encoding="utf-8", errors="ignore")[:1500])
        elif p.is_dir():
            for sub in list(p.rglob("*.py"))[:2] + list(p.rglob("*.md"))[:2]:
                try:
                    snippets.append(f"--- {sub.relative_to(REPO_PATH)} ---\n" + sub.read_text(encoding="utf-8", errors="ignore")[:800])
                except:
                    pass
    data["code_snippets"] = "\n\n".join(snippets[:6])

    # Check for screenshots/demo artifacts (judges love these)
    screenshot_count = len(list(REPO_PATH.rglob("*.png"))) + len(list(REPO_PATH.rglob("*.jpg")))
    data["screenshot_count"] = screenshot_count
    if screenshot_count >= 5:
        ok(f"Found {screenshot_count} screenshots/images — good for demo presentation")
    else:
        warn(f"Only {screenshot_count} screenshots — add more for a compelling submission")

    return data

# ── TEST 7: Airia Platform Evidence (live API checks) ────────────────────────
def test_airia_platform_evidence():
    """Collect live Airia platform evidence by calling backend endpoints."""
    header("TEST 7/7 — Airia Platform Integration Evidence")
    ev = {
        "airia_status": None,
        "compat_report": None,
        "compat_overall": None,
        "compat_checks_pass": 0,
        "compat_checks_total": 0,
        "mcp_tools": None,
        "mcp_tool_count": 0,
        "mcp_config_sha256": None,
        "race_weekend_stages": 0,
        "f1_theme_endpoints": [],
        "airia_endpoints": [],
    }

    base = BACKEND_URL

    # /api/airia/status
    try:
        r = requests.get(f"{base}/api/airia/status", timeout=5)
        if r.status_code == 200:
            ev["airia_status"] = r.json()
            ok(f"Airia status: {ev['airia_status'].get('status')}")
        else:
            warn(f"Airia status returned {r.status_code}")
    except Exception as e:
        warn(f"Airia status unreachable: {e}")

    # /api/airia/compat_report
    try:
        r = requests.get(f"{base}/api/airia/compat_report", timeout=10)
        if r.status_code == 200:
            ev["compat_report"] = r.json()
            ev["compat_overall"] = ev["compat_report"].get("overall")
            checks = ev["compat_report"].get("checks", [])
            ev["compat_checks_pass"] = sum(1 for c in checks if c.get("passed"))
            ev["compat_checks_total"] = len(checks)
            ok(f"Compat report: {ev['compat_overall']} ({ev['compat_checks_pass']}/{ev['compat_checks_total']} checks)")
        else:
            warn(f"Compat report returned {r.status_code}")
    except Exception as e:
        warn(f"Compat report unreachable: {e}")

    # /api/mcp/tools
    try:
        r = requests.get(f"{base}/api/mcp/tools", timeout=5)
        if r.status_code == 200:
            data = r.json()
            ev["mcp_tool_count"] = data.get("tool_count", 0)
            ev["mcp_tools"] = [t.get("name") for t in data.get("tools", [])]
            ok(f"MCP tools: {ev['mcp_tool_count']} tools available for Airia MCP Gateway")
        else:
            warn(f"MCP tools returned {r.status_code}")
    except Exception as e:
        warn(f"MCP tools unreachable: {e}")

    # /api/mcp/config
    try:
        r = requests.get(f"{base}/api/mcp/config", timeout=5)
        if r.status_code == 200:
            data = r.json()
            ev["mcp_config_sha256"] = data.get("config_sha256")
            ok(f"MCP Gateway config SHA256: {ev['mcp_config_sha256'][:16]}..." if ev["mcp_config_sha256"] else "MCP config generated (no sha256)")
        else:
            warn(f"MCP config returned {r.status_code}")
    except Exception as e:
        warn(f"MCP config unreachable: {e}")

    # /api/race-weekend/stages
    try:
        r = requests.get(f"{base}/api/race-weekend/stages", timeout=5)
        if r.status_code == 200:
            data = r.json()
            stages = data.get("stages", [])
            ev["race_weekend_stages"] = len(stages)
            ok(f"Race Weekend Stages: {ev['race_weekend_stages']} stages ({[s.get('key') for s in stages]})")
        else:
            warn(f"Race weekend stages returned {r.status_code}")
    except Exception as e:
        warn(f"Race weekend stages unreachable: {e}")

    # Check all F1/Airia themed endpoints
    try:
        r = requests.get(f"{base}/openapi.json", timeout=5)
        if r.status_code == 200:
            paths = list(r.json().get("paths", {}).keys())
            ev["f1_theme_endpoints"] = [p for p in paths if any(k in p.lower() for k in ["race", "lap", "pit", "f1", "telemetry", "weekend", "stage"])]
            ev["airia_endpoints"] = [p for p in paths if any(k in p.lower() for k in ["airia", "mcp", "bundle", "compat", "blueprint"])]
            ok(f"F1 theme endpoints: {len(ev['f1_theme_endpoints'])}")
            ok(f"Airia platform endpoints: {len(ev['airia_endpoints'])}")
    except Exception:
        pass

    return ev


# ── OBJECTIVE SCORE (deterministic, LLM-independent) ─────────────────────────
def compute_objective_score(backend, airia_ev, autonomy, tests, docs):
    """Deterministic objective score based on measurable facts.

    Returns a dict with per-dimension scores (0–10) and overall.
    """
    scores = {}

    # 1. Agent Autonomy (30%)
    # Signals: has_agent_loop, autonomy_score/4, test suite > 1000 tests
    auto_pts = 0
    if autonomy.get("has_agent_loop"):
        auto_pts += 3
    auto_pts += min(autonomy.get("autonomy_score", 0), 4) * 1.25  # 0–5
    if tests.get("passed", 0) >= 100:
        auto_pts += 1
    if tests.get("passed", 0) >= 1000:
        auto_pts += 1
    scores["agent_autonomy"] = round(min(auto_pts, 10.0), 1)

    # 2. Workflow Impact (25%)
    wf_pts = 0
    features = backend.get("core_features", {})
    for feat in ["document_ingestion", "reconciliation", "exceptions", "review_queue", "audit_trail", "agent"]:
        if features.get(feat):
            wf_pts += 1.2
    if tests.get("passed", 0) >= 500:
        wf_pts += 1
    scores["workflow_impact"] = round(min(wf_pts, 10.0), 1)

    # 3. F1 Theme Alignment (20%)
    f1_pts = 0
    f1_mentions = docs.get("f1_in_readme", 0)
    f1_pts += min(f1_mentions * 0.4, 3)  # up to 3 pts from README
    f1_eps = len(airia_ev.get("f1_theme_endpoints", []))
    f1_pts += min(f1_eps * 0.5, 3)       # up to 3 pts from endpoints
    if airia_ev.get("race_weekend_stages", 0) >= 6:
        f1_pts += 2                       # race weekend model
    if features.get("race_control"):
        f1_pts += 2                       # race control UI
    scores["f1_theme_alignment"] = round(min(f1_pts, 10.0), 1)

    # 4. Airia Platform (15%)
    airia_pts = 0
    compat = airia_ev.get("compat_overall")
    if compat == "PASS":
        airia_pts += 3
    checks_pass = airia_ev.get("compat_checks_pass", 0)
    airia_pts += min(checks_pass * 0.5, 4)   # up to 4 pts for check passes
    if airia_ev.get("mcp_tool_count", 0) >= 8:
        airia_pts += 2                       # MCP server with 8 tools
    airia_eps = len(airia_ev.get("airia_endpoints", []))
    airia_pts += min(airia_eps * 0.3, 2)     # up to 2 pts for endpoints
    if airia_ev.get("mcp_config_sha256"):
        airia_pts += 0.5                     # MCP config export
    scores["airia_platform"] = round(min(airia_pts, 10.0), 1)

    # 5. Demo Quality (10%)
    demo_pts = 0
    if docs.get("screenshot_count", 0) >= 10:
        demo_pts += 3
    elif docs.get("screenshot_count", 0) >= 3:
        demo_pts += 1
    if docs.get("airia_integration_files", []):
        demo_pts += 2
    readme = docs.get("readme", "")
    if len(readme) > 2000:
        demo_pts += 2
    if tests.get("pytest_passed"):
        demo_pts += 2
    if backend.get("running"):
        demo_pts += 1
    scores["demo_quality"] = round(min(demo_pts, 10.0), 1)

    # Weighted overall
    weights = {
        "agent_autonomy": 0.30,
        "workflow_impact": 0.25,
        "f1_theme_alignment": 0.20,
        "airia_platform": 0.15,
        "demo_quality": 0.10,
    }
    overall = sum(scores[k] * weights[k] for k in weights)
    scores["overall"] = round(overall, 2)

    return scores


# ── LLM JUDGE ────────────────────────────────────────────────
def judge_with_ollama(backend, frontend, workflow, autonomy, tests, docs, airia_ev=None):
    header("SENDING TO LOCAL LLM JUDGE")
    warn(f"Model: {OLLAMA_MODEL} | This may take 2-5 minutes...")

    if airia_ev is None:
        airia_ev = {}

    # Compute objective score first — include in prompt as hard evidence
    obj = compute_objective_score(backend, airia_ev, autonomy, tests, docs)
    ok(f"Objective score pre-computed: {obj.get('overall')}/10")

    # Build structured evidence facts (these are FACTS, not opinions)
    evidence_facts = f"""
=== HARD EVIDENCE FACTS (verified by automated checks — NOT opinions) ===

BACKEND:
- Running on port 8090: {backend.get('running')}
- Total API endpoints: {len(backend.get('endpoints', []))}
- Core features detected: {json.dumps(backend.get('core_features', {}), indent=2)}

AIRIA PLATFORM INTEGRATION:
- /api/airia/status: {airia_ev.get('airia_status', {}).get('status', 'NOT CALLED')}
- /api/airia/compat_report OVERALL: {airia_ev.get('compat_overall', 'UNKNOWN')}
- Compat checks passed: {airia_ev.get('compat_checks_pass', 0)} out of {airia_ev.get('compat_checks_total', 0)}
- MCP Server present: {'YES' if airia_ev.get('mcp_tool_count', 0) > 0 else 'NO'}
- MCP tool count (for Airia MCP Gateway): {airia_ev.get('mcp_tool_count', 0)}
- MCP tools: {airia_ev.get('mcp_tools', [])}
- MCP Gateway config sha256: {airia_ev.get('mcp_config_sha256', 'NOT GENERATED')}
- Airia-specific API endpoints: {airia_ev.get('airia_endpoints', [])}

F1 THEME:
- Race Weekend Stage Model endpoints: {'YES' if airia_ev.get('race_weekend_stages', 0) > 0 else 'NO'}
- Race Weekend stages count: {airia_ev.get('race_weekend_stages', 0)} (canonical model: qualifying→formation→pit_stop_1→safety_car→pit_stop_2→checkered_flag)
- F1-themed endpoints: {airia_ev.get('f1_theme_endpoints', [])}
- F1 mentions in README: {docs.get('f1_in_readme', 0)}

AGENT AUTONOMY:
- Has agent loop (perceive→decide→act): {autonomy.get('has_agent_loop')}
- Autonomy signals present: {json.dumps(autonomy.get('agent_signals', {}), indent=2)}
- Autonomy score (internal signals): {autonomy.get('autonomy_score')}/4

TESTS:
- pytest: {tests.get('passed', 0)} passed, {tests.get('failed', 0)} failed
- Test suite passing: {tests.get('pytest_passed')}

SCREENSHOTS/DEMOS:
- Screenshot count: {docs.get('screenshot_count', 0)}
- Airia integration files: {docs.get('airia_integration_files', [])}

OBJECTIVE SCORE (deterministic, pre-computed from facts above):
- Agent Autonomy:     {obj.get('agent_autonomy')}/10
- Workflow Impact:    {obj.get('workflow_impact')}/10
- F1 Theme:          {obj.get('f1_theme_alignment')}/10
- Airia Platform:    {obj.get('airia_platform')}/10
- Demo Quality:      {obj.get('demo_quality')}/10
- Weighted Overall:  {obj.get('overall')}/10
=== END HARD EVIDENCE ===
"""

    prompt = f"""You are a senior judge for the Airia "Race Beyond the Track" hackathon.
Hosted by Airia (official Williams F1 partner). $20,000 in prizes. Deadline: March 1, 2026.

{HACKATHON_CRITERIA}

== PROJECT: LedgerLive — Finance Ops Close Agent ==
Automated finance close workflow: document ingestion → OCR/extraction → reconciliation 
→ exception triage → HITL review → evidence binder → audit trail.
Uses an F1 Race Control metaphor: pit stops = checkpoints, safety car = fail-closed approvals,
telemetry = audit trail, court pack = stewards evidence, race weekend stages = close milestones.
Stack: FastAPI (port 8090), React/Vite, SQLite.

{evidence_facts}

README (first 3000 chars):
{docs.get('readme', '')[:3000]}

Compat report checks detail:
{json.dumps(airia_ev.get('compat_report', {}).get('checks', []), indent=2)[:2000] if airia_ev.get('compat_report') else 'Not available'}

== YOUR TASK ==
Study the HARD EVIDENCE FACTS above carefully. Score LedgerLive for THIS specific hackathon.

IMPORTANT SCORING RULES:
- The objective score above is pre-computed from verifiable facts. Your LLM score should be
  CLOSE to the objective score unless you have strong evidence to adjust it.
- If MCP Server is present with 8+ tools AND compat_report is PASS, Airia Platform >= 7.
- If Race Weekend stage model with 6 stages exists AND F1 endpoints exist, F1 Theme >= 7.5.
- If agent_loop is True AND 4000+ tests pass with perceive→decide→act pattern, Agent Autonomy >= 8.
- Always cite which evidence lines justify each subscore.

Respond ONLY with valid JSON (no markdown code fences, no extra text):
{{
  "current_score": <weighted average, float>,
  "breakdown": {{
    "agent_autonomy": <0.0-10.0, based on evidence>,
    "workflow_impact": <0.0-10.0, based on evidence>,
    "f1_theme_alignment": <0.0-10.0, based on evidence>,
    "airia_platform": <0.0-10.0, based on evidence>,
    "demo_quality": <0.0-10.0, based on evidence>
  }},
  "evidence_citations": {{
    "agent_autonomy": "<which evidence lines justify this score>",
    "workflow_impact": "<which evidence lines justify this score>",
    "f1_theme_alignment": "<which evidence lines justify this score>",
    "airia_platform": "<which evidence lines justify this score>",
    "demo_quality": "<which evidence lines justify this score>"
  }},
  "what_works": ["strength 1", "strength 2", "strength 3"],
  "critical_gaps": ["gap 1 with specific fix", "gap 2 with specific fix"],
  "f1_reframing_ideas": ["specific F1 improvement 1", "specific F1 improvement 2"],
  "airia_integration_plan": "<2-3 sentence concrete plan>",
  "fastest_wins_before_deadline": ["win 1 (<2h)", "win 2", "win 3"],
  "submission_ready": <true/false>,
  "judge_summary": "<honest 3-sentence assessment>"
}}"""

    try:
        response = client.chat.completions.create(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=2000
        )
        raw = response.choices[0].message.content.strip()

        # Strip markdown fences
        if "```" in raw:
            for part in raw.split("```"):
                part = part.strip().lstrip("json").strip()
                try:
                    result = json.loads(part)
                    result["_objective_score"] = obj
                    return result
                except:
                    pass

        result = json.loads(raw)
        result["_objective_score"] = obj
        return result

    except json.JSONDecodeError as e:
        fail(f"LLM returned invalid JSON: {e}")
        print(f"  Raw output (first 500): {raw[:500]}")
        # Fall back to objective score
        obj_result = {
            "current_score": obj["overall"],
            "breakdown": {
                "agent_autonomy": obj["agent_autonomy"],
                "workflow_impact": obj["workflow_impact"],
                "f1_theme_alignment": obj["f1_theme_alignment"],
                "airia_platform": obj["airia_platform"],
                "demo_quality": obj["demo_quality"],
            },
            "what_works": ["Objective scoring applied (LLM JSON parse failed)"],
            "critical_gaps": ["LLM returned malformed JSON — using objective score"],
            "f1_reframing_ideas": [],
            "airia_integration_plan": "Continue improving MCP + compat report",
            "fastest_wins_before_deadline": [],
            "submission_ready": obj["overall"] >= 8.5,
            "judge_summary": f"Objective score: {obj['overall']}/10 (LLM fallback)",
            "_objective_score": obj,
        }
        return obj_result
    except Exception as e:
        fail(f"Ollama failed: {e}")
        warn("Make sure Ollama is running: ollama serve")
        return None

    prompt = f"""You are a senior judge for the Airia "Race Beyond the Track" hackathon.
Hosted by Airia (official Williams F1 partner). $20,000 in prizes. Deadline: March 1, 2026.

{HACKATHON_CRITERIA}

== PROJECT: LedgerLive — Finance Ops Close Agent ==
Automated finance close workflow: document ingestion → OCR/extraction → reconciliation 
→ exception triage → HITL review → evidence binder → audit trail.
Stack: FastAPI (port 8090), React/Vite (port 4174), SQLite.

== TEST RESULTS ==

Backend API:
- Running: {backend.get('running')}
- Total endpoints: {len(backend.get('endpoints', []))}
- Core features present: {backend.get('core_features', {})}

Frontend:
- Running: {frontend.get('running')}
- Port: {frontend.get('port')}

Workflow Tests:
{json.dumps(workflow, indent=2)}

Agent Autonomy:
- Has agent loop: {autonomy.get('has_agent_loop')}
- Autonomy score: {autonomy.get('autonomy_score')}/4
- Signals: {autonomy.get('agent_signals', {})}

Test Suite:
- pytest passed: {tests.get('pytest_passed')}
- Tests: {tests.get('passed')} passed, {tests.get('failed')} failed

Documentation:
- F1 theme mentions in README: {docs.get('f1_in_readme', 0)}
- Airia integration files: {docs.get('airia_integration_files', [])}
- Screenshot count: {docs.get('screenshot_count', 0)}

README (first 2000 chars):
{docs.get('readme', '')[:2000]}

Code snippets:
{docs.get('code_snippets', '')[:2500]}

== YOUR TASK ==
Score LedgerLive for THIS specific hackathon. Key considerations:
1. The F1/racing theme is required — how well does a finance close agent map to race operations?
2. The platform is Airia's no-code agent builder — does this project integrate or demonstrate compatibility?
3. Agent autonomy is the #1 criterion — does LedgerLive act autonomously or require constant human input?
4. The deadline is March 1 — what are the FASTEST wins to improve the score?

Respond ONLY with valid JSON (no other text, no markdown fences):
{{
  "current_score": 7.0,
  "breakdown": {{
    "agent_autonomy": 6.0,
    "workflow_impact": 8.5,
    "f1_theme_alignment": 5.0,
    "airia_platform": 3.0,
    "demo_quality": 7.0
  }},
  "what_works": [
    "strength 1",
    "strength 2",
    "strength 3"
  ],
  "critical_gaps": [
    "gap 1 with specific fix",
    "gap 2 with specific fix"
  ],
  "f1_reframing_ideas": [
    "Specific idea to make LedgerLive feel F1-themed (e.g. rename reconciliation → pit stop sync)",
    "Another F1 angle specific to this project"
  ],
  "airia_integration_plan": "Concrete 2-3 sentence plan for how to connect LedgerLive to Airia's platform before March 1",
  "fastest_wins_before_deadline": [
    "Thing you can do in <2 hours that would most improve your score",
    "Second fastest win",
    "Third fastest win"
  ],
  "submission_ready": false,
  "judge_summary": "Honest 3-sentence assessment for this specific hackathon."
}}"""

    try:
        response = client.chat.completions.create(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=2000
        )
        raw = response.choices[0].message.content.strip()

        # Strip markdown fences
        if "```" in raw:
            for part in raw.split("```"):
                part = part.strip().lstrip("json").strip()
                try:
                    return json.loads(part)
                except:
                    pass

        return json.loads(raw)

    except json.JSONDecodeError as e:
        fail(f"LLM returned invalid JSON: {e}")
        print(f"  Raw output (first 500): {raw[:500]}")
        return None
    except Exception as e:
        fail(f"Ollama failed: {e}")
        warn("Make sure Ollama is running: ollama serve")
        return None

# ── PRINT RESULTS ─────────────────────────────────────────────
def print_results(score_data):
    if not score_data:
        fail("No score generated.")
        return

    s = score_data.get("current_score", 0)
    color = Fore.GREEN if s >= 8 else (Fore.YELLOW if s >= 6 else Fore.RED)

    header("HACKATHON EVALUATION — LEDGERLIVE × AIRIA/WILLIAMS F1")
    print(f"\n  {color}OVERALL SCORE: {s}/10{Style.RESET_ALL}")
    print(f"  {Fore.RED}⏰ DEADLINE: March 1, 2026 11:59 PM AEDT{Style.RESET_ALL}")

    bd = score_data.get("breakdown", {})
    print(f"\n  Score Breakdown:")
    print(f"    Agent Autonomy:       {bd.get('agent_autonomy', '?')}/10  ← most important")
    print(f"    Workflow Impact:      {bd.get('workflow_impact', '?')}/10")
    print(f"    F1 Theme Alignment:   {bd.get('f1_theme_alignment', '?')}/10")
    print(f"    Airia Platform:       {bd.get('airia_platform', '?')}/10")
    print(f"    Demo Quality:         {bd.get('demo_quality', '?')}/10")

    works = score_data.get("what_works", [])
    if works:
        print(f"\n  {Fore.GREEN}✓ STRENGTHS:{Style.RESET_ALL}")
        for w in works:
            print(f"    • {w}")

    gaps = score_data.get("critical_gaps", [])
    if gaps:
        print(f"\n  {Fore.RED}✗ CRITICAL GAPS:{Style.RESET_ALL}")
        for g in gaps:
            print(f"    • {g}")

    f1_ideas = score_data.get("f1_reframing_ideas", [])
    if f1_ideas:
        print(f"\n  {Fore.CYAN}🏎️  F1 REFRAMING IDEAS:{Style.RESET_ALL}")
        for idea in f1_ideas:
            print(f"    • {idea}")

    airia_plan = score_data.get("airia_integration_plan", "")
    if airia_plan:
        print(f"\n  {Fore.CYAN}🔗 AIRIA INTEGRATION PLAN:{Style.RESET_ALL}")
        print(f"  {airia_plan}")

    fastest = score_data.get("fastest_wins_before_deadline", [])
    if fastest:
        print(f"\n  {Fore.YELLOW}⚡ FASTEST WINS BEFORE MARCH 1:{Style.RESET_ALL}")
        for i, win in enumerate(fastest, 1):
            print(f"    {i}. {win}")

    summary = score_data.get("judge_summary", "")
    if summary:
        print(f"\n  {Fore.CYAN}Judge Summary:{Style.RESET_ALL}")
        print(f"  {summary}")

    ready = score_data.get("submission_ready", False)
    status = f"{Fore.GREEN}YES — Submit now!{Style.RESET_ALL}" if ready else f"{Fore.RED}NOT YET — fix gaps first{Style.RESET_ALL}"
    print(f"\n  Submission Ready: {status}")
    print(f"\n{'='*62}\n")

# ── MAIN ──────────────────────────────────────────────────────
if __name__ == "__main__":
    header("LedgerLive — Airia/Williams F1 Hackathon Auto-Judge")
    print(f"  Repo     : {REPO_PATH}")
    print(f"  Backend  : {BACKEND_URL}")
    print(f"  Frontend : {FRONTEND_URL}")
    print(f"  Model    : {OLLAMA_MODEL}")
    print(f"  {Fore.RED}Deadline : March 1, 2026 11:59 PM AEDT{Style.RESET_ALL}")

    if not REPO_PATH.exists():
        fail(f"Repo not found at {REPO_PATH}")
        warn("Set path: $env:LEDGER_REPO_PATH = 'C:\\Aarav\\ledgerlive'")
        sys.exit(1)

    procs = []
    try:
        procs = start_services()

        backend_results  = test_backend()
        frontend_results = test_frontend()
        workflow_results = test_core_workflow(backend_results)
        autonomy_results = test_agent_autonomy(backend_results)
        test_results     = run_existing_tests()
        docs_data        = analyze_code_and_docs()
        airia_ev         = test_airia_platform_evidence()

        score_data = judge_with_ollama(
            backend_results, frontend_results,
            workflow_results, autonomy_results,
            test_results, docs_data, airia_ev
        )

        print_results(score_data)

        # Save results
        out = {
            "backend": backend_results,
            "frontend": frontend_results,
            "workflow": workflow_results,
            "autonomy": autonomy_results,
            "tests": test_results,
            "airia_platform_evidence": airia_ev,
            "objective_score": compute_objective_score(backend_results, airia_ev, autonomy_results, test_results, docs_data),
            "llm_score": score_data,
        }
        out_file = REPO_PATH / "hackathon_evaluation_airia.json"
        with open(out_file, "w") as f:
            json.dump(out, f, indent=2)
        ok(f"Results saved to: {out_file}")

    finally:
        for p in procs:
            try:
                p.terminate()
            except:
                pass
        ok("Cleanup done")
