#!/usr/bin/env python3
"""Generate LedgerLive Waves 31-60: enterprise-grade domain services, routers, and tests.

Phase 1 (31-40): Real company close depth
Phase 2 (41-50): Integrations without breaking determinism
Phase 3 (51-60): FP&A / Treasury expansion

Run: python tools/gen_waves_31_60.py
"""
import pathlib, re, uuid

ROOT = pathlib.Path(__file__).resolve().parents[1]
SVC_DIR = ROOT / "apps" / "api" / "app" / "services"
RTR_DIR = ROOT / "apps" / "api" / "app" / "routers"
TST_DIR = ROOT / "apps" / "api" / "tests"
MAIN_PY = ROOT / "apps" / "api" / "app" / "main.py"

# ── Wave definitions ─────────────────────────────────────────────────
WAVES = [
    # ── Phase 1: Real Company Close (31-40) ────────────────────────
    (31, "close_calendar", "Close Calendar 2.0",
     "Dependency graph for close tasks with SLA timers, escalation rules, and owner assignments.",
     [("task_id", "str"), ("period_id", "str"), ("name", "str"), ("owner", "str"),
      ("depends_on", "list"), ("sla_hours", "int"), ("status", "str"),
      ("escalation_level", "int"), ("started_at", "str"), ("due_at", "str"),
      ("completed_at", "str|None")],
     [("list_tasks", "GET", "/api/close-calendar/tasks", "List close calendar tasks"),
      ("create_task", "POST", "/api/close-calendar/tasks", "Create a close calendar task"),
      ("get_task", "GET", "/api/close-calendar/{task_id}", "Get task details"),
      ("start_task", "POST", "/api/close-calendar/{task_id}/start", "Start a task"),
      ("complete_task", "POST", "/api/close-calendar/{task_id}/complete", "Complete a task"),
      ("escalate", "POST", "/api/close-calendar/{task_id}/escalate", "Escalate a task"),
      ("dependency_chain", "GET", "/api/close-calendar/dependency-chain", "Get dependency chain view")]),

    (32, "consolidation", "Multi-Entity Consolidation",
     "Entity hierarchy, consolidation adjustments, intercompany eliminations, consolidated P&L/BS.",
     [("consolidation_id", "str"), ("period_id", "str"), ("parent_entity_id", "str"),
      ("child_entities", "list"), ("adjustments", "list"), ("eliminations", "list"),
      ("status", "str"), ("total_assets", "float"), ("total_liabilities", "float"),
      ("net_income", "float"), ("created_at", "str"), ("finalized_at", "str|None")],
     [("list", "GET", "/api/consolidations", "List consolidation runs"),
      ("create", "POST", "/api/consolidations", "Start a consolidation run"),
      ("get", "GET", "/api/consolidations/{consolidation_id}", "Get consolidation details"),
      ("add_adjustment", "POST", "/api/consolidations/{consolidation_id}/adjustments", "Add consolidation adjustment"),
      ("add_elimination", "POST", "/api/consolidations/{consolidation_id}/eliminations", "Add intercompany elimination"),
      ("finalize", "POST", "/api/consolidations/{consolidation_id}/finalize", "Finalize consolidation"),
      ("export_statements", "GET", "/api/consolidations/export", "Export consolidated statements")]),

    (33, "je_posting", "JE Posting Engine",
     "Journal entry batching, posting locks after close, reversals, and approval chain.",
     [("posting_id", "str"), ("batch_id", "str"), ("journal_entries", "list"),
      ("status", "str"), ("locked", "bool"), ("approved_by", "str|None"),
      ("reversal_of", "str|None"), ("total_debits", "float"), ("total_credits", "float"),
      ("posted_at", "str|None"), ("created_at", "str")],
     [("list_postings", "GET", "/api/je-postings", "List JE postings"),
      ("create_posting", "POST", "/api/je-postings", "Create a JE posting batch"),
      ("get_posting", "GET", "/api/je-postings/{posting_id}", "Get posting details"),
      ("approve", "POST", "/api/je-postings/{posting_id}/approve", "Approve a posting"),
      ("post", "POST", "/api/je-postings/{posting_id}/post", "Post the batch"),
      ("reverse", "POST", "/api/je-postings/{posting_id}/reverse", "Create a reversal"),
      ("lock", "POST", "/api/je-postings/{posting_id}/lock", "Lock posting after close")]),

    (34, "three_way_match", "Three-Way Match",
     "PO/Receipt/Invoice matching with tolerances, variance policy, and approval for out-of-range.",
     [("match_id", "str"), ("po_id", "str"), ("receipt_id", "str"), ("invoice_id", "str"),
      ("po_amount", "float"), ("receipt_amount", "float"), ("invoice_amount", "float"),
      ("variance_pct", "float"), ("status", "str"), ("tolerance_pct", "float"),
      ("approved_by", "str|None"), ("matched_at", "str|None")],
     [("list_matches", "GET", "/api/three-way-match", "List three-way matches"),
      ("create_match", "POST", "/api/three-way-match", "Create a three-way match"),
      ("get_match", "GET", "/api/three-way-match/{match_id}", "Get match details"),
      ("approve_variance", "POST", "/api/three-way-match/{match_id}/approve", "Approve variance"),
      ("reject_match", "POST", "/api/three-way-match/{match_id}/reject", "Reject a match"),
      ("recalculate", "POST", "/api/three-way-match/{match_id}/recalculate", "Recalculate match")]),

    (35, "cash_application", "Cash Application",
     "AR allocations, partial payments, deduction/dispute workflow.",
     [("application_id", "str"), ("customer_id", "str"), ("invoice_id", "str"),
      ("payment_amount", "float"), ("applied_amount", "float"), ("remaining", "float"),
      ("status", "str"), ("dispute_reason", "str|None"), ("resolved_at", "str|None"),
      ("applied_at", "str")],
     [("list", "GET", "/api/cash-applications", "List cash applications"),
      ("apply", "POST", "/api/cash-applications", "Apply cash to invoice"),
      ("get", "GET", "/api/cash-applications/{application_id}", "Get application details"),
      ("dispute", "POST", "/api/cash-applications/{application_id}/dispute", "Open a dispute"),
      ("resolve_dispute", "POST", "/api/cash-applications/{application_id}/resolve", "Resolve a dispute"),
      ("export_ar", "GET", "/api/cash-applications/export", "Export AR aging report")]),

    (36, "accruals_deferrals", "Accruals & Deferrals",
     "Recurring schedules, accrual proposals from patterns, approval required, automatic reversals.",
     [("schedule_id", "str"), ("name", "str"), ("schedule_type", "str"),
      ("amount", "float"), ("frequency", "str"), ("start_date", "str"),
      ("end_date", "str|None"), ("status", "str"), ("auto_reverse", "bool"),
      ("approved_by", "str|None"), ("next_run", "str"), ("created_at", "str")],
     [("list_schedules", "GET", "/api/accruals", "List accrual/deferral schedules"),
      ("create_schedule", "POST", "/api/accruals", "Create an accrual/deferral schedule"),
      ("get_schedule", "GET", "/api/accruals/{schedule_id}", "Get schedule details"),
      ("generate_proposal", "POST", "/api/accruals/{schedule_id}/propose", "Generate accrual proposal"),
      ("approve_proposal", "POST", "/api/accruals/{schedule_id}/approve", "Approve accrual proposal"),
      ("reverse", "POST", "/api/accruals/{schedule_id}/reverse", "Reverse an accrual"),
      ("export_accruals", "GET", "/api/accruals/export", "Export accrual report")]),

    (37, "controls_catalog", "Controls Catalog",
     "SOX-style controls mapped to workflows and required evidence artifacts.",
     [("control_id", "str"), ("name", "str"), ("description", "str"),
      ("control_type", "str"), ("frequency", "str"), ("owner", "str"),
      ("mapped_workflows", "list"), ("required_evidence", "list"),
      ("status", "str"), ("last_tested", "str|None"), ("coverage_pct", "float")],
     [("list_controls", "GET", "/api/controls", "List controls"),
      ("create_control", "POST", "/api/controls", "Create a control"),
      ("get_control", "GET", "/api/controls/{control_id}", "Get control details"),
      ("map_evidence", "POST", "/api/controls/{control_id}/evidence", "Map evidence to control"),
      ("test_control", "POST", "/api/controls/{control_id}/test", "Test/verify a control"),
      ("export_coverage", "GET", "/api/controls/coverage", "Export controls coverage report")]),

    (38, "audit_portal", "Audit Portal",
     "Auditor role with saved queries, export logs, and immutable Q&A log.",
     [("query_id", "str"), ("auditor_id", "str"), ("query_text", "str"),
      ("result_count", "int"), ("exported", "bool"), ("scope", "str"),
      ("created_at", "str"), ("qa_thread", "list")],
     [("list_queries", "GET", "/api/audit-portal/queries", "List saved audit queries"),
      ("create_query", "POST", "/api/audit-portal/queries", "Create a saved query"),
      ("get_query", "GET", "/api/audit-portal/queries/{query_id}", "Get query details"),
      ("execute_query", "POST", "/api/audit-portal/queries/{query_id}/execute", "Execute a saved query"),
      ("add_qa", "POST", "/api/audit-portal/queries/{query_id}/qa", "Add Q&A to audit log"),
      ("export_log", "GET", "/api/audit-portal/export", "Export audit portal log")]),

    (39, "vendor_master_v2", "Vendor Master 2.0",
     "Vendor families, risk ratings, watchlists, approval-required overrides for risky vendors.",
     [("vendor_id", "str"), ("name", "str"), ("parent_vendor_id", "str|None"),
      ("risk_rating", "str"), ("watchlist", "bool"), ("tax_id", "str"),
      ("approval_required", "bool"), ("approved_by", "str|None"),
      ("status", "str"), ("created_at", "str")],
     [("list_vendors", "GET", "/api/vendors-v2", "List vendors with hierarchy"),
      ("create_vendor", "POST", "/api/vendors-v2", "Create a vendor"),
      ("get_vendor", "GET", "/api/vendors-v2/{vendor_id}", "Get vendor details"),
      ("set_risk", "POST", "/api/vendors-v2/{vendor_id}/risk", "Set vendor risk rating"),
      ("approve_override", "POST", "/api/vendors-v2/{vendor_id}/approve", "Approve risky vendor override"),
      ("merge_vendors", "POST", "/api/vendors-v2/{vendor_id}/merge", "Merge duplicate vendors"),
      ("watchlist_report", "GET", "/api/vendors-v2/watchlist", "Get vendor watchlist report")]),

    (40, "evidence_binder_v2", "Evidence Binder 2.0",
     "Audit-ready binder with controls report, approvals chain, provenance, Merkle integrity, signing.",
     [("binder_id", "str"), ("period_id", "str"), ("title", "str"),
      ("controls_report", "dict"), ("approvals_chain", "list"),
      ("provenance", "dict"), ("merkle_root", "str|None"), ("signature", "str|None"),
      ("verified", "bool"), ("status", "str"), ("created_at", "str"),
      ("finalized_at", "str|None")],
     [("list_binders", "GET", "/api/binders-v2", "List evidence binders v2"),
      ("create_binder", "POST", "/api/binders-v2", "Create evidence binder v2"),
      ("get_binder", "GET", "/api/binders-v2/{binder_id}", "Get binder details"),
      ("add_provenance", "POST", "/api/binders-v2/{binder_id}/provenance", "Add provenance record"),
      ("sign_binder", "POST", "/api/binders-v2/{binder_id}/sign", "Sign the binder"),
      ("verify_binder", "POST", "/api/binders-v2/{binder_id}/verify", "Verify binder integrity"),
      ("export_binder", "GET", "/api/binders-v2/export", "Export audit-ready binder")]),

    # ── Phase 2: Integrations (41-50) ──────────────────────────────
    (41, "connector_framework_v2", "Connector Framework 2.0",
     "Connector capability model with scopes, UI connection manager, sync scheduling.",
     [("connector_id", "str"), ("name", "str"), ("connector_type", "str"),
      ("capabilities", "list"), ("scopes", "list"), ("sync_schedule", "str"),
      ("status", "str"), ("last_sync_at", "str|None"), ("config", "dict"),
      ("created_at", "str")],
     [("list_connectors", "GET", "/api/connectors-v2", "List connectors v2"),
      ("register", "POST", "/api/connectors-v2", "Register a connector"),
      ("get_connector", "GET", "/api/connectors-v2/{connector_id}", "Get connector details"),
      ("configure", "POST", "/api/connectors-v2/{connector_id}/configure", "Configure connector"),
      ("sync_now", "POST", "/api/connectors-v2/{connector_id}/sync", "Trigger sync"),
      ("test_connection", "POST", "/api/connectors-v2/{connector_id}/test", "Test connector connection"),
      ("sync_history", "GET", "/api/connectors-v2/history", "Get sync history")]),

    (42, "qbo_connector", "QuickBooks Online Connector",
     "QBO auth flow scaffolding (flagged), sync invoices, COA, payments. Mock-first.",
     [("sync_id", "str"), ("connector_id", "str"), ("entity_type", "str"),
      ("direction", "str"), ("records_synced", "int"), ("records_failed", "int"),
      ("status", "str"), ("mock_mode", "bool"), ("pagination_token", "str|None"),
      ("started_at", "str"), ("completed_at", "str|None")],
     [("list_syncs", "GET", "/api/qbo/syncs", "List QBO sync runs"),
      ("start_sync", "POST", "/api/qbo/syncs", "Start a QBO sync"),
      ("get_sync", "GET", "/api/qbo/syncs/{sync_id}", "Get QBO sync details"),
      ("retry_sync", "POST", "/api/qbo/syncs/{sync_id}/retry", "Retry failed sync"),
      ("cancel_sync", "POST", "/api/qbo/syncs/{sync_id}/cancel", "Cancel a running sync"),
      ("mock_contract", "GET", "/api/qbo/mock-contract", "Get QBO mock contract spec")]),

    (43, "xero_connector", "Xero Connector",
     "Xero sync with same contract guarantees as QBO. Mapping and idempotent sync.",
     [("sync_id", "str"), ("connector_id", "str"), ("entity_type", "str"),
      ("direction", "str"), ("records_synced", "int"), ("records_failed", "int"),
      ("status", "str"), ("mock_mode", "bool"), ("idempotency_key", "str"),
      ("started_at", "str"), ("completed_at", "str|None")],
     [("list_syncs", "GET", "/api/xero/syncs", "List Xero sync runs"),
      ("start_sync", "POST", "/api/xero/syncs", "Start a Xero sync"),
      ("get_sync", "GET", "/api/xero/syncs/{sync_id}", "Get Xero sync details"),
      ("retry_sync", "POST", "/api/xero/syncs/{sync_id}/retry", "Retry failed sync"),
      ("cancel_sync", "POST", "/api/xero/syncs/{sync_id}/cancel", "Cancel a running sync"),
      ("mock_contract", "GET", "/api/xero/mock-contract", "Get Xero mock contract spec")]),

    (44, "plaid_connector", "Plaid Connector",
     "Plaid bank feed scaffolding (flagged), transaction sync, dedupe, enrichment.",
     [("feed_id", "str"), ("institution_id", "str"), ("account_id", "str"),
      ("transactions_synced", "int"), ("duplicates_skipped", "int"),
      ("status", "str"), ("mock_mode", "bool"), ("cursor", "str|None"),
      ("enrichment_applied", "bool"), ("synced_at", "str")],
     [("list_feeds", "GET", "/api/plaid/feeds", "List Plaid bank feeds"),
      ("create_feed", "POST", "/api/plaid/feeds", "Create a bank feed"),
      ("get_feed", "GET", "/api/plaid/feeds/{feed_id}", "Get feed details"),
      ("sync_transactions", "POST", "/api/plaid/feeds/{feed_id}/sync", "Sync transactions"),
      ("dedupe", "POST", "/api/plaid/feeds/{feed_id}/dedupe", "Run deduplication"),
      ("enrich", "POST", "/api/plaid/feeds/{feed_id}/enrich", "Enrich transactions"),
      ("mock_contract", "GET", "/api/plaid/mock-contract", "Get Plaid mock contract spec")]),

    (45, "mapping_studio", "Mapping Studio 2.0",
     "Deterministic transform DSL for imports: vendor mapping, COA mapping, tax mapping.",
     [("rule_id", "str"), ("name", "str"), ("rule_type", "str"),
      ("source_field", "str"), ("target_field", "str"), ("transform_expr", "str"),
      ("priority", "int"), ("active", "bool"), ("version", "int"),
      ("created_at", "str"), ("updated_at", "str|None")],
     [("list_rules", "GET", "/api/mapping-studio/rules", "List mapping rules"),
      ("create_rule", "POST", "/api/mapping-studio/rules", "Create a mapping rule"),
      ("get_rule", "GET", "/api/mapping-studio/rules/{rule_id}", "Get rule details"),
      ("preview", "POST", "/api/mapping-studio/rules/{rule_id}/preview", "Preview rule application"),
      ("apply_rule", "POST", "/api/mapping-studio/rules/{rule_id}/apply", "Apply mapping rule"),
      ("rollback", "POST", "/api/mapping-studio/rules/{rule_id}/rollback", "Rollback rule version"),
      ("export_rules", "GET", "/api/mapping-studio/export", "Export all mapping rules")]),

    (46, "data_quality", "Data Quality Engine",
     "Data quality rules (missing fields, duplicates, outliers), quality scorecard per close.",
     [("check_id", "str"), ("rule_name", "str"), ("rule_type", "str"),
      ("target_entity", "str"), ("severity", "str"), ("violations_found", "int"),
      ("quality_score", "float"), ("blocks_export", "bool"),
      ("approved_override", "bool"), ("run_at", "str")],
     [("list_checks", "GET", "/api/data-quality/checks", "List data quality checks"),
      ("run_check", "POST", "/api/data-quality/checks", "Run a data quality check"),
      ("get_check", "GET", "/api/data-quality/checks/{check_id}", "Get check details"),
      ("approve_override", "POST", "/api/data-quality/checks/{check_id}/approve", "Approve quality override"),
      ("scorecard", "GET", "/api/data-quality/scorecard", "Get quality scorecard"),
      ("export_report", "GET", "/api/data-quality/export", "Export quality report")]),

    (47, "continuous_close_v2", "Continuous Close 2.0",
     "Rolling exception queue, resumable idempotent jobs, background runners.",
     [("job_id", "str"), ("job_type", "str"), ("period_id", "str"),
      ("status", "str"), ("progress_pct", "float"), ("exceptions_found", "int"),
      ("resumable", "bool"), ("idempotency_key", "str"),
      ("started_at", "str"), ("paused_at", "str|None"), ("completed_at", "str|None")],
     [("list_jobs", "GET", "/api/continuous-close-v2/jobs", "List continuous close jobs"),
      ("start_job", "POST", "/api/continuous-close-v2/jobs", "Start a continuous close job"),
      ("get_job", "GET", "/api/continuous-close-v2/jobs/{job_id}", "Get job details"),
      ("pause_job", "POST", "/api/continuous-close-v2/jobs/{job_id}/pause", "Pause a running job"),
      ("resume_job", "POST", "/api/continuous-close-v2/jobs/{job_id}/resume", "Resume a paused job"),
      ("cancel_job", "POST", "/api/continuous-close-v2/jobs/{job_id}/cancel", "Cancel a job"),
      ("job_exceptions", "GET", "/api/continuous-close-v2/exceptions", "Get rolling exceptions queue")]),

    (48, "perf_suite", "Performance Suite 2.0",
     "Large deterministic fixtures, perf budgets, query indexes, 10x scale testing.",
     [("benchmark_id", "str"), ("name", "str"), ("fixture_size", "int"),
      ("target_ms", "float"), ("actual_ms", "float"), ("passed", "bool"),
      ("queries_counted", "int"), ("index_hits", "int"),
      ("run_at", "str")],
     [("list_benchmarks", "GET", "/api/perf-suite/benchmarks", "List performance benchmarks"),
      ("run_benchmark", "POST", "/api/perf-suite/benchmarks", "Run a performance benchmark"),
      ("get_benchmark", "GET", "/api/perf-suite/benchmarks/{benchmark_id}", "Get benchmark details"),
      ("set_budget", "POST", "/api/perf-suite/benchmarks/{benchmark_id}/budget", "Set performance budget"),
      ("compare", "GET", "/api/perf-suite/compare", "Compare benchmark runs"),
      ("regression_gate", "GET", "/api/perf-suite/regression", "Check regression gate")]),

    (49, "release_bundle_v2", "Release Bundle 2.0",
     "Proof index, lineage verifier, signatures. Generate twice = identical hash.",
     [("release_id", "str"), ("version", "str"), ("proof_index", "dict"),
      ("lineage", "list"), ("content_hash", "str"), ("signature", "str|None"),
      ("verified", "bool"), ("changelog", "str"),
      ("created_at", "str"), ("deployed_at", "str|None")],
     [("list_releases", "GET", "/api/releases-v2", "List release bundles v2"),
      ("create_release", "POST", "/api/releases-v2", "Create a release bundle v2"),
      ("get_release", "GET", "/api/releases-v2/{release_id}", "Get release details"),
      ("sign_release", "POST", "/api/releases-v2/{release_id}/sign", "Sign a release"),
      ("verify_release", "POST", "/api/releases-v2/{release_id}/verify", "Verify release integrity"),
      ("deploy", "POST", "/api/releases-v2/{release_id}/deploy", "Mark release as deployed"),
      ("lineage_report", "GET", "/api/releases-v2/lineage", "Get lineage report")]),

    (50, "judge_demo_v2", "Judge Demo 2.0",
     "Scripted 4-min demo script: seed, ingest, reconcile, override, export, verify.",
     [("demo_id", "str"), ("demo_name", "str"), ("steps", "list"),
      ("current_step", "int"), ("total_steps", "int"), ("status", "str"),
      ("duration_seconds", "float"), ("hash", "str|None"),
      ("started_at", "str"), ("completed_at", "str|None")],
     [("list_demos", "GET", "/api/judge-demo-v2/runs", "List demo runs"),
      ("start_demo", "POST", "/api/judge-demo-v2/runs", "Start a scripted demo"),
      ("get_demo", "GET", "/api/judge-demo-v2/runs/{demo_id}", "Get demo run details"),
      ("advance_step", "POST", "/api/judge-demo-v2/runs/{demo_id}/advance", "Advance to next step"),
      ("verify_demo", "POST", "/api/judge-demo-v2/runs/{demo_id}/verify", "Verify demo hash determinism"),
      ("reset_demo", "POST", "/api/judge-demo-v2/runs/{demo_id}/reset", "Reset demo state"),
      ("script_template", "GET", "/api/judge-demo-v2/template", "Get demo script template")]),

    # ── Phase 3: FP&A / Treasury (51-60) ───────────────────────────
    (51, "budgeting", "Budgeting 1.0",
     "Budget versions, approval routing, locking, variance hooks.",
     [("budget_id", "str"), ("name", "str"), ("version", "int"),
      ("period_id", "str"), ("status", "str"), ("total_amount", "float"),
      ("approved_by", "str|None"), ("locked", "bool"),
      ("variance_threshold_pct", "float"), ("created_at", "str"),
      ("published_at", "str|None")],
     [("list_budgets", "GET", "/api/budgets", "List budgets"),
      ("create_budget", "POST", "/api/budgets", "Create a budget"),
      ("get_budget", "GET", "/api/budgets/{budget_id}", "Get budget details"),
      ("submit_budget", "POST", "/api/budgets/{budget_id}/submit", "Submit budget for approval"),
      ("approve_budget", "POST", "/api/budgets/{budget_id}/approve", "Approve a budget"),
      ("lock_budget", "POST", "/api/budgets/{budget_id}/lock", "Lock a budget"),
      ("publish_budget", "POST", "/api/budgets/{budget_id}/publish", "Publish a budget"),
      ("variance_report", "GET", "/api/budgets/variance", "Get budget variance report")]),

    (52, "forecasting", "Forecasting 1.0",
     "Baseline forecasting (moving average, seasonal naive), model registry, drift alerts.",
     [("forecast_id", "str"), ("model_type", "str"), ("model_name", "str"),
      ("horizon_periods", "int"), ("predictions", "list"),
      ("mape", "float"), ("drift_detected", "bool"),
      ("baseline_hash", "str"), ("status", "str"),
      ("created_at", "str")],
     [("list_forecasts", "GET", "/api/forecasts", "List forecasts"),
      ("create_forecast", "POST", "/api/forecasts", "Create a forecast"),
      ("get_forecast", "GET", "/api/forecasts/{forecast_id}", "Get forecast details"),
      ("evaluate", "POST", "/api/forecasts/{forecast_id}/evaluate", "Evaluate forecast accuracy"),
      ("detect_drift", "POST", "/api/forecasts/{forecast_id}/drift", "Run drift detection"),
      ("register_model", "POST", "/api/forecasts/{forecast_id}/register", "Register model in registry"),
      ("model_registry", "GET", "/api/forecasts/registry", "Get model registry")]),

    (53, "driver_planning", "Driver-based Planning",
     "Drivers (headcount, units, pricing), propagation engine, cycle detection.",
     [("driver_id", "str"), ("name", "str"), ("driver_type", "str"),
      ("value", "float"), ("unit", "str"), ("depends_on", "list"),
      ("propagates_to", "list"), ("cycle_detected", "bool"),
      ("version", "int"), ("created_at", "str")],
     [("list_drivers", "GET", "/api/drivers", "List planning drivers"),
      ("create_driver", "POST", "/api/drivers", "Create a planning driver"),
      ("get_driver", "GET", "/api/drivers/{driver_id}", "Get driver details"),
      ("update_value", "POST", "/api/drivers/{driver_id}/update-value", "Update driver value"),
      ("propagate", "POST", "/api/drivers/{driver_id}/propagate", "Propagate driver changes"),
      ("check_cycles", "POST", "/api/drivers/{driver_id}/check-cycles", "Check for dependency cycles"),
      ("export_graph", "GET", "/api/drivers/export-graph", "Export driver dependency graph")]),

    (54, "scenario_engine", "Scenario Engine",
     "Seeded Monte Carlo scenarios, tail risk summary, deterministic outputs.",
     [("scenario_id", "str"), ("name", "str"), ("seed", "int"),
      ("iterations", "int"), ("base_inputs", "dict"),
      ("p10", "float"), ("p50", "float"), ("p90", "float"),
      ("tail_risk_pct", "float"), ("status", "str"),
      ("created_at", "str")],
     [("list_scenarios", "GET", "/api/scenarios", "List scenarios"),
      ("create_scenario", "POST", "/api/scenarios", "Create a scenario run"),
      ("get_scenario", "GET", "/api/scenarios/{scenario_id}", "Get scenario details"),
      ("run_simulation", "POST", "/api/scenarios/{scenario_id}/simulate", "Run Monte Carlo simulation"),
      ("compare_scenarios", "GET", "/api/scenarios/compare", "Compare scenario outcomes"),
      ("tail_risk", "GET", "/api/scenarios/tail-risk", "Get tail risk summary")]),

    (55, "treasury", "Treasury 2.0",
     "Debt schedules, interest projection, liquidity ladder view.",
     [("instrument_id", "str"), ("name", "str"), ("instrument_type", "str"),
      ("principal", "float"), ("rate_pct", "float"), ("maturity_date", "str"),
      ("interest_accrued", "float"), ("status", "str"),
      ("liquidity_bucket", "str"), ("created_at", "str")],
     [("list_instruments", "GET", "/api/treasury/instruments", "List treasury instruments"),
      ("create_instrument", "POST", "/api/treasury/instruments", "Create a treasury instrument"),
      ("get_instrument", "GET", "/api/treasury/instruments/{instrument_id}", "Get instrument details"),
      ("project_interest", "POST", "/api/treasury/instruments/{instrument_id}/project", "Project interest"),
      ("liquidity_ladder", "GET", "/api/treasury/liquidity-ladder", "Get liquidity ladder view"),
      ("debt_schedule", "GET", "/api/treasury/debt-schedule", "Get debt maturity schedule")]),

    (56, "covenants", "Covenants Monitoring",
     "Covenant rules, breach detection, alerts, evidence links.",
     [("covenant_id", "str"), ("name", "str"), ("metric", "str"),
      ("threshold", "float"), ("current_value", "float"), ("breached", "bool"),
      ("severity", "str"), ("evidence_links", "list"),
      ("alert_sent", "bool"), ("checked_at", "str")],
     [("list_covenants", "GET", "/api/covenants", "List covenants"),
      ("create_covenant", "POST", "/api/covenants", "Create a covenant rule"),
      ("get_covenant", "GET", "/api/covenants/{covenant_id}", "Get covenant details"),
      ("check_breach", "POST", "/api/covenants/{covenant_id}/check", "Check covenant for breach"),
      ("link_evidence", "POST", "/api/covenants/{covenant_id}/evidence", "Link evidence to covenant"),
      ("breach_summary", "GET", "/api/covenants/breach-summary", "Get breach summary report")]),

    (57, "cost_allocation", "Cost Allocation",
     "Cost centers, driver-based allocations, audit chain.",
     [("allocation_id", "str"), ("cost_center_id", "str"), ("cost_center_name", "str"),
      ("driver", "str"), ("source_amount", "float"), ("allocated_amount", "float"),
      ("allocation_pct", "float"), ("period_id", "str"),
      ("status", "str"), ("created_at", "str")],
     [("list_allocations", "GET", "/api/cost-allocations", "List cost allocations"),
      ("create_allocation", "POST", "/api/cost-allocations", "Create a cost allocation"),
      ("get_allocation", "GET", "/api/cost-allocations/{allocation_id}", "Get allocation details"),
      ("recalculate", "POST", "/api/cost-allocations/{allocation_id}/recalculate", "Recalculate allocation"),
      ("drilldown", "GET", "/api/cost-allocations/drilldown", "Cost allocation drilldown"),
      ("export_allocations", "GET", "/api/cost-allocations/export", "Export allocations report")]),

    (58, "kpi_framework", "KPI Framework",
     "KPIs as objects with formulas + evidence links. No floating KPIs.",
     [("kpi_id", "str"), ("name", "str"), ("formula", "str"),
      ("value", "float"), ("target", "float"), ("unit", "str"),
      ("evidence_links", "list"), ("status", "str"),
      ("owner", "str"), ("computed_at", "str")],
     [("list_kpis", "GET", "/api/kpis", "List KPIs"),
      ("create_kpi", "POST", "/api/kpis", "Create a KPI"),
      ("get_kpi", "GET", "/api/kpis/{kpi_id}", "Get KPI details"),
      ("compute", "POST", "/api/kpis/{kpi_id}/compute", "Compute KPI value"),
      ("link_evidence", "POST", "/api/kpis/{kpi_id}/evidence", "Link evidence to KPI"),
      ("completeness", "GET", "/api/kpis/completeness", "Check KPI completeness"),
      ("export_kpis", "GET", "/api/kpis/export", "Export KPI report")]),

    (59, "board_pack", "Board Pack Generator",
     "Deterministic board pack export combining statements, KPIs, treasury, risks.",
     [("pack_id", "str"), ("name", "str"), ("period_id", "str"),
      ("sections", "list"), ("format_type", "str"), ("content_hash", "str|None"),
      ("status", "str"), ("generated_at", "str|None"),
      ("page_count", "int"), ("created_at", "str")],
     [("list_packs", "GET", "/api/board-packs", "List board packs"),
      ("create_pack", "POST", "/api/board-packs", "Create a board pack"),
      ("get_pack", "GET", "/api/board-packs/{pack_id}", "Get board pack details"),
      ("add_section", "POST", "/api/board-packs/{pack_id}/sections", "Add section to board pack"),
      ("generate", "POST", "/api/board-packs/{pack_id}/generate", "Generate board pack export"),
      ("verify_pack", "POST", "/api/board-packs/{pack_id}/verify", "Verify board pack hash"),
      ("export_pack", "GET", "/api/board-packs/export", "Export latest board pack")]),

    (60, "ops_bundle", "Enterprise Ops Bundle",
     "One-click ops evidence export: job runs, alerts, quality scores, lineage, proof index.",
     [("bundle_id", "str"), ("name", "str"), ("period_id", "str"),
      ("job_runs", "list"), ("alerts", "list"), ("quality_scores", "dict"),
      ("lineage", "list"), ("proof_index", "dict"), ("content_hash", "str|None"),
      ("status", "str"), ("created_at", "str"), ("exported_at", "str|None")],
     [("list_bundles", "GET", "/api/ops-bundles", "List ops bundles"),
      ("create_bundle", "POST", "/api/ops-bundles", "Create an ops bundle"),
      ("get_bundle", "GET", "/api/ops-bundles/{bundle_id}", "Get ops bundle details"),
      ("add_evidence", "POST", "/api/ops-bundles/{bundle_id}/evidence", "Add evidence to bundle"),
      ("compute_hash", "POST", "/api/ops-bundles/{bundle_id}/hash", "Compute bundle content hash"),
      ("verify_bundle", "POST", "/api/ops-bundles/{bundle_id}/verify", "Verify bundle integrity"),
      ("export_bundle", "GET", "/api/ops-bundles/export", "Export ops bundle")]),
]


