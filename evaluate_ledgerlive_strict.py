# ============================================================
# evaluate_ledgerlive_strict.py
# BRUTAL HACKATHON JUDGE — No mercy mode
# Airia "Race Beyond the Track" — Williams F1 / Atlassian
#
# This judge grades like a VC partner who has seen 500 demos.
# It does NOT reward:
#   - Having lots of endpoints (anyone can scaffold)
#   - Passing unit tests (table stakes)
#   - Screenshot counts
#   - Keywords in README
#
# It ONLY rewards:
#   - Live data flowing end-to-end RIGHT NOW
#   - A demo story a non-technical F1 judge would remember
#   - Genuine AI decisions (not CRUD with an LLM bolted on)
#   - Something that would make Williams Racing say "we need this"
#   - Airia platform actually callable (not just referenced)
# ============================================================

import subprocess, requests, json, time, sys, os, re
from pathlib import Path
from datetime import datetime, timezone

try:
    from openai import OpenAI
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "openai", "colorama", "requests"], check=True)
    from openai import OpenAI
    from colorama import Fore, Style, init
    init(autoreset=True)

# ── CONFIG ───────────────────────────────────────────────────
REPO_PATH    = Path(os.getenv("LEDGER_REPO_PATH", r"C:\Aarav\ledgerlive"))
BACKEND_URL  = "http://127.0.0.1:8090"
FRONTEND_URL = "http://127.0.0.1:4174"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "devstral")

client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")

# ── HELPERS ──────────────────────────────────────────────────
def hdr(text):
    print(f"\n{Fore.CYAN}{'='*64}\n  {text}\n{'='*64}{Style.RESET_ALL}")

def ok(m):    print(f"  {Fore.GREEN}✓ {m}{Style.RESET_ALL}")
def fail(m):  print(f"  {Fore.RED}✗ {m}{Style.RESET_ALL}")
def warn(m):  print(f"  {Fore.YELLOW}⚠ {m}{Style.RESET_ALL}")
def score_line(label, val, max_val, note=""):
    bar = "█" * int(val) + "░" * (max_val - int(val))
    color = Fore.GREEN if val >= max_val*0.8 else (Fore.YELLOW if val >= max_val*0.5 else Fore.RED)
    print(f"  {color}{label:<32} {bar} {val:.1f}/{max_val}  {note}{Style.RESET_ALL}")

# ── HARD EVIDENCE TESTS ───────────────────────────────────────
# These are binary: either it works RIGHT NOW or it doesn't.
# No partial credit for "we plan to" or "it's in the code".

