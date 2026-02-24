# Airia Community Bundle — Import Guide

## Bundle Location

```
artifacts/airia/community_bundle/
├── manifest.json              # Bundle metadata + deterministic hashes
├── tools.json                 # Airia tool registry entries (8 tools)
├── workflow_template.json     # 5-step orchestration DAG
├── runbooks.md                # Human-readable runbooks for each step
├── screenshots_manifest.json  # Proof screenshots index
├── checksums.txt              # sha256 of each bundle file
└── verify_bundle.py           # Offline checksum verifier
```

## Generating the Bundle

```bash
make airia:bundle    # writes all 7 files deterministically
make airia:validate  # checks completeness + hash stability
make airia:verify    # offline checksum pass/fail
```

Or via CLI directly:

```bash
python tools/airia_bundle.py --action bundle
python tools/airia_bundle.py --action validate
python tools/airia_bundle.py --action verify
```

## Bundle Structure

### `manifest.json`

```json
{
  "name": "ledgerlive-race-control-close-agent",
  "version": "v0.302.0-ledgerlive",
  "category": "Finance / Period Close",
  "tags": ["finance", "close", "f1", "williams", "airia", "reconciliation"],
  "bundle_hash": "<sha256 of stable content>",
  "template_hash": "<sha256 of workflow_template.json>"
}
```

### `tools.json` — 8 Tool Entries

| Tool ID | Type | Purpose |
|---------|------|---------|
| `ledgerlive.ingest` | DocumentReader | OCR + extraction from sub-ledger feeds |
| `ledgerlive.reconcile` | DataMatcher | AP/AR matching with drift budget |
| `ledgerlive.triage` | Classifier | Exception severity + routing |
| `ledgerlive.hitl_review` | HumanInTheLoop | Approval gate with chain |
| `ledgerlive.audit_trail` | EventLogger | Immutable append-only evidence log |
| `ledgerlive.evidence_binder` | DocumentWriter | Signed PDF + sha256 assertions |
| `ledgerlive.blueprint_builder` | WorkflowCompiler | Maps close tasks to Airia steps |
| `ledgerlive.race_control` | Dashboard | Real-time close-progress monitor |

### `workflow_template.json` — 5-Step DAG

| Step | ID | Description |
|------|----|------------|
| 1 | `ingest` | Ingest sub-ledger docs, run OCR |
| 2 | `reconcile` | Match AP/AR, flag variances |
| 3 | `triage` | Classify exceptions, apply SLA |
| 4 | `review` | HITL approval gate |
| 5 | `close` | Seal evidence binder, write audit trail |

## Importing into Airia

1. Open the Airia platform → **Community → Import Bundle**
2. Upload `artifacts/airia/community_bundle/manifest.json`
3. Airia validates the bundle hash and imports all tools + template
4. Click **Deploy** to activate the workflow in your workspace
5. Navigate to the **Race Control** embedded dashboard for real-time monitoring

## Offline Verification

```bash
python artifacts/airia/community_bundle/verify_bundle.py
# → PASS  (all checksums match)
```

Exit code 0 = PASS, exit code 1 = FAIL (with diff output).