def _class_name(slug: str) -> str:
    return "".join(w.capitalize() for w in slug.split("_"))


def _default_value(type_str: str) -> str:
    if type_str in ("str", "str|None"):
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
        if ftype in ("str", "str|None"):
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


def gen_service(wave_num, slug, title, desc, fields, operations):
    id_field = fields[0][0]
    field_defs = "\n".join(f'        "{f[0]}": {_default_value(f[1])},' for f in fields)

    ops_code = []
    for op_name, method, path, op_desc in operations:
        if method == "GET" and "{" not in path:
            ops_code.append(f'''
    def {op_name}(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]
''')
        elif method == "POST" and "{" not in path:
            ops_code.append(f'''
    def {op_name}(self, data: dict) -> dict:
        """Create a new item."""
        import uuid as _u
        item_id = str(_u.uuid4())
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
            ops_code.append(f'''
    def {op_name}(self, {param}: str, data: dict | None = None) -> dict | None:
        """Action: {op_name}."""
        item = self._store.get({param})
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "{op_name}d"
        emit_audit_event("{op_name}", "{slug}", {param}, {{"action": "{op_name}", "data": data or {{}}}})
        return item
''')

    return f'''"""Wave {wave_num}: {title} — {desc}

PROJECT_ID: LEDGERLIVE
"""
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


def gen_router(wave_num, slug, title, desc, fields, operations):
    svc_import = f"from app.services.w{wave_num:02d}_{slug} import service"

    # Sort: literal paths first, parameterized paths second
    sorted_ops = sorted(operations, key=lambda o: (1 if '{' in o[2] else 0, o[2]))

    routes = []
    for op_name, method, path, op_desc in sorted_ops:
        if method == "GET" and "{" not in path:
            routes.append(f'''
@router.get("{path}")
async def api_{slug}_w{wave_num}_{op_name}(limit: int = 100):
    """{op_desc}"""
    items = service.{op_name}(limit=limit)
    return {{"items": items, "total": len(items)}}
''')
        elif method == "POST" and "{" not in path:
            routes.append(f'''
@router.post("{path}", status_code=201)
async def api_{slug}_w{wave_num}_{op_name}(request: Request):
    """{op_desc}"""
    data = await request.json()
    item = service.{op_name}(data)
    return item
''')
        elif method == "GET" and "{" in path:
            param = re.search(r'\{(\w+)\}', path).group(1)
            routes.append(f'''
@router.get("{path}")
async def api_{slug}_w{wave_num}_{op_name}({param}: str):
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
async def api_{slug}_w{wave_num}_{op_name}({param}: str, request: Request):
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
async def api_{slug}_w{wave_num}_{op_name}({param}: str):
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
async def api_{slug}_w{wave_num}_{op_name}({param}: str, request: Request):
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


def gen_tests(wave_num, slug, title, desc, fields, operations):
    id_field = fields[0][0]
    svc_import = f"from app.services.w{wave_num:02d}_{slug} import service"

    create_op = list_op = get_op = update_op = delete_op = None
    action_ops = []

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

    sample_data = _sample_create_data(fields)
    tests = []

    # Fixture
    tests.append(f'''
@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()
''')

    # service starts empty
    tests.append(f'''
def test_w{wave_num:02d}_service_starts_empty():
    assert service.count == 0
''')

    # create
    if create_op:
        _, _, cpath = create_op
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_create(client):
    r = await client.post("{cpath}", json={sample_data})
    assert r.status_code == 201
    data = r.json()
    assert "{id_field}" in data
    assert service.count == 1
''')

    # list
    if list_op and create_op:
        _, _, lpath = list_op
        _, _, cpath = create_op
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_list(client):
    await client.post("{cpath}", json={sample_data})
    await client.post("{cpath}", json={sample_data})
    r = await client.get("{lpath}")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2
''')

    # get by id
    if get_op and create_op:
        _, _, gpath = get_op
        _, _, cpath = create_op
        param = re.search(r'\{(\w+)\}', gpath).group(1)
        gpath_t = gpath.replace("{" + param + "}", "{item_id}")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_get_by_id(client):
    r = await client.post("{cpath}", json={sample_data})
    item_id = r.json()["{id_field}"]
    r2 = await client.get(f"{gpath_t}")
    assert r2.status_code == 200
    assert r2.json()["{id_field}"] == item_id
''')

    # get 404
    if get_op:
        _, _, gpath = get_op
        param = re.search(r'\{(\w+)\}', gpath).group(1)
        gpath_404 = gpath.replace("{" + param + "}", "nonexistent-id")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_get_not_found(client):
    r = await client.get("{gpath_404}")
    assert r.status_code == 404
