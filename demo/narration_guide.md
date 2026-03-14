# LedgerLive — Demo Narration Guide

## Universal Opening (30 seconds)

> "Every quarter, finance teams spend 40+ hours manually closing their books.
> Reconciling transactions, chasing missing documents, triaging exceptions —
> it's tedious, error-prone, and costs companies an average of $300,000 per year
> in errors alone. LedgerLive changes that."

## Dashboard Walkthrough (60 seconds)

> [Show Dashboard at /dashboard]
> "This is the LedgerLive dashboard — think of it as your finance pit lane.
> At a glance you can see: documents processed, OCR pipeline status,
> reconciliation progress, and open exceptions. Everything updates in real-time."

## Reconciliation (45 seconds)

> [Navigate to /reconciliations]
> "The AI agent runs bank-to-GL, subledger-to-GL, and vendor statement
> reconciliations automatically. Each result shows the match score AND the
> agent's reasoning — not just 'matched' or 'unmatched', but WHY."

## Exception Triage (45 seconds)

> [Navigate to /exceptions]
> "When the agent finds a mismatch, it doesn't just flag it. It classifies
> the exception — is this a timing difference the agent can auto-resolve?
> Or a duplicate payment that needs a human's eyes? Critical items pause the
> entire close process until resolved. We call this the Safety Car."

## HITL Review (30 seconds)

> [Navigate to /review-queue]
> "High-severity exceptions are routed to the right approver. Each item shows
> the full reasoning chain — you can see exactly why the AI escalated this."

## Close Statement (30 seconds)

> "LedgerLive doesn't replace your finance team — it gives them superpowers.
> Every decision is explained, every artifact is sealed with SHA-256, and
> every approval is logged. It's not a black box — it's a glass cockpit."

---

## Gemini-Specific Section (60 seconds)

> [Navigate to /live-voice]
> "Now here's what makes this special for the Gemini challenge. The CFO can
> literally TALK to their ledger. Watch this..."
> [Click Connect, then ask: "What exceptions need my review?"]
> "LedgerBot responds in real-time, pulling live data from the reconciliation
> engine. I can say 'approve exception 1' and the system updates immediately —
> all via voice."

## DigitalOcean-Specific Section (45 seconds)

> [Show /gradient metrics]
> "The document OCR pipeline runs on DigitalOcean Gradient AI — GPU-backed
> inference that processes invoices at 94%+ confidence. The database runs on
> Managed Postgres, documents are stored in Spaces, and the whole stack
> deploys to App Platform with a single command."

## Airia-Specific Section (45 seconds)

> [Show /airia readiness page]
> "The system exposes 8 MCP tools for Airia integration. The IngestionAgent,
> ReconciliationAgent, ExceptionTriageAgent, and HITLCoordinator all
> orchestrate through Airia's flow engine. Here's the compatibility report —
> all 10 checks passing."

## GitLab-Specific Section (45 seconds)

> [Show /api/gitlab/compliance-rules]
> "The compliance agent monitors every merge request that touches financial
> configuration. It runs 10 rules — from tolerance changes to account code
> modifications — and generates a signed audit artifact on merge."
