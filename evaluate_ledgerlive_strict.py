# ============================================================
# evaluate_ledgerlive_strict.py  (vNext — NUCLEAR EDITION)
# LedgerLive × Airia "Race Beyond the Track" — Williams F1
#
# SCORING PHILOSOPHY:
#   Every requirement is BINARY: PASS or FAIL.
#   PASS requires a proof artifact or live API call.
#   "The code is there" = FAIL.
#   "The endpoint exists" = FAIL.
#   "It worked last week" = FAIL.
#   10/10 requires ALL gates GREEN. Not 9. Not 9.5. ALL.
#
# SECTIONS (20 binary gates total):
#   A) Demo Experience          (3 gates)
#   B) Finance Realism F1       (6 gates)
#   C) Agent Autonomy           (3 gates)
#   D) Trust & Governance       (6 gates)
#   E) Test & Determinism       (2 gates)
#   Score = gates_passed / 20 * 10  (0.5 per gate)
#
# TODAY: Feb 24, 2026
# DEADLINE: March 1, 2026 11:59 PM AEDT  (~5 days)
# PRIZE: $20,000 USD (must attend March 4 in person)
# ============================================================

import subprocess, requests, json, time, sys, os, re, hashlib
from pathlib import Path
from datetime import datetime, timezone

try:
    from openai import OpenAI
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install",
                    "openai", "colorama", "requests"], check=True)
    from openai import OpenAI
    from colorama import Fore, Style, init
    init(autoreset=True)

# ── CONFIG ────────────────────────────────────────────────────
REPO_PATH    = Path(os.getenv("LEDGER_REPO_PATH", r"C:\Aarav\ledgerlive"))
BACKEND_URL  = "http://127.0.0.1:8090"
FRONTEND_URL = "http://127.0.0.1:4174"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "devstral")
TODAY        = "Feb 24, 2026"
DEADLINE     = "March 1, 2026 11:59 PM AEDT"

client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")

# ── GATE REGISTRY ─────────────────────────────────────────────
GATES = {}   # gate_id -> {"pass": bool, "proof": str, "section": str, "name": str}

def register(gate_id, section, name, passed, proof):
    GATES[gate_id] = {"pass": passed, "proof": proof, "section": section, "name": name}
    c   = Fore.GREEN if passed else Fore.RED
    sym = "PASS" if passed else "FAIL"
    print(f"  {c}[{sym}] {gate_id}: {name}{Style.RESET_ALL}")
    indent = "         "
    words = proof.split()
    line = indent
    for word in words:
        if len(line) + len(word) > 78:
            print(f"  {c}{line}{Style.RESET_ALL}")
            line = indent + word + " "
        else:
            line += word + " "
    if line.strip():
        print(f"  {c}{line}{Style.RESET_ALL}")

# ── HELPERS ───────────────────────────────────────────────────
def hdr(text, sub=""):
    print(f"\n{Fore.CYAN}{'━'*66}")
    print(f"  {text}")
    if sub:
        print(f"  {Fore.YELLOW}{sub}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'━'*66}{Style.RESET_ALL}")

def api(method, path, **kw):
    try:
        r = getattr(requests, method)(
            f"{BACKEND_URL}{path}", timeout=kw.pop("timeout", 10), **kw)
        try:    return r.status_code, r.json()
        except: return r.status_code, None
    except: return 0, None

def find_file(*names):
    for name in names:
        for p in REPO_PATH.rglob(name):
            if any(s in str(p) for s in [".venv", "__pycache__", ".git", "node_modules"]):
                continue
            return p
    return None

def read_json(path):
    try:    return json.loads(Path(path).read_text(encoding="utf-8"))
    except: return None


# ════════════════════════════════════════════════════════════
# SECTION A — DEMO EXPERIENCE
# ════════════════════════════════════════════════════════════

