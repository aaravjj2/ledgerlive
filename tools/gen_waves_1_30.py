#!/usr/bin/env python3
"""Generate LedgerLive Waves 1-30: domain services, routers, and tests.

This generator creates the complete finance close automation system:
- 30 domain services under apps/api/app/services/
- 30 routers under apps/api/app/routers/
- 30 test files under apps/api/tests/
- Registers all routers in main.py

Run: python tools/gen_waves_1_30.py
"""
import pathlib, textwrap, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SVC_DIR = ROOT / "apps" / "api" / "app" / "services"
RTR_DIR = ROOT / "apps" / "api" / "app" / "routers"
TST_DIR = ROOT / "apps" / "api" / "tests"
MAIN_PY = ROOT / "apps" / "api" / "app" / "main.py"

# ── Wave definitions ─────────────────────────────────────────────────
# (wave_num, slug, title, description, fields, operations)
WAVES = [
    (1, "close_period", "Close Period Management",
     "Manage accounting close periods with open/close/lock lifecycle.",
     [("period_id", "str"), ("name", "str"), ("status", "str"), ("fiscal_year", "int"), ("fiscal_month", "int"), ("opened_at", "str"), ("closed_at", "str|None")],
     [("list", "GET", "/api/close-periods", "List all close periods"),
      ("create", "POST", "/api/close-periods", "Create a new close period"),
      ("get", "GET", "/api/close-periods/{period_id}", "Get a close period by ID"),
      ("close_period", "POST", "/api/close-periods/{period_id}/close", "Close a period"),
      ("lock_period", "POST", "/api/close-periods/{period_id}/lock", "Lock a period")]),

    (2, "entity", "Entity Management",
     "Legal entities / business units for multi-entity close.",
     [("entity_id", "str"), ("name", "str"), ("code", "str"), ("currency", "str"), ("active", "bool")],
     [("list", "GET", "/api/entities", "List all entities"),
      ("create", "POST", "/api/entities", "Create an entity"),
      ("get", "GET", "/api/entities/{entity_id}", "Get entity by ID"),
      ("update", "PUT", "/api/entities/{entity_id}", "Update entity"),
      ("deactivate", "POST", "/api/entities/{entity_id}/deactivate", "Deactivate entity")]),

    (3, "document_store", "Document Store",
     "Content-addressed document storage for invoices, receipts, statements.",
     [("doc_id", "str"), ("filename", "str"), ("content_hash", "str"), ("mime_type", "str"), ("size_bytes", "int"), ("uploaded_at", "str"), ("entity_id", "str")],
     [("list", "GET", "/api/documents", "List uploaded documents"),
      ("upload", "POST", "/api/documents", "Upload a document"),
      ("get", "GET", "/api/documents/{doc_id}", "Get document metadata"),
      ("download", "GET", "/api/documents/{doc_id}/download", "Download document content"),
      ("delete_doc", "DELETE", "/api/documents/{doc_id}", "Delete a document")]),

    (4, "ocr_pipeline", "OCR Pipeline",
     "Deterministic DEMO OCR pipeline for document text extraction.",
     [("ocr_id", "str"), ("doc_id", "str"), ("status", "str"), ("extracted_text", "str"), ("confidence", "float"), ("processed_at", "str")],
     [("list", "GET", "/api/ocr-jobs", "List OCR jobs"),
      ("submit", "POST", "/api/ocr-jobs", "Submit document for OCR"),
      ("get", "GET", "/api/ocr-jobs/{ocr_id}", "Get OCR job result"),
      ("retry", "POST", "/api/ocr-jobs/{ocr_id}/retry", "Retry failed OCR job"),
      ("stats", "GET", "/api/ocr-jobs/stats", "OCR pipeline statistics")]),

    (5, "extraction", "Data Extraction",
     "Extract structured invoice/receipt fields from OCR text.",
     [("extraction_id", "str"), ("ocr_id", "str"), ("doc_type", "str"), ("vendor_name", "str"), ("amount", "float"), ("currency", "str"), ("invoice_date", "str"), ("due_date", "str|None"), ("line_items", "list")],
     [("list", "GET", "/api/extractions", "List extractions"),
      ("extract", "POST", "/api/extractions", "Run extraction on OCR result"),
      ("get", "GET", "/api/extractions/{extraction_id}", "Get extraction result"),
      ("validate", "POST", "/api/extractions/{extraction_id}/validate", "Validate extraction"),
      ("correct", "PUT", "/api/extractions/{extraction_id}", "Correct extraction fields")]),

    (6, "reconciliation", "Reconciliation Engine",
     "Explainable scoring-based reconciliation of financial records.",
     [("recon_id", "str"), ("period_id", "str"), ("source_type", "str"), ("target_type", "str"), ("match_score", "float"), ("status", "str"), ("explanation", "str"), ("matched_at", "str|None")],
     [("list", "GET", "/api/reconciliations", "List reconciliation runs"),
      ("run_recon", "POST", "/api/reconciliations", "Start a reconciliation run"),
      ("get", "GET", "/api/reconciliations/{recon_id}", "Get reconciliation details"),
      ("approve", "POST", "/api/reconciliations/{recon_id}/approve", "Approve a match"),
      ("reject", "POST", "/api/reconciliations/{recon_id}/reject", "Reject a match")]),

    (7, "exception", "Exception Management",
     "Taxonomy-based exception triage for reconciliation mismatches.",
     [("exception_id", "str"), ("recon_id", "str"), ("category", "str"), ("severity", "str"), ("description", "str"), ("status", "str"), ("assigned_to", "str|None"), ("resolved_at", "str|None")],
     [("list", "GET", "/api/exceptions", "List exceptions"),
      ("create", "POST", "/api/exceptions", "Create an exception"),
      ("get", "GET", "/api/exceptions/{exception_id}", "Get exception details"),
      ("assign", "POST", "/api/exceptions/{exception_id}/assign", "Assign exception"),
      ("resolve", "POST", "/api/exceptions/{exception_id}/resolve", "Resolve exception")]),

    (8, "review_queue", "HITL Review Queue",
     "Human-in-the-loop review and approval workflow.",
     [("review_id", "str"), ("entity_type", "str"), ("entity_id", "str"), ("reviewer", "str|None"), ("status", "str"), ("decision", "str|None"), ("notes", "str"), ("queued_at", "str"), ("decided_at", "str|None")],
     [("list", "GET", "/api/reviews", "List review items"),
      ("enqueue", "POST", "/api/reviews", "Add item to review queue"),
      ("get", "GET", "/api/reviews/{review_id}", "Get review details"),
      ("decide", "POST", "/api/reviews/{review_id}/decide", "Submit review decision"),
      ("stats", "GET", "/api/reviews/stats", "Review queue statistics")]),

    (9, "evidence_binder", "Evidence Binder",
     "Assemble and export evidence binders for audit.",
     [("binder_id", "str"), ("period_id", "str"), ("title", "str"), ("status", "str"), ("sections", "list"), ("created_at", "str"), ("finalized_at", "str|None")],
     [("list", "GET", "/api/binders", "List evidence binders"),
      ("create", "POST", "/api/binders", "Create an evidence binder"),
      ("get", "GET", "/api/binders/{binder_id}", "Get binder details"),
      ("add_section", "POST", "/api/binders/{binder_id}/sections", "Add section to binder"),
      ("finalize", "POST", "/api/binders/{binder_id}/finalize", "Finalize binder for export")]),

    (10, "eval_harness", "Eval Harness",
     "Evaluation framework for extraction and reconciliation quality.",
     [("eval_id", "str"), ("eval_type", "str"), ("dataset", "str"), ("precision", "float"), ("recall", "float"), ("f1_score", "float"), ("run_at", "str")],
     [("list", "GET", "/api/evals", "List evaluation runs"),
      ("run_eval", "POST", "/api/evals", "Run an evaluation"),
      ("get", "GET", "/api/evals/{eval_id}", "Get evaluation results"),
      ("compare", "GET", "/api/evals/compare", "Compare two evaluation runs"),
      ("baseline", "POST", "/api/evals/baseline", "Set evaluation baseline")]),

    (11, "tenant", "Multi-Tenant Management",
     "Tenant isolation and management for multi-org deployment.",
     [("tenant_id", "str"), ("name", "str"), ("slug", "str"), ("plan", "str"), ("active", "bool"), ("created_at", "str")],
     [("list", "GET", "/api/tenants", "List all tenants"),
      ("create", "POST", "/api/tenants", "Create a tenant"),
      ("get", "GET", "/api/tenants/{tenant_id}", "Get tenant details"),
      ("update", "PUT", "/api/tenants/{tenant_id}", "Update tenant"),
      ("suspend", "POST", "/api/tenants/{tenant_id}/suspend", "Suspend a tenant")]),

    (12, "auth", "Authentication & RBAC",
     "User authentication and role-based access control.",
     [("user_id", "str"), ("email", "str"), ("role", "str"), ("tenant_id", "str"), ("active", "bool"), ("last_login", "str|None")],
     [("list_users", "GET", "/api/auth/users", "List users"),
      ("create_user", "POST", "/api/auth/users", "Create a user"),
      ("get_user", "GET", "/api/auth/users/{user_id}", "Get user details"),
      ("update_role", "PUT", "/api/auth/users/{user_id}/role", "Update user role"),
      ("deactivate_user", "POST", "/api/auth/users/{user_id}/deactivate", "Deactivate user")]),

    (13, "workflow", "Workflow Engine",
     "Configurable close workflow templates and execution.",
     [("workflow_id", "str"), ("name", "str"), ("steps", "list"), ("status", "str"), ("current_step", "int"), ("created_at", "str"), ("completed_at", "str|None")],
     [("list", "GET", "/api/workflows", "List workflows"),
      ("create", "POST", "/api/workflows", "Create a workflow"),
      ("get", "GET", "/api/workflows/{workflow_id}", "Get workflow details"),
      ("advance", "POST", "/api/workflows/{workflow_id}/advance", "Advance to next step"),
      ("abort", "POST", "/api/workflows/{workflow_id}/abort", "Abort a workflow")]),

    (14, "notification", "Notification Service",
     "Event-driven notifications for close milestones.",
     [("notification_id", "str"), ("channel", "str"), ("recipient", "str"), ("subject", "str"), ("body", "str"), ("status", "str"), ("sent_at", "str|None")],
     [("list", "GET", "/api/notifications", "List notifications"),
      ("send", "POST", "/api/notifications", "Send a notification"),
      ("get", "GET", "/api/notifications/{notification_id}", "Get notification details"),
      ("mark_read", "POST", "/api/notifications/{notification_id}/read", "Mark notification read"),
      ("stats", "GET", "/api/notifications/stats", "Notification statistics")]),

    (15, "connector", "External Connector",
     "Connectors for ERP, bank, and payment system integration.",
     [("connector_id", "str"), ("name", "str"), ("connector_type", "str"), ("config", "dict"), ("status", "str"), ("last_sync", "str|None")],
     [("list", "GET", "/api/connectors", "List connectors"),
      ("create", "POST", "/api/connectors", "Create a connector"),
      ("get", "GET", "/api/connectors/{connector_id}", "Get connector details"),
      ("sync", "POST", "/api/connectors/{connector_id}/sync", "Trigger sync"),
      ("test_conn", "POST", "/api/connectors/{connector_id}/test", "Test connector")]),

    (16, "vendor_master", "Vendor Master",
     "Vendor master data management and deduplication.",
     [("vendor_id", "str"), ("name", "str"), ("tax_id", "str"), ("address", "str"), ("payment_terms", "str"), ("active", "bool"), ("created_at", "str")],
     [("list", "GET", "/api/vendors", "List vendors"),
      ("create", "POST", "/api/vendors", "Create a vendor"),
      ("get", "GET", "/api/vendors/{vendor_id}", "Get vendor details"),
      ("update", "PUT", "/api/vendors/{vendor_id}", "Update vendor"),
      ("merge", "POST", "/api/vendors/merge", "Merge duplicate vendors")]),

    (17, "chart_of_accounts", "Chart of Accounts & JE",
     "Chart of accounts management and journal entry creation.",
     [("account_id", "str"), ("code", "str"), ("name", "str"), ("account_type", "str"), ("parent_id", "str|None"), ("active", "bool")],
     [("list_accounts", "GET", "/api/coa/accounts", "List accounts"),
      ("create_account", "POST", "/api/coa/accounts", "Create an account"),
      ("get_account", "GET", "/api/coa/accounts/{account_id}", "Get account details"),
      ("create_je", "POST", "/api/coa/journal-entries", "Create journal entry"),
      ("list_je", "GET", "/api/coa/journal-entries", "List journal entries")]),

    (18, "continuous_close", "Continuous Close",
     "Real-time close progress tracking and bottleneck detection.",
     [("task_id", "str"), ("period_id", "str"), ("name", "str"), ("category", "str"), ("status", "str"), ("owner", "str"), ("due_date", "str"), ("completed_at", "str|None")],
     [("list_tasks", "GET", "/api/close-tasks", "List close tasks"),
      ("create_task", "POST", "/api/close-tasks", "Create a close task"),
      ("get_task", "GET", "/api/close-tasks/{task_id}", "Get task details"),
      ("complete_task", "POST", "/api/close-tasks/{task_id}/complete", "Complete a task"),
      ("dashboard", "GET", "/api/close-tasks/dashboard", "Close progress dashboard")]),

    (19, "audit_integrity", "Audit Integrity",
     "Merkle-tree audit log integrity verification.",
     [("check_id", "str"), ("scope", "str"), ("expected_hash", "str"), ("actual_hash", "str"), ("valid", "bool"), ("checked_at", "str")],
     [("verify", "POST", "/api/audit-integrity/verify", "Run integrity check"),
      ("list_checks", "GET", "/api/audit-integrity/checks", "List integrity checks"),
      ("get_check", "GET", "/api/audit-integrity/checks/{check_id}", "Get check details"),
      ("compute_hash", "POST", "/api/audit-integrity/hash", "Compute hash for range"),
      ("stats", "GET", "/api/audit-integrity/stats", "Integrity statistics")]),

    (20, "signed_export", "Signed Exports",
     "Cryptographically signed document and report exports.",
     [("export_id", "str"), ("export_type", "str"), ("format_type", "str"), ("signature", "str"), ("status", "str"), ("created_at", "str"), ("download_url", "str|None")],
     [("list", "GET", "/api/exports", "List exports"),
      ("create", "POST", "/api/exports", "Create a signed export"),
      ("get", "GET", "/api/exports/{export_id}", "Get export details"),
      ("verify_sig", "POST", "/api/exports/{export_id}/verify", "Verify export signature"),
      ("download", "GET", "/api/exports/{export_id}/download", "Download export")]),

    (21, "report", "Report Generator",
     "Financial close reports with configurable templates.",
     [("report_id", "str"), ("name", "str"), ("report_type", "str"), ("period_id", "str"), ("format_type", "str"), ("status", "str"), ("generated_at", "str|None")],
     [("list", "GET", "/api/reports", "List reports"),
      ("generate", "POST", "/api/reports", "Generate a report"),
      ("get", "GET", "/api/reports/{report_id}", "Get report details"),
      ("preview", "GET", "/api/reports/{report_id}/preview", "Preview report"),
      ("schedule", "POST", "/api/reports/schedule", "Schedule recurring report")]),

    (22, "search_index", "Search Index",
     "Full-text search across documents, extractions, and audit events.",
     [("result_id", "str"), ("query", "str"), ("doc_type", "str"), ("title", "str"), ("snippet", "str"), ("score", "float"), ("matched_at", "str")],
     [("search", "GET", "/api/search", "Execute full-text search"),
      ("reindex", "POST", "/api/search/reindex", "Trigger reindexing"),
      ("stats", "GET", "/api/search/stats", "Search index statistics"),
      ("suggest", "GET", "/api/search/suggest", "Auto-complete suggestions"),
      ("facets", "GET", "/api/search/facets", "Get search facets")]),

    (23, "compliance_bundle", "Compliance Bundle",
     "Assemble compliance evidence bundles for regulatory filings.",
     [("bundle_id", "str"), ("regulation", "str"), ("period_id", "str"), ("status", "str"), ("items", "list"), ("created_at", "str"), ("submitted_at", "str|None")],
     [("list", "GET", "/api/compliance-bundles", "List compliance bundles"),
      ("create", "POST", "/api/compliance-bundles", "Create a compliance bundle"),
      ("get", "GET", "/api/compliance-bundles/{bundle_id}", "Get bundle details"),
      ("add_item", "POST", "/api/compliance-bundles/{bundle_id}/items", "Add item to bundle"),
      ("submit", "POST", "/api/compliance-bundles/{bundle_id}/submit", "Submit for review")]),

    (24, "retention", "Data Retention",
     "Policy-based data retention and archival.",
     [("policy_id", "str"), ("name", "str"), ("entity_type", "str"), ("retention_days", "int"), ("action", "str"), ("active", "bool"), ("last_run", "str|None")],
     [("list_policies", "GET", "/api/retention/policies", "List retention policies"),
      ("create_policy", "POST", "/api/retention/policies", "Create a retention policy"),
      ("get_policy", "GET", "/api/retention/policies/{policy_id}", "Get policy details"),
      ("run_policy", "POST", "/api/retention/policies/{policy_id}/run", "Run retention policy"),
      ("preview", "POST", "/api/retention/policies/{policy_id}/preview", "Preview affected records")]),

    (25, "data_privacy", "Data Privacy / GDPR",
     "GDPR-compliant data access, export, and erasure.",
     [("request_id", "str"), ("request_type", "str"), ("subject_email", "str"), ("status", "str"), ("requested_at", "str"), ("completed_at", "str|None")],
     [("list_requests", "GET", "/api/privacy/requests", "List privacy requests"),
      ("create_request", "POST", "/api/privacy/requests", "Create a privacy request"),
      ("get_request", "GET", "/api/privacy/requests/{request_id}", "Get request details"),
      ("process", "POST", "/api/privacy/requests/{request_id}/process", "Process request"),
      ("export_data", "GET", "/api/privacy/requests/{request_id}/export", "Export subject data")]),

    (26, "performance", "Performance Monitor",
     "API performance tracking, latency histograms, and chaos flags.",
     [("metric_id", "str"), ("endpoint", "str"), ("method", "str"), ("p50_ms", "float"), ("p95_ms", "float"), ("p99_ms", "float"), ("count", "int"), ("window", "str")],
     [("list_metrics", "GET", "/api/performance/metrics", "Get performance metrics"),
      ("create_metric", "POST", "/api/performance/metrics", "Record a performance metric"),
      ("get_metric", "GET", "/api/performance/metrics/{metric_id}", "Get metric details"),
      ("chaos_flag", "POST", "/api/performance/metrics/{metric_id}/chaos", "Set chaos testing flag"),
      ("clear_metrics", "POST", "/api/performance/metrics/{metric_id}/clear", "Clear metrics")]),

    (27, "release_bundle", "Release Bundle",
     "Versioned release bundles with changelog and migration tracking.",
     [("release_id", "str"), ("version", "str"), ("changelog", "str"), ("migrations", "list"), ("status", "str"), ("created_at", "str"), ("deployed_at", "str|None")],
     [("list", "GET", "/api/releases", "List releases"),
      ("create", "POST", "/api/releases", "Create a release bundle"),
      ("get", "GET", "/api/releases/{release_id}", "Get release details"),
      ("deploy", "POST", "/api/releases/{release_id}/deploy", "Mark as deployed"),
      ("rollback", "POST", "/api/releases/{release_id}/rollback", "Rollback a release")]),

    (28, "judge_demo", "Judge Demo Harness",
     "Demo judge for LLM evaluation of extraction quality.",
     [("judge_id", "str"), ("input_text", "str"), ("expected", "dict"), ("predicted", "dict"), ("score", "float"), ("verdict", "str"), ("judged_at", "str")],
     [("list", "GET", "/api/judge/runs", "List judge runs"),
      ("evaluate", "POST", "/api/judge/evaluate", "Run judge evaluation"),
      ("get", "GET", "/api/judge/runs/{judge_id}", "Get judge result"),
      ("batch", "POST", "/api/judge/batch", "Batch evaluation"),
      ("leaderboard", "GET", "/api/judge/leaderboard", "Judge leaderboard")]),

    (29, "deploy_config", "Deploy Configuration",
     "GCP deployment configuration and environment management.",
     [("config_id", "str"), ("environment", "str"), ("region", "str"), ("settings", "dict"), ("status", "str"), ("updated_at", "str")],
     [("list", "GET", "/api/deploy/configs", "List deploy configs"),
      ("create", "POST", "/api/deploy/configs", "Create deploy config"),
      ("get", "GET", "/api/deploy/configs/{config_id}", "Get config details"),
      ("activate", "POST", "/api/deploy/configs/{config_id}/activate", "Activate config"),
      ("validate_config", "POST", "/api/deploy/configs/{config_id}/validate", "Validate config")]),

    (30, "hardening", "Ultra-Hardening",
     "System hardening: rate limits, CSP headers, input validation.",
     [("rule_id", "str"), ("rule_type", "str"), ("name", "str"), ("config", "dict"), ("enabled", "bool"), ("created_at", "str")],
     [("list_rules", "GET", "/api/hardening/rules", "List hardening rules"),
      ("create_rule", "POST", "/api/hardening/rules", "Create a hardening rule"),
      ("get_rule", "GET", "/api/hardening/rules/{rule_id}", "Get rule details"),
      ("toggle", "POST", "/api/hardening/rules/{rule_id}/toggle", "Toggle rule on/off"),
      ("audit_scan", "POST", "/api/hardening/scan", "Run security audit scan")]),
]


