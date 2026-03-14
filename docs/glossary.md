# Glossary of Finance Terms

> Key terms used throughout LedgerLive documentation and the finance close process.

---

**Accrual**
An accounting entry that recognizes revenue or expenses before cash changes hands. Accruals ensure financial statements reflect economic activity in the period it occurred, not when payment was made or received.

**Audit Trail**
A chronological record of every action taken in the system. In LedgerLive, every state mutation emits an audit event with a unique event ID, trace ID, timestamp, action type, and detail payload. The audit trail is append-only.

**Cash Application**
The process of matching incoming customer payments to outstanding invoices. LedgerLive automates this through the reconciliation engine by matching bank deposit lines to AR open items.

**Chart of Accounts (COA)**
A structured list of all accounts used to record financial transactions. The COA defines account numbers, names, types (asset, liability, equity, revenue, expense), and hierarchy. LedgerLive manages COA through Wave 17.

**Close Period**
A defined time range (month, quarter, year) for which financial records are finalized. Closing a period means all transactions are reconciled, exceptions resolved, and the evidence binder sealed. No further changes are permitted after close.

**Consolidation**
The process of combining financial statements from multiple legal entities into a single set of group-level statements. Involves eliminating intercompany transactions, translating foreign currencies, and applying consolidation adjustments.

**Deferral**
An accounting entry that postpones recognition of revenue or expense to a future period. The opposite of an accrual. A prepaid subscription is a common deferral -- cash is paid now, but the expense is recognized monthly.

**Evidence Binder**
A packaged collection of all artifacts for a close period: source documents, reconciliation results, exception resolutions, approval chains, and audit events. LedgerLive seals each binder with a SHA-256 hash for tamper detection.

**Exception**
A reconciliation mismatch that cannot be auto-approved. Exceptions are classified by category (timing, duplicate, missing, amount mismatch) and severity (low, medium, high). High-severity exceptions require human review.

**General Ledger (GL)**
The master accounting record that contains all financial transactions for an organization. Every debit and credit posts to the GL. Reconciliation compares source documents against GL entries.

**HITL (Human-in-the-Loop)**
A design pattern where the AI agent handles routine decisions autonomously but routes uncertain or high-impact items to a human reviewer. In LedgerLive, HITL applies to high-severity exceptions and items where the agent's confidence is below 70%.

**Intercompany Elimination**
During consolidation, transactions between entities within the same corporate group must be removed to avoid double-counting. For example, if Entity A sells to Entity B, that revenue and expense cancel out at the group level.

**Journal Entry (JE)**
A record of a financial transaction in the general ledger. Each JE has a debit side and a credit side that must balance. LedgerLive's JE posting module (Wave 33) automates suggested entries based on reconciliation results.

**Materiality Threshold**
The dollar amount below which variances are considered immaterial and can be auto-resolved. Exceptions below the materiality threshold do not require human review. This threshold is configurable per entity and period.

**Reconciliation**
The process of comparing two sets of records (e.g., bank statement vs. GL) to confirm they agree. LedgerLive scores each match on amount, date, and reference similarity, producing a composite match score with a human-readable explanation.

**Segregation of Duties (SoD)**
An internal control principle requiring that no single individual performs all steps of a critical process. In LedgerLive, the person who creates an exception cannot be the same person who approves its resolution.

**SLA (Service Level Agreement)**
A commitment to complete a task within a defined timeframe. In the close process, SLAs define deadlines for reconciliation completion, exception resolution, and binder finalization. The SLA monitor (Wave 224) tracks adherence.

**SOX (Sarbanes-Oxley Act)**
US federal legislation requiring public companies to maintain effective internal controls over financial reporting. LedgerLive's audit trail, evidence binders, and segregation of duties support SOX compliance requirements.

**Three-Way Match**
A verification process that compares three documents: the purchase order, the goods receipt, and the vendor invoice. All three must agree on quantity and price before payment is approved. LedgerLive automates this through Wave 34.

**Variance**
The difference between two values being compared during reconciliation. A variance of $0.02 on a $10,000 transaction is likely a rounding issue. A variance of $5,000 is likely a missing entry or duplicate. Variance analysis drives exception classification.