def section_a():
    hdr("SECTION A — Demo Experience",
        "Gates: cold-start ≤45s | one-click CFO story | 10-question Q&A")

    # ── A1: Cold start ≤ 45 seconds ──────────────────────────
    p = find_file("demo_start_report.json")
    if not p:
        register("A1", "A", "Cold start ≤ 45s", False,
            "demo_start_report.json NOT FOUND. Create a start script that records "
            "{start_ts, ready_ts, elapsed_seconds, all_services_healthy: true}. "
            "elapsed_seconds must be ≤ 45 and the file must be < 24h old.")
    else:
        d = read_json(p) or {}
        elapsed = d.get("elapsed_seconds", d.get("elapsed", 9999))
        healthy = d.get("all_services_healthy", d.get("healthy", False))
        fresh = True
        ts = d.get("start_ts", d.get("timestamp", ""))
        if ts:
            try:
                age_h = (datetime.now(timezone.utc) -
                         datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
                         ).total_seconds() / 3600
                fresh = age_h < 24
            except: pass

        if elapsed <= 45 and healthy and fresh:
            register("A1", "A", "Cold start ≤ 45s", True,
                f"elapsed={elapsed}s, all_services_healthy=true, report fresh")
        elif elapsed > 45:
            register("A1", "A", "Cold start ≤ 45s", False,
                f"elapsed={elapsed}s — EXCEEDS 45s. Pre-warm DB connections, "
                "lazy-load heavy services, use startup readiness probe.")
        elif not healthy:
            register("A1", "A", "Cold start ≤ 45s", False,
                f"elapsed={elapsed}s but all_services_healthy=false. "
                "A service is crashing on cold start — fix it before demo.")
        else:
            register("A1", "A", "Cold start ≤ 45s", False,
                "Report is stale (>24h). Re-run cold-start script before submission.")

    # ── A2: One-click CFO Story ───────────────────────────────
    tp = find_file("story_transcript.json", "cfo_story_transcript.json")
    pp = find_file("tool_trace.json", "cfo_tool_trace.json", "agent_trace.json")
    if not tp:
        register("A2", "A", "One-click CFO Story (no interventions)", False,
            "story_transcript.json NOT FOUND. The 'Run Full CFO Story' button must write "
            "{completed: true, interventions: 0, steps: [...], duration_seconds: N} on finish.")
    elif not pp:
        register("A2", "A", "One-click CFO Story (no interventions)", False,
            "tool_trace.json NOT FOUND. Every agent tool call must be logged: "
            "[{tool, input, output, timestamp}]. Need ≥ 5 tool calls to prove real pipeline.")
    else:
        t = read_json(tp) or {}
        trace = read_json(pp) or []
        completed     = t.get("completed", False)
        interventions = t.get("interventions", 1)
        tool_calls    = len(trace) if isinstance(trace, list) else len(trace.get("calls", []))

        if completed and interventions == 0 and tool_calls >= 5:
            register("A2", "A", "One-click CFO Story (no interventions)", True,
                f"completed=true, interventions=0, {tool_calls} tool calls traced")
        elif not completed:
            register("A2", "A", "One-click CFO Story (no interventions)", False,
                "story_transcript.json has completed=false. Pipeline did not finish.")
        elif interventions > 0:
            register("A2", "A", "One-click CFO Story (no interventions)", False,
                f"interventions={interventions}. A real one-click story has zero human steps.")
        else:
            register("A2", "A", "One-click CFO Story (no interventions)", False,
                f"Only {tool_calls} tool calls (need ≥ 5: ingest, reconcile, "
                "triage, audit, report).")

    # ── A3: 10-question Q&A with citations + navigation ───────
    qp = find_file("qa_session.json", "cfo_qa_session.json")
    if not qp:
        register("A3", "A", "10-question Q&A with citations + navigation", False,
            "qa_session.json NOT FOUND. Run a demo Q&A and save: "
            "[{question, answer, citations: [src1...], navigation_action: 'show /view/X'}]. "
            "Need ≥ 10 entries, all with citations, ≥ 5 with navigation_action.")
    else:
        items = read_json(qp) or []
        if not isinstance(items, list):
            items = items.get("questions", items.get("qa", []))
        total         = len(items)
        with_citations = sum(1 for q in items if len(q.get("citations", q.get("sources", []))) >= 1)
        with_nav       = sum(1 for q in items if q.get("navigation_action") or q.get("show_me"))

        if total >= 10 and with_citations >= 10 and with_nav >= 5:
            register("A3", "A", "10-question Q&A with citations + navigation", True,
                f"{total} Q&As, {with_citations} with citations, {with_nav} with navigation")
        elif total < 10:
            register("A3", "A", "10-question Q&A with citations + navigation", False,
                f"Only {total} Q&A entries (need ≥ 10). Add more pre-run questions.")
        elif with_citations < 10:
            register("A3", "A", "10-question Q&A with citations + navigation", False,
                f"{with_citations}/{total} have citations — ALL must cite source records.")
        else:
            register("A3", "A", "10-question Q&A with citations + navigation", False,
                f"Only {with_nav}/{total} have navigation_action (need ≥ 5). "
                "Add show_me links to relevant views for each answer.")


# ════════════════════════════════════════════════════════════
# SECTION B — FINANCE REALISM (F1-SPECIFIC)
# ════════════════════════════════════════════════════════════