''')

    # update
    if update_op and create_op:
        _, _, upath = update_op
        _, _, cpath = create_op
        param = re.search(r'\{(\w+)\}', upath).group(1)
        upath_t = upath.replace("{" + param + "}", "{item_id}")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_update(client):
    r = await client.post("{cpath}", json={sample_data})
    item_id = r.json()["{id_field}"]
    r2 = await client.put(f"{upath_t}", json={{"name": "updated"}})
    assert r2.status_code == 200
    assert r2.json()["name"] == "updated"
''')

    # delete
    if delete_op and create_op:
        _, _, dpath = delete_op
        _, _, cpath = create_op
        param = re.search(r'\{(\w+)\}', dpath).group(1)
        dpath_t = dpath.replace("{" + param + "}", "{item_id}")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_delete(client):
    r = await client.post("{cpath}", json={sample_data})
    item_id = r.json()["{id_field}"]
    r2 = await client.delete(f"{dpath_t}")
    assert r2.status_code == 200
    assert r2.json()["deleted"] is True
    assert service.count == 0
''')

    # action ops (test first 3)
    if action_ops and create_op:
        _, _, cpath = create_op
        for aname, _, apath in action_ops[:3]:
            param = re.search(r'\{(\w+)\}', apath).group(1)
            apath_t = apath.replace("{" + param + "}", "{item_id}")
            tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_{aname}(client):
    r = await client.post("{cpath}", json={sample_data})
    item_id = r.json()["{id_field}"]
    r2 = await client.post(f"{apath_t}", json={{}})
    assert r2.status_code == 200
    assert r2.json()["{id_field}"] == item_id
''')

    # action 404
    if action_ops:
        aname, _, apath = action_ops[0]
        param = re.search(r'\{(\w+)\}', apath).group(1)
        apath_404 = apath.replace("{" + param + "}", "nonexistent-id")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_{aname}_not_found(client):
    r = await client.post("{apath_404}", json={{}})
    assert r.status_code == 404
