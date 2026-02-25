# LedgerLive — AI Finance Close Agent

> **One-liner pitch:** LedgerLive is an autonomous AI agent that closes your books like a Williams F1 pit crew closes a race — every document ingested, every mismatch triaged, every decision explained, every artifact sealed.

> The finance close process is a race. LedgerLive operates it like the Williams F1 pit wall:
> lanes hold position, checkpoints gate progress, incidents surface in real-time, approvals
> gate the car through scrutineering, and every tool trace becomes the telemetry pack
> the stewards audit. No LLM keys required — fully deterministic in DEMO mode.

## Screenshots

![Race Control Dashboard](artifacts/debug/test-07-race-control.png)
*Race Control: live lanes, scoreboard, and incident tracking during a close cycle.*

![Dashboard Overview](artifacts/debug/test-01-dashboard.png)
*Dashboard: Pit Lane overview showing documents, OCR, reconciliations, and exceptions at a glance.*

## Project Identity

```
PROJECT_ID: LEDGERLIVE
```

## What It Does

LedgerLive is a **no-code, deterministic finance-close orchestration agent** built on the Airia
platform. It turns a month-end close — a multi-team, multi-approval, deadline-critical operation —
into a race-control metaphor every CFO can read at a glance.

**Finance reality:** sub-ledger feeds, AP matching, cutoff reviews, intercompany elimination,
exception triage, HITL approvals, and signed evidence bundles.

**F1 metaphor:** lanes, pit stops, telemetry packs, safety cars, lap completions, and court packs
for the stewards.

The agent runs 340+ deterministic service waves, exports Airia community bundles, and proves
every assertion with real sha256 hashes — never constants.

## 3-Step Quickstart

```bash
# 1 — Start demo (API + web preview)
make demo

# 2 — Open Race Control in your browser
open http://127.0.0.1:4173/race-control

# 3 — Click "▷ Run Canonical" to seed the full golden scenario
```

## F1 Glossary

| F1 Term | Finance Reality |
|---------|-----------------|
| Race Control | Close Command Center |
| Pit Stops | Close Checkpoints |
| Laps | Close Stages / Milestones |
| Telemetry | Tool Trace + Audit Trail + Drift Budgets |
| Safety Car | Fail-Closed + Approvals Required |
| Pit Wall | Approver Chain + SLA Escalations |
| Incident Log | Exceptions / Blockers / Policy Events |
| Court Pack | Stewards Evidence Package |
| DRS Zone | Fast-path Auto-approval |

## Why Racing Fits

Pit stops are timed checkpoints; a slow reconciliation is a slow pit stop visible in lap delta.
Telemetry is the audit trail; every tool call emits traces; the court pack is the stewards' evidence.
Safety Car pauses automation for approvals — fail-closed until the pit wall gives all-clear.

## Why Airia

1. **Orchestration** — 340+ deterministic waves as Airia template steps
2. **Security** — typed guards; no write without HITL approval; fail-closed on ambiguity
3. **No-code export** — Blueprint Builder compiles workflows into Airia community bundles

## Architecture

| Layer | Tech | Port |
|-------|------|------|
| API | FastAPI + Python 3.14 | 8090 |
| Web | React 18 + Vite + Tailwind | 5173 (dev) / 4173 (preview) |
| DB | SQLite (local) | — |
| E2E | Playwright MCP headed-only | — |

## Gates

- `tools/gates/no_apex_references.py` — Zero Apex Terminal references
- `tools/gates/no_network_in_tests.py` — No outbound network in tests

## Airia Community Bundle

```bash
make airia:bundle    # generate deterministic bundle
make airia:validate  # strict readiness check
make airia:verify    # offline checksum verification
make airia:compat    # run Airia Compatibility Report
```

Bundle output: `artifacts/airia/community_bundle/`

See [docs/airia/AIRIA_OVERVIEW.md](docs/airia/AIRIA_OVERVIEW.md) for full details.

## Airia Compatibility Report

`GET /api/airia/compat_report` produces a deterministic proof: bundle structure, pinned schemas,
acyclic DAG, HITL approvals, fail-closed rules, required outputs, checksum verification.
`overall: PASS` — all checks verified offline, no API keys required.

Run: `make airia:compat`

## No-Code Builder Preview

The `/airia` page shows the workflow DAG as interactive step cards with approval/fail-closed badges,
mapped tool IDs, and links to dossier artifacts. An Import Walkthrough explains each step.