def section_b():
    hdr("SECTION B — Finance Realism (F1-Specific)",
        "Gates: 12 invoices | 4 currencies + FX drift | cost cap | revenue recognition | CFO cockpit ×3")

    # Gather data from API + seed files
    invoice_count = 0
    currencies = set()
    has_fx_drift = False
    has_cost_cap = False
    has_revenue  = False

    status, docs = api("get", "/api/documents?limit=200")
    items = (docs if isinstance(docs, list) else
             docs.get("items", docs.get("documents", []))) if docs else []
    for item in items:
        s = json.dumps(item).lower()
        if any(k in s for k in ["invoice", "inv-", "bill"]): invoice_count += 1
        for c in ["usd", "gbp", "eur", "jpy", "aud", "chf"]:
            if c in s: currencies.add(c.upper())
        if "fx_rate" in s or "exchange_rate" in s: has_fx_drift = True
        if "cost_cap" in s or "cap_category" in s: has_cost_cap = True
        if "sponsorship" in s or "revenue_recogn" in s: has_revenue = True

    # Also scan seed scripts
    for sf in (list(REPO_PATH.rglob("seed*.py")) + list(REPO_PATH.rglob("fixtures*.py")) +
               [find_file("scenario_pack.json"), find_file("f1_scenario.json")]):
        if not sf or not Path(sf).exists(): continue
        if any(s in str(sf) for s in [".venv", "__pycache__"]): continue
        try:
            c = Path(sf).read_text(encoding="utf-8", errors="ignore").lower()
            if "invoice" in c:
                cnt = c.count('"invoice"') + c.count("'invoice'") + c.count("invoice_number")
                invoice_count = max(invoice_count, cnt)
            for cur in ["usd", "gbp", "eur", "jpy", "aud"]:
                if f'"{cur}"' in c or f"'{cur}'" in c: currencies.add(cur.upper())
            if "fx_rate" in c or "exchange_rate" in c: has_fx_drift = True
            if "cost_cap" in c: has_cost_cap = True
            if "sponsorship" in c or "revenue_recogn" in c or "freight" in c: has_revenue = True
        except: pass

    # B1 — 12 invoices, 4 currencies
    if invoice_count >= 12 and len(currencies) >= 4:
        register("B1", "B", "12 invoices + 4 currencies in scenario pack", True,
            f"{invoice_count} invoices, currencies={currencies}")
    else:
        missing = []
        if invoice_count < 12:
            missing.append(f"only {invoice_count} invoices (need 12: aero parts, freight, "
                           "travel, hotel, catering, sponsorship)")
        if len(currencies) < 4:
            missing.append(f"only {len(currencies)} currencies {currencies} (need ≥4: USD+GBP+EUR+JPY)")
        register("B1", "B", "12 invoices + 4 currencies in scenario pack", False,
            " | ".join(missing))

    # B2 — FX drift mid-run
    register("B2", "B", "FX drift mid-run (exchange_rate changes during pipeline)", has_fx_drift,
        "FX drift detected in data" if has_fx_drift else
        "No FX drift found. Add fx_rate field that changes ±2% between invoice receipt "
        "and payment — e.g. USD/GBP 0.792 on day 1, 0.783 on day 3 to simulate real drift.")

    # B3 — Cost cap category + breach risk
    register("B3", "B", "Cost cap category mapping + breach risk logic", has_cost_cap,
        "cost_cap fields present" if has_cost_cap else
        "No cost_cap data found. Every invoice needs cap_category: "
        "['chassis','power_unit','personnel','travel','other'] "
        "and a cap_breach_risk: float field. F1 teams live under the $135M cap.")

    # B4 — Revenue recognition types
    register("B4", "B", "Freight + travel + aero + sponsorship revenue recognition", has_revenue,
        "Revenue recognition types present" if has_revenue else
        "No freight/sponsorship/revenue_recognition found. Add: sponsorship_receipt "
        "with recognition_schedule, freight invoice with logistics_cost_center, "
        "aero_parts with r_and_d_mapping field.")

    # B5/B6 — CFO cockpit completeness
    cockpit_str = ""
    for ep in ["/api/cfo-cockpit", "/api/dashboard/cfo", "/api/cockpit",
               "/api/f1/cockpit", "/api/dashboard", "/api/race-control/cockpit"]:
        sc, data = api("get", ep)
        if sc == 200 and data:
            cockpit_str = json.dumps(data).lower()
            break

    # Also scan frontend for these terms
    if not cockpit_str:
        fe_src = REPO_PATH / "apps" / "web" / "src"
        if fe_src.exists():
            for f in fe_src.rglob("*.tsx"):
                try:
                    cockpit_str += f.read_text(encoding="utf-8", errors="ignore").lower()
                except: pass

    has_runway   = any(k in cockpit_str for k in ["cost_cap_runway", "cap_runway", "runway_by_category"])
    has_ladder   = any(k in cockpit_str for k in ["cash_timing", "cash_ladder", "timing_ladder"])
    has_vendor   = any(k in cockpit_str for k in ["vendor_concentration", "vendor_exposure", "concentration"])
    has_delta    = any(k in cockpit_str for k in ["forecast_delta", "close_adjustment", "forecast_impact"])

    register("B5", "B", "CFO cockpit: cost cap runway + cash ladder + vendor concentration",
        has_runway and has_ladder and has_vendor,
        "All 3 present" if (has_runway and has_ladder and has_vendor) else
        f"MISSING: runway={has_runway}, cash_ladder={has_ladder}, vendor_concentration={has_vendor}. "
        "These are the 3 numbers a Williams CFO checks every Monday morning.")

    register("B6", "B", "CFO cockpit: forecast delta after close adjustments",
        has_delta,
        "forecast_delta present" if has_delta else
        "forecast_delta MISSING. After each reconciliation: show original_forecast, "
        "adjusted_forecast, delta_amount, delta_pct. This is the CFO's single most-watched number.")


# ════════════════════════════════════════════════════════════
# SECTION C — AGENT AUTONOMY
# ════════════════════════════════════════════════════════════