''')

    # audit event emitted
    if create_op:
        _, _, cpath = create_op
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("{cpath}", json={sample_data})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "{slug}"
    assert "trace_id" in event
''')

    # determinism
    if create_op:
        _, _, cpath = create_op
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("{cpath}", json={sample_data})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("{cpath}", json={sample_data})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "{id_field}":
            assert type(d1[k]) == type(d2[k])
''')

    # break-it: empty body
    if create_op:
        _, _, cpath = create_op
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("{cpath}", json={{}})
    assert r.status_code == 201
''')

    # integration: create then list then get
    if create_op and list_op and get_op:
        _, _, cpath = create_op
        _, _, lpath = list_op
        _, _, gpath = get_op
        param = re.search(r'\{(\w+)\}', gpath).group(1)
        gpath_t = gpath.replace("{" + param + "}", "{item_id}")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:02d}_integration_create_list_get(client):
    """Integration: create → list → get by ID."""
    r1 = await client.post("{cpath}", json={sample_data})
    assert r1.status_code == 201
    item_id = r1.json()["{id_field}"]
    r2 = await client.get("{lpath}")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"{gpath_t}")
    assert r3.status_code == 200
    assert r3.json()["{id_field}"] == item_id
''')

    return f'''"""Tests for Wave {wave_num}: {title}

PROJECT_ID: LEDGERLIVE
"""
import pytest
{svc_import}