def test_live_data_flow():
    """Does real data actually move through the system end to end?"""
    hdr("EVIDENCE TEST 1 — Live Data Flow (Binary Pass/Fail)")
    evidence = {}

    # 1a. Can we actually ingest a document and get back extracted data?
    try:
        # Try posting a minimal fake document
        fake_doc = b"%PDF-1.4 fake document content for testing"
        r = requests.post(
            f"{BACKEND_URL}/api/documents",
            files={"file": ("test.pdf", fake_doc, "application/pdf")},
            data={"name": "test_invoice.pdf"},
            timeout=10
        )
        if r.status_code in [200, 201, 202]:
            doc_data = r.json()
            evidence["ingestion_works"] = True
            evidence["doc_id"] = doc_data.get("id") or doc_data.get("document_id") or "unknown"
            ok(f"Document ingestion: LIVE — got doc_id={evidence['doc_id']}")
        else:
            evidence["ingestion_works"] = False
            fail(f"Document ingestion returned {r.status_code}: {r.text[:200]}")
    except Exception as e:
        evidence["ingestion_works"] = False
        fail(f"Document ingestion DEAD: {e}")

    # 1b. Can we retrieve documents list with actual data?
    try:
        r = requests.get(f"{BACKEND_URL}/api/documents", timeout=5)
        docs = r.json()
        count = len(docs) if isinstance(docs, list) else docs.get("total", docs.get("count", 0))
        if isinstance(count, int) and count > 0:
            evidence["has_real_documents"] = True
            ok(f"Documents in DB: {count} real records")
        else:
            evidence["has_real_documents"] = False
            warn(f"Documents endpoint returns empty/zero — no seed data? Response: {str(docs)[:100]}")
    except Exception as e:
        evidence["has_real_documents"] = False
        fail(f"Cannot read documents: {e}")

    # 1c. Do reconciliations have actual results (not empty)?
    try:
        r = requests.get(f"{BACKEND_URL}/api/reconciliations", timeout=5)
        data = r.json()
        count = len(data) if isinstance(data, list) else data.get("total", 0)
        if count > 0:
            evidence["has_reconciliation_data"] = True
            ok(f"Reconciliation records: {count}")
        else:
            evidence["has_reconciliation_data"] = False
            warn("Reconciliation DB is EMPTY — judges will see blank screens in demo")
    except Exception as e:
        evidence["has_reconciliation_data"] = False
        fail(f"Cannot read reconciliations: {e}")

    # 1d. Does the OCR job pipeline actually run asynchronously?
    try:
        r = requests.get(f"{BACKEND_URL}/api/ocr-jobs/stats", timeout=5)
        stats = r.json()
        evidence["ocr_stats"] = stats
        # Check if there are any completed jobs (proves it ran)
        completed = stats.get("completed", stats.get("done", 0))
        if completed > 0:
            ok(f"OCR pipeline has run: {completed} completed jobs")
            evidence["ocr_has_run"] = True
        else:
            warn(f"OCR pipeline shows 0 completed jobs — has it ever actually run? Stats: {stats}")
            evidence["ocr_has_run"] = False
    except Exception as e:
        evidence["ocr_has_run"] = False
        warn(f"OCR stats endpoint: {e}")

    # 1e. Exceptions — are there any real ones with AI classifications?
    try:
        r = requests.get(f"{BACKEND_URL}/api/exceptions", timeout=5)
        data = r.json()
        items = data if isinstance(data, list) else data.get("items", data.get("exceptions", []))
        if len(items) > 0:
            sample = items[0]
            has_ai = any(k in str(sample).lower() for k in ["confidence", "severity", "classification", "reason", "ai_", "model"])
            if has_ai:
                ok(f"Exceptions: {len(items)} found WITH AI classification fields")
                evidence["exceptions_have_ai"] = True
            else:
                warn(f"Exceptions: {len(items)} found but NO AI classification fields — just CRUD")
                evidence["exceptions_have_ai"] = False
        else:
            warn("Exception list is EMPTY — judges need to see real exceptions triaged")
            evidence["exceptions_have_ai"] = False
    except Exception as e:
        evidence["exceptions_have_ai"] = False
        fail(f"Cannot read exceptions: {e}")

    return evidence