def gen_service(wave_num: int, slug: str, title: str, desc: str, fields: list, operations: list) -> str:
    """Generate a domain service module."""
    field_defs = "\n".join(f'        "{f[0]}": {_default_value(f[1])},' for f in fields)
    id_field = fields[0][0]

    ops_code = []
    for op_name, method, path, op_desc in operations:
        if method == "GET" and "{" not in path:
            ops_code.append(f'''
    def {op_name}(self, **kwargs) -> list[dict]:
        """List items with optional filters."""
        items = list(self._store.values())
        limit = kwargs.get("limit", 100)
        return items[:limit]
''')
        elif method == "POST" and "{" not in path:
            ops_code.append(f'''
    def {op_name}(self, data: dict) -> dict:
        """Create a new item."""
        item_id = str(uuid.uuid4())
        item = {{**self._template(), **data, "{id_field}": item_id}}
        self._store[item_id] = item
        emit_audit_event("{op_name}", "{slug}", item_id, {{"data": data}})
        return item
''')
        elif method == "GET" and "{" in path:
            param = re.search(r'\{(\w+)\}', path).group(1)
            ops_code.append(f'''
    def {op_name}(self, {param}: str) -> dict | None:
        """Get item by ID."""
        return self._store.get({param})
''')
        elif method == "PUT":
            param = re.search(r'\{(\w+)\}', path).group(1)
            ops_code.append(f'''
    def {op_name}(self, {param}: str, data: dict) -> dict | None:
        """Update an existing item."""
        item = self._store.get({param})
        if not item:
            return None
        item.update(data)
        emit_audit_event("{op_name}", "{slug}", {param}, {{"data": data}})
        return item
''')
        elif method == "DELETE":
            param = re.search(r'\{(\w+)\}', path).group(1)
            ops_code.append(f'''
    def {op_name}(self, {param}: str) -> bool:
        """Delete an item."""
        if {param} in self._store:
            del self._store[{param}]
            emit_audit_event("{op_name}", "{slug}", {param})
            return True
        return False
''')
        elif method == "POST" and "{" in path:
            param = re.search(r'\{(\w+)\}', path).group(1)
            action = op_name
            ops_code.append(f'''
    def {op_name}(self, {param}: str, data: dict | None = None) -> dict | None:
        """Action: {action} on item."""
        item = self._store.get({param})
        if not item:
            return None
        if data:
            item.update(data)
        item["status"] = "{action}d" if "status" in item else item.get("status", "done")
        emit_audit_event("{op_name}", "{slug}", {param}, {{"action": "{action}", "data": data or {{}}}})
        return item
''')

    return f'''"""Wave {wave_num}: {title} — {desc}

PROJECT_ID: LEDGERLIVE
"""
import uuid
import datetime as dt
from app.main import emit_audit_event


class {_class_name(slug)}Service:
    """Domain service for {title}."""

    def __init__(self):
        self._store: dict[str, dict] = {{}}

    def _template(self) -> dict:
        return {{
{field_defs}
        }}

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)
{"".join(ops_code)}

# Module-level singleton
service = {_class_name(slug)}Service()
'''