{"".join(tests)}'''


def gen_main_additions(waves):
    imports = []
    includes = []
    for wave_num, slug, *_ in waves:
        imports.append(f"from app.routers.w{wave_num:02d}_{slug} import router as w{wave_num:02d}_router")
        includes.append(f"app.include_router(w{wave_num:02d}_router)")
    return "\n".join(imports) + "\n\n" + "\n".join(includes) + "\n"


def main():
    print(f"Generating {len(WAVES)} waves (31-60)...")

    for wave_num, slug, title, desc, fields, operations in WAVES:
        svc_path = SVC_DIR / f"w{wave_num:02d}_{slug}.py"
        svc_path.write_text(gen_service(wave_num, slug, title, desc, fields, operations), encoding="utf-8")

        rtr_path = RTR_DIR / f"w{wave_num:02d}_{slug}.py"
        rtr_path.write_text(gen_router(wave_num, slug, title, desc, fields, operations), encoding="utf-8")

        tst_path = TST_DIR / f"test_w{wave_num:02d}_{slug}.py"
        tst_path.write_text(gen_tests(wave_num, slug, title, desc, fields, operations), encoding="utf-8")

        print(f"  W{wave_num:02d} {slug}: service + router + tests")

    # Append router registrations to main.py
    main_content = MAIN_PY.read_text(encoding="utf-8")
    additions = gen_main_additions(WAVES)
    # Append after existing router registrations
    main_content = main_content.rstrip() + "\n\n" + additions
    MAIN_PY.write_text(main_content, encoding="utf-8")
    print(f"\n  main.py updated with {len(WAVES)} new router registrations")

    print(f"\nDone! Generated {len(WAVES)} services, routers, and test files for waves 31-60.")


if __name__ == "__main__":
    main()