def test_ai_decision_quality():
    """Is the AI making real decisions or is it just routing/labeling?"""
    hdr("EVIDENCE TEST 2 — AI Decision Quality (The Hard Part)")
    evidence = {}

    # 2a. Does the agent endpoint return a real reasoning trace?
    agent_endpoints = [
        "/api/workflows",
        "/api/agent/run",
        "/api/agent/status",
        "/api/pipeline/run",
    ]
    for ep in agent_endpoints:
        try:
            r = requests.get(f"{BACKEND_URL}{ep}", timeout=5)
            if r.status_code == 200:
                data = r.json()
                # Look for reasoning/explanation fields
                data_str = json.dumps(data).lower()
                has_reasoning = any(k in data_str for k in [
                    "reasoning", "explanation", "rationale", "confidence",
                    "because", "therefore", "analysis", "decision"
                ])
                evidence["workflow_endpoint"] = ep
                evidence["has_reasoning"] = has_reasoning
                if has_reasoning:
                    ok(f"{ep}: returns data WITH reasoning/explanation fields")
                else:
                    warn(f"{ep}: returns data but NO reasoning — agent looks like a scheduler, not a thinker")
                break
        except:
            pass
    else:
        evidence["has_reasoning"] = False
        fail("No working workflow/agent endpoint found that returns reasoning")

    # 2b. Try to trigger an actual AI decision and time it
    decision_endpoints = [
        ("/api/exceptions/{id}/resolve", "POST"),
        ("/api/reviews/{id}/decide", "POST"),
        ("/api/reconciliations/{id}/approve", "POST"),
    ]
    # Get a real ID first
    try:
        r = requests.get(f"{BACKEND_URL}/api/exceptions?limit=1", timeout=5)
        data = r.json()
        items = data if isinstance(data, list) else data.get("items", [])
        if items:
            real_id = items[0].get("id", items[0].get("exception_id", "1"))
            start = time.time()
            r2 = requests.post(
                f"{BACKEND_URL}/api/exceptions/{real_id}/resolve",
                json={"method": "auto", "reasoning": "test"},
                timeout=15
            )
            elapsed = time.time() - start
            if r2.status_code in [200, 201]:
                evidence["can_resolve_exception"] = True
                evidence["resolution_time_ms"] = round(elapsed * 1000)
                ok(f"Exception auto-resolve: WORKS in {evidence['resolution_time_ms']}ms")
            else:
                evidence["can_resolve_exception"] = False
                warn(f"Exception resolve returned {r2.status_code}: {r2.text[:150]}")
        else:
            evidence["can_resolve_exception"] = False
            warn("No exceptions to test resolution against — seed data missing")
    except Exception as e:
        evidence["can_resolve_exception"] = False
        warn(f"Exception resolve test failed: {e}")

    # 2c. Does the LLM actually get called? (check for LLM-related config/endpoints)
    llm_signals = []
    for ep in ["/api/agent/config", "/api/settings", "/api/config", "/api/health"]:
        try:
            r = requests.get(f"{BACKEND_URL}{ep}", timeout=4)
            if r.status_code == 200:
                text = r.text.lower()
                if any(k in text for k in ["openai", "anthropic", "ollama", "llm", "gpt", "claude", "model"]):
                    llm_signals.append(ep)
        except:
            pass

    # Also check source code
    for pattern in ["**/*.py"]:
        for f in REPO_PATH.rglob(pattern):
            if any(s in str(f) for s in [".venv", "__pycache__", ".git"]):
                continue
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                if any(k in content for k in ["openai.chat", "anthropic.messages", "ollama", "litellm", "langchain"]):
                    llm_signals.append(str(f.name))
                    break
            except:
                pass
        if llm_signals:
            break

    evidence["llm_actually_called"] = bool(llm_signals)
    if llm_signals:
        ok(f"LLM is actually invoked: {llm_signals[:3]}")
    else:
        fail("NO LLM calls detected — this might just be rule-based automation, not AI")
        fail("Judges WILL ask 'where is the AI?' — you need a real model making decisions")

    return evidence


def test_demo_story():
    """Can a non-technical Williams F1 judge follow a 3-minute demo without confusion?"""
    hdr("EVIDENCE TEST 3 — Demo Story & F1 Narrative Quality")
    evidence = {}

    # 3a. Race weekend workflow — does it actually have stages?
    try:
        r = requests.get(f"{BACKEND_URL}/api/race-control", timeout=5)
        if r.status_code == 200:
            data = r.json()
            evidence["race_control_live"] = True
            ok(f"Race control dashboard: LIVE — {str(data)[:150]}")
        else:
            r2 = requests.get(f"{BACKEND_URL}/api/f1", timeout=5)
            evidence["race_control_live"] = r2.status_code == 200
            if not evidence["race_control_live"]:
                fail("Race control endpoint returns non-200 — F1 theme is just cosmetic naming")
    except:
        evidence["race_control_live"] = False
        fail("Race control endpoint unreachable")

    # 3b. Check if the UI has a coherent demo flow (look at frontend source)
    frontend_src = REPO_PATH / "apps" / "web" / "src"
    if frontend_src.exists():
        all_components = list(frontend_src.rglob("*.tsx")) + list(frontend_src.rglob("*.jsx"))
        component_names = [f.stem.lower() for f in all_components]
        
        demo_critical = {
            "dashboard": any("dashboard" in n for n in component_names),
            "race_themed_view": any(k in n for n in component_names for k in ["race", "f1", "pit", "lap", "circuit"]),
            "document_view": any(k in n for n in component_names for k in ["document", "upload", "ingest"]),
            "exceptions_view": any(k in n for n in component_names for k in ["exception", "triage", "alert"]),
            "audit_view": any(k in n for n in component_names for k in ["audit", "trail", "log", "history"]),
        }
        evidence["ui_components"] = demo_critical

        missing = [k for k, v in demo_critical.items() if not v]
        present = [k for k, v in demo_critical.items() if v]
        for p in present:
            ok(f"UI component '{p}': present")
        for m in missing:
            fail(f"UI component '{m}': MISSING — demo will have a dead end")

        evidence["ui_completeness"] = len(present) / len(demo_critical)
    else:
        evidence["ui_completeness"] = 0
        fail("Frontend src not found")

    # 3c. Does the demo have a narrative hook? (check for demo/walkthrough docs)
    demo_docs = []
    for name in ["DEMO.md", "WALKTHROUGH.md", "PITCH.md", "demo.md", "HACKATHON.md", "SUBMISSION.md"]:
        p = REPO_PATH / name
        if p.exists():
            demo_docs.append(name)
            ok(f"Demo doc found: {name}")

    evidence["has_demo_script"] = bool(demo_docs)
    if not demo_docs:
        fail("No DEMO.md or walkthrough doc — you have NO scripted demo narrative")
        fail("Without this, judges will wander around confused during the live demo")

    # 3d. Is there a video demo? (judges weight this heavily)
    video_files = list(REPO_PATH.rglob("*.mp4")) + list(REPO_PATH.rglob("*.webm")) + list(REPO_PATH.rglob("*.mov"))
    evidence["has_video"] = bool(video_files)
    if video_files:
        ok(f"Video demo found: {video_files[0].name}")
    else:
        fail("NO video demo — Airia hackathons heavily weight demo presentation")
        fail("Record a 90-second Loom/OBS walkthrough before March 1")

    return evidence