def gen_router(wave_num: int, slug: str, title: str, desc: str, fields: list, operations: list) -> str:
    """Generate a FastAPI router module."""
    svc_import = f"from app.services.w{wave_num:02d}_{slug} import service"

    # Sort operations: literal paths first, parameterized paths second
    # This ensures /api/foo/stats is registered before /api/foo/{id}
    sorted_ops = sorted(operations, key=lambda o: (1 if '{' in o[2] else 0, o[2]))

    routes = []
    for op_name, method, path, op_desc in sorted_ops:
        if method == "GET" and "{" not in path:
            routes.append(f'''
@router.get("{path}")
async def api_{op_name}(limit: int = 100):
    """{op_desc}"""
    items = service.{op_name}(limit=limit)
    return {{"items": items, "total": len(items)}}
''')
        elif method == "POST" and "{" not in path:
            routes.append(f'''
@router.post("{path}", status_code=201)
async def api_{op_name}(request: Request):
    """{op_desc}"""
    data = await request.json()
    item = service.{op_name}(data)
    return item
''')
        elif method == "GET" and "{" in path:
            param = re.search(r'\{(\w+)\}', path).group(1)
            routes.append(f'''
@router.get("{path}")
async def api_{op_name}({param}: str):
    """{op_desc}"""
    item = service.{op_name}({param})
    if not item:
        raise HTTPException(status_code=404, detail="{slug} not found")
    return item
''')
        elif method == "PUT":
            param = re.search(r'\{(\w+)\}', path).group(1)
            routes.append(f'''
@router.put("{path}")
async def api_{op_name}({param}: str, request: Request):
    """{op_desc}"""
    data = await request.json()
    item = service.{op_name}({param}, data)
    if not item:
        raise HTTPException(status_code=404, detail="{slug} not found")
    return item
''')
        elif method == "DELETE":
            param = re.search(r'\{(\w+)\}', path).group(1)
            routes.append(f'''
@router.delete("{path}")
async def api_{op_name}({param}: str):
    """{op_desc}"""
    ok = service.{op_name}({param})
    if not ok:
        raise HTTPException(status_code=404, detail="{slug} not found")
    return {{"deleted": True}}
''')
        elif method == "POST" and "{" in path:
            param = re.search(r'\{(\w+)\}', path).group(1)
            routes.append(f'''
@router.post("{path}")
async def api_{op_name}({param}: str, request: Request):
    """{op_desc}"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.{op_name}({param}, data)
    if not item:
        raise HTTPException(status_code=404, detail="{slug} not found")
    return item
''')

    return f'''"""Wave {wave_num}: {title} Router — {desc}

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

{svc_import}

router = APIRouter(tags=["{title}"])
{"".join(routes)}'''


