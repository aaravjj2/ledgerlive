# CFO Demo Walkthrough — Williams F1 Quarterly Close

## Problem

A Williams Racing CFO faces a quarterly close with:
- 8 invoices across 3 currencies (GBP/EUR/USD) totaling $22M+ in payables
- FIA cost cap compliance at $135M with only $3.8M runway
- 3 exceptions: duplicate payment ($78K), FX variance ($142.5K), missing PO ($45K)
- Manual close takes 66 hours across 5 stages

**Without LedgerLive:** 2+ weeks of manual reconciliation, exception triage done in spreadsheets, cost cap risk discovered too late.

## What the Agent Does

LedgerLive runs an autonomous **perceive→decide→act** loop:

1. **PERCEIVE** — reads live state from documents, OCR, reconciliations, exceptions, workflows
2. **DECIDE** — applies triage rules with confidence scoring (auto-resolve low-risk, escalate high-risk)
3. **ACT** — executes actions: resolve exceptions, advance workflows, post to Airia webhook

Each cycle produces a full decision trace with reasoning, citations, and audit trail.

## What Changed (Before → After)

| Metric | Before (Manual) | After (Agent) |
|--------|-----------------|---------------|
| Close time | 66 hours | 4.1 hours (16x faster) |
| Exception triage | 12 hours manual | 18 minutes auto |
| Cost cap visibility | End-of-quarter report | Real-time runway |
| Exceptions auto-resolved | 0% | 67% (2/3) |
| Dollar impact saved | $0 | $123K recovered |
| Audit trail | Spreadsheet notes | SHA-256 sealed traces |

## Why the CFO Cares

1. **Cost cap compliance** — real-time runway display ($3.8M / 2.8% buffer) prevents FIA penalties
2. **Risk visibility** — FX variance on Mercedes HPP power unit invoice surfaced immediately, not at quarter-end
3. **Audit readiness** — every decision has reasoning, citations, and a checksum; court pack generated on demand
4. **Speed** — the close is a race; 16x speedup means Williams can react to cost pressures within the same quarter

## Demo Flow (6 Steps)

1. **Pit Stop: Ingest** — `/documents` — 5 invoices land (Mercedes HPP, DHL, Hilton, Pirelli, sponsors)
2. **Qualifying: Reconcile** — `/reconciliation` — agent matches 94.3% of entries automatically
3. **Safety Car: Triage** — `/exceptions` — 3 exceptions flagged with confidence scores
4. **DRS Zone: Auto-Resolve** — `/exceptions` — 2/3 resolved; duplicate recovered, hospitality excluded
5. **Pit Wall: Approve** — `/review-queue` — CFO reviews FX hedge recommendation
6. **Podium: Seal** — `/race-control` — court pack with SHA-256 integrity seals

## Key Endpoints

| Endpoint | Method | What It Does |
|----------|--------|-------------|
| `/api/agent/cycle` | POST | Run one perceive→decide→act cycle |
| `/api/agent/perceive` | GET | Read-only perception of current state |
| `/api/cfo/cockpit` | GET | Cost cap runway, exception impact, close velocity |
| `/api/cfo/scenario` | GET | Full Williams Q1 2026 scenario pack |
| `/api/cfo/story-mode` | GET | 6-step guided walkthrough |
| `/api/agent/ask` | POST | Ask Race Engineer (conversational) |
| `/api/webhook/airia` | POST | Airia inbound webhook trigger |
| `/api/webhook/airia/export` | POST | Export results in Airia format |
| `/api/race-control` | GET | Live race control dashboard state |

## Test IDs for E2E

- `cfo-story-step-1` through `cfo-story-step-6` — story mode panels
- `ask-race-engineer-panel` — conversational agent input
