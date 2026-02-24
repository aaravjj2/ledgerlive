# LedgerLive Race Control Close Agent (Airia / Williams F1 Hackathon)

> The finance close process is a race. LedgerLive operates it like the Williams F1 pit wall:
> lanes hold position, checkpoints gate progress, incidents surface in real-time, approvals
> gate the car through scrutineering, and every tool trace becomes the telemetry pack
> the stewards audit. No LLM keys required — fully deterministic in DEMO mode.

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

### Why Racing Fits

Pit stops are **timed checkpoints** — a reconciliation run that takes twice as long as its SLA
is a slow pit stop; the team sees it immediately in the lap delta.

Telemetry is the **audit trail** — every tool call emits a structured trace; the court pack
is the stewards' evidence package containing those traces plus signed verification hashes.

Safety Car is **pause automation for approvals/risk** — when an approval chain is unresolved,
the close automation halts (fail-closed) until the pit wall gives the all-clear, just as racing
drivers slow behind the safety car until the track is declared safe.

## Why Airia

LedgerLive showcases the Airia platform's three core strengths:

1. **Orchestration** — 340+ deterministic waves chained into a single close workflow, all
   expressible as Airia template steps with typed inputs and outputs.
2. **Security posture** — every action passes through a typed guard; no write without approval
   in HITL lanes; fail-closed on all ambiguity.
3. **No-code template export** — Blueprint Builder (W301-305) compiles close workflows into
   Airia community bundles; no API keys required for demo mode.

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

The `GET /api/airia/compat_report` endpoint produces a deterministic proof report:

| Check | What it validates |
|-------|-------------------|
| Bundle Structure Completeness | All 7 required files present |
| Tool Schemas Version-Pinned | Every tool has a pinned schema_version |
| Workflow DAG Acyclic + Stable Ordering | Steps are unique, monotonically ordered |
| Approvals for Sensitive Steps | HITL gate exists before close |
| Fail-Closed Rules Enabled | `on_error=halt` on critical steps |
| Required Outputs Present | telemetry, court, replay, narrative documented |
| Deterministic Checksums Match | sha256 hashes match bundle files |

`overall: PASS` — all checks verified offline, no API keys required.

Run: `make airia:compat` to write `artifacts/airia/community_bundle/compat_report.json`.

## No-Code Builder Preview

The `/airia` page ships a live **No-Code Builder Preview** showing the workflow DAG
as interactive step cards, each with:

- Approval-required / fail-closed / evidence-required badges
- Mapped tool ID and I/O schema version
- Link to dossier / verification artifacts

An **Import Walkthrough** panel explains each step of importing the bundle into Airia:
what gets created, how it's configured, and which endpoints it calls.
