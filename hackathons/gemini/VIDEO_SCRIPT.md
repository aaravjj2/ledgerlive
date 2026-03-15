# LedgerLive — Gemini Live Agent Challenge Demo Video Script

**Video Length:** 4 minutes
**Target Audience:** Hackathon judges, Google DevRel
**Production URL:** https://ledgerlive-web-zkw2sk4rha-uc.a.run.app

---

## Pre-Recording Checklist

- [ ] Browser open at https://ledgerlive-web-zkw2sk4rha-uc.a.run.app
- [ ] Microphone active for narration
- [ ] Screen recorder ready (1440×900 or higher)
- [ ] Terminal window ready with curl command pre-typed
- [ ] Run golden scenario first: `POST /api/ops/golden-scenario-run` to ensure data

---

## Scene 1: The Hook [0:00 – 0:25]

**Screen:** LedgerLive Dashboard `/`
**Action:** Load dashboard, let metrics render

> **NARRATION:**
> "Finance close cycles are high-stakes, time-pressured operations. A missed exception, a stalled approval,
> a reconciliation mismatch — any one of these can delay a quarterly close by days.
>
> What if your CFO had a voice assistant that could triage exceptions, monitor reconciliation status,
> and approve low-risk items in real time — just by talking?"

**Action:** Highlight the metric cards: Exceptions (3 open), Reconciliation (94.2%), Close Status

---

## Scene 2: The Live Voice Assistant [0:25 – 1:30]

**Screen:** Navigate to `/live-voice`
**Action:** Click "Connect" to start Gemini Live session

> **NARRATION:**
> "This is LedgerBot — powered by Gemini 2.0 Flash Live API, running on Google Cloud Run.
> It has real-time access to your reconciliation data, exception queue, and audit trail.
> Let me ask it something directly."

**Action:** Ask via microphone (or text input):

**Query 1:** *"Show me the critical exceptions right now."*

> *(LedgerBot responds)*
>
> **NARRATION:**
> "It found 3 open exceptions — including a $7,800 duplicate payment.
> And it's not just reading a list — it's reasoning about priority and exposure."

**Query 2:** *"What's blocking the close cycle?"*

> *(LedgerBot responds with close cycle analysis)*
>
> **NARRATION:**
> "Revenue Recognition at 85%, Accounts Payable at 62% — blocked, waiting for CFO sign-off.
> LedgerBot identified the blocker and what needs to happen to unblock it."

**Query 3:** *"Can you approve the low-risk exceptions after I confirm?"*

> *(LedgerBot requests explicit confirmation)*
>
> **NARRATION:**
> "Notice what it does here: it asks for confirmation before modifying any record.
> This is intentional — the system always keeps a human in the loop for financial decisions."

---

## Scene 3: Race Control — Close Orchestration [1:30 – 2:15]

**Screen:** Navigate to `/race-control`
**Action:** Show the Race Control dashboard loading with live data

> **NARRATION:**
> "The Race Control view gives finance teams a real-time command center for the close cycle.
> Modeled after Formula 1 — because close cycles ARE races against time.
>
> We can see 6 workstream lanes, their completion percentages, and blockers.
> The Race Weekend Timeline shows every stage from document ingestion to CFO sign-off."

**Action:** Click "▷ Run Canonical" button

> **NARRATION:**
> "Triggering the golden scenario seeds all data — documents, reconciliations, exceptions,
> approvals, and security events — in a single deterministic run.
>
> Watch the lane status update in real time."

**Action:** Point to scoreboard cards (Health: green, SLA: 87.5%)

---

## Scene 4: Exception Triage Flow [2:15 – 2:50]

**Screen:** Navigate to `/exceptions`
**Action:** Show 3 exceptions with severity badges

> **NARRATION:**
> "Here's the exception queue. Three items flagged by our reconciliation engine.
>
> The critical one — a $7,800 amount delta — needs immediate human review.
> LedgerBot can help triage these verbally and route approvals to the right people."

**Action:** Click "Resolve" on the medium exception, show it disappears

**Screen:** Navigate to `/reconciliation`
**Action:** Show 94.2% match rate, 3 reconciliations

> **NARRATION:**
> "Reconciliation at 94.2% — 847 transactions processed, 3 exceptions flagged for review.
> The automated matching engine handled the rest. We're on track for the FY25-Q4 deadline."

---

## Scene 5: Audit Trail — Immutable & Sealed [2:50 – 3:15]

**Screen:** Navigate to `/audit`
**Action:** Show audit log events flowing in (newest first)

> **NARRATION:**
> "Every action in LedgerLive is written to an immutable audit trail.
> Document classifications, reconciliation matches, exception flags, approval decisions —
> all timestamped and SHA-256 sealed.
>
> LedgerBot can query this trail: 'What happened to invoice INV-2024-0847 yesterday?'
> And it will trace every event in plain language."

---

## Scene 6: Architecture & Gemini Integration [3:15 – 3:35]

**Screen:** Split: Voice page + terminal showing curl command

**Action:** Run in terminal:
```bash
curl -s -X POST https://ledgerlive-api-zkw2sk4rha-uc.a.run.app/api/voice/ask \
  -H "Content-Type: application/json" \
  -d '{"text": "Show me the open exceptions"}'
```

**Action:** Show response with `latency_ms: 89` on screen

> **NARRATION:**
> "Under the hood: the voice endpoint connects to Gemini 2.0 Flash Live API.
> The agent has 8 registered tools — get_exceptions, approve_exception, get_audit_log,
> and more — enabling real function calling against live financial data.
>
> Sub-100ms latency on Google Cloud Run. Production-ready."

---

## Scene 7: Impact & Close [3:35 – 4:00]

**Screen:** Return to Dashboard `/`
**Action:** Pan across dashboard metrics

> **NARRATION:**
> "LedgerLive demonstrates what AI-native finance operations can look like.
>
> Not a chatbot on top of a spreadsheet — but a real-time close agent
> with voice interaction, tool calling, immutable audit trails, and human-in-the-loop controls.
>
> Built on Gemini 2.0 Flash Live API, deployed on Google Cloud Run, live right now.
>
> This is LedgerBot. Finance close, reimagined."

**Action:** Pause on dashboard with all green metrics

---

## Post-Recording

After recording, reference these artifacts in the submission:
- `hackathons/gemini/PROOF_PACK.md` — Deployment proof, API tests, screenshots
- `hackathons/gemini/LIVE_URLS.md` — Live URLs and smoke test results
- `artifacts/demo/` — Screenshots of all 8 pages (8/8 LOOKS GOOD)
- `apps/api/app/services/gemini_live.py` — Gemini Live session implementation
- `apps/api/app/routers/gemini_voice.py` — WebSocket + REST voice endpoints

---

## Key Demo Facts to Remember

| Metric | Value |
|--------|-------|
| Voice API latency | 78–89ms |
| Reconciliation match rate | 94.2% |
| Transactions processed | 847 |
| Open exceptions | 3 (1 critical, 1 high, 1 medium) |
| Total exposure | ~$9,500 |
| Close progress | 73.5% overall |
| SLA adherence | 87.5% |
| Backend tests | 4,280 passing |
| E2E Playwright tests | 88/88 passing |
| Pages verified | 8/8 LOOKS GOOD |
