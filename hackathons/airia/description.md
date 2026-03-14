# LedgerLive -- Multi-Agent Finance Close on Airia

## The Problem

The monthly financial close is not one task -- it is dozens of tasks spanning multiple teams, systems, and approval chains. The ingestion team pulls documents from Google Drive and email. The reconciliation team matches bank feeds to the general ledger. The exception team triages mismatches. The controller reviews and signs off. Each handoff is a potential failure point: a missed document, a stale spreadsheet, a Slack message that went unread.

Manual coordination across these teams and systems costs mid-market finance departments 40+ hours per quarter and introduces errors that auditors find months later.

## The Solution

LedgerLive deploys **four specialized AI agents** orchestrated through the **Airia platform**. Each agent owns one phase of the close. Airia handles orchestration, webhook delivery, tool routing, and the no-code builder experience. The agents do not share a monolithic context -- each operates within its domain, hands off structured data to the next, and logs every decision for audit.

### The Four Agents

| Agent | Domain | What it does |
|-------|--------|-------------|
| **IngestionAgent** | Document intake | Watches Google Drive folders and email inboxes. Pulls invoices, bank statements, and contracts. Computes content hashes, deduplicates, and queues for OCR extraction. |
| **ReconciliationAgent** | Matching | Runs bank-to-GL, subledger-to-GL, and vendor statement reconciliations. Produces match scores, explanations, and reasoning traces for every pair. |
| **ExceptionTriageAgent** | Anomaly handling | Classifies each mismatch by severity and type (timing difference, duplicate payment, missing entry). Auto-resolves low-risk items. Escalates critical items with confidence scores and recommended actions. |
| **HITLCoordinatorAgent** | Human-in-the-loop | Routes escalated items to the right approver via Slack and the review queue. Generates HITL documents with full context so reviewers can approve in one click, not dig through data. |

### Nested Agent Architecture

The agents form a directed pipeline, but the architecture supports nesting. The ExceptionTriageAgent can invoke a sub-agent to investigate a specific anomaly pattern (e.g., a currency conversion discrepancy that requires pulling FX rate history). The HITLCoordinatorAgent dynamically generates approval documents that include the entire decision chain -- which agent decided what, with what confidence, and why.

## How Airia Is Used

LedgerLive integrates with Airia at five touchpoints:

1. **Community Listing** -- LedgerLive is packaged as an Airia Community listing with a `bundle.json` manifest, tool definitions, and metadata. The `make airia:bundle` command generates the listing artifact.

2. **MCP Tools** -- Eight Model Context Protocol tools are registered with Airia: `query_exceptions`, `approve_item`, `run_reconciliation`, `get_close_status`, `upload_document`, `get_evidence_binder`, `search_audit_log`, and `get_workflow_status`. Each tool has a JSON schema, is callable from Airia's agent runtime, and returns structured responses.

3. **Webhook Delivery** -- Airia delivers events to LedgerLive's `/api/airia/webhook_inbound` endpoint. The agent processes events (new document uploaded, approval completed, escalation triggered) and logs delivery receipts.

4. **No-Code Builder** -- LedgerLive exposes a Blueprint Builder that maps to Airia's no-code interface. Finance users configure close workflows (which entities, which reconciliation types, which approval chains) without writing code. The builder generates executable workflow definitions.

5. **Compatibility Verification** -- `make airia:compat` runs a 10-check compatibility report: schema validation, tool registration, workflow presence, fail-closed rules, blueprint accessibility, required outputs, and deterministic checksums.

## Cross-System Integration

| System | Integration |
|--------|------------|
| **Google Drive** | IngestionAgent watches shared folders for new documents |
| **Slack** | HITLCoordinatorAgent sends approval requests and receives responses |
| **QuickBooks (mock)** | GL data source for reconciliation; chart of accounts for mapping |
| **Email** | IngestionAgent processes invoices from vendor email threads |

## What Makes This Novel

- **Nested agent invocation**: Agents spawn sub-agents for specialized investigation, not just sequential handoff.
- **Dynamic HITL document generation**: The HITLCoordinatorAgent builds approval documents on the fly, including the full reasoning chain from upstream agents. Reviewers see *why* an item was escalated, not just *that* it was escalated.
- **Audit-sealed orchestration log**: Every agent decision, tool call, and webhook delivery is logged with SHA-256 checksums. The evidence binder is regenerable and tamper-evident.

## Impact

- **4,269 passing tests** with full Airia compatibility verification
- **8 MCP tools** callable from Airia's agent runtime
- **10/10 Airia compatibility checks** passing on every commit
- **Hands-free close orchestration** across four specialized agents
- **Court-ready evidence binders** with complete decision lineage

## Repository

- **GitHub**: [github.com/aaravjj2/ledgerlive](https://github.com/aaravjj2/ledgerlive)
- **Branch**: `waves`
- **Quick start**: `git clone && cp .env.example .env && make demo`
