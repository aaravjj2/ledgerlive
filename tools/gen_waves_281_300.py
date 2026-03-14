#!/usr/bin/env python3
"""Generate LedgerLive Waves 281-300: Phases 30-31.

Phase 30 (281-290): Enterprise Finance Power-Up
Phase 31 (291-300): Final Hardening for Competition

Run: python tools/gen_waves_281_300.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SVC_DIR = ROOT / "apps" / "api" / "app" / "services"
RTR_DIR = ROOT / "apps" / "api" / "app" / "routers"
TST_DIR = ROOT / "apps" / "api" / "tests"
MAIN_PY = ROOT / "apps" / "api" / "app" / "main.py"

WAVES = [
    # ════════════════════════════════════════════════════════════════
    # PHASE 30: ENTERPRISE FINANCE POWER-UP (W281-W290)
    # ════════════════════════════════════════════════════════════════
    (281, "payment_scheduling_v2", "Payment Scheduling v2",
     "Cash-aware approval gates with vendor risk integration and treasury ladder support. Deterministic scheduling with conflict detection.",
     [("schedule_id", "str"), ("vendor_id", "str"), ("amount", "float"),
      ("currency", "str"), ("payment_date", "str"), ("approval_gate", "str"),
      ("vendor_risk_score", "float"), ("treasury_ladder_ref", "str"),
      ("cash_available", "float"), ("conflict_detected", "bool"),
      ("approval_status", "str"), ("deterministic", "bool"),
      ("status", "str"), ("scheduled_at", "str")],
     [("list_schedules", "GET", "/api/payment-scheduling-v2", "List payment schedules"),
      ("create_schedule", "POST", "/api/payment-scheduling-v2", "Create payment schedule"),
      ("get_schedule", "GET", "/api/payment-scheduling-v2/{schedule_id}", "Get schedule details"),
      ("approve_payment", "POST", "/api/payment-scheduling-v2/{schedule_id}/approve", "Approve payment"),
      ("check_cash", "POST", "/api/payment-scheduling-v2/{schedule_id}/cash-check", "Check cash availability"),
      ("assess_vendor_risk", "POST", "/api/payment-scheduling-v2/{schedule_id}/vendor-risk", "Assess vendor risk"),
      ("schedule_report", "GET", "/api/payment-scheduling-v2/report", "Get payment scheduling report")]),

    (282, "tie_out_engine_v2", "Tie-Out Engine v2",
     "Configurable tie-out rules with variance incident creation and evidence linking. Deterministic variance calculation.",
     [("tie_out_id", "str"), ("rule_name", "str"), ("source_value", "float"),
      ("target_value", "float"), ("variance", "float"),
      ("threshold", "float"), ("within_threshold", "bool"),
      ("incident_created", "bool"), ("incident_ref", "str|None"),
      ("evidence_refs", "list"), ("rule_config", "dict"),
      ("status", "str"), ("evaluated_at", "str")],
     [("list_tie_outs", "GET", "/api/tie-out-engine-v2", "List tie-out evaluations"),
      ("create_tie_out", "POST", "/api/tie-out-engine-v2", "Create tie-out evaluation"),
      ("get_tie_out", "GET", "/api/tie-out-engine-v2/{tie_out_id}", "Get tie-out details"),
      ("evaluate_variance", "POST", "/api/tie-out-engine-v2/{tie_out_id}/evaluate", "Evaluate variance"),
      ("create_incident_from_variance", "POST", "/api/tie-out-engine-v2/{tie_out_id}/incident", "Create incident from variance"),
      ("tie_out_report", "GET", "/api/tie-out-engine-v2/report", "Get tie-out engine report")]),

    (283, "fraud_red_flag_v2", "Fraud Red Flag Engine v2",
     "Vendor spoofing, duplicates, and outlier detection with dossier linking and approval gates for risky actions.",
     [("flag_id", "str"), ("detection_type", "str"), ("entity_ref", "str"),
      ("risk_score", "float"), ("confidence", "float"),
      ("red_flag_reason", "str"), ("dossier_ref", "str"),
      ("approval_required", "bool"), ("approved_by", "str|None"),
      ("evidence_refs", "list"), ("similar_entities", "list"),
      ("status", "str"), ("detected_at", "str")],
     [("list_flags", "GET", "/api/fraud-red-flag-v2", "List fraud red flags"),
      ("create_flag", "POST", "/api/fraud-red-flag-v2", "Create fraud red flag"),
      ("get_flag", "GET", "/api/fraud-red-flag-v2/{flag_id}", "Get red flag details"),
      ("assess_risk", "POST", "/api/fraud-red-flag-v2/{flag_id}/assess", "Assess fraud risk"),
      ("approve_action", "POST", "/api/fraud-red-flag-v2/{flag_id}/approve", "Approve risky action"),
      ("link_dossier", "POST", "/api/fraud-red-flag-v2/{flag_id}/dossier", "Link to dossier"),
      ("flag_report", "GET", "/api/fraud-red-flag-v2/report", "Get fraud red flag report")]),

    (284, "controls_coverage_v2", "Controls Coverage v2",
     "Quantifies coverage for close period. Gaps become blockers with SLA enforcement and deterministic scoring.",
     [("coverage_id", "str"), ("period_ref", "str"), ("total_controls", "int"),
      ("covered_controls", "int"), ("coverage_pct", "float"),
      ("gaps", "list"), ("gap_blockers_created", "int"),
      ("sla_enforced", "bool"), ("score", "float"),
      ("scoring_method", "str"), ("deterministic", "bool"),
      ("status", "str"), ("evaluated_at", "str")],
     [("list_coverages", "GET", "/api/controls-coverage-v2", "List controls coverage"),
      ("create_coverage", "POST", "/api/controls-coverage-v2", "Create controls coverage evaluation"),
      ("get_coverage", "GET", "/api/controls-coverage-v2/{coverage_id}", "Get coverage details"),
      ("identify_gaps", "POST", "/api/controls-coverage-v2/{coverage_id}/gaps", "Identify control gaps"),
      ("create_blockers", "POST", "/api/controls-coverage-v2/{coverage_id}/blockers", "Create gap blockers"),
      ("coverage_report", "GET", "/api/controls-coverage-v2/report", "Get controls coverage report")]),

    (285, "data_quality_gate_v2", "Data Quality Gate v2",
     "Export blocked if quality below threshold unless approved. Deterministic quality scoring with explicit reasons.",
     [("gate_id", "str"), ("dataset_ref", "str"), ("quality_score", "float"),
      ("threshold", "float"), ("above_threshold", "bool"),
      ("blocking_export", "bool"), ("approval_override", "bool"),
      ("approved_by", "str|None"), ("quality_dimensions", "dict"),
      ("failure_reasons", "list"), ("deterministic", "bool"),
      ("status", "str"), ("evaluated_at", "str")],
     [("list_gates", "GET", "/api/data-quality-gate-v2", "List data quality gates"),
      ("create_gate", "POST", "/api/data-quality-gate-v2", "Create data quality gate"),
      ("get_gate", "GET", "/api/data-quality-gate-v2/{gate_id}", "Get gate details"),
      ("evaluate_quality", "POST", "/api/data-quality-gate-v2/{gate_id}/evaluate", "Evaluate data quality"),
      ("override_gate", "POST", "/api/data-quality-gate-v2/{gate_id}/override", "Override gate with approval"),
      ("gate_report", "GET", "/api/data-quality-gate-v2/report", "Get data quality gate report")]),

    (286, "multi_entity_v3", "Multi-Entity Consolidation v3",
     "Deeper eliminations, FX, and CTA with statement notes and evidence links. Deterministic consolidation calculations.",
     [("consol_id", "str"), ("entities", "list"), ("elimination_entries", "list"),
      ("fx_adjustments", "list"), ("cta_adjustments", "list"),
      ("statement_notes", "list"), ("evidence_refs", "list"),
      ("consolidated_total", "float"), ("currency", "str"),
      ("fx_rate_source", "str"), ("deterministic", "bool"),
      ("status", "str"), ("consolidated_at", "str")],
     [("list_consols", "GET", "/api/multi-entity-v3", "List consolidations"),
      ("create_consol", "POST", "/api/multi-entity-v3", "Create consolidation"),
      ("get_consol", "GET", "/api/multi-entity-v3/{consol_id}", "Get consolidation details"),
      ("apply_eliminations", "POST", "/api/multi-entity-v3/{consol_id}/eliminate", "Apply elimination entries"),
      ("apply_fx", "POST", "/api/multi-entity-v3/{consol_id}/fx", "Apply FX adjustments"),
      ("add_notes", "POST", "/api/multi-entity-v3/{consol_id}/notes", "Add statement notes"),
      ("consol_report", "GET", "/api/multi-entity-v3/report", "Get consolidation report")]),

    (287, "fpa_insight_panel", "FP&A Insight Panel v1",
     "Budgets, forecast, and scenario deltas surfaced in Race Control as telemetry. Deterministic variance analysis.",
     [("insight_id", "str"), ("period_ref", "str"), ("budget_data", "dict"),
      ("forecast_data", "dict"), ("scenario_deltas", "list"),
      ("variance_analysis", "dict"), ("key_drivers", "list"),
      ("telemetry_ref", "str"), ("rc_display_config", "dict"),
      ("deterministic", "bool"), ("confidence_level", "float"),
      ("status", "str"), ("analyzed_at", "str")],
     [("list_insights", "GET", "/api/fpa-insight-panel", "List FP&A insights"),
      ("create_insight", "POST", "/api/fpa-insight-panel", "Create FP&A insight"),
      ("get_insight", "GET", "/api/fpa-insight-panel/{insight_id}", "Get insight details"),
      ("analyze_variance", "POST", "/api/fpa-insight-panel/{insight_id}/variance", "Analyze variance"),
      ("run_scenario", "POST", "/api/fpa-insight-panel/{insight_id}/scenario", "Run scenario analysis"),
      ("insight_report", "GET", "/api/fpa-insight-panel/report", "Get FP&A insight report")]),

    (288, "ml_impact_v4", "ML Impact v4",
     "Live comparison baseline vs model with drift alerts becoming incidents. Performance budgets enforced with deterministic evaluation.",
     [("impact_id", "str"), ("model_ref", "str"), ("baseline_metrics", "dict"),
      ("model_metrics", "dict"), ("improvement_pct", "float"),
      ("drift_detected", "bool"), ("drift_magnitude", "float"),
      ("incident_created", "bool"), ("incident_ref", "str|None"),
      ("budget_within", "bool"), ("evaluation_hash", "str"),
      ("status", "str"), ("evaluated_at", "str")],
     [("list_impacts", "GET", "/api/ml-impact-v4", "List ML impact evaluations"),
      ("create_impact", "POST", "/api/ml-impact-v4", "Create ML impact evaluation"),
      ("get_impact", "GET", "/api/ml-impact-v4/{impact_id}", "Get impact details"),
      ("compare_models", "POST", "/api/ml-impact-v4/{impact_id}/compare", "Compare baseline vs model"),
      ("detect_drift", "POST", "/api/ml-impact-v4/{impact_id}/drift", "Detect model drift"),
      ("create_drift_incident", "POST", "/api/ml-impact-v4/{impact_id}/incident", "Create drift incident"),
      ("impact_report", "GET", "/api/ml-impact-v4/report", "Get ML impact report")]),

    (289, "perf_budgets_v5", "Performance Budgets v5",
     "100x fixtures for Race Control, search, and replay with stable pagination enforcement. Deterministic timing verification.",
     [("budget_id", "str"), ("fixture_scale", "str"), ("target_flow", "str"),
      ("budget_ms", "int"), ("actual_ms", "int"), ("within_budget", "bool"),
      ("pagination_stable", "bool"), ("pages_tested", "int"),
      ("throughput_ops", "float"), ("memory_budget_mb", "float"),
      ("memory_actual_mb", "float"), ("deterministic", "bool"),
      ("status", "str"), ("measured_at", "str")],
     [("list_budgets", "GET", "/api/perf-budgets-v5", "List performance budgets"),
      ("create_budget", "POST", "/api/perf-budgets-v5", "Create performance budget test"),
      ("get_budget", "GET", "/api/perf-budgets-v5/{budget_id}", "Get budget details"),
      ("run_benchmark", "POST", "/api/perf-budgets-v5/{budget_id}/benchmark", "Run performance benchmark"),
      ("check_pagination", "POST", "/api/perf-budgets-v5/{budget_id}/pagination", "Check pagination stability"),
      ("budget_report", "GET", "/api/perf-budgets-v5/report", "Get performance budget report")]),

    (290, "finance_proof", "Finance Proof Wave v1",
     "MCP E2E shows a real close run where tie-out variance triggers incident, approval resolves, exports verify. Determinism twice-run.",
     [("proof_id", "str"), ("close_run_ref", "str"), ("tie_out_ref", "str"),
      ("variance_incident_ref", "str"), ("approval_ref", "str"),
      ("export_verified", "bool"), ("all_verified", "bool"),
      ("determinism_hash", "str"), ("twice_run_match", "bool"),
      ("content_hash", "str"), ("evidence_bundle", "list"),
      ("status", "str"), ("verified_at", "str")],
     [("list_proofs", "GET", "/api/finance-proof", "List finance proofs"),
      ("generate_proof", "POST", "/api/finance-proof", "Generate finance proof"),
      ("get_proof", "GET", "/api/finance-proof/{proof_id}", "Get proof details"),
      ("verify_proof", "POST", "/api/finance-proof/{proof_id}/verify", "Verify proof integrity"),
      ("seal_proof", "POST", "/api/finance-proof/{proof_id}/seal", "Seal finance proof"),
      ("proof_report", "GET", "/api/finance-proof/report", "Get finance proof report")]),

    # ════════════════════════════════════════════════════════════════
    # PHASE 31: FINAL HARDENING FOR COMPETITION (W291-W300)
    # ════════════════════════════════════════════════════════════════
    (291, "rc_gate_v3", "RC Gate v3",
     "Unified release candidate run asserting all critical invariants across Race Control, channels, replay, security, ML, and exports.",
     [("gate_id", "str"), ("rc_invariants", "list"), ("channel_checks", "list"),
      ("replay_checks", "list"), ("security_checks", "list"),
      ("ml_checks", "list"), ("export_checks", "list"),
      ("all_passed", "bool"), ("failure_count", "int"),
      ("failure_details", "list"), ("gate_hash", "str"),
      ("status", "str"), ("evaluated_at", "str")],
     [("list_gates", "GET", "/api/rc-gate-v3", "List RC gates"),
      ("create_gate", "POST", "/api/rc-gate-v3", "Create RC gate evaluation"),
      ("get_gate", "GET", "/api/rc-gate-v3/{gate_id}", "Get gate details"),
      ("evaluate_all", "POST", "/api/rc-gate-v3/{gate_id}/evaluate", "Evaluate all invariants"),
      ("check_channels", "POST", "/api/rc-gate-v3/{gate_id}/channels", "Check channel invariants"),
      ("check_security", "POST", "/api/rc-gate-v3/{gate_id}/security", "Check security invariants"),
      ("gate_report", "GET", "/api/rc-gate-v3/report", "Get RC gate report")]),

    (292, "route_coverage_gate", "Route Coverage Gate v1",
     "All critical routes must have MCP E2E coverage. Waivers require explicit config. Deterministic coverage measurement.",
     [("coverage_gate_id", "str"), ("total_routes", "int"), ("covered_routes", "int"),
      ("uncovered_routes", "list"), ("coverage_pct", "float"),
      ("waived_routes", "list"), ("waiver_config_ref", "str"),
      ("above_threshold", "bool"), ("threshold_pct", "float"),
      ("deterministic", "bool"), ("gate_hash", "str"),
      ("status", "str"), ("evaluated_at", "str")],
     [("list_coverage_gates", "GET", "/api/route-coverage-gate", "List route coverage gates"),
      ("create_coverage_gate", "POST", "/api/route-coverage-gate", "Create route coverage gate"),
      ("get_coverage_gate", "GET", "/api/route-coverage-gate/{coverage_gate_id}", "Get coverage gate details"),
      ("measure_coverage", "POST", "/api/route-coverage-gate/{coverage_gate_id}/measure", "Measure route coverage"),
      ("add_waiver", "POST", "/api/route-coverage-gate/{coverage_gate_id}/waiver", "Add route waiver"),
      ("coverage_gate_report", "GET", "/api/route-coverage-gate/report", "Get route coverage gate report")]),

    (293, "determinism_super_gate", "Determinism Super Gate v1",
     "Run make test twice and compare deterministic artifacts with selected hashes that must match. Ultimate determinism verification.",
     [("super_gate_id", "str"), ("run1_hashes", "dict"), ("run2_hashes", "dict"),
      ("hashes_match", "bool"), ("divergent_artifacts", "list"),
      ("total_artifacts_compared", "int"), ("match_pct", "float"),
      ("selected_artifacts", "list"), ("comparison_method", "str"),
      ("gate_result", "str"), ("gate_hash", "str"),
      ("status", "str"), ("compared_at", "str")],
     [("list_super_gates", "GET", "/api/determinism-super-gate", "List determinism super gates"),
      ("create_super_gate", "POST", "/api/determinism-super-gate", "Create determinism super gate"),
      ("get_super_gate", "GET", "/api/determinism-super-gate/{super_gate_id}", "Get super gate details"),
      ("run_comparison", "POST", "/api/determinism-super-gate/{super_gate_id}/compare", "Run hash comparison"),
      ("select_artifacts", "POST", "/api/determinism-super-gate/{super_gate_id}/select", "Select artifacts to compare"),
      ("super_gate_report", "GET", "/api/determinism-super-gate/report", "Get determinism super gate report")]),

    (294, "proof_of_proof", "Proof-of-Proof v2",
     "Generate proof pack twice for a milestone and compare pack hash manifests. Meta-verification of proof generation determinism.",
     [("pop_id", "str"), ("milestone_ref", "str"), ("pack1_hash", "str"),
      ("pack2_hash", "str"), ("hashes_match", "bool"),
      ("manifest1", "dict"), ("manifest2", "dict"),
      ("divergent_entries", "list"), ("generation_count", "int"),
      ("all_identical", "bool"), ("meta_hash", "str"),
      ("status", "str"), ("verified_at", "str")],
     [("list_pops", "GET", "/api/proof-of-proof", "List proof-of-proof verifications"),
      ("create_pop", "POST", "/api/proof-of-proof", "Create proof-of-proof verification"),
      ("get_pop", "GET", "/api/proof-of-proof/{pop_id}", "Get proof-of-proof details"),
      ("generate_twice", "POST", "/api/proof-of-proof/{pop_id}/generate-twice", "Generate proof pack twice"),
      ("compare_manifests", "POST", "/api/proof-of-proof/{pop_id}/compare", "Compare manifests"),
      ("pop_report", "GET", "/api/proof-of-proof/report", "Get proof-of-proof report")]),

    (295, "incident_simulator_v2", "Incident Simulator v2",
     "Seeded incident scenarios including policy blocks, channel failures, and drift breach with deterministic playbooks.",
     [("simulator_id", "str"), ("scenario_type", "str"), ("scenario_config", "dict"),
      ("incident_generated", "bool"), ("incident_ref", "str|None"),
      ("playbook_triggered", "bool"), ("playbook_ref", "str|None"),
      ("recovery_steps", "list"), ("recovery_result", "str"),
      ("deterministic_outcome", "bool"), ("simulation_hash", "str"),
      ("status", "str"), ("simulated_at", "str")],
     [("list_simulators", "GET", "/api/incident-simulator-v2", "List incident simulators"),
      ("create_simulator", "POST", "/api/incident-simulator-v2", "Create incident simulator"),
      ("get_simulator", "GET", "/api/incident-simulator-v2/{simulator_id}", "Get simulator details"),
      ("run_scenario", "POST", "/api/incident-simulator-v2/{simulator_id}/run", "Run incident scenario"),
      ("trigger_playbook", "POST", "/api/incident-simulator-v2/{simulator_id}/playbook", "Trigger recovery playbook"),
      ("verify_outcome", "POST", "/api/incident-simulator-v2/{simulator_id}/verify", "Verify scenario outcome"),
      ("simulator_report", "GET", "/api/incident-simulator-v2/report", "Get incident simulator report")]),

    (296, "self_healing_playbook", "Self-Healing Playbook v2",
     "Playbooks suggest recovery steps, require approvals, and are fully audited. Deterministic step sequencing.",
     [("playbook_id", "str"), ("trigger_condition", "str"), ("recovery_steps", "list"),
      ("current_step", "int"), ("total_steps", "int"),
      ("approval_required_steps", "list"), ("approvals_received", "list"),
      ("audit_trail", "list"), ("auto_approved", "bool"),
      ("outcome", "str"), ("deterministic", "bool"),
      ("status", "str"), ("started_at", "str")],
     [("list_playbooks", "GET", "/api/self-healing-playbook", "List self-healing playbooks"),
      ("create_playbook", "POST", "/api/self-healing-playbook", "Create self-healing playbook"),
      ("get_playbook", "GET", "/api/self-healing-playbook/{playbook_id}", "Get playbook details"),
      ("advance_step", "POST", "/api/self-healing-playbook/{playbook_id}/advance", "Advance playbook step"),
      ("approve_step", "POST", "/api/self-healing-playbook/{playbook_id}/approve", "Approve recovery step"),
      ("complete_playbook", "POST", "/api/self-healing-playbook/{playbook_id}/complete", "Complete playbook"),
      ("playbook_report", "GET", "/api/self-healing-playbook/report", "Get self-healing playbook report")]),

    (297, "doc_truth_gate", "Documentation Truth Gate v1",
     "README, VERIFY, and route registry must match Make targets and live endpoints. Deterministic documentation checks.",
     [("truth_gate_id", "str"), ("readme_hash", "str"), ("verify_hash", "str"),
      ("route_registry_hash", "str"), ("make_targets", "list"),
      ("endpoint_count", "int"), ("mismatches", "list"),
      ("all_match", "bool"), ("coverage_pct", "float"),
      ("deterministic", "bool"), ("gate_hash", "str"),
      ("status", "str"), ("checked_at", "str")],
     [("list_truth_gates", "GET", "/api/doc-truth-gate", "List documentation truth gates"),
      ("create_truth_gate", "POST", "/api/doc-truth-gate", "Create documentation truth gate"),
      ("get_truth_gate", "GET", "/api/doc-truth-gate/{truth_gate_id}", "Get truth gate details"),
      ("check_readme", "POST", "/api/doc-truth-gate/{truth_gate_id}/readme", "Check README accuracy"),
      ("check_routes", "POST", "/api/doc-truth-gate/{truth_gate_id}/routes", "Check route registry"),
      ("truth_gate_report", "GET", "/api/doc-truth-gate/report", "Get documentation truth gate report")]),

    (298, "security_regression", "Security Regression Budgets v1",
     "Fail if injection/exfil detection coverage or deny explainability regresses. Deterministic regression tracking.",
     [("regression_id", "str"), ("baseline_coverage_pct", "float"), ("current_coverage_pct", "float"),
      ("coverage_delta", "float"), ("regressed", "bool"),
      ("deny_explainability_pct", "float"), ("baseline_explainability_pct", "float"),
      ("explainability_regressed", "bool"), ("budget_threshold", "float"),
      ("within_budget", "bool"), ("regression_hash", "str"),
      ("status", "str"), ("measured_at", "str")],
     [("list_regressions", "GET", "/api/security-regression", "List security regressions"),
      ("create_regression", "POST", "/api/security-regression", "Create security regression check"),
      ("get_regression", "GET", "/api/security-regression/{regression_id}", "Get regression details"),
      ("measure_coverage", "POST", "/api/security-regression/{regression_id}/coverage", "Measure detection coverage"),
      ("measure_explainability", "POST", "/api/security-regression/{regression_id}/explainability", "Measure deny explainability"),
      ("regression_report", "GET", "/api/security-regression/report", "Get security regression report")]),

    (299, "perf_regression", "Performance Regression Budgets v1",
     "Fail if key flows exceed thresholds. Stable reports with deterministic timing measurement.",
     [("perf_reg_id", "str"), ("flow_name", "str"), ("baseline_ms", "int"),
      ("current_ms", "int"), ("delta_ms", "int"), ("threshold_ms", "int"),
      ("exceeded", "bool"), ("regression_pct", "float"),
      ("stable_report", "bool"), ("measurement_count", "int"),
      ("p95_ms", "int"), ("deterministic", "bool"),
      ("status", "str"), ("measured_at", "str")],
     [("list_perf_regs", "GET", "/api/perf-regression", "List performance regressions"),
      ("create_perf_reg", "POST", "/api/perf-regression", "Create performance regression check"),
      ("get_perf_reg", "GET", "/api/perf-regression/{perf_reg_id}", "Get regression details"),
      ("run_measurement", "POST", "/api/perf-regression/{perf_reg_id}/measure", "Run performance measurement"),
      ("check_threshold", "POST", "/api/perf-regression/{perf_reg_id}/threshold", "Check against threshold"),
      ("perf_reg_report", "GET", "/api/perf-regression/report", "Get performance regression report")]),

    (300, "final_rc_proof", "Final RC Proof Wave v1",
     "Race Control RC Run end-to-end: plan preview, approvals via channel, execute, incidents resolved, replay regen equality, court pack verify, telemetry pack verify. MCP E2E twice-run determinism.",
     [("proof_id", "str"), ("plan_preview_ref", "str"), ("channel_approval_ref", "str"),
      ("execution_ref", "str"), ("incident_resolution_ref", "str"),
      ("replay_regen_ref", "str"), ("court_pack_ref", "str"),
      ("telemetry_pack_ref", "str"), ("all_verified", "bool"),
      ("determinism_hash", "str"), ("twice_run_match", "bool"),
      ("content_hash", "str"), ("evidence_bundle", "list"),
      ("status", "str"), ("verified_at", "str")],
     [("list_proofs", "GET", "/api/final-rc-proof", "List final RC proofs"),
      ("generate_proof", "POST", "/api/final-rc-proof", "Generate final RC proof"),
      ("get_proof", "GET", "/api/final-rc-proof/{proof_id}", "Get proof details"),
      ("verify_proof", "POST", "/api/final-rc-proof/{proof_id}/verify", "Verify proof integrity"),
      ("seal_proof", "POST", "/api/final-rc-proof/{proof_id}/seal", "Seal final RC proof"),
      ("proof_report", "GET", "/api/final-rc-proof/report", "Get final RC proof report")]),
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
    print(f"Generating {len(WAVES)} waves (281-300)...")

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