def test_submission_completeness():
    """Would this submission be disqualified or penalized on technicalities?"""
    hdr("EVIDENCE TEST 4 — Submission Completeness (DQ Risk)")
    evidence = {}

    # 4a. README quality — not word count, actual content
    readme = REPO_PATH / "README.md"
    if readme.exists():
        content = readme.read_text(encoding="utf-8", errors="ignore")
        checks = {
            "has_one_liner_pitch":    bool(re.search(r"(what is|about|overview|pitch)", content[:500], re.I)),
            "has_setup_instructions": bool(re.search(r"(install|setup|getting started|quick start|run)", content, re.I)),
            "has_architecture_diagram": ("```" in content or "diagram" in content.lower() or "architecture" in content.lower()),
            "has_airia_mention":      "airia" in content.lower(),
            "has_williams_f1_mention": any(k in content.lower() for k in ["williams", "f1", "formula", "race"]),
            "has_screenshots_in_readme": ("![" in content or "png" in content.lower() or "screenshot" in content.lower()),
            "has_license":            bool(re.search(r"(license|mit|apache|gpl)", content, re.I)),
            "under_5000_chars":       len(content) < 5000,  # too short = bad
        }
        evidence["readme_checks"] = checks
        for k, v in checks.items():
            if v:
                ok(f"README: {k}")
            else:
                warn(f"README MISSING: {k}")
        evidence["readme_score"] = sum(checks.values()) / len(checks)
    else:
        evidence["readme_score"] = 0
        fail("No README.md — automatic disqualification risk")

    # 4b. Does the repo have a clear project structure or is it a mess?
    root_files = [f.name for f in REPO_PATH.iterdir() if f.is_file()]
    clutter_score = sum(1 for f in root_files if f.endswith((".log", ".tmp", ".bak")))
    mystery_pngs  = len([f for f in root_files if f.startswith("test-") and f.endswith(".png")])

    if mystery_pngs > 10:
        warn(f"{mystery_pngs} test-*.png files in root — looks like debugging artifacts, clean this up")
        evidence["repo_is_clean"] = False
    else:
        evidence["repo_is_clean"] = True
        ok("Repo root looks clean")

    # 4c. Can someone run this in under 5 minutes from a fresh clone?
    has_makefile     = (REPO_PATH / "Makefile").exists()
    has_docker       = any(REPO_PATH.rglob("docker-compose*.yml"))
    has_setup_script = any(REPO_PATH.rglob("setup.sh")) or any(REPO_PATH.rglob("setup.ps1"))
    has_env_example  = any(REPO_PATH.rglob(".env.example")) or any(REPO_PATH.rglob("*.env.example"))

    evidence["onboarding"] = {
        "makefile": has_makefile,
        "docker_compose": has_docker,
        "setup_script": has_setup_script,
        "env_example": has_env_example,
    }

    if has_makefile:
        ok("Makefile present — `make run` onboarding possible")
    else:
        warn("No Makefile — new judges can't run this in one command")

    if not has_env_example:
        fail("No .env.example — judges won't know what env vars are needed")

    return evidence