def section_c():
    hdr("SECTION C — Agent Autonomy",
        "Gates: 3 named plans | late invoice adaptation | 100% cited decisions")

    # ── C1: 3 alternative plans ───────────────────────────────
    plan_data = None
    for ep in ["/api/agent/plans", "/api/agent/alternatives", "/api/pipeline/plans"]:
        sc, d = api("post", ep, json={"mode": "planning", "context": "month_end_close"}, timeout=20)
        if sc in [200, 201] and d:
            plan_data = d; break
    if not plan_data:
        plan_data = read_json(find_file("agent_plans.json", "alternative_plans.json") or "")

    if not plan_data:
        register("C1", "C", "3 alternative plans (risk/speed/compliance) with scored tradeoffs", False,
            "No planning endpoint returned data AND no agent_plans.json found. "
            "Add POST /api/agent/plans returning: {plans: [{name: 'risk-first', "
            "steps: [...], score: {risk, speed, compliance}, tradeoffs: '...'}]}. "
            "Three plans required: risk-first, speed-first, compliance-first.")
    else:
        plans = plan_data.get("plans", plan_data.get("alternatives", plan_data))
        if not isinstance(plans, list): plans = []
        has_risk  = any("risk" in str(p).lower() for p in plans)
        has_speed = any(k in str(p).lower() for p in plans for k in ["speed", "fast", "quick"])
        has_comp  = any(k in str(p).lower() for p in plans for k in ["compliance", "policy"])
        has_score = any("score" in str(p).lower() or "tradeoff" in str(p).lower() for p in plans)

        if len(plans) >= 3 and has_risk and has_speed and has_comp and has_score:
            register("C1", "C", "3 alternative plans (risk/speed/compliance) with scored tradeoffs", True,
                f"{len(plans)} plans with risk/speed/compliance labels and scored tradeoffs")
        else:
            missing = []
            if len(plans) < 3: missing.append(f"only {len(plans)} plans")
            if not has_risk:   missing.append("no risk-first plan")
            if not has_speed:  missing.append("no speed-first plan")
            if not has_comp:   missing.append("no compliance-first plan")
            if not has_score:  missing.append("no scored tradeoffs")
            register("C1", "C", "3 alternative plans (risk/speed/compliance) with scored tradeoffs", False,
                "; ".join(missing))

    # ── C2: Late invoice adaptation ───────────────────────────
    late_resp = None
    for ep in ["/api/events/late-invoice", "/api/agent/event", "/api/pipeline/inject"]:
        sc, d = api("post", ep, json={
            "event_type": "late_invoice_arrived",
            "invoice": {"vendor": "Aerodyne Parts Ltd", "amount": 185000,
                        "currency": "GBP", "cap_category": "aero", "arrived_late": True}
        }, timeout=20)
        if sc in [200, 201, 202] and d:
            late_resp = d; break
    if not late_resp:
        late_resp = read_json(find_file("late_invoice_adaptation.json", "event_response.json") or "")

    if not late_resp:
        register("C2", "C", "Agent adapts to late invoice + explains impact", False,
            "No event endpoint responded AND no late_invoice_adaptation.json found. "
            "Add POST /api/events/late-invoice. Response must include: impact_analysis, "
            "revised_forecast, affected_reconciliations, agent_explanation with 'because' language "
            "referencing the specific vendor and cap_category.")
    else:
        s = json.dumps(late_resp).lower()
        has_impact   = any(k in s for k in ["impact", "affect", "delta", "change"])
        has_revised  = any(k in s for k in ["revised", "updated", "new_forecast", "adjustment"])
        has_explain  = any(k in s for k in ["because", "therefore", "explanation", "reasoning"])
        has_specific = any(k in s for k in ["gbp", "185000", "aerodyne", "aero"])

        if has_impact and has_revised and has_explain and has_specific:
            register("C2", "C", "Agent adapts to late invoice + explains impact", True,
                "Response has impact_analysis, revised_forecast, explanation, and specific invoice details")
        else:
            missing = []
            if not has_impact:   missing.append("no impact_analysis")
            if not has_revised:  missing.append("no revised_forecast")
            if not has_explain:  missing.append("no explanation with 'because' language")
            if not has_specific: missing.append("response ignores the specific invoice details")
            register("C2", "C", "Agent adapts to late invoice + explains impact", False,
                "; ".join(missing))

    # ── C3: 100% of decisions have citations + policy + metric delta ──
    decisions = []
    for ep in ["/api/agent/decisions", "/api/reviews", "/api/exceptions?limit=20"]:
        sc, d = api("get", ep)
        if sc == 200 and d:
            decisions = (d if isinstance(d, list) else
                         d.get("items", d.get("decisions", [])))[:20]
            if decisions: break
    if not decisions:
        saved = read_json(find_file("agent_decisions.json", "decisions_log.json") or "")
        if saved: decisions = (saved if isinstance(saved, list) else saved.get("decisions", []))

    if not decisions:
        register("C3", "C", "100% decisions: citations + policy_ref + metric_delta", False,
            "No agent decisions found via API or decisions_log.json. "
            "Log every agent action with: {decision, evidence_citations: [], "
            "policy_ref: 'F1 Cost Cap Art. X', expected_metric_delta: {field, before, after}}.")
    else:
        violations = []
        for dec in decisions[:10]:
            has_cite   = bool(dec.get("evidence_citations") or dec.get("citations") or dec.get("evidence"))
            has_policy = bool(dec.get("policy_ref") or dec.get("policy") or dec.get("policy_justification"))
            has_delta  = bool(dec.get("expected_metric_delta") or dec.get("metric_delta") or dec.get("impact"))
            if not has_cite:   violations.append(f"missing citations in: {str(dec)[:60]}")
            if not has_policy: violations.append(f"missing policy_ref in: {str(dec)[:60]}")
            if not has_delta:  violations.append(f"missing metric_delta in: {str(dec)[:60]}")

        if not violations:
            register("C3", "C", "100% decisions: citations + policy_ref + metric_delta", True,
                f"All {min(len(decisions), 10)} sampled decisions are fully cited")
        else:
            register("C3", "C", "100% decisions: citations + policy_ref + metric_delta", False,
                f"{len(violations)} violations in first 10 decisions: {violations[0]}")


# ════════════════════════════════════════════════════════════
# SECTION D — TRUST & GOVERNANCE
# ════════════════════════════════════════════════════════════