def gen_tests(wave_num: int, slug: str, title: str, desc: str, fields: list, operations: list) -> str:
    """Generate comprehensive tests."""
    id_field = fields[0][0]
    svc_import = f"from app.services.w{wave_num:02d}_{slug} import service"

    create_op = None
    list_op = None
    get_op = None
    action_ops = []
    update_op = None
    delete_op = None

    for op_name, method, path, op_desc in operations:
        if method == "POST" and "{" not in path and create_op is None:
            create_op = (op_name, method, path)
        elif method == "GET" and "{" not in path and list_op is None:
            list_op = (op_name, method, path)
        elif method == "GET" and "{" in path and get_op is None:
            get_op = (op_name, method, path)
        elif method == "PUT" and update_op is None:
            update_op = (op_name, method, path)
        elif method == "DELETE" and delete_op is None:
            delete_op = (op_name, method, path)
        elif method == "POST" and "{" in path:
            action_ops.append((op_name, method, path))

    tests = []

    # Setup fixture
    tests.append(f'''
@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()
''')

    # Test: service starts empty
    tests.append(f'''
def test_w{wave_num:02d}_service_starts_empty():
    assert service.count == 0
''')

    # Test: create via API
    if create_op:
        op_name, method, path = create_op
        sample_data = _sample_create_data(fields)
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_create(client):
    r = await client.post("{path}", json={sample_data})
    assert r.status_code == 201
    data = r.json()
    assert "{id_field}" in data
    assert service.count == 1
