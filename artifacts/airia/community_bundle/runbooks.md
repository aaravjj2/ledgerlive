# LedgerLive Close Workflow — Runbooks

## Step 1: Document Ingest

**F1 Metaphor:** Sensor data arriving from the car.

**What it does:** Collects all sub-ledger documents for the close period (AP invoices, AR
settlements, payroll accruals, intercompany entries) and runs OCR + structured extraction.

**When to use:** First step of every close cycle. Triggered automatically on schedule or
manually via Race Control.

**What can go wrong:**
- Document feed unavailable → `halt` triggered, incident created, pit-wall alerted
- OCR confidence < threshold → document queued for manual review

**Resolution:** Re-trigger feed, or upload document manually via Documents page.

---

## Step 2: AP/AR Reconciliation

**F1 Metaphor:** Computing lap delta — is the variance within tolerance or an outlier?

**What it does:** Matches AP invoices against AR settlements. Items within `drift_threshold_pct`
are auto-approved. Items outside threshold become exceptions.

**When to use:** Runs automatically after ingest completes.

**What can go wrong:**
- High exception rate → review drift threshold configuration
- Currency mismatch → intercompany entries may need manual FX alignment

**Resolution:** Adjust drift threshold in config, or manually clear items in Reconciliation page.

---

## Step 3: Exception Triage

**F1 Metaphor:** Deploying marshal flags — yellow for caution, red for halt.

**What it does:** Classifies each exception as P1 (critical, blocks close), P2 (high, same-day
SLA), or P3 (low, next-day SLA). Routes each to the appropriate review queue.

**When to use:** Runs automatically after reconciliation.

**What can go wrong:**
- Unclassified exception type → falls to P1 by default (fail-safe)
- SLA already breached → P1 escalation to department head

**Resolution:** Review Exceptions page. Override classification if needed.

---

## Step 4: HITL Approval Gate

**F1 Metaphor:** Pit stop — the pit wall must confirm before the car re-joins the track.

**What it does:** Routes classified exceptions to the configured approver chain. Monitors
deadline. Escalates overdue approvals. Blocks close progress until all P1/P2 items cleared.

**When to use:** Runs after triage. Human action required.

**What can go wrong:**
- Approver unavailable → escalation to next level in chain
- Deadline passed → automatic escalation to close manager

**Resolution:** Review Queue page. Approve, reject, or reassign items.

---

## Step 5: Seal Evidence Binder

**F1 Metaphor:** Chequered flag — the court pack is sealed for the stewards.

**What it does:** Compiles all approved items, audit log entries, and system assertions into
a signed evidence PDF with sha256 manifest. Writes final audit trail entry.

**When to use:** Runs automatically after all P1/P2 items approved.

**What can go wrong:**
- Outstanding P1 items → binder seal blocked (fail-closed)
- Storage unavailable → retry 3x then alert

**Resolution:** Clear all P1/P2 items in Review Queue, then re-trigger close step.

---

## Audit Trail Notes

Every action in all 5 steps is logged to the immutable audit trail with:
- Actor (user or system)
- Timestamp (UTC)
- Event type
- Payload sha256

The audit trail is available at `/audit` and exported in the evidence binder.

---

## Output Artifacts

### Telemetry Pack
The telemetry pack captures every tool trace, tool call input/output, drift budget evaluation,
and system event generated during the close cycle. It is the F1 pit-wall telemetry for auditors.
Exported via `POST /api/ops/export/telemetry-pack`. Always deterministic — same inputs produce
the same SHA-256 hash.

### Court Pack
The court pack is the stewards' evidence package: approved items, telemetry pack reference,
and the sealed evidence binder manifest. Exported via `POST /api/ops/export/court-pack`.

### Replay Log
The replay log allows any completed close cycle to be deterministically replayed from the
same input seed. The replay is bit-for-bit identical across runs — every SHA-256 assertion
remains stable. Use `GET /api/ops/replay/{run_id}` to fetch the replay index.

### Narrative Close Report
The narrative report is a human-readable, prose-form summary of the close cycle. It includes
a timeline, exception summary, approval trace, and final attestation. The narrative is rendered
deterministically from the underlying event log and can be exported to PDF or Markdown.
Available at `GET /api/ops/narrative/{run_id}`.