def test_airia_real_integration():
    """Is Airia actually integrated or just mentioned 89 times in comments?"""
    hdr("EVIDENCE TEST 5 — Airia Integration (Real vs Fake)")
    evidence = {}

    # 5a. Can Airia's platform actually CALL this backend?
    # Airia needs: webhook endpoints, MCP tools, or REST APIs with auth
    webhook_endpoints = []
    mcp_endpoints = []
    try:
        r = requests.get(f"{BACKEND_URL}/openapi.json", timeout=5)
        spec = r.json()
        paths = list(spec.get("paths", {}).keys())

        webhook_endpoints = [p for p in paths if any(k in p.lower() for k in ["webhook", "callback", "hook", "notify"])]
        mcp_endpoints     = [p for p in paths if "mcp" in p.lower()]
        airia_endpoints   = [p for p in paths if "airia" in p.lower()]

        evidence["webhook_endpoints"] = webhook_endpoints
        evidence["mcp_endpoints"]     = mcp_endpoints
        evidence["airia_endpoints"]   = airia_endpoints

        if webhook_endpoints:
            ok(f"Webhook endpoints (Airia can trigger): {webhook_endpoints[:3]}")
        else:
            fail("NO webhook/callback endpoints — Airia cannot trigger your agent autonomously")
            fail("Add POST /webhook/airia that accepts Airia's agent call payload")

        if mcp_endpoints:
            ok(f"MCP endpoints: {mcp_endpoints[:3]}")
        else:
            warn("No MCP endpoints — Airia's native integration path uses MCP tools")

        if airia_endpoints:
            ok(f"Airia-specific endpoints: {airia_endpoints[:5]}")
        else:
            warn("No /airia/* endpoints — integration looks superficial")

    except Exception as e:
        fail(f"Could not check integration endpoints: {e}")

    # 5b. Check if Airia client is actually instantiated in code (not just imported)
    airia_actually_used = False
    for f in (REPO_PATH / "apps" / "api").rglob("*.py"):
        if any(s in str(f) for s in [".venv", "__pycache__"]):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            # Look for actual API calls, not just imports or comments
            if re.search(r"airia\.(client|api|agent|send|call|post|get)\(", content, re.I):
                airia_actually_used = True
                ok(f"Airia client ACTUALLY CALLED in: {f.name}")
                break
            elif re.search(r"requests\.(post|get).*airia", content, re.I):
                airia_actually_used = True
                ok(f"HTTP call to Airia detected in: {f.name}")
                break
        except:
            pass

    evidence["airia_actually_called"] = airia_actually_used
    if not airia_actually_used:
        fail("Airia is referenced in 89 files but NEVER actually called")
        fail("Having 'airia' in comments/strings is not integration — judges will ask for a live demo")
        fail("At minimum: POST to Airia's webhook with your agent result after each close cycle")

    return evidence


