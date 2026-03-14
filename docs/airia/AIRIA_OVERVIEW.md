# Airia Platform — LedgerLive Integration Overview

## Agent Summary

**LedgerLive Race Control Close Agent** is a deterministic, no-LLM-key orchestration agent that
models month-end financial close as a Williams F1 race-control operation.

| Property | Value |
|----------|-------|
| Agent Name | LedgerLive Race Control Close Agent |
| Category | Finance → Period Close |
| Platform | Airia Community Bundle |
| Version | v0.302.0-ledgerlive |
| Waves | 340 deterministic service waves |
| Tests | 4042+ passing |
| Mode | DEMO (no API keys) / LOCAL (dev) |

## What Problem It Solves

Month-end close is multi-team, multi-approval, and deadline-critical.
Traditional finance teams track it in spreadsheets or project-management tools with no real-time
visibility, no audit trail, and no fail-closed safety.

LedgerLive replaces that with a race-control metaphor:

| Finance Problem | LedgerLive Solution |
|-----------------|---------------------|
| No close-progress visibility | Race Control dashboard, lap completion indicators |
| Exception triage latency | Real-time incident log with SLA escalation |
| Approval chains scattered | HITL review queue with approver chain |
| Audit evidence manual | Automated evidence binder + sha256 assertions |
| Intercompany DR/CR matching | Reconciliation engine with drift budget |
| Cutoff date management | Safety-car mode: fail-closed until approvals |

## Airia Platform Fit

| Airia Capability | How LedgerLive Uses It |
|-----------------|----------------------|
| Tool Registry | 8+ specialized tools: OCR, reconciliation, exception triage, HITL, audit |
| Workflow Templates | 5-step DAG covering the full close cycle |
| No-code Blueprint Builder | Waves 301-305 compile close workflows visually |
| Community Bundle Export | `make airia:bundle` → shareable bundle for other Airia users |
| Deterministic Demo Mode | Zero API keys; all 340 waves run reproducibly |
| Security Posture | Fail-closed guards; no write without approval |

## Integration Points

- `/airia` — Airia Readiness page (bundle hash, PASS badge, tools list)
- `GET /api/airia/status` — JSON: hash, template_hash, validator_status, tools
- `POST /api/airia/generate-bundle` — create/refresh community bundle
- `POST /api/airia/validate-bundle` — strict readiness check
- `POST /api/airia/verify-bundle` — offline checksum verification

## Quick Start (Demo Mode)

```bash
# Start the full stack in DEMO mode
make demo

# Generate the Airia community bundle
make airia:bundle

# Validate the bundle is Airia-import-ready
make airia:validate

# Verify bundle checksums offline
make airia:verify
```