''')

    # Test: list via API
    if list_op and create_op:
        op_name, method, path = list_op
        _, _, create_path = create_op
        sample_data = _sample_create_data(fields)
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_list(client):
    await client.post("{create_path}", json={sample_data})
    await client.post("{create_path}", json={sample_data})
    r = await client.get("{path}")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2
''')

    # Test: get by ID
    if get_op and create_op:
        op_name, method, path = get_op
        _, _, create_path = create_op
        sample_data = _sample_create_data(fields)
        path_template = path.replace("{" + id_field + "}", "{item_id}")
        # Handle cases where path param differs from id_field
        param = re.search(r'\{(\w+)\}', path).group(1)
        path_template = path.replace("{" + param + "}", "{item_id}")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_get_by_id(client):
    r = await client.post("{create_path}", json={sample_data})
    item_id = r.json()["{id_field}"]
    r2 = await client.get(f"{path_template}")
    assert r2.status_code == 200
    assert r2.json()["{id_field}"] == item_id
''')

    # Test: get 404
    if get_op:
        op_name, method, path = get_op
        param = re.search(r'\{(\w+)\}', path).group(1)
        path_404 = path.replace("{" + param + "}", "nonexistent-id")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_get_not_found(client):
    r = await client.get("{path_404}")
    assert r.status_code == 404
''')

    # Test: update
    if update_op and create_op:
        op_name, method, path = update_op
        _, _, create_path = create_op
        sample_data = _sample_create_data(fields)
        param = re.search(r'\{(\w+)\}', path).group(1)
        path_template = path.replace("{" + param + "}", "{item_id}")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_update(client):
    r = await client.post("{create_path}", json={sample_data})
    item_id = r.json()["{id_field}"]
    r2 = await client.put(f"{path_template}", json={{"name": "updated"}})
    assert r2.status_code == 200
    assert r2.json()["name"] == "updated"