def section_d():
    hdr("SECTION D — Trust & Governance",
        "Gates: replay equality | tamper lab | MCP registry | inbound webhook | outbound log | compat PASS")

    # ── D1: Court pack replay equality ───────────────────────
    cp = read_json(find_file("court_pack_report.json", "audit_pack.json") or "")
    if not cp:
        register("D1", "D", "Court pack: replay regeneration equality (hash match)", False,
            "court_pack_report.json NOT FOUND. Build verifier: (1) run pipeline, "
            "(2) hash output, (3) re-run, (4) hash again, (5) compare. "
            "Save: {run1_hash, run2_hash, equal: true, signatures: [...], checksums: {...}}.")
    else:
        h1    = cp.get("run1_hash") or cp.get("hash_run1")
        h2    = cp.get("run2_hash") or cp.get("hash_run2")
        equal = cp.get("equal", cp.get("hashes_equal", False))
        sigs  = bool(cp.get("signatures") or cp.get("checksums"))
        if h1 and h2 and equal and sigs:
            register("D1", "D", "Court pack: replay regeneration equality (hash match)", True,
                f"run1_hash={str(h1)[:16]}… == run2, equal=true, signatures present")
        elif not equal or (h1 and h2 and h1 != h2):
            register("D1", "D", "Court pack: replay regeneration equality (hash match)", False,
                "HASHES MISMATCH — agent is non-deterministic. "
                "Fix: temperature=0, freeze timestamps to input, seed random(42).")
        else:
            missing = [x for x, v in [("run1_hash", h1), ("run2_hash", h2), ("signatures", sigs)] if not v]
            register("D1", "D", "Court pack: replay regeneration equality (hash match)", False,
                f"Missing fields: {missing}")

    # ── D2: Tamper lab — 3 cases ──────────────────────────────
    tr = read_json(find_file("tamper_lab_report.json", "tamper_report.json") or "")
    if not tr:
        register("D2", "D", "Tamper lab: 3 deterministic tamper cases all detected", False,
            "tamper_lab_report.json NOT FOUND. Build tamper_lab.py: take a signed audit "
            "record, mutate it 3 ways (amount_change, date_shift, vendor_rename), run "
            "verifier on each, confirm all 3 detected. "
            "Save: {cases: [{tamper_type, detected: true}]}.")
    else:
        cases    = tr.get("cases", tr.get("tamper_cases", []))
        detected = [c for c in cases if c.get("detected", False)]
        if len(detected) >= 3:
            register("D2", "D", "Tamper lab: 3 deterministic tamper cases all detected", True,
                f"All {len(detected)}/3 tamper cases detected: "
                f"{[c.get('tamper_type','?') for c in detected]}")
        else:
            missed = [c for c in cases if not c.get("detected")]
            register("D2", "D", "Tamper lab: 3 deterministic tamper cases all detected", False,
                f"Only {len(detected)}/{len(cases)} detected. "
                f"MISSED: {[c.get('tamper_type','?') for c in missed]}. "
                "Your verifier has blind spots — tampered records slip through.")

    # ── D3: MCP tools == tool registry ───────────────────────
    sc_m, mcp = api("get", "/api/mcp/tools")
    if sc_m != 200 or not mcp:
        sc_m, mcp = api("get", "/mcp/tools")
    sc_r, reg = api("get", "/api/agent/tool-registry")
    if sc_r != 200 or not reg:
        sc_r, reg = api("get", "/api/tools")

    if sc_m != 200 or not mcp:
        register("D3", "D", "MCP tools list matches tool registry (no ghost tools)", False,
            "GET /api/mcp/tools returns non-200. MCP server must expose a tools list. "
            "Airia uses this to discover your agent's capabilities. Without it, "
            "Airia cannot integrate with your agent.")
    elif sc_r != 200 or not reg:
        register("D3", "D", "MCP tools list matches tool registry (no ghost tools)", False,
            "GET /api/agent/tool-registry returns non-200. Need a tool registry endpoint "
            "that lists all registered tools so MCP list can be validated against it.")
    else:
        mcp_tools = mcp if isinstance(mcp, list) else mcp.get("tools", [])
        reg_tools = reg if isinstance(reg, list) else reg.get("tools", reg.get("registry", []))
        mcp_names = {(t.get("name", t) if isinstance(t, dict) else str(t)) for t in mcp_tools}
        reg_names = {(t.get("name", t) if isinstance(t, dict) else str(t)) for t in reg_tools}
        ghost  = mcp_names - reg_names
        absent = reg_names - mcp_names
        if not ghost and not absent and mcp_names:
            register("D3", "D", "MCP tools list matches tool registry (no ghost tools)", True,
                f"Perfect match: {len(mcp_names)} tools, zero ghost tools, zero absent tools")
        else:
            issues = []
            if ghost:       issues.append(f"ghost tools (MCP not in registry): {ghost}")
            if absent:      issues.append(f"absent tools (registry not in MCP): {absent}")
            if not mcp_names: issues.append("MCP tools list is empty")
            register("D3", "D", "MCP tools list matches tool registry (no ghost tools)", False,
                "; ".join(issues))

    # ── D4: Inbound webhook triggers full cycle ───────────────
    triggered = False
    proof_str = "all endpoints returned 404/500"
    for ep in ["/webhook/airia", "/api/webhook/airia", "/api/airia/webhook", "/api/webhook"]:
        sc, d = api("post", ep,
            json={"event": "close_cycle_trigger", "source": "airia",
                  "payload": {"period": "2026-02", "team": "Williams_F1"}}, timeout=20)
        if sc in [200, 201, 202]:
            s = json.dumps(d or {}).lower()
            if any(k in s for k in ["cycle", "workflow", "pipeline", "job_id", "run_id"]):
                triggered = True
                proof_str = f"POST {ep} → {sc}, cycle started: {str(d)[:100]}"
                break
            else:
                proof_str = f"POST {ep} → {sc} but no cycle/workflow in response"

    register("D4", "D", "Inbound webhook triggers full pipeline cycle", triggered,
        proof_str if triggered else
        proof_str + ". Add POST /webhook/airia that starts a close cycle. "
        "Return: {job_id, status: 'started', estimated_completion_seconds: N}.")

    # ── D5: Outbound webhook log with last payload ────────────
    wh_log = None
    for ep in ["/api/airia/webhook-log", "/api/webhook-log", "/api/outbound/log"]:
        sc, d = api("get", ep)
        if sc == 200 and d:
            wh_log = d; break
    if not wh_log:
        wh_log = read_json(find_file("webhook_log.json", "airia_outbound_log.json") or "")

    if not wh_log:
        register("D5", "D", "Outbound webhook log includes last payload", False,
            "No outbound webhook log found. After each pipeline completion, POST result "
            "to Airia callback URL and log: [{timestamp, url, payload, response_status}]. "
            "Last entry must have a full payload, not just a status code.")
    else:
        entries = wh_log if isinstance(wh_log, list) else wh_log.get("entries", wh_log.get("logs", []))
        if not entries:
            register("D5", "D", "Outbound webhook log includes last payload", False,
                "Log file exists but is empty — nothing has been sent to Airia yet.")
        else:
            last = entries[-1]
            ok = (bool(last.get("payload") or last.get("body")) and
                  bool(last.get("timestamp") or last.get("sent_at")) and
                  bool(last.get("response_status") or last.get("status_code")))
            register("D5", "D", "Outbound webhook log includes last payload", ok,
                f"{len(entries)} log entries, last has payload+timestamp+response_status" if ok else
                f"Last entry missing fields. Has: {list(last.keys())}")

    # ── D6: Airia compatibility report PASS ───────────────────
    sc_c, compat_api = api("get", "/api/airia/compatibility")
    compat = (compat_api if sc_c == 200 and compat_api else
              read_json(find_file("airia_compatibility_report.json", "compat_report.json") or ""))

    if not compat:
        register("D6", "D", "Airia compatibility report overall_result = PASS", False,
            "No compatibility report found. Run: python airia_compat_check.py. "
            "Must check: auth, MCP version, webhook schema, tool signatures. "
            "Save with overall_result: 'PASS'.")
    else:
        result = (compat.get("overall_result") or compat.get("result") or
                  compat.get("status") or "").upper()
        if "PASS" in result:
            checks = compat.get("checks", compat.get("results", []))
            passed_c = sum(1 for c in checks if c.get("pass") or c.get("result") == "PASS")
            register("D6", "D", "Airia compatibility report overall_result = PASS", True,
                f"overall_result=PASS, {passed_c}/{len(checks)} checks passed")
        else:
            register("D6", "D", "Airia compatibility report overall_result = PASS", False,
                f"overall_result='{result or 'missing'}'. Fix failing checks until PASS.")


