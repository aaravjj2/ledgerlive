# LedgerLive -- Compliance-Aware GitLab Duo Agent for Finance Config

## The Problem

In regulated finance operations, configuration changes in code have compliance implications that typical CI/CD pipelines do not catch. When a developer modifies a reconciliation threshold, changes an approval routing rule, or updates a chart of accounts mapping, those changes can trigger SOX control violations, alter audit trail integrity, or break segregation-of-duties requirements. Standard code review catches syntax errors. It does not catch compliance errors.

Finance teams discover these issues during quarterly audits -- weeks or months after the change shipped. Remediation is expensive. Restatements are worse.

## The Solution

LedgerLive integrates a **GitLab Duo Agent** that monitors every merge request for finance-sensitive configuration changes. When a developer pushes a change to a reconciliation rule, approval threshold, or GL mapping, the agent:

1. **Detects** the config change using pattern matching on file paths and content diffs
2. **Analyzes** the compliance impact using Claude (Anthropic) for semantic understanding of what the change means in a finance context
3. **Runs** automated compliance checks against the controls catalog (SOX, SOC 2, GDPR)
4. **Generates** audit artifacts -- a compliance impact report attached to the MR as a comment
5. **Blocks or approves** the MR based on risk level, with a clear explanation of why

The agent is not a linter. It understands that changing `RECON_THRESHOLD` from 100 to 10000 is not a typo -- it is a control change that affects the materiality of auto-resolved exceptions.

## Anthropic Integration (Bonus Prize: $13,500)

LedgerLive uses **Claude** (via the Anthropic API) as the compliance reasoning engine inside the GitLab Duo Agent:

- **Semantic diff analysis** -- Claude reads the full diff context (not just the changed lines) and identifies which changes have compliance implications. It distinguishes between a comment update and a threshold change.
- **Control mapping** -- Claude maps each compliance-relevant change to the affected controls in the controls catalog. "Changing the approval threshold from $5,000 to $50,000 weakens SOX control AC-7: Transaction Approval Limits."
- **Impact narrative** -- Claude generates a human-readable compliance impact summary posted as an MR comment. Auditors can read the MR thread and understand the compliance decision without opening a separate tool.
- **Risk classification** -- Claude assigns a risk level (LOW / MEDIUM / HIGH / CRITICAL) to each change, driving the automated block/approve decision.

## Google Cloud Integration (Bonus Prize: $13,500)

The GitLab Duo Agent runner executes as a **Google Cloud Function**:

- **Serverless execution** -- The agent runs as a Cloud Function triggered by GitLab webhook events. Zero infrastructure to manage, automatic scaling, pay-per-invocation.
- **Secret Manager** -- API keys for Anthropic, GitLab, and the LedgerLive backend are stored in Google Cloud Secret Manager. The Cloud Function accesses them at runtime via IAM-bound service accounts.
- **Cloud Logging** -- Every agent invocation, compliance check result, and MR annotation is logged to Cloud Logging for audit trail integrity.

## Green Agent (Bonus Prize: $3,000)

LedgerLive implements **tiered inference by risk level** to minimize energy consumption:

| Risk Level | Model Used | Rationale |
|------------|-----------|-----------|
| LOW | Local regex + rule engine | No LLM invocation. Pattern matching handles trivial changes (comments, formatting). |
| MEDIUM | Claude Haiku | Lightweight model for standard config changes. 3x lower energy than full analysis. |
| HIGH / CRITICAL | Claude Sonnet | Full semantic analysis reserved for changes that affect controls, thresholds, or approval chains. |

The agent logs the model tier used for each invocation. Over a typical quarter with 500 MRs, approximately 70% are LOW (no LLM call), 20% are MEDIUM (Haiku), and 10% are HIGH/CRITICAL (Sonnet). Estimated energy savings: 60-75% compared to running full Sonnet analysis on every MR.

## Architecture

```
GitLab MR Webhook
      |
      v
Google Cloud Function (agent runner)
      |
      +---> Pattern detection (local, no LLM)
      |
      +---> Claude Haiku / Sonnet (compliance reasoning)
      |
      +---> LedgerLive API (controls catalog, audit log)
      |
      v
GitLab MR Comment (compliance impact report)
GitLab MR Approval / Block
```

## What the Agent Catches

- Reconciliation threshold changes that weaken auto-resolution controls
- Approval routing modifications that break segregation of duties
- Chart of accounts mapping changes that affect financial statement classification
- Data retention policy modifications that violate GDPR or legal hold requirements
- Encryption configuration changes that affect SOC 2 compliance

## Impact

- **Pre-merge compliance detection** -- Issues found in the MR, not in the quarterly audit
- **Auditor-readable MR threads** -- Compliance narrative attached to every relevant change
- **4,269 passing tests** including compliance-specific test scenarios
- **60-75% energy reduction** via tiered inference (Green Agent approach)
- **Zero manual compliance review** for low-risk changes (automated pattern matching)

## Repository

- **GitHub**: [github.com/aaravjj2/ledgerlive](https://github.com/aaravjj2/ledgerlive)
- **Branch**: `waves`
- **Quick start**: `git clone && cp .env.example .env && make demo`