def compute_strict_score(live, ai, demo, submission, airia):
    """Weighted scoring — no bonus points for scaffolding."""
    scores = {}

    # CRITERION 1: Agent Autonomy (30%) — harshest
    autonomy_pts = 0
    if live.get("ingestion_works"):        autonomy_pts += 1.5
    if live.get("has_real_documents"):     autonomy_pts += 0.5
    if live.get("ocr_has_run"):            autonomy_pts += 1.5
    if live.get("exceptions_have_ai"):     autonomy_pts += 2.0
    if ai.get("has_reasoning"):            autonomy_pts += 2.0
    if ai.get("can_resolve_exception"):    autonomy_pts += 1.5
    if ai.get("llm_actually_called"):      autonomy_pts += 1.0
    scores["agent_autonomy"] = min(autonomy_pts, 10.0)

    # CRITERION 2: Workflow Impact (25%)
    workflow_pts = 0
    if live.get("ingestion_works"):               workflow_pts += 2.0
    if live.get("has_reconciliation_data"):       workflow_pts += 2.0
    if live.get("exceptions_have_ai"):            workflow_pts += 2.0
    if ai.get("can_resolve_exception"):           workflow_pts += 2.0
    if submission.get("readme_score", 0) > 0.7:  workflow_pts += 2.0
    scores["workflow_impact"] = min(workflow_pts, 10.0)

    # CRITERION 3: F1 Theme (20%) — must feel native, not bolted on
    f1_pts = 0
    if demo.get("race_control_live"):                         f1_pts += 3.0
    if demo.get("ui_components", {}).get("race_themed_view"): f1_pts += 2.5
    if submission.get("readme_checks", {}).get("has_williams_f1_mention"): f1_pts += 1.5
    if demo.get("has_demo_script"):                           f1_pts += 2.0  # race-day narrative
    if demo.get("ui_completeness", 0) >= 0.8:                 f1_pts += 1.0
    scores["f1_theme"] = min(f1_pts, 10.0)

    # CRITERION 4: Airia Platform (15%) — real integration only
    airia_pts = 0
    if airia.get("webhook_endpoints"):               airia_pts += 3.0
    if airia.get("mcp_endpoints"):                   airia_pts += 3.0
    if airia.get("airia_actually_called"):            airia_pts += 3.0
    if airia.get("airia_endpoints"):                 airia_pts += 1.0
    scores["airia_platform"] = min(airia_pts, 10.0)

    # CRITERION 5: Demo Quality (10%) — can you win in 3 minutes?
    demo_pts = 0
    if demo.get("has_video"):                            demo_pts += 4.0  # huge weight
    if demo.get("has_demo_script"):                      demo_pts += 3.0
    if demo.get("ui_completeness", 0) >= 0.8:            demo_pts += 2.0
    if submission.get("repo_is_clean"):                  demo_pts += 1.0
    scores["demo_quality"] = min(demo_pts, 10.0)

    # Weighted final
    weights = {
        "agent_autonomy": 0.30,
        "workflow_impact": 0.25,
        "f1_theme":        0.20,
        "airia_platform":  0.15,
        "demo_quality":    0.10,
    }
    final = sum(scores[k] * weights[k] for k in scores)
    return final, scores