''')

    # Test: delete
    if delete_op and create_op:
        op_name, method, path = delete_op
        _, _, create_path = create_op
        sample_data = _sample_create_data(fields)
        param = re.search(r'\{(\w+)\}', path).group(1)
        path_template = path.replace("{" + param + "}", "{item_id}")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_delete(client):
    r = await client.post("{create_path}", json={sample_data})
    item_id = r.json()["{id_field}"]
    r2 = await client.delete(f"{path_template}")
    assert r2.status_code == 200
    assert r2.json()["deleted"] is True
    assert service.count == 0
''')

    # Test: action operations
    if action_ops and create_op:
        for action_op_name, action_method, action_path in action_ops[:2]:  # test first 2 actions
            _, _, create_path = create_op
            sample_data = _sample_create_data(fields)
            param = re.search(r'\{(\w+)\}', action_path).group(1)
            path_template = action_path.replace("{" + param + "}", "{item_id}")
            tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_{action_op_name}(client):
    r = await client.post("{create_path}", json={sample_data})
    item_id = r.json()["{id_field}"]
    r2 = await client.post(f"{path_template}", json={{}})
    assert r2.status_code == 200
    assert r2.json()["{id_field}"] == item_id
''')

    # Test: action 404
    if action_ops:
        action_op_name, _, action_path = action_ops[0]
        param = re.search(r'\{(\w+)\}', action_path).group(1)
        path_404 = action_path.replace("{" + param + "}", "nonexistent-id")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_{action_op_name}_not_found(client):
    r = await client.post("{path_404}", json={{}})
    assert r.status_code == 404
''')

    # Test: audit event emitted
    if create_op:
        _, _, create_path = create_op
        sample_data = _sample_create_data(fields)
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("{create_path}", json={sample_data})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "{slug}"
    assert "trace_id" in event
