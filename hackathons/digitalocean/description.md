# LedgerLive -- Full-Stack Finance Agent on DigitalOcean

## The Problem

Small and mid-market finance teams run the monthly close with spreadsheets, email threads, and manual data entry. Document OCR -- extracting invoice amounts, dates, and vendor names from scanned PDFs -- is a persistent bottleneck. Enterprise OCR solutions require GPU compute that costs thousands per month. These teams cannot justify the spend, so they type the numbers by hand.

The result: 40+ hours per quarter on manual close, a 3-5% error rate on hand-keyed data, and audit findings that trace directly to transcription mistakes.

## The Solution

LedgerLive is a full-stack finance close agent deployed entirely on **DigitalOcean infrastructure**. It uses **Gradient AI** for GPU-accelerated document extraction, **Managed PostgreSQL** for transactional data, **App Platform** for zero-downtime deployments, and **Spaces** for tamper-evident document storage. The entire platform runs on DigitalOcean -- no external cloud dependencies.

The agent automates the close end-to-end: ingest documents, extract fields via Gradient AI, reconcile against the general ledger, triage exceptions with confidence scores, route approvals to the right person, and compile a sealed evidence binder for auditors.

## How Gradient AI Is Used

LedgerLive integrates Gradient AI at three stages of the document pipeline:

1. **Document extraction** -- Scanned invoices and bank statements are sent to Gradient AI's inference endpoint. The model extracts structured fields (vendor name, invoice number, amount, date, line items) from unstructured PDF images. Each field includes a confidence score so the agent knows when to trust the extraction and when to escalate for human review.

2. **Field classification** -- Extracted fields are classified into accounting categories (revenue, expense, asset, liability) using Gradient AI's fine-tuned classification model. This powers the automated reconciliation engine -- the agent matches extracted line items to GL accounts without manual mapping.

3. **Confidence scoring and anomaly detection** -- Gradient AI provides per-field confidence that feeds the exception triage system. Fields below 85% confidence are flagged for human review. Unusual patterns (a vendor invoice 10x the historical average) trigger anomaly alerts routed to the controller.

## Architecture

```
User --> App Platform (React + Vite)
           |
           v
         App Platform (FastAPI API)
           |
           +---> Gradient AI (document extraction, classification, scoring)
           |
           +---> Managed PostgreSQL (close cycles, reconciliations, exceptions)
           |
           +---> Spaces (document storage, evidence binders, audit artifacts)
```

All components run on DigitalOcean. No external cloud services are required.

| Service | Role |
|---------|------|
| **App Platform** | Hosts both the FastAPI backend and the React frontend with auto-scaling and zero-downtime deploys. |
| **Gradient AI** | GPU inference for OCR extraction, field classification, and confidence scoring. |
| **Managed PostgreSQL** | Stores close cycles, entities, reconciliation results, exceptions, workflows, and audit logs. |
| **Spaces** | S3-compatible object storage for uploaded documents, signed exports, and sealed evidence binders. |

## Special Prize Categories

### Best AI Agent Persona: LedgerBot

LedgerBot is the AI persona that runs the close. It uses an F1 racing metaphor -- each close stage is a race phase (pit stop for ingestion, qualifying for reconciliation, safety car for exceptions, checkered flag for sign-off). LedgerBot narrates every decision with racing commentary: "Timing difference on APAC-2847 -- auto-resolving, no pit stop needed." The persona is consistent across the dashboard, API responses, Slack notifications, and the voice interface. It makes accounting accessible without dumbing it down.

### Best Program for the People: Small Business Mode

LedgerLive ships a Small Business Mode designed for companies with fewer than 50 employees and no dedicated accounting team. When `APP_MODE=SMALL_BIZ` is set, the agent simplifies terminology (no "subledger reconciliation" -- just "check your bank matches"), reduces the number of approval steps, and provides guided walkthroughs for first-time users. The goal: a business owner with no accounting background can close their books in under 30 minutes.

## Impact

- **4,269 passing tests** across unit, integration, and E2E suites
- **340 API endpoints** covering the full close lifecycle
- **94%+ OCR confidence** on standard invoice formats via Gradient AI
- **Sub-30-minute close** for small businesses in Small Business Mode
- **Tamper-evident audit trail** with SHA-256 sealed evidence binders stored in Spaces

## Repository

- **GitHub**: [github.com/aaravjj2/ledgerlive](https://github.com/aaravjj2/ledgerlive)
- **Branch**: `waves`
- **Quick start**: `git clone && cp .env.example .env && make demo`