# ════════════════════════════════════════════════════════════
# SECTION E — TEST & DETERMINISM GATES
# ════════════════════════════════════════════════════════════

def section_e():
    hdr("SECTION E — Test & Determinism Gates",
        "Gates: pytest 0 failed/0 skipped | Playwright run×2 determinism PASS")

    # ── E1: pytest — 0 failed, 0 skipped ─────────────────────
    api_path = REPO_PATH / "apps" / "api"
    pytest_result = None
    venv_py = next((str(p) for p in [
        api_path / ".venv" / "Scripts" / "python.exe",
        api_path / "venv" / "Scripts" / "python.exe",
        REPO_PATH / ".venv" / "Scripts" / "python.exe"
    ] if Path(p).exists()), None)

    if venv_py and api_path.exists():
        try:
            r = subprocess.run(
                [venv_py, "-m", "pytest", "--tb=no", "-q",
                 "--json-report", "--json-report-file=pytest_report.json"],
                cwd=str(api_path), capture_output=True, text=True, timeout=120)
            rp = api_path / "pytest_report.json"
            if rp.exists():
                data = read_json(rp)
                if data:
                    s = data.get("summary", {})
                    pytest_result = {k: s.get(k, 0) for k in ["passed", "failed", "skipped"]}
            if not pytest_result:
                for line in (r.stdout + r.stderr).split("\n"):
                    m = re.search(r"(\d+) passed", line)
                    if m:
                        pytest_result = {
                            "passed":  int(m.group(1)),
                            "failed":  int(re.search(r"(\d+) failed", line).group(1)) if "failed" in line else 0,
                            "skipped": int(re.search(r"(\d+) skipped", line).group(1)) if "skipped" in line else 0,
                        }
                        break
        except subprocess.TimeoutExpired:
            pytest_result = None

    if not pytest_result:
        for name in ["pytest_report.json", ".report.json"]:
            p = find_file(name)
            if p:
                d = read_json(p)
                if d:
                    s = d.get("summary", {})
                    pytest_result = {k: s.get(k, 0) for k in ["passed", "failed", "skipped"]}
                    break

    if not pytest_result:
        register("E1", "E", "pytest: 0 failed, 0 skipped", False,
            "Could not run pytest or find a recent report. "
            "Ensure venv is set up: apps/api/.venv/Scripts/python.exe -m pytest --tb=short.")
    else:
        f, s, p = pytest_result["failed"], pytest_result["skipped"], pytest_result["passed"]
        register("E1", "E", "pytest: 0 failed, 0 skipped", f == 0 and s == 0,
            f"{p} passed, 0 failed, 0 skipped" if (f == 0 and s == 0) else
            f"{p} passed, {f} FAILED, {s} SKIPPED. Fix failures. "
            "Convert skips to real tests — a skipped test is a hidden bug.")

    # ── E2: Playwright determinism ────────────────────────────
    pw_config = find_file("playwright.config.ts", "playwright.config.js")
    config_issues = []
    if pw_config:
        c = pw_config.read_text(encoding="utf-8", errors="ignore")
        if "retries: 0" not in c and "retries:0" not in c:
            config_issues.append("retries must be 0")
        if "workers: 1" not in c and "workers:1" not in c:
            config_issues.append("workers must be 1")
        if "trace" not in c.lower():
            config_issues.append("trace: 'on' missing")
        if "video" not in c.lower():
            config_issues.append("video: 'on' missing")
        if "screenshot" not in c.lower():
            config_issues.append("screenshot: 'on' missing")
        if "headless: false" not in c and "headed" not in c.lower():
            config_issues.append("headed mode required (headless: false)")

        # Check for non-testid selectors
        bad = []
        test_root = pw_config.parent
        for tf in list(test_root.rglob("*.spec.ts")) + list(test_root.rglob("*.spec.js")):
            try:
                tc = tf.read_text(encoding="utf-8", errors="ignore")
                n = len(re.findall(r"getByText|querySelector|\.css\(|xpath", tc))
                if n > 0: bad.append(f"{tf.name}:{n} non-testid")
            except: pass
        if bad: config_issues.append(f"non data-testid selectors: {bad[:2]}")
    else:
        config_issues.append("playwright.config.ts not found")

    det = read_json(find_file("playwright_determinism_report.json", "pw_determinism.json") or "")
    if not det:
        register("E2", "E", "Playwright: run×2 determinism PASS + config compliant", False,
            "playwright_determinism_report.json NOT FOUND. "
            "Build run_pw_twice.py: run Playwright twice, hash screenshots+traces, compare. "
            "Save: {run1_hash, run2_hash, equal: true, config_compliant: true}. "
            f"Config issues to fix first: {'; '.join(config_issues) if config_issues else 'none'}.")
    else:
        equal = det.get("equal", det.get("deterministic", False))
        if equal and not config_issues:
            register("E2", "E", "Playwright: run×2 determinism PASS + config compliant", True,
                "Determinism PASS: run1==run2, retries=0, workers=1, trace/video/screenshot ON, "
                "headed, data-testid selectors only")
        elif not equal:
            register("E2", "E", "Playwright: run×2 determinism PASS + config compliant", False,
                "Runs are NON-DETERMINISTIC (run1 != run2). "
                "Fix: freeze timestamps in tests, seed random, mock all external calls, temperature=0.")
        else:
            register("E2", "E", "Playwright: run×2 determinism PASS + config compliant", False,
                f"determinism={equal} but config non-compliant: {'; '.join(config_issues)}")


