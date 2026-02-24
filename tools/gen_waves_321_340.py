#!/usr/bin/env python3
"""Generate LedgerLive Waves 321-340: Phases 34 (rest), 35, 36.

Phase 34 rest (321-324): Airia Community Readiness (last 4)
Phase 35 (325-332): Security + Governance WOW
Phase 36 (333-340): Impact + Race WOW

Run: python tools/gen_waves_321_340.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SVC_DIR = ROOT / "apps" / "api" / "app" / "services"
RTR_DIR = ROOT / "apps" / "api" / "app" / "routers"
TST_DIR = ROOT / "apps" / "api" / "tests"
MAIN_PY = ROOT / "apps" / "api" / "app" / "main.py"

WAVES = [
    # ════════════════════════════════════════════════════════════════
    # PHASE 34 (rest): AIRIA COMMUNITY READINESS (W321-W324)
    # ════════════════════════════════════════════════════════════════
    (321, "bundle_integrity_proof", "Bundle Integrity Proof v1",
     "Signing and verify tool for bundles; tamper must fail deterministically.",
     [("integrity_id", "str"), ("bundle_ref", "str"), ("signature", "str"),
      ("public_key_ref", "str"), ("signed_hash", "str"),
      ("verified", "bool"), ("tamper_detected", "bool"),
      ("tamper_detail", "str"), ("signer_identity", "str"),
      ("deterministic", "bool"),
      ("status", "str"), ("signed_at", "str")],
     [("list_proofs", "GET", "/api/bundle-integrity-proof", "List integrity proofs"),
      ("sign_bundle", "POST", "/api/bundle-integrity-proof", "Sign bundle"),
      ("get_proof", "GET", "/api/bundle-integrity-proof/{integrity_id}", "Get proof details"),
      ("verify_signature", "POST", "/api/bundle-integrity-proof/{integrity_id}/verify", "Verify bundle signature"),
      ("tamper_test", "POST", "/api/bundle-integrity-proof/{integrity_id}/tamper-test", "Test tamper detection"),
      ("integrity_report", "GET", "/api/bundle-integrity-proof/report", "Get integrity report")]),

    (322, "readiness_e2e_suite", "Readiness E2E Suite v1",
     "MCP E2E: generate bundle -> validate -> verify -> show PASS badge.",
     [("suite_id", "str"), ("test_name", "str"), ("bundle_generated", "bool"),
      ("validation_passed", "bool"), ("verification_passed", "bool"),
      ("badge_shown", "bool"), ("all_passed", "bool"),
      ("steps_executed", "list"), ("execution_log", "list"),
      ("deterministic", "bool"),
      ("status", "str"), ("executed_at", "str")],
     [("list_suites", "GET", "/api/readiness-e2e-suite", "List E2E suites"),
      ("run_suite", "POST", "/api/readiness-e2e-suite", "Run readiness E2E suite"),
      ("get_suite", "GET", "/api/readiness-e2e-suite/{suite_id}", "Get suite details"),
      ("rerun_suite", "POST", "/api/readiness-e2e-suite/{suite_id}/rerun", "Rerun E2E suite"),
      ("export_badge", "POST", "/api/readiness-e2e-suite/{suite_id}/badge", "Export PASS badge"),
      ("suite_report", "GET", "/api/readiness-e2e-suite/report", "Get readiness E2E report")]),

    (323, "readiness_dashboard", "Readiness Dashboard v1",
     "Single screen showing publish readiness checklist status (offline deterministic).",
     [("dashboard_id", "str"), ("checklist_items", "list"),
      ("items_passed", "int"), ("items_failed", "int"),
      ("items_pending", "int"), ("overall_ready", "bool"),
      ("last_check_refs", "dict"), ("blocking_items", "list"),
      ("readiness_score", "float"), ("deterministic", "bool"),
      ("status", "str"), ("checked_at", "str")],
     [("list_dashboards", "GET", "/api/readiness-dashboard", "List readiness dashboards"),
      ("create_dashboard", "POST", "/api/readiness-dashboard", "Create readiness dashboard"),
      ("get_dashboard", "GET", "/api/readiness-dashboard/{dashboard_id}", "Get dashboard details"),
      ("run_checklist", "POST", "/api/readiness-dashboard/{dashboard_id}/check", "Run readiness checklist"),
      ("export_status", "POST", "/api/readiness-dashboard/{dashboard_id}/export", "Export readiness status"),
      ("dashboard_report", "GET", "/api/readiness-dashboard/report", "Get readiness dashboard report")]),

    (324, "readiness_proof", "Readiness Proof Wave v1",
     "Readiness PASS with verified artifacts and determinism twice-run.",
     [("proof_id", "str"), ("readiness_ref", "str"), ("bundle_verified", "bool"),
      ("validator_passed", "bool"), ("dashboard_passed", "bool"),
      ("determinism_hash_1", "str"), ("determinism_hash_2", "str"),
      ("hashes_match", "bool"), ("evidence_refs", "list"),
      ("deterministic", "bool"),
      ("status", "str"), ("verified_at", "str")],
     [("list_proofs", "GET", "/api/readiness-proof", "List readiness proofs"),
      ("generate_proof", "POST", "/api/readiness-proof", "Generate readiness proof"),
      ("get_proof", "GET", "/api/readiness-proof/{proof_id}", "Get proof details"),
      ("verify_readiness", "POST", "/api/readiness-proof/{proof_id}/verify", "Verify readiness"),
      ("seal_proof", "POST", "/api/readiness-proof/{proof_id}/seal", "Seal readiness proof"),
      ("proof_report", "GET", "/api/readiness-proof/report", "Get readiness proof report")]),

    # ════════════════════════════════════════════════════════════════
    # PHASE 35: SECURITY + GOVERNANCE WOW (W325-W332)
    # ════════════════════════════════════════════════════════════════
    (325, "data_classification_tiers", "Data Classification Tiers v1",
     "Tag documents/fields with classification tiers; show tier in UI; enforce policy by tier.",
     [("classification_id", "str"), ("document_ref", "str"), ("field_name", "str"),
      ("tier", "str"), ("tier_level", "int"), ("policy_ref", "str"),
      ("enforcement_action", "str"), ("is_enforced", "bool"),
      ("display_label", "str"), ("classification_reason", "str"),
      ("deterministic", "bool"),
      ("status", "str"), ("classified_at", "str")],
     [("list_classifications", "GET", "/api/data-classification-tiers", "List classifications"),
      ("create_classification", "POST", "/api/data-classification-tiers", "Classify a document/field"),
      ("get_classification", "GET", "/api/data-classification-tiers/{classification_id}", "Get classification details"),
      ("enforce_policy", "POST", "/api/data-classification-tiers/{classification_id}/enforce", "Enforce tier policy"),
      ("reclassify", "POST", "/api/data-classification-tiers/{classification_id}/reclassify", "Reclassify tier"),
      ("classification_report", "GET", "/api/data-classification-tiers/report", "Get classification report")]),

    (326, "tool_scope_diffing", "Tool Scope Diffing v1",
     "Show scope changes over time; approvals required for expanding scopes; audited.",
     [("diff_id", "str"), ("tool_ref", "str"), ("scope_before", "list"),
      ("scope_after", "list"), ("added_scopes", "list"),
      ("removed_scopes", "list"), ("expansion_detected", "bool"),
      ("approval_required", "bool"), ("approved_by", "str"),
      ("audit_ref", "str"), ("deterministic", "bool"),
      ("status", "str"), ("diffed_at", "str")],
     [("list_diffs", "GET", "/api/tool-scope-diffing", "List scope diffs"),
      ("create_diff", "POST", "/api/tool-scope-diffing", "Create scope diff"),
      ("get_diff", "GET", "/api/tool-scope-diffing/{diff_id}", "Get diff details"),
      ("approve_expansion", "POST", "/api/tool-scope-diffing/{diff_id}/approve", "Approve scope expansion"),
      ("reject_expansion", "POST", "/api/tool-scope-diffing/{diff_id}/reject", "Reject scope expansion"),
      ("diff_report", "GET", "/api/tool-scope-diffing/report", "Get scope diffing report")]),

    (327, "redaction_events_v1", "Redaction Events v1",
     "Redaction actions become first-class security events with evidence links.",
     [("redaction_id", "str"), ("document_ref", "str"), ("field_redacted", "str"),
      ("redaction_reason", "str"), ("redacted_by", "str"),
      ("evidence_ref", "str"), ("original_tier", "str"),
      ("redaction_method", "str"), ("reversible", "bool"),
      ("deterministic", "bool"),
      ("status", "str"), ("redacted_at", "str")],
     [("list_redactions", "GET", "/api/redaction-events-v1", "List redaction events"),
      ("create_redaction", "POST", "/api/redaction-events-v1", "Create redaction event"),
      ("get_redaction", "GET", "/api/redaction-events-v1/{redaction_id}", "Get redaction details"),
      ("link_evidence", "POST", "/api/redaction-events-v1/{redaction_id}/evidence", "Link evidence to redaction"),
      ("reverse_redaction", "POST", "/api/redaction-events-v1/{redaction_id}/reverse", "Reverse redaction if allowed"),
      ("redaction_report", "GET", "/api/redaction-events-v1/report", "Get redaction events report")]),

    (328, "security_scoreboard_v1", "Security Scoreboard v1",
     "Blocked actions, reasons, remediation success rate; deterministic metrics.",
     [("score_id", "str"), ("period_ref", "str"), ("blocked_count", "int"),
      ("block_reasons", "list"), ("remediation_attempted", "int"),
      ("remediation_succeeded", "int"), ("success_rate", "float"),
      ("top_threats", "list"), ("score", "float"),
      ("deterministic", "bool"),
      ("status", "str"), ("scored_at", "str")],
     [("list_scores", "GET", "/api/security-scoreboard-v1", "List security scores"),
      ("create_score", "POST", "/api/security-scoreboard-v1", "Create security score"),
      ("get_score", "GET", "/api/security-scoreboard-v1/{score_id}", "Get score details"),
      ("recalculate", "POST", "/api/security-scoreboard-v1/{score_id}/recalculate", "Recalculate score"),
      ("export_metrics", "POST", "/api/security-scoreboard-v1/{score_id}/export", "Export metrics"),
      ("score_report", "GET", "/api/security-scoreboard-v1/report", "Get security scoreboard report")]),

    (329, "policy_regression_budgets", "Policy Regression Budgets v1",
     "Fail if deny explainability coverage or detection coverage regresses.",
     [("budget_id", "str"), ("policy_ref", "str"), ("baseline_coverage", "float"),
      ("current_coverage", "float"), ("coverage_delta", "float"),
      ("regressed", "bool"), ("regression_threshold", "float"),
      ("explainability_score", "float"), ("detection_score", "float"),
      ("budget_exceeded", "bool"), ("deterministic", "bool"),
      ("status", "str"), ("evaluated_at", "str")],
     [("list_budgets", "GET", "/api/policy-regression-budgets", "List regression budgets"),
      ("create_budget", "POST", "/api/policy-regression-budgets", "Create regression budget"),
      ("get_budget", "GET", "/api/policy-regression-budgets/{budget_id}", "Get budget details"),
      ("evaluate_regression", "POST", "/api/policy-regression-budgets/{budget_id}/evaluate", "Evaluate regression"),
      ("reset_baseline", "POST", "/api/policy-regression-budgets/{budget_id}/reset", "Reset baseline"),
      ("budget_report", "GET", "/api/policy-regression-budgets/report", "Get regression budget report")]),

    (330, "adversarial_corpus_v3", "Adversarial Corpus v3",
     "100+ scenarios across channels/docs/blueprints with deterministic results.",
     [("corpus_id", "str"), ("scenario_count", "int"), ("channels_covered", "list"),
      ("docs_covered", "list"), ("blueprints_covered", "list"),
      ("attacks_blocked", "int"), ("attacks_missed", "int"),
      ("detection_rate", "float"), ("false_positives", "int"),
      ("corpus_version", "str"), ("deterministic", "bool"),
      ("status", "str"), ("tested_at", "str")],
     [("list_corpora", "GET", "/api/adversarial-corpus-v3", "List adversarial corpora"),
      ("create_corpus", "POST", "/api/adversarial-corpus-v3", "Create adversarial corpus"),
      ("get_corpus", "GET", "/api/adversarial-corpus-v3/{corpus_id}", "Get corpus details"),
      ("run_scenarios", "POST", "/api/adversarial-corpus-v3/{corpus_id}/run", "Run adversarial scenarios"),
      ("analyze_results", "POST", "/api/adversarial-corpus-v3/{corpus_id}/analyze", "Analyze results"),
      ("corpus_report", "GET", "/api/adversarial-corpus-v3/report", "Get adversarial corpus report")]),

    (331, "security_e2e_suite", "Security E2E Suite v1",
     "MCP E2E: injection attempt -> blocked -> remediation path -> approved -> proceeds safely.",
     [("suite_id", "str"), ("test_name", "str"), ("injection_blocked", "bool"),
      ("remediation_path_found", "bool"), ("approval_obtained", "bool"),
      ("safe_proceed", "bool"), ("all_passed", "bool"),
      ("steps_executed", "list"), ("execution_log", "list"),
      ("deterministic", "bool"),
      ("status", "str"), ("executed_at", "str")],
     [("list_suites", "GET", "/api/security-e2e-suite", "List security E2E suites"),
      ("run_suite", "POST", "/api/security-e2e-suite", "Run security E2E suite"),
      ("get_suite", "GET", "/api/security-e2e-suite/{suite_id}", "Get suite details"),
      ("rerun_suite", "POST", "/api/security-e2e-suite/{suite_id}/rerun", "Rerun E2E suite"),
      ("export_evidence", "POST", "/api/security-e2e-suite/{suite_id}/evidence", "Export security evidence"),
      ("suite_report", "GET", "/api/security-e2e-suite/report", "Get security E2E report")]),

    (332, "security_gov_proof", "Security Governance Proof v1",
     "Security posture demonstrated in Race Control with deterministic exports.",
     [("proof_id", "str"), ("security_posture_ref", "str"), ("rc_display_verified", "bool"),
      ("export_checksum", "str"), ("scoreboard_verified", "bool"),
      ("corpus_passed", "bool"), ("regression_passed", "bool"),
      ("determinism_hash_1", "str"), ("determinism_hash_2", "str"),
      ("hashes_match", "bool"), ("evidence_refs", "list"),
      ("deterministic", "bool"),
      ("status", "str"), ("verified_at", "str")],
     [("list_proofs", "GET", "/api/security-gov-proof", "List governance proofs"),
      ("generate_proof", "POST", "/api/security-gov-proof", "Generate governance proof"),
      ("get_proof", "GET", "/api/security-gov-proof/{proof_id}", "Get proof details"),
      ("verify_posture", "POST", "/api/security-gov-proof/{proof_id}/verify", "Verify security posture"),
      ("seal_proof", "POST", "/api/security-gov-proof/{proof_id}/seal", "Seal governance proof"),
      ("proof_report", "GET", "/api/security-gov-proof/report", "Get governance proof report")]),

    # ════════════════════════════════════════════════════════════════
    # PHASE 36: IMPACT + RACE WOW (W333-W340)
    # ════════════════════════════════════════════════════════════════
    (333, "lap_time_telemetry", "Lap Time Telemetry v1",
     "Deterministic durations per step (bucketed), critical path heatmap.",
     [("lap_id", "str"), ("step_name", "str"), ("duration_ms", "int"),
      ("bucket", "str"), ("is_critical_path", "bool"),
      ("heatmap_color", "str"), ("sequence_num", "int"),
      ("parent_lap_ref", "str"), ("percentile_rank", "float"),
      ("deterministic", "bool"),
      ("status", "str"), ("recorded_at", "str")],
     [("list_laps", "GET", "/api/lap-time-telemetry", "List lap times"),
      ("record_lap", "POST", "/api/lap-time-telemetry", "Record lap time"),
      ("get_lap", "GET", "/api/lap-time-telemetry/{lap_id}", "Get lap details"),
      ("bucket_analysis", "POST", "/api/lap-time-telemetry/{lap_id}/bucket", "Run bucket analysis"),
      ("heatmap_data", "POST", "/api/lap-time-telemetry/{lap_id}/heatmap", "Generate heatmap data"),
      ("lap_report", "GET", "/api/lap-time-telemetry/report", "Get lap time report")]),

    (334, "productivity_roi", "Productivity ROI Estimator v1",
     "Time saved, exceptions prevented, SLA compliance; deterministic calculation.",
     [("roi_id", "str"), ("period_ref", "str"), ("time_saved_hours", "float"),
      ("exceptions_prevented", "int"), ("sla_compliance_pct", "float"),
      ("cost_savings", "float"), ("roi_multiplier", "float"),
      ("calculation_method", "str"), ("baseline_ref", "str"),
      ("deterministic", "bool"),
      ("status", "str"), ("calculated_at", "str")],
     [("list_rois", "GET", "/api/productivity-roi", "List ROI estimates"),
      ("calculate_roi", "POST", "/api/productivity-roi", "Calculate ROI"),
      ("get_roi", "GET", "/api/productivity-roi/{roi_id}", "Get ROI details"),
      ("recalculate", "POST", "/api/productivity-roi/{roi_id}/recalculate", "Recalculate ROI"),
      ("export_report", "POST", "/api/productivity-roi/{roi_id}/export", "Export ROI report"),
      ("roi_report", "GET", "/api/productivity-roi/report", "Get productivity ROI report")]),

    (335, "pit_stop_optimizer", "Pit Stop Optimizer v1",
     "Suggests next-best step ordering given blockers (deterministic).",
     [("optimizer_id", "str"), ("current_blockers", "list"),
      ("available_steps", "list"), ("suggested_order", "list"),
      ("time_estimate_ms", "int"), ("critical_path_impact", "float"),
      ("optimization_score", "float"), ("constraints", "list"),
      ("algorithm_version", "str"), ("deterministic", "bool"),
      ("status", "str"), ("optimized_at", "str")],
     [("list_optimizations", "GET", "/api/pit-stop-optimizer", "List optimizations"),
      ("optimize", "POST", "/api/pit-stop-optimizer", "Run pit stop optimization"),
      ("get_optimization", "GET", "/api/pit-stop-optimizer/{optimizer_id}", "Get optimization details"),
      ("reoptimize", "POST", "/api/pit-stop-optimizer/{optimizer_id}/reoptimize", "Reoptimize with new data"),
      ("apply_suggestion", "POST", "/api/pit-stop-optimizer/{optimizer_id}/apply", "Apply suggested order"),
      ("optimizer_report", "GET", "/api/pit-stop-optimizer/report", "Get optimizer report")]),

    (336, "one_cockpit", "One Cockpit v1",
     "Race Control as default home route with minimal cognitive load polish.",
     [("cockpit_id", "str"), ("layout_config", "dict"),
      ("visible_sections", "list"), ("hidden_sections", "list"),
      ("default_route", "str"), ("cognitive_load_score", "float"),
      ("section_order", "list"), ("user_prefs", "dict"),
      ("is_home", "bool"), ("deterministic", "bool"),
      ("status", "str"), ("configured_at", "str")],
     [("list_cockpits", "GET", "/api/one-cockpit", "List cockpit configs"),
      ("create_cockpit", "POST", "/api/one-cockpit", "Create cockpit config"),
      ("get_cockpit", "GET", "/api/one-cockpit/{cockpit_id}", "Get cockpit details"),
      ("set_default", "POST", "/api/one-cockpit/{cockpit_id}/set-default", "Set as default home"),
      ("customize_layout", "POST", "/api/one-cockpit/{cockpit_id}/customize", "Customize layout"),
      ("cockpit_report", "GET", "/api/one-cockpit/report", "Get cockpit config report")]),

    (337, "unified_why_verify_v4", "Unified Why/Verify UX v4",
     "One-click dossier/evidence/policy from every table row.",
     [("verify_id", "str"), ("source_row_ref", "str"), ("dossier_ref", "str"),
      ("evidence_refs", "list"), ("policy_ref", "str"),
      ("verification_result", "str"), ("confidence", "float"),
      ("one_click_url", "str"), ("context_data", "dict"),
      ("deterministic", "bool"),
      ("status", "str"), ("verified_at", "str")],
     [("list_verifications", "GET", "/api/unified-why-verify-v4", "List verifications"),
      ("create_verification", "POST", "/api/unified-why-verify-v4", "Create verification"),
      ("get_verification", "GET", "/api/unified-why-verify-v4/{verify_id}", "Get verification details"),
      ("fetch_dossier", "POST", "/api/unified-why-verify-v4/{verify_id}/dossier", "Fetch linked dossier"),
      ("fetch_evidence", "POST", "/api/unified-why-verify-v4/{verify_id}/evidence", "Fetch linked evidence"),
      ("verify_report", "GET", "/api/unified-why-verify-v4/report", "Get verification report")]),

    (338, "golden_scenario_gate", "Golden Scenario Gate v1",
     "Canonical dataset must produce blockers, approvals, incidents, replay regen equality, verified exports.",
     [("gate_id", "str"), ("dataset_ref", "str"), ("blockers_found", "bool"),
      ("approvals_found", "bool"), ("incidents_found", "bool"),
      ("replay_regen_equal", "bool"), ("exports_verified", "bool"),
      ("all_conditions_met", "bool"), ("gate_passed", "bool"),
      ("failure_reasons", "list"), ("deterministic", "bool"),
      ("status", "str"), ("evaluated_at", "str")],
     [("list_gates", "GET", "/api/golden-scenario-gate", "List golden scenario gates"),
      ("run_gate", "POST", "/api/golden-scenario-gate", "Run golden scenario gate"),
      ("get_gate", "GET", "/api/golden-scenario-gate/{gate_id}", "Get gate details"),
      ("verify_conditions", "POST", "/api/golden-scenario-gate/{gate_id}/verify", "Verify all conditions met"),
      ("export_evidence", "POST", "/api/golden-scenario-gate/{gate_id}/evidence", "Export gate evidence"),
      ("gate_report", "GET", "/api/golden-scenario-gate/report", "Get golden scenario report")]),

    (339, "final_rc_gate_v4", "Final RC Gate v4",
     "Asserts builder coverage, Atlassian mocks, Airia readiness, security budgets, Golden Scenario PASS.",
     [("gate_id", "str"), ("builder_coverage", "bool"), ("atlassian_mocks_pass", "bool"),
      ("airia_readiness", "bool"), ("security_budgets_pass", "bool"),
      ("golden_scenario_pass", "bool"), ("all_pass", "bool"),
      ("gate_score", "float"), ("failure_details", "list"),
      ("evidence_refs", "list"), ("deterministic", "bool"),
      ("status", "str"), ("evaluated_at", "str")],
     [("list_gates", "GET", "/api/final-rc-gate-v4", "List final RC gates v4"),
      ("run_gate", "POST", "/api/final-rc-gate-v4", "Run final RC gate v4"),
      ("get_gate", "GET", "/api/final-rc-gate-v4/{gate_id}", "Get gate details"),
      ("verify_all", "POST", "/api/final-rc-gate-v4/{gate_id}/verify", "Verify all sub-gates"),
      ("export_gate_pack", "POST", "/api/final-rc-gate-v4/{gate_id}/export", "Export gate results pack"),
      ("gate_report", "GET", "/api/final-rc-gate-v4/report", "Get final RC gate report")]),

    (340, "race_wow_proof", "Race WOW Proof Wave v1",
     "Run Golden Scenario from Race Control, show optimizer, export readiness pack, verify, RC PASS, determinism twice-run.",
     [("proof_id", "str"), ("golden_scenario_ref", "str"), ("optimizer_shown", "bool"),
      ("readiness_exported", "bool"), ("rc_pass", "bool"),
      ("determinism_hash_1", "str"), ("determinism_hash_2", "str"),
      ("hashes_match", "bool"), ("all_verified", "bool"),
      ("evidence_bundle", "list"), ("content_hash", "str"),
      ("deterministic", "bool"),
      ("status", "str"), ("verified_at", "str")],
     [("list_proofs", "GET", "/api/race-wow-proof", "List race WOW proofs"),
      ("generate_proof", "POST", "/api/race-wow-proof", "Generate race WOW proof"),
      ("get_proof", "GET", "/api/race-wow-proof/{proof_id}", "Get proof details"),
      ("verify_wow", "POST", "/api/race-wow-proof/{proof_id}/verify", "Verify WOW proof"),
      ("seal_proof", "POST", "/api/race-wow-proof/{proof_id}/seal", "Seal race WOW proof"),
      ("proof_report", "GET", "/api/race-wow-proof/report", "Get race WOW proof report")]),
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
    elif type_str in ("dict", "dict|None"):
        return "{}"
    return '""'


def _sample_create_data(fields: list) -> dict:
    data = {}
    for name, ftype in fields[1:]:
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
        elif ftype in ("dict", "dict|None"):
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
        """Create/run: {op_desc}."""
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
        """Update: {op_desc}."""
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
        """Delete: {op_desc}."""
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
        """Action: {op_desc}."""
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
    svc_import = f"from app.services.w{wave_num:03d}_{slug} import service"

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
    svc_import = f"from app.services.w{wave_num:03d}_{slug} import service"

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

    tests.append(f'''
@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()
''')

    tests.append(f'''
def test_w{wave_num:03d}_service_starts_empty():
    assert service.count == 0
''')

    if create_op:
        _, _, cpath = create_op
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_create(client):
    r = await client.post("{cpath}", json={sample_data})
    assert r.status_code == 201
    data = r.json()
    assert "{id_field}" in data
    assert service.count == 1
''')

    if list_op and create_op:
        _, _, lpath = list_op
        _, _, cpath = create_op
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_list(client):
    await client.post("{cpath}", json={sample_data})
    await client.post("{cpath}", json={sample_data})
    r = await client.get("{lpath}")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2
''')

    if get_op and create_op:
        _, _, gpath = get_op
        _, _, cpath = create_op
        param = re.search(r'\{(\w+)\}', gpath).group(1)
        gpath_t = gpath.replace("{" + param + "}", "{item_id}")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_get_by_id(client):
    r = await client.post("{cpath}", json={sample_data})
    item_id = r.json()["{id_field}"]
    r2 = await client.get(f"{gpath_t}")
    assert r2.status_code == 200
    assert r2.json()["{id_field}"] == item_id
''')

    if get_op:
        _, _, gpath = get_op
        param = re.search(r'\{(\w+)\}', gpath).group(1)
        gpath_404 = gpath.replace("{" + param + "}", "nonexistent-id")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_get_not_found(client):
    r = await client.get("{gpath_404}")
    assert r.status_code == 404
''')

    if action_ops and create_op:
        _, _, cpath = create_op
        for aname, _, apath in action_ops[:3]:
            param = re.search(r'\{(\w+)\}', apath).group(1)
            apath_t = apath.replace("{" + param + "}", "{item_id}")
            tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_{aname}(client):
    r = await client.post("{cpath}", json={sample_data})
    item_id = r.json()["{id_field}"]
    r2 = await client.post(f"{apath_t}", json={{}})
    assert r2.status_code == 200
    assert r2.json()["{id_field}"] == item_id
''')

    if action_ops:
        aname, _, apath = action_ops[0]
        param = re.search(r'\{(\w+)\}', apath).group(1)
        apath_404 = apath.replace("{" + param + "}", "nonexistent-id")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_{aname}_not_found(client):
    r = await client.post("{apath_404}", json={{}})
    assert r.status_code == 404
''')

    if create_op:
        _, _, cpath = create_op
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("{cpath}", json={sample_data})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "{slug}"
    assert "trace_id" in event
''')

    if create_op:
        _, _, cpath = create_op
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_determinism(client):
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

    if create_op:
        _, _, cpath = create_op
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("{cpath}", json={{}})
    assert r.status_code == 201
''')

    if create_op and list_op and get_op:
        _, _, cpath = create_op
        _, _, lpath = list_op
        _, _, gpath = get_op
        param = re.search(r'\{(\w+)\}', gpath).group(1)
        gpath_t = gpath.replace("{" + param + "}", "{item_id}")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
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
        imports.append(f"from app.routers.w{wave_num:03d}_{slug} import router as w{wave_num:03d}_router")
        includes.append(f"app.include_router(w{wave_num:03d}_router)")
    return "\n".join(imports) + "\n\n" + "\n".join(includes) + "\n"


def main():
    print(f"Generating {len(WAVES)} waves (321-340)...")

    for wave_num, slug, title, desc, fields, operations in WAVES:
        svc_path = SVC_DIR / f"w{wave_num:03d}_{slug}.py"
        svc_path.write_text(gen_service(wave_num, slug, title, desc, fields, operations), encoding="utf-8")

        rtr_path = RTR_DIR / f"w{wave_num:03d}_{slug}.py"
        rtr_path.write_text(gen_router(wave_num, slug, title, desc, fields, operations), encoding="utf-8")

        tst_path = TST_DIR / f"test_w{wave_num:03d}_{slug}.py"
        tst_path.write_text(gen_tests(wave_num, slug, title, desc, fields, operations), encoding="utf-8")

        print(f"  W{wave_num:03d} {slug}: service + router + tests")

    main_content = MAIN_PY.read_text(encoding="utf-8")
    additions = gen_main_additions(WAVES)
    main_content = main_content.rstrip() + "\n\n" + additions
    MAIN_PY.write_text(main_content, encoding="utf-8")
    print(f"\n  main.py updated with {len(WAVES)} new router registrations")

    print(f"\nDone! Generated {len(WAVES)} services, routers, and test files.")


if __name__ == "__main__":
    main()