def brutal_llm_judgment(live, ai, demo, submission, airia, computed_score, computed_breakdown):
    """Ask the LLM to be a harsh VC-style judge, not a cheerleader."""
    hdr("LLM BRUTAL JUDGE")
    warn(f"Model: {OLLAMA_MODEL} — instructed to be maximally critical...")

    # Deadline urgency
    now_utc = datetime.now(timezone.utc)
    # March 1 11:59 PM AEDT = March 1 12:59 PM UTC
    deadline_utc = datetime(2026, 3, 1, 12, 59, 0, tzinfo=timezone.utc)
    hours_left = max(0, (deadline_utc - now_utc).total_seconds() / 3600)

    prompt = f"""You are a brutally honest hackathon judge. You are a VC partner who has seen 500 hackathon demos.
You do NOT give participation trophies. You do NOT soften feedback.
You have watched Williams F1 operate a $300M racing team. You know what "good" looks like.
You are judging for Airia — an AI agent platform company — who wants to see REAL agent autonomy.

HACKATHON: Airia "Race Beyond the Track" — Williams F1 / Atlassian
DEADLINE: {hours_left:.0f} hours from now
PRIZE: $20,000 USD. Only 1 winner.

PROJECT: LedgerLive — Finance Ops Close Agent
Stack: FastAPI :8090, React/Vite :4174, SQLite

== HARD EVIDENCE (what actually works right now) ==

Live Data Flow:
- Document ingestion works live: {live.get('ingestion_works')}
- Real documents in DB: {live.get('has_real_documents')} 
- OCR pipeline has actually run: {live.get('ocr_has_run')}
- Exceptions have AI classification: {live.get('exceptions_have_ai')}
- Reconciliation data exists: {live.get('has_reconciliation_data')}

AI Decision Quality:
- Agent returns reasoning/explanation: {ai.get('has_reasoning')}
- Can actually resolve an exception live: {ai.get('can_resolve_exception')}
- LLM is actually called (not just rule-based): {ai.get('llm_actually_called')}
- Resolution time: {ai.get('resolution_time_ms', 'N/A')}ms

Demo Story:
- Race control dashboard live: {demo.get('race_control_live')}
- Has scripted demo narrative (DEMO.md): {demo.get('has_demo_script')}
- Has video demo: {demo.get('has_video')}
- UI completeness: {demo.get('ui_completeness', 0)*100:.0f}%
- UI components present: {demo.get('ui_components', {})}

Submission Quality:
- README completeness: {submission.get('readme_score', 0)*100:.0f}%
- README checks: {submission.get('readme_checks', {})}
- Repo is clean: {submission.get('repo_is_clean')}
- Has .env.example: {submission.get('onboarding', {}).get('env_example')}
- Has Makefile: {submission.get('onboarding', {}).get('makefile')}

Airia Integration (REAL vs FAKE):
- Webhook endpoints that Airia can call: {airia.get('webhook_endpoints', [])}
- MCP tool endpoints: {airia.get('mcp_endpoints', [])}
- Airia client actually called in code: {airia.get('airia_actually_called')}
- Airia-specific endpoints: {len(airia.get('airia_endpoints', []))}

== COMPUTED SCORE (evidence-based) ==
Overall: {computed_score:.1f}/10
{json.dumps(computed_breakdown, indent=2)}

== YOUR JOB ==
You are NOT allowed to be encouraging. You are NOT allowed to say "great foundation".
You must answer these exact questions with ruthless honesty:

1. If you were a Williams F1 CFO watching a 3-minute demo RIGHT NOW, would you remember this project tomorrow? Why or why not?
2. What is the single most likely reason this project does NOT win?
3. What are the top 3 things that, if fixed in the next {hours_left:.0f} hours, would most change the outcome?
4. Is the AI actually doing anything a simple Python script couldn't do? Be specific.
5. Does the F1 theme feel real or is it just renamed buttons?

Respond ONLY as valid JSON (no markdown, no preamble):
{{
  "overall_score": {computed_score:.1f},
  "breakdown": {json.dumps(computed_breakdown)},
  "would_williams_remember_it": false,
  "why_it_loses": "Single most likely reason this project does not win — be brutally specific",
  "top_3_fixes": [
    "Fix 1 — specific, doable in <{int(hours_left/3)} hours, with exact implementation detail",
    "Fix 2 — specific, doable in <{int(hours_left/3)} hours",
    "Fix 3 — specific, doable in <{int(hours_left/3)} hours"
  ],
  "is_ai_real_or_fake": "Honest assessment: is the AI making decisions a Python if-else couldn't make?",
  "f1_theme_honest_take": "Is the F1 theme genuine or cosmetic? What would make it feel real?",
  "submission_ready": false,
  "brutal_summary": "One paragraph. No softening. What does this project need to go from where it is to winning $20,000?"
}}"""

    try:
        response = client.chat.completions.create(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": "You are a brutal, honest hackathon judge. You never soften feedback. You give specific, actionable criticism. You respond only in valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.05,
            max_tokens=2500
        )
        raw = response.choices[0].message.content.strip()

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
        print(f"  Raw: {raw[:600]}")
        return None
    except Exception as e:
        fail(f"Ollama failed: {e}")
        warn("Run: ollama serve   (in a separate terminal)")
        return None