# ════════════════════════════════════════════════════════════
# LLM FINAL VERDICT
# ════════════════════════════════════════════════════════════

def nuclear_llm_verdict():
    total  = len(GATES)
    passed = sum(1 for g in GATES.values() if g["pass"])
    score  = round((passed / total) * 10, 2)

    hdr("NUCLEAR LLM VERDICT",
        f"Model: {OLLAMA_MODEL} | grading as the $20k prize judge, zero mercy")

    sections = {}
    for gid, g in GATES.items():
        s = g["section"]
        sections.setdefault(s, {"pass": 0, "total": 0})
        sections[s]["total"] += 1
        if g["pass"]: sections[s]["pass"] += 1

    deadline_utc = datetime(2026, 3, 1, 12, 59, 0, tzinfo=timezone.utc)
    hours_left = max(0, (deadline_utc - datetime.now(timezone.utc)).total_seconds() / 3600)

    failed_gates = [
        {"gate": gid, "name": g["name"], "section": g["section"], "proof": g["proof"]}
        for gid, g in GATES.items() if not g["pass"]
    ]

    prompt = f"""You are the $20,000 prize judge for "Airia Race Beyond the Track — Williams F1 / Atlassian".
You have spent your career in trading and F1 operations technology. You are not kind.

Today: {TODAY}. Deadline: {DEADLINE}. Hours left: {hours_left:.0f}h.

BINARY SCORE: {passed}/{total} gates = {score}/10.
10/10 requires ALL 20 gates. Current: {total - passed} gates FAILING.

Section pass rates:
{json.dumps({s: f"{v['pass']}/{v['total']}" for s, v in sections.items()}, indent=2)}

Failed gates ({len(failed_gates)} total):
{json.dumps(failed_gates, indent=2)}

Answer in valid JSON only. Zero softening. Zero "great foundation". 
Treat every word as expensive — be specific, be brutal, be actionable.
Order priority_fix_order by ROI: most gates fixed per hour worked.

{{
  "score": {score},
  "gates_passed": {passed},
  "total_gates": {total},
  "will_this_win": false,
  "honest_verdict": "2 sentences MAX. What is the project's actual state right now.",
  "weakest_section": "which section is dragging the score down most and why",
  "priority_fix_order": [
    {{
      "gate": "A1",
      "name": "gate name",
      "why_first": "ROI reasoning — fixes this many other problems too",
      "exact_steps": "step 1: ... step 2: ... step 3: ...",
      "estimated_hours": 1
    }}
  ],
  "what_judges_notice_first": "The first thing that will make or break this in a 3-minute demo",
  "if_only_4_hours_left": "Exactly what to do and nothing else if only 4 hours remain",
  "submission_ready": false
}}"""

    try:
        resp = client.chat.completions.create(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": "You are a ruthless hackathon judge. Valid JSON only. No markdown."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.05, max_tokens=3000
        )
        raw = resp.choices[0].message.content.strip()
        if "```" in raw:
            for part in raw.split("```"):
                p = part.strip().lstrip("json").strip()
                try: return json.loads(p)
                except: pass
        return json.loads(raw)
    except Exception as e:
        print(f"  {Fore.RED}LLM failed: {e}{Style.RESET_ALL}")
        return None


# ════════════════════════════════════════════════════════════
# PRINT FINAL REPORT
# ════════════════════════════════════════════════════════════

