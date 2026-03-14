# How It Works: Reconciliation Engine and Close Flow

> This document explains the end-to-end financial close process in LedgerLive,
> from document ingestion through evidence binder generation.

---

## Overview

LedgerLive automates the month-end close by chaining four stages together:

1. **Ingest and Extract** -- Documents enter the system, get OCR-processed, and have fields extracted.
2. **Match and Reconcile** -- Extracted data is matched against the general ledger using a scoring algorithm.
3. **Triage Exceptions** -- Mismatches are classified by severity and routed for resolution.
4. **Seal and Ship** -- Approved results are assembled into a tamper-evident evidence binder.

---

## Stage 1: Document Ingest, OCR, and Field Extraction

### Ingest

When a document (invoice, bank statement, vendor statement) arrives via `POST /api/documents`, the system:

1. Computes a SHA-256 content hash for deduplication and tamper detection.
2. Stores metadata (filename, upload timestamp, source entity).
3. Emits an audit event: `create` on `document`.

### OCR Processing

The document is submitted to the OCR pipeline (`POST /api/ocr-jobs`):

1. Text extraction runs with confidence scoring (target: >94%).
2. Each job tracks status (`pending` -> `processing` -> `completed`).
3. Extracted text is stored alongside the original document reference.

### Field Extraction

After OCR, the extraction service (Wave 5) identifies structured fields:

- **Amounts** (invoice total, line items, tax)
- **Dates** (invoice date, due date, payment date)
- **Reference numbers** (invoice number, PO number, check number)
- **Counterparty identifiers** (vendor name, account number)

Each extracted field carries a confidence score. Fields below the confidence threshold are flagged for manual review.

---

## Stage 2: Multi-Way Matching

LedgerLive supports three reconciliation types:

| Type | Source | Target | Use Case |
|------|--------|--------|----------|
| Bank-to-GL | Bank statement lines | General ledger entries | Cash reconciliation |
| Subledger-to-GL | AP/AR subledger | GL control account | Subledger tie-out |
| Vendor statement | Vendor-provided statement | Internal AP records | Vendor balance confirmation |

### Matching Algorithm

Each candidate pair is scored across three dimensions:

1. **Amount match** -- Fuzzy match with configurable tolerance (default: $0.50 or 0.1%).
   The score is `1.0 - (abs(source_amount - target_amount) / max(source_amount, 1))`.

2. **Date window** -- Transactions must fall within a configurable window (default: 3 business days).
   Score: `1.0` if same day, linearly decaying to `0.5` at the window boundary.

3. **Reference match** -- Fuzzy string matching on reference/invoice numbers.
   Uses normalized edit distance. Score: `1.0` for exact match, `0.0` for no similarity.

The **composite match score** is a weighted average:

```
match_score = (0.50 * amount_score) + (0.25 * date_score) + (0.25 * reference_score)
```

Matches scoring above `0.85` are auto-approved. Matches between `0.60` and `0.85` are flagged for review. Matches below `0.60` generate an exception.

### Explanation

Every reconciliation result includes a human-readable `explanation` field describing why the match succeeded or failed. This explanation is included in the evidence binder and audit trail.

---

## Stage 3: Exception Classification

When a reconciliation produces a mismatch (score < 0.85), the exception classifier assigns:

### Severity Levels

| Severity | Criteria | Action |
|----------|----------|--------|
| **Low / Info** | Amount variance < materiality threshold, timing differences | Auto-resolve (95% confidence) |
| **Medium** | Moderate variance, pattern-based issues | Auto-resolve (75% confidence) or manual review |
| **High** | Large variance, duplicate payments, missing entries | Escalate to review queue |

### Exception Categories

- `timing_difference` -- Transaction recorded in different periods.
- `rounding_variance` -- Sub-penny differences from FX or rounding.
- `duplicate_payment` -- Same amount/vendor/date appears twice.
- `missing_entry` -- Source transaction has no GL counterpart.
- `amount_mismatch` -- Amounts differ beyond tolerance.
- `unidentified` -- Cannot be classified automatically.

### Auto-Resolve vs. Escalate Logic

The agent applies rule-based triage during its Decide phase:

1. **Low-severity exceptions**: Auto-resolved immediately. The resolution includes a reasoning trace explaining why the item is below the materiality threshold.
2. **Medium-severity exceptions**: Auto-resolved if the agent's confidence exceeds 70%. Otherwise, escalated to the review queue.
3. **High-severity exceptions**: Always escalated to the HITL review queue with the reasoning trace attached.

---

## Stage 4: Human-in-the-Loop Review

Items routed to the review queue (`/api/review-queue`) follow this flow:

1. **Assignment** -- The system assigns the item to the appropriate reviewer based on amount thresholds and entity.
2. **Review** -- The reviewer sees the AI's reasoning, the original documents, and the reconciliation details.
3. **Decision** -- The reviewer approves or rejects. Both actions emit audit events with the reviewer's identity and rationale.
4. **Workflow advance** -- Once all blocking exceptions are resolved (by agent or human), the agent advances the workflow to the next stage.

---

## Stage 5: Evidence Binder Generation

After all reconciliations are approved and exceptions resolved, the evidence binder assembles the audit package:

1. **Create binder** (`POST /api/evidence-binder`) -- Opens a new binder for the close period.
2. **Add sections** -- Each section includes documents, reconciliation results, exception resolutions, and approval chains.
3. **Finalize** (`POST /api/evidence-binder/{id}/finalize`) -- Seals the binder with a SHA-256 hash of all contents.

The finalized binder provides:

- Tamper-evident integrity (any modification invalidates the hash).
- Complete decision trace from ingestion through approval.
- Auditor-ready packaging with document cross-references.

---

## End-to-End Flow Diagram

```
Document Upload
      |
      v
  OCR Pipeline (>94% confidence)
      |
      v
  Field Extraction (amounts, dates, references)
      |
      v
  Reconciliation Engine
      |
      +-- match_score >= 0.85 --> Auto-Approve
      |
      +-- 0.60 <= score < 0.85 --> Flag for Review
      |
      +-- score < 0.60 ----------> Create Exception
                                        |
                                        v
                                  Exception Classifier
                                        |
                          +-------------+-------------+
                          |             |             |
                       Low/Info      Medium         High
                          |             |             |
                     Auto-Resolve   Conditional   Escalate
                                    Resolve        to HITL
                                        |             |
                                        v             v
                                   Review Queue --> Approve/Reject
                                                        |
                                                        v
                                                Evidence Binder (SHA-256 sealed)
```