def print_brutal_results(result, computed_score, breakdown):
    if not result:
        result = {}

    s = result.get("overall_score", computed_score)
    color = Fore.GREEN if s >= 8 else (Fore.YELLOW if s >= 6 else Fore.RED)

    hdr("BRUTAL EVALUATION RESULTS — LEDGERLIVE × AIRIA/WILLIAMS F1")
    print(f"\n  {color}EVIDENCE-BASED SCORE: {s:.1f}/10{Style.RESET_ALL}")
    print(f"  (This score requires live proof. No credit for scaffolding.)\n")

    print(f"  Weighted Breakdown:")
    score_line("Agent Autonomy      (30%)", breakdown.get("agent_autonomy", 0), 10, "← hardest to fake")
    score_line("Workflow Impact     (25%)", breakdown.get("workflow_impact", 0), 10)
    score_line("F1 Theme Alignment  (20%)", breakdown.get("f1_theme", 0), 10)
    score_line("Airia Platform      (15%)", breakdown.get("airia_platform", 0), 10, "← real calls only")
    score_line("Demo Quality        (10%)", breakdown.get("demo_quality", 0), 10, "← video is huge")

    williams = result.get("would_williams_remember_it", False)
    print(f"\n  {Fore.CYAN}Would Williams F1 CFO remember this demo?{Style.RESET_ALL}")
    print(f"  {'YES' if williams else Fore.RED + 'NO' + Style.RESET_ALL}")

    why_loses = result.get("why_it_loses", "")
    if why_loses:
        print(f"\n  {Fore.RED}WHY IT LOSES:{Style.RESET_ALL}")
        print(f"  {why_loses}")

    fixes = result.get("top_3_fixes", [])
    if fixes:
        print(f"\n  {Fore.YELLOW}TOP 3 FIXES (do these NOW — in order):{Style.RESET_ALL}")
        for i, fix in enumerate(fixes, 1):
            print(f"  {i}. {fix}")

    ai_real = result.get("is_ai_real_or_fake", "")
    if ai_real:
        print(f"\n  {Fore.CYAN}Is the AI real or fake?{Style.RESET_ALL}")
        print(f"  {ai_real}")

    f1_take = result.get("f1_theme_honest_take", "")
    if f1_take:
        print(f"\n  {Fore.CYAN}F1 Theme — honest take:{Style.RESET_ALL}")
        print(f"  {f1_take}")

    summary = result.get("brutal_summary", "")
    if summary:
        print(f"\n  {Fore.RED}BRUTAL SUMMARY:{Style.RESET_ALL}")
        print(f"  {summary}")

    ready = result.get("submission_ready", False)
    status = f"{Fore.GREEN}YES{Style.RESET_ALL}" if ready else f"{Fore.RED}NOT YET{Style.RESET_ALL}"
    print(f"\n  Submission Ready: {status}")
    print(f"\n{'='*64}\n")


# ── MAIN ──────────────────────────────────────────────────────
if __name__ == "__main__":
    hdr("LedgerLive — BRUTAL Airia/Williams F1 Hackathon Judge")
    print(f"  Repo     : {REPO_PATH}")
    print(f"  Model    : {OLLAMA_MODEL}")
    print(f"  {Fore.RED}Mode     : NO MERCY — evidence only, no credit for scaffolding{Style.RESET_ALL}")

    if not REPO_PATH.exists():
        fail(f"Repo not found at {REPO_PATH}")
        sys.exit(1)

    # Assume services already running (you started them manually)
    # But try to detect them
    backend_up = False
    try:
        requests.get(f"{BACKEND_URL}/docs", timeout=3)
        backend_up = True
        ok("Backend already running")
    except:
        warn("Backend not detected — trying to start it...")
        subprocess.Popen(
            ["powershell", "-Command",
             f'cd "{REPO_PATH}\\apps\\api" && .venv\\Scripts\\python -m uvicorn app.main:app --port 8090'],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        time.sleep(8)

    try:
        live_evidence  = test_live_data_flow()
        ai_evidence    = test_ai_decision_quality()
        demo_evidence  = test_demo_story()
        sub_evidence   = test_submission_completeness()
        airia_evidence = test_airia_real_integration()

        final_score, breakdown = compute_strict_score(
            live_evidence, ai_evidence, demo_evidence, sub_evidence, airia_evidence
        )

        result = brutal_llm_judgment(
            live_evidence, ai_evidence, demo_evidence, sub_evidence, airia_evidence,
            final_score, breakdown
        )

        print_brutal_results(result, final_score, breakdown)

        # Save
        out_file = REPO_PATH / "brutal_evaluation.json"
        with open(out_file, "w") as f:
            json.dump({
                "live": live_evidence, "ai": ai_evidence, "demo": demo_evidence,
                "submission": sub_evidence, "airia": airia_evidence,
                "computed_score": final_score, "breakdown": breakdown,
                "llm_judgment": result
            }, f, indent=2, default=str)
        ok(f"Results saved: {out_file}")

    except KeyboardInterrupt:
        warn("Interrupted")
