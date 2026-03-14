#!/usr/bin/env python3
"""Generate LedgerLive Waves 201-220: Phases 20-22.

Phase 20 (201-208): Live parity + resilience
Phase 21 (209-214): Close Replay + Time Travel Audit
Phase 22 (215-220): ML impact + hackpack automation

Run: python tools/gen_waves_201_220.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SVC_DIR = ROOT / "apps" / "api" / "app" / "services"
RTR_DIR = ROOT / "apps" / "api" / "app" / "routers"
TST_DIR = ROOT / "apps" / "api" / "tests"
MAIN_PY = ROOT / "apps" / "api" / "app" / "main.py"

# ── Wave Definitions ─────────────────────────────────────────────────
# (wave_num, slug, title, desc, fields, operations)
WAVES = [
    # ════════════════════════════════════════════════════════════════
    # PHASE 20: LIVE PARITY + RESILIENCE (W201-W208)
    # ════════════════════════════════════════════════════════════════
    (201, "parity_harness", "Provider Parity Harness v1",
     "Runs canonical close session script through simulator, gemini shim, and airia shim. Outputs parity_report with tool plan, trace, binder, board pack, dossier hashes.",
     [("parity_id", "str"), ("provider_name", "str"), ("session_script", "str"),
      ("tool_plan_hash", "str|None"), ("tool_trace_hash", "str|None"),
      ("binder_hash", "str|None"), ("board_pack_hash", "str|None"),
      ("dossier_count", "int"), ("dossier_hash", "str|None"),
      ("parity_result", "str"), ("mismatches", "list"),
      ("status", "str"), ("executed_at", "str")],
     [("list_parity", "GET", "/api/parity-harness", "List parity harness runs"),
      ("run_parity", "POST", "/api/parity-harness", "Run parity harness against provider shim"),
      ("get_parity", "GET", "/api/parity-harness/{parity_id}", "Get parity run details"),
      ("compare_providers", "POST", "/api/parity-harness/{parity_id}/compare", "Compare provider outputs"),
      ("verify_hashes", "POST", "/api/parity-harness/{parity_id}/verify", "Verify all hashes match"),
      ("parity_report", "GET", "/api/parity-harness/report", "Get parity report")]),

    (202, "live_reconnect", "Live Reconnect Buffering Resume v2",
     "Session buffering with deterministic replay of streamed events. Resume token model prevents duplicated tool calls on reconnect. Protocol schema versioning.",
     [("reconnect_id", "str"), ("session_id", "str"), ("resume_token", "str"),
      ("buffer_size", "int"), ("events_buffered", "list"),
      ("reconnect_count", "int"), ("duplicate_calls_prevented", "int"),
      ("protocol_version", "str"), ("schema_valid", "bool"),
      ("final_hash", "str|None"), ("status", "str"),
      ("created_at", "str")],
     [("list_reconnects", "GET", "/api/live-reconnect", "List reconnect records"),
      ("create_reconnect", "POST", "/api/live-reconnect", "Create reconnect session"),
      ("get_reconnect", "GET", "/api/live-reconnect/{reconnect_id}", "Get reconnect details"),
      ("buffer_event", "POST", "/api/live-reconnect/{reconnect_id}/buffer", "Buffer a streamed event"),
      ("resume_session", "POST", "/api/live-reconnect/{reconnect_id}/resume", "Resume session from token"),
      ("validate_protocol", "POST", "/api/live-reconnect/{reconnect_id}/validate", "Validate protocol schema"),
      ("reconnect_report", "GET", "/api/live-reconnect/report", "Get reconnect report")]),

    (203, "exactly_once", "Exactly-Once Tool Effects v2",
     "Every tool call requires idempotency_key. Executor enforces exactly-once. Side effect ledger per close_period for verification.",
     [("effect_id", "str"), ("tool_name", "str"), ("idempotency_key", "str"),
      ("close_period_id", "str"), ("mutation_count", "int"),
      ("duplicate_attempts", "int"), ("side_effect_ledger", "list"),
      ("ledger_hash", "str|None"), ("exactly_once_verified", "bool"),
      ("status", "str"), ("verified_at", "str")],
     [("list_effects", "GET", "/api/exactly-once", "List tool effect records"),
      ("record_effect", "POST", "/api/exactly-once", "Record tool effect with idempotency key"),
      ("get_effect", "GET", "/api/exactly-once/{effect_id}", "Get effect details"),
      ("verify_once", "POST", "/api/exactly-once/{effect_id}/verify", "Verify exactly-once enforcement"),
      ("hammer_test", "POST", "/api/exactly-once/{effect_id}/hammer", "Hammer test same key multiple times"),
      ("effect_report", "GET", "/api/exactly-once/report", "Get exactly-once report")]),

    (204, "adversarial_corpus", "Agent Policy Adversarial Corpus v1",
     "Adversarial prompt corpus and tool misuse scenarios: bypass approvals, export without dossier, change locked periods. Policy engine blocks with deterministic reasons.",
     [("corpus_id", "str"), ("scenario_name", "str"), ("attack_type", "str"),
      ("prompt_text", "str"), ("tool_call_attempted", "str"),
      ("policy_result", "str"), ("blocked", "bool"),
      ("deny_reason", "str|None"), ("audit_deny_logged", "bool"),
      ("deterministic", "bool"), ("status", "str"),
      ("tested_at", "str")],
     [("list_corpus", "GET", "/api/adversarial-corpus", "List adversarial corpus scenarios"),
      ("add_scenario", "POST", "/api/adversarial-corpus", "Add adversarial scenario"),
      ("get_scenario", "GET", "/api/adversarial-corpus/{corpus_id}", "Get scenario details"),
      ("run_scenario", "POST", "/api/adversarial-corpus/{corpus_id}/run", "Run adversarial scenario"),
      ("verify_blocked", "POST", "/api/adversarial-corpus/{corpus_id}/verify", "Verify scenario was blocked"),
      ("corpus_report", "GET", "/api/adversarial-corpus/report", "Get adversarial corpus report")]),

    (205, "smoke_recorder", "Deployed Smoke Recorder v1",
     "Smoke scripts record deploy evidence pack: timestamps, endpoints, smoke_report, screenshots. Never in CI. Offline validators for format and schema.",
     [("recorder_id", "str"), ("deploy_target", "str"), ("evidence_pack", "dict"),
      ("timestamps", "list"), ("endpoints_checked", "list"),
      ("smoke_report", "dict"), ("screenshots_ref", "list"),
      ("pack_hash", "str|None"), ("schema_valid", "bool"),
      ("status", "str"), ("recorded_at", "str")],
     [("list_recordings", "GET", "/api/smoke-recorder", "List smoke recordings"),
      ("create_recording", "POST", "/api/smoke-recorder", "Create smoke recording"),
      ("get_recording", "GET", "/api/smoke-recorder/{recorder_id}", "Get recording details"),
      ("validate_pack", "POST", "/api/smoke-recorder/{recorder_id}/validate", "Validate evidence pack format"),
      ("validate_schema", "POST", "/api/smoke-recorder/{recorder_id}/schema", "Validate smoke report schema"),
      ("recorder_report", "GET", "/api/smoke-recorder/report", "Get smoke recorder report")]),

    (206, "transcript_export", "Transcript Tool Trace Exporter v1",
     "Session transcript pack: transcript.jsonl, tool_trace.jsonl, verifier_results.json, checksums, signature. Deterministic ordering and stable hashes.",
     [("export_id", "str"), ("session_id", "str"), ("transcript_lines", "int"),
      ("tool_trace_lines", "int"), ("verifier_results_count", "int"),
      ("checksums", "dict"), ("signature", "str|None"),
      ("content_hash", "str|None"), ("ordering_stable", "bool"),
      ("status", "str"), ("exported_at", "str")],
     [("list_exports", "GET", "/api/transcript-export", "List transcript exports"),
      ("create_export", "POST", "/api/transcript-export", "Create transcript export"),
      ("get_export", "GET", "/api/transcript-export/{export_id}", "Get export details"),
      ("verify_checksums", "POST", "/api/transcript-export/{export_id}/verify", "Verify checksums and signature"),
      ("download_pack", "POST", "/api/transcript-export/{export_id}/download", "Download transcript pack"),
      ("export_report", "GET", "/api/transcript-export/report", "Get transcript export report")]),

    (207, "multi_tenant", "Multi-Tenant Live Sessions v1",
     "Live sessions scoped to tenant/workspace. Auth/RBAC enforced. Cross-tenant access to artifacts and tool traces prevented.",
     [("tenant_id", "str"), ("workspace_id", "str"), ("session_id", "str"),
      ("owner_role", "str"), ("access_policy", "dict"),
      ("isolation_verified", "bool"), ("cross_tenant_blocked", "bool"),
      ("blocked_attempts", "list"), ("rbac_result", "str"),
      ("status", "str"), ("created_at", "str")],
     [("list_tenants", "GET", "/api/multi-tenant", "List tenant session configs"),
      ("create_tenant", "POST", "/api/multi-tenant", "Create tenant session config"),
      ("get_tenant", "GET", "/api/multi-tenant/{tenant_id}", "Get tenant details"),
      ("verify_isolation", "POST", "/api/multi-tenant/{tenant_id}/verify", "Verify tenant isolation"),
      ("test_cross_access", "POST", "/api/multi-tenant/{tenant_id}/cross-access", "Test cross-tenant access blocked"),
      ("tenant_report", "GET", "/api/multi-tenant/report", "Get multi-tenant report")]),

    (208, "fail_closed", "Fail-Closed Posture v1",
     "If verifier cannot prove invariants or evidence missing, action becomes approval required or blocked. Never auto-approve under uncertainty.",
     [("posture_id", "str"), ("action_type", "str"), ("verifier_result", "str"),
      ("evidence_present", "bool"), ("invariants_proven", "bool"),
      ("fail_closed_triggered", "bool"), ("approval_required", "bool"),
      ("blocked", "bool"), ("reason", "str|None"),
      ("fallback_decision", "str"), ("status", "str"),
      ("evaluated_at", "str")],
     [("list_postures", "GET", "/api/fail-closed", "List fail-closed evaluations"),
      ("evaluate_posture", "POST", "/api/fail-closed", "Evaluate fail-closed posture"),
      ("get_posture", "GET", "/api/fail-closed/{posture_id}", "Get posture details"),
      ("trigger_fail_closed", "POST", "/api/fail-closed/{posture_id}/trigger", "Trigger fail-closed scenario"),
      ("verify_blocked", "POST", "/api/fail-closed/{posture_id}/verify", "Verify action was blocked"),
      ("posture_report", "GET", "/api/fail-closed/report", "Get fail-closed posture report")]),

    # ════════════════════════════════════════════════════════════════
    # PHASE 21: CLOSE REPLAY + TIME TRAVEL AUDIT (W209-W214)
    # ════════════════════════════════════════════════════════════════
    (209, "run_artifact_store", "Run Artifact Store v2",
     "Canonical replay artifacts for each close run: doc hashes, OCR text hashes, extraction outputs, transactions snapshot, tool plan, tool trace, approvals. Content-addressed.",
     [("artifact_id", "str"), ("close_period_id", "str"), ("artifact_type", "str"),
      ("content_address", "str"), ("version", "int"),
      ("doc_hashes", "list"), ("ocr_hashes", "list"),
      ("extraction_outputs", "dict"), ("transactions_snapshot", "dict"),
      ("tool_plan_ref", "str|None"), ("tool_trace_ref", "str|None"),
      ("approvals_snapshot", "list"), ("manifest_hash", "str|None"),
      ("status", "str"), ("stored_at", "str")],
     [("list_artifacts", "GET", "/api/run-artifacts", "List run artifacts"),
      ("store_artifact", "POST", "/api/run-artifacts", "Store canonical replay artifact"),
      ("get_artifact", "GET", "/api/run-artifacts/{artifact_id}", "Get artifact details"),
      ("verify_manifest", "POST", "/api/run-artifacts/{artifact_id}/verify", "Verify artifact manifest hash"),
      ("restore_snapshot", "POST", "/api/run-artifacts/{artifact_id}/restore", "Restore snapshot from artifact"),
      ("artifact_report", "GET", "/api/run-artifacts/report", "Get artifact store report")]),

    (210, "replay_engine", "Replay Engine v1",
     "Replay close run from artifacts: re-run recon, triage, approvals simulation in sandbox. Output replay_report with step hashes. Deterministic replay.",
     [("replay_id", "str"), ("close_period_id", "str"), ("artifact_id", "str"),
      ("replay_steps", "list"), ("current_step", "int"),
      ("total_steps", "int"), ("step_hashes", "dict"),
      ("binder_hash", "str|None"), ("dossier_hash", "str|None"),
      ("replay_result", "str"), ("failure_reason", "str|None"),
      ("status", "str"), ("replayed_at", "str")],
     [("list_replays", "GET", "/api/replay-engine", "List replay runs"),
      ("start_replay", "POST", "/api/replay-engine", "Start replay from artifacts"),
      ("get_replay", "GET", "/api/replay-engine/{replay_id}", "Get replay details"),
      ("advance_step", "POST", "/api/replay-engine/{replay_id}/advance", "Advance replay step"),
      ("verify_replay", "POST", "/api/replay-engine/{replay_id}/verify", "Verify replay hashes match original"),
      ("replay_report", "GET", "/api/replay-engine/report", "Get replay engine report")]),

    (211, "replay_viewer", "Replay Viewer UI v1",
     "UI page Replay: timeline of steps, tool trace rows linked to dossiers, evidence span viewer. Fully data-testid instrumented.",
     [("viewer_id", "str"), ("replay_id", "str"), ("timeline_steps", "list"),
      ("tool_trace_rows", "list"), ("dossier_links", "list"),
      ("evidence_spans", "list"), ("current_step_index", "int"),
      ("page_testid", "str"), ("highlight_active", "bool"),
      ("status", "str"), ("opened_at", "str")],
     [("list_viewers", "GET", "/api/replay-viewer", "List replay viewer states"),
      ("create_viewer", "POST", "/api/replay-viewer", "Create replay viewer session"),
      ("get_viewer", "GET", "/api/replay-viewer/{viewer_id}", "Get viewer state"),
      ("step_forward", "POST", "/api/replay-viewer/{viewer_id}/step", "Step forward in timeline"),
      ("open_dossier", "POST", "/api/replay-viewer/{viewer_id}/dossier", "Open linked dossier"),
      ("highlight_evidence", "POST", "/api/replay-viewer/{viewer_id}/highlight", "Highlight evidence span"),
      ("viewer_report", "GET", "/api/replay-viewer/report", "Get replay viewer report")]),

    (212, "binder_regen", "Binder Regeneration From Replay",
     "Regenerate binder and board pack from replay artifacts. Must be byte-identical to original exports. Hard gate on hash equality.",
     [("regen_id", "str"), ("replay_id", "str"), ("original_binder_hash", "str"),
      ("regen_binder_hash", "str|None"), ("original_board_hash", "str"),
      ("regen_board_hash", "str|None"), ("byte_identical", "bool"),
      ("hash_match", "bool"), ("gate_result", "str"),
      ("status", "str"), ("regenerated_at", "str")],
     [("list_regens", "GET", "/api/binder-regen", "List binder regenerations"),
      ("regenerate", "POST", "/api/binder-regen", "Regenerate binder from replay"),
      ("get_regen", "GET", "/api/binder-regen/{regen_id}", "Get regeneration details"),
      ("verify_identity", "POST", "/api/binder-regen/{regen_id}/verify", "Verify byte-identical match"),
      ("compare_hashes", "POST", "/api/binder-regen/{regen_id}/compare", "Compare original vs regen hashes"),
      ("regen_report", "GET", "/api/binder-regen/report", "Get binder regeneration report")]),

    (213, "regression_harness", "Replay Regression Harness v1",
     "Replays N canonical runs and compares tool plan hash, binder hash, dossier hashes. Fails on drift unless baseline update approved.",
     [("harness_id", "str"), ("run_count", "int"), ("canonical_runs", "list"),
      ("tool_plan_diffs", "list"), ("binder_diffs", "list"),
      ("dossier_diffs", "list"), ("drift_detected", "bool"),
      ("baseline_approved", "bool"), ("diff_report_hash", "str|None"),
      ("status", "str"), ("executed_at", "str")],
     [("list_harnesses", "GET", "/api/regression-harness", "List regression harness runs"),
      ("run_harness", "POST", "/api/regression-harness", "Run regression harness"),
      ("get_harness", "GET", "/api/regression-harness/{harness_id}", "Get harness run details"),
      ("approve_baseline", "POST", "/api/regression-harness/{harness_id}/approve", "Approve baseline update"),
      ("detect_drift", "POST", "/api/regression-harness/{harness_id}/drift", "Detect drift in canonical runs"),
      ("harness_report", "GET", "/api/regression-harness/report", "Get regression harness report")]),

    (214, "court_pack", "Audit Court Mode Export v1",
     "Single zip: original binder+sig, replay binder+sig, parity report, transcript pack, explanation graph, audit integrity proof. VERIFY script validates offline.",
     [("pack_id", "str"), ("close_period_id", "str"), ("original_binder_ref", "str"),
      ("replay_binder_ref", "str"), ("parity_report_ref", "str"),
      ("transcript_pack_ref", "str"), ("explanation_graph_ref", "str"),
      ("integrity_proof_ref", "str"), ("verify_script_included", "bool"),
      ("all_checksums_valid", "bool"), ("content_hash", "str|None"),
      ("status", "str"), ("exported_at", "str")],
     [("list_packs", "GET", "/api/court-pack", "List court mode export packs"),
      ("generate_pack", "POST", "/api/court-pack", "Generate court mode export pack"),
      ("get_pack", "GET", "/api/court-pack/{pack_id}", "Get pack details"),
      ("verify_pack", "POST", "/api/court-pack/{pack_id}/verify", "Verify all checksums and signatures"),
      ("download_pack", "POST", "/api/court-pack/{pack_id}/download", "Download court pack"),
      ("pack_report", "GET", "/api/court-pack/report", "Get court pack report")]),

    # ════════════════════════════════════════════════════════════════
    # PHASE 22: ML IMPACT + HACKPACK AUTOMATION (W215-W220)
    # ════════════════════════════════════════════════════════════════
    (215, "model_impact", "Model Impact Dashboard v1",
     "Compare review queue volume reduction, false match reduction, calibration error improvement. Computed on fixture-eval runs deterministically.",
     [("impact_id", "str"), ("model_id", "str"), ("eval_run_id", "str"),
      ("review_queue_baseline", "int"), ("review_queue_with_model", "int"),
      ("volume_reduction_pct", "float"), ("false_match_baseline", "int"),
      ("false_match_with_model", "int"), ("false_match_reduction_pct", "float"),
      ("calibration_error", "float"), ("improvement_pct", "float"),
      ("status", "str"), ("computed_at", "str")],
     [("list_impacts", "GET", "/api/model-impact", "List model impact evaluations"),
      ("compute_impact", "POST", "/api/model-impact", "Compute model impact metrics"),
      ("get_impact", "GET", "/api/model-impact/{impact_id}", "Get impact details"),
      ("compare_baseline", "POST", "/api/model-impact/{impact_id}/compare", "Compare baseline vs model metrics"),
      ("verify_metrics", "POST", "/api/model-impact/{impact_id}/verify", "Verify metrics determinism"),
      ("impact_report", "GET", "/api/model-impact/report", "Get model impact report")]),

    (216, "drift_budgets", "Drift Monitoring Budgets Enforced",
     "Drift snapshot per release: dataset hash, model hash, metrics. Budget enforcement fails if key metrics regress beyond thresholds.",
     [("budget_id", "str"), ("release_tag", "str"), ("dataset_hash", "str"),
      ("model_hash", "str"), ("metrics_snapshot", "dict"),
      ("thresholds", "dict"), ("budget_pass", "bool"),
      ("regression_detected", "bool"), ("regressed_metrics", "list"),
      ("drift_report_hash", "str|None"), ("status", "str"),
      ("evaluated_at", "str")],
     [("list_budgets", "GET", "/api/drift-budgets", "List drift budget evaluations"),
      ("evaluate_budget", "POST", "/api/drift-budgets", "Evaluate drift budget"),
      ("get_budget", "GET", "/api/drift-budgets/{budget_id}", "Get budget details"),
      ("check_regression", "POST", "/api/drift-budgets/{budget_id}/regression", "Check for metric regression"),
      ("enforce_threshold", "POST", "/api/drift-budgets/{budget_id}/enforce", "Enforce budget thresholds"),
      ("budget_report", "GET", "/api/drift-budgets/report", "Get drift budget report")]),

    (217, "gradient_provenance", "Gradient Provenance Capture v1",
     "When Gradient live enabled, capture provenance: job spec hash, artifact hash, endpoint hash. DEMO generates deterministic provenance placeholder.",
     [("provenance_id", "str"), ("job_spec_hash", "str"), ("artifact_hash", "str"),
      ("endpoint_hash", "str"), ("live_mode", "bool"),
      ("placeholder_mode", "bool"), ("provenance_data", "dict"),
      ("schema_valid", "bool"), ("content_hash", "str|None"),
      ("status", "str"), ("captured_at", "str")],
     [("list_provenance", "GET", "/api/gradient-provenance", "List provenance records"),
      ("capture_provenance", "POST", "/api/gradient-provenance", "Capture gradient provenance"),
      ("get_provenance", "GET", "/api/gradient-provenance/{provenance_id}", "Get provenance details"),
      ("validate_provenance", "POST", "/api/gradient-provenance/{provenance_id}/validate", "Validate provenance schema"),
      ("generate_placeholder", "POST", "/api/gradient-provenance/{provenance_id}/placeholder", "Generate DEMO placeholder"),
      ("provenance_report", "GET", "/api/gradient-provenance/report", "Get provenance report")]),

    (218, "arch_diagram", "Auto Architecture Diagram Generator v1",
     "Generate architecture diagram from routers registry, tool registry, workflow DAG, storage components. Output dot/mermaid source deterministically.",
     [("diagram_id", "str"), ("diagram_name", "str"), ("source_format", "str"),
      ("routers_count", "int"), ("tools_count", "int"),
      ("workflow_nodes", "int"), ("storage_components", "list"),
      ("source_content", "str"), ("content_hash", "str|None"),
      ("deterministic", "bool"), ("status", "str"),
      ("generated_at", "str")],
     [("list_diagrams", "GET", "/api/arch-diagrams", "List architecture diagrams"),
      ("generate_diagram", "POST", "/api/arch-diagrams", "Generate architecture diagram"),
      ("get_diagram", "GET", "/api/arch-diagrams/{diagram_id}", "Get diagram details"),
      ("validate_diagram", "POST", "/api/arch-diagrams/{diagram_id}/validate", "Validate diagram source"),
      ("export_diagram", "POST", "/api/arch-diagrams/{diagram_id}/export", "Export diagram artifact"),
      ("diagram_report", "GET", "/api/arch-diagrams/report", "Get diagram generation report")]),

    (219, "checklist_verifier", "Hackathon Checklist Auto-Verifier v1",
     "Checklists for Gemini/Airia/DO/Automation hackathons. make verify-hackathons checks repo artifacts and bundles offline. Deterministic report.",
     [("check_id", "str"), ("hackathon_name", "str"), ("checklist_items", "list"),
      ("items_passed", "int"), ("items_failed", "int"),
      ("items_total", "int"), ("missing_items", "list"),
      ("report_hash", "str|None"), ("deterministic", "bool"),
      ("status", "str"), ("verified_at", "str")],
     [("list_checks", "GET", "/api/checklist-verifier", "List checklist verifications"),
      ("run_check", "POST", "/api/checklist-verifier", "Run hackathon checklist verification"),
      ("get_check", "GET", "/api/checklist-verifier/{check_id}", "Get check details"),
      ("verify_item", "POST", "/api/checklist-verifier/{check_id}/verify", "Verify individual checklist item"),
      ("trigger_failure", "POST", "/api/checklist-verifier/{check_id}/fail", "Trigger missing item failure"),
      ("check_report", "GET", "/api/checklist-verifier/report", "Get checklist verification report")]),

    (220, "submit_all_v3", "Submission Hardening v3",
     "make submit-all outputs gemini/airia/do/automation bundles with index and checksums. TOUR >=240s covering parity, replay, court pack, impact, verifier, submit.",
     [("submission_id", "str"), ("bundle_type", "str"), ("target_hackathon", "str"),
      ("output_path", "str"), ("index_generated", "bool"),
      ("checksums", "dict"), ("signatures", "dict"),
      ("tour_duration_s", "float"), ("determinism_pass", "bool"),
      ("twice_run_hash_1", "str|None"), ("twice_run_hash_2", "str|None"),
      ("status", "str"), ("generated_at", "str")],
     [("list_submissions", "GET", "/api/submit-all-v3", "List submission bundles"),
      ("generate_submission", "POST", "/api/submit-all-v3", "Generate submission bundle"),
      ("get_submission", "GET", "/api/submit-all-v3/{submission_id}", "Get submission details"),
      ("verify_bundle", "POST", "/api/submit-all-v3/{submission_id}/verify", "Verify bundle completeness"),
      ("verify_determinism", "POST", "/api/submit-all-v3/{submission_id}/determinism", "Verify twice-run determinism"),
      ("submission_report", "GET", "/api/submit-all-v3/report", "Get submission hardening report")]),
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
def test_w{wave_num:03d}_service_starts_empty():
    assert service.count == 0
''')

    # create
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

    # list
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

    # get by id
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

    # get 404
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

    # action ops (test first 3)
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

    # action 404
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

    # audit event emitted
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

    # determinism
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

    # break-it: empty body
    if create_op:
        _, _, cpath = create_op
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_break_it_empty_body(client):
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
    print(f"Generating {len(WAVES)} waves (201-220)...")

    for wave_num, slug, title, desc, fields, operations in WAVES:
        svc_path = SVC_DIR / f"w{wave_num:03d}_{slug}.py"
        svc_path.write_text(gen_service(wave_num, slug, title, desc, fields, operations), encoding="utf-8")

        rtr_path = RTR_DIR / f"w{wave_num:03d}_{slug}.py"
        rtr_path.write_text(gen_router(wave_num, slug, title, desc, fields, operations), encoding="utf-8")

        tst_path = TST_DIR / f"test_w{wave_num:03d}_{slug}.py"
        tst_path.write_text(gen_tests(wave_num, slug, title, desc, fields, operations), encoding="utf-8")

        print(f"  W{wave_num:03d} {slug}: service + router + tests")

    # Append router registrations to main.py
    main_content = MAIN_PY.read_text(encoding="utf-8")
    additions = gen_main_additions(WAVES)
    main_content = main_content.rstrip() + "\n\n" + additions
    MAIN_PY.write_text(main_content, encoding="utf-8")
    print(f"\n  main.py updated with {len(WAVES)} new router registrations")

    print(f"\nDone! Generated {len(WAVES)} services, routers, and test files.")


if __name__ == "__main__":
    main()