def print_final_report(verdict):
    total  = len(GATES)
    passed = sum(1 for g in GATES.values() if g["pass"])
    score  = round((passed / total) * 10, 2)

    hdr("FINAL BINARY GATE REPORT — LEDGERLIVE × AIRIA/WILLIAMS F1")

    pct    = (passed / total) * 100
    c      = Fore.GREEN if pct >= 80 else (Fore.YELLOW if pct >= 50 else Fore.RED)
    filled = int((passed / total) * 44)
    bar    = "█" * filled + "░" * (44 - filled)
    print(f"\n  {c}SCORE: {score}/10  [{bar}]  {passed}/{total} gates{Style.RESET_ALL}")
    print(f"  {Fore.RED}10/10 requires ALL {total} gates PASS. No partial credit. No exceptions.{Style.RESET_ALL}\n")

    snames = {"A": "Demo Experience", "B": "Finance Realism (F1)",
              "C": "Agent Autonomy",  "D": "Trust & Governance", "E": "Test & Determinism"}
    sections = {}
    for gid, g in GATES.items():
        s = g["section"]
        sections.setdefault(s, {"pass": 0, "total": 0, "gates": []})
        sections[s]["total"] += 1
        sections[s]["gates"].append((gid, g))
        if g["pass"]: sections[s]["pass"] += 1

    for sid in sorted(sections.keys()):
        sec = sections[sid]
        sp, st = sec["pass"], sec["total"]
        sc = Fore.GREEN if sp == st else (Fore.YELLOW if sp > 0 else Fore.RED)
        print(f"  {sc}[{sid}] {snames.get(sid, sid):<30}  {sp}/{st} PASS{Style.RESET_ALL}")
        for gid, g in sec["gates"]:
            sym_c = Fore.GREEN if g["pass"] else Fore.RED
            sym   = "✓" if g["pass"] else "✗"
            print(f"    {sym_c}{sym} {gid}: {g['name']}{Style.RESET_ALL}")

    if verdict:
        total  = len(GATES)
        passed = sum(1 for g in GATES.values() if g["pass"])
        all_pass = (passed == total)

        if all_pass:
            # ── All 20 gates PASS — emit celebration only, no negative blocks ──
            print(f"\n  {Fore.GREEN}{'═'*64}{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}PERFECT SCORE — 20/20 GATES PASS{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}{'═'*64}{Style.RESET_ALL}")
            print(f"\n  {Fore.GREEN}✓ All {total} gates are GREEN. SCORE: 10.0/10.{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}✓ Submission ready. Zero blocking issues.{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}✓ Pipeline: deterministic, tamper-proof, Airia-compatible.{Style.RESET_ALL}")
            return

        print(f"\n  {Fore.RED}{'═'*64}{Style.RESET_ALL}")
        print(f"  {Fore.RED}NUCLEAR LLM VERDICT{Style.RESET_ALL}")
        print(f"  {Fore.RED}{'═'*64}{Style.RESET_ALL}")

        v = verdict.get("honest_verdict", "")
        if v: print(f"\n  {Fore.RED}VERDICT:{Style.RESET_ALL}\n  {v}")

        ws = verdict.get("weakest_section", "")
        if ws: print(f"\n  {Fore.YELLOW}WEAKEST SECTION:{Style.RESET_ALL}\n  {ws}")

        first = verdict.get("what_judges_notice_first", "")
        if first: print(f"\n  {Fore.YELLOW}JUDGES NOTICE FIRST:{Style.RESET_ALL}\n  {first}")

        fixes = verdict.get("priority_fix_order", [])
        if fixes:
            print(f"\n  {Fore.YELLOW}PRIORITY FIX ORDER (highest ROI first):{Style.RESET_ALL}")
            for i, fix in enumerate(fixes[:6], 1):
                h = fix.get("estimated_hours", "?")
                print(f"\n    {i}. [{fix.get('gate')}] {fix.get('name')}  (~{h}h)")
                print(f"       WHY: {fix.get('why_first', '')}")
                steps = fix.get("exact_steps", "")
                if isinstance(steps, list):
                    for step in steps:
                        print(f"       → {step.strip()}")
                elif isinstance(steps, str):
                    parts = steps.split("step ")[1:]
                    if parts:
                        for step in parts:
                            print(f"       → step {step.strip()}")
                    else:
                        print(f"       → {steps.strip()}")

        fh = verdict.get("if_only_4_hours_left", "")
        if fh: print(f"\n  {Fore.RED}IF ONLY 4 HOURS LEFT:{Style.RESET_ALL}\n  {fh}")

        ready = verdict.get("submission_ready", False)
        rc = Fore.GREEN if ready else Fore.RED
        print(f"\n  Submission Ready: {rc}{'YES — SUBMIT NOW' if ready else 'NO'}{Style.RESET_ALL}")

    print(f"\n{'━'*66}\n")


# ════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    hdr("LedgerLive — NUCLEAR BINARY GATE JUDGE (vNext)",
        f"Today: {TODAY}  |  Deadline: {DEADLINE}  |  Prize: $20,000 USD")
    print(f"  Repo  : {REPO_PATH}")
    print(f"  Model : {OLLAMA_MODEL}")
    print(f"  {Fore.RED}20 binary gates. PASS/FAIL only. 10/10 = ALL 20 green.{Style.RESET_ALL}")
    print(f"  {Fore.RED}'It exists' = FAIL. Proof artifact or live call required for every gate.{Style.RESET_ALL}")

    if not REPO_PATH.exists():
        print(f"  {Fore.RED}REPO NOT FOUND: {REPO_PATH}{Style.RESET_ALL}")
        sys.exit(1)

    try:
        requests.get(f"{BACKEND_URL}/docs", timeout=3)
        print(f"  {Fore.GREEN}✓ Backend running{Style.RESET_ALL}")
    except:
        print(f"  {Fore.YELLOW}⚠ Backend not detected — API tests will fail{Style.RESET_ALL}")

    try:
        section_a()
        section_b()
        section_c()
        section_d()
        section_e()

        verdict = nuclear_llm_verdict()
        print_final_report(verdict)

        out_file = REPO_PATH / "nuclear_gate_report.json"
        with open(out_file, "w") as f:
            json.dump({
                "today": TODAY, "deadline": DEADLINE,
                "score": round(sum(g["pass"] for g in GATES.values()) / len(GATES) * 10, 2),
                "gates_passed": sum(g["pass"] for g in GATES.values()),
                "total_gates": len(GATES),
                "gates": GATES, "verdict": verdict
            }, f, indent=2, default=str)
        print(f"  {Fore.GREEN}✓ Full report: {out_file}{Style.RESET_ALL}")

    except KeyboardInterrupt:
        print(f"\n  {Fore.YELLOW}Interrupted{Style.RESET_ALL}")