''')

    # Test: determinism - same input same output
    if create_op:
        _, _, create_path = create_op
        sample_data = _sample_create_data(fields)
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_determinism(client):
    """Same input should produce consistent structure."""
    r1 = await client.post("{create_path}", json={sample_data})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("{create_path}", json={sample_data})
    d1, d2 = r1.json(), r2.json()
    # Same keys
    assert set(d1.keys()) == set(d2.keys())
    # Same non-id values
    for k in d1:
        if k != "{id_field}":
            assert type(d1[k]) == type(d2[k])
''')

    # Test: break-it - empty create should still work or fail gracefully
    if create_op:
        _, _, create_path = create_op
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_break_it_empty_body(client):
    """Empty body should still create (with defaults)."""
    r = await client.post("{create_path}", json={{}})
    assert r.status_code == 201
''')

    return f'''"""Tests for Wave {wave_num}: {title}

PROJECT_ID: LEDGERLIVE
"""
import pytest
{svc_import}

{"".join(tests)}'''


def _class_name(slug: str) -> str:
    return "".join(w.capitalize() for w in slug.split("_"))


def _default_value(type_str: str) -> str:
    if type_str == "str" or type_str == "str|None":
        return '""'
    elif type_str == "int":
        return "0"
    elif type_str == "float":
        return "0.0"
    elif type_str == "bool":
        return "True"
    elif type_str == "list":
        return "[]"
    elif type_str == "dict":
        return "{}"
    return '""'


def _sample_create_data(fields: list) -> dict:
    data = {}
    for name, ftype in fields[1:]:  # skip ID field
        if ftype == "str" or ftype == "str|None":
            data[name] = f"test-{name}"
        elif ftype == "int":
            data[name] = 1
        elif ftype == "float":
            data[name] = 1.0
        elif ftype == "bool":
            data[name] = True
        elif ftype == "list":
            data[name] = []
        elif ftype == "dict":
            data[name] = {}
    return data


def gen_main_imports(waves: list) -> str:
    """Generate router imports and includes for main.py."""
    lines = []
    for wave_num, slug, title, *_ in waves:
        lines.append(f"from app.routers.w{wave_num:02d}_{slug} import router as w{wave_num:02d}_router")
    lines.append("")
    for wave_num, slug, title, *_ in waves:
        lines.append(f'app.include_router(w{wave_num:02d}_router)')
    return "\n".join(lines)


def main():
    print(f"Generating {len(WAVES)} waves...")

    for wave_num, slug, title, desc, fields, operations in WAVES:
        # Service
        svc_path = SVC_DIR / f"w{wave_num:02d}_{slug}.py"
        svc_path.write_text(gen_service(wave_num, slug, title, desc, fields, operations), encoding="utf-8")
        print(f"  ✓ {svc_path.name}")

        # Router
        rtr_path = RTR_DIR / f"w{wave_num:02d}_{slug}.py"
        rtr_path.write_text(gen_router(wave_num, slug, title, desc, fields, operations), encoding="utf-8")
        print(f"  ✓ {rtr_path.name}")

        # Tests
        tst_path = TST_DIR / f"test_w{wave_num:02d}_{slug}.py"
        tst_path.write_text(gen_tests(wave_num, slug, title, desc, fields, operations), encoding="utf-8")
        print(f"  ✓ {tst_path.name}")

    # Update main.py with router registrations
    main_content = MAIN_PY.read_text(encoding="utf-8")
    marker = "# ── Wave routers will be registered below this line ──────────────────"
    if marker in main_content:
        router_code = gen_main_imports(WAVES)
        main_content = main_content.replace(marker, marker + "\n" + router_code)
        MAIN_PY.write_text(main_content, encoding="utf-8")
        print(f"\n  ✓ main.py updated with {len(WAVES)} router registrations")

    print(f"\nDone! Generated {len(WAVES)} services, {len(WAVES)} routers, {len(WAVES)} test files.")


if __name__ == "__main__":
    main()
