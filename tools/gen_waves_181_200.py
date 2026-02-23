#!/usr/bin/env python3
"""Generate LedgerLive Waves 181-200: Phases 17-19.

Phase 17 (181-188): Real implementations behind flags
Phase 18 (189-194): Evidence-first decision dossier
Phase 19 (195-200): Deployment proof + production hygiene

Run: python tools/gen_waves_181_200.py
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
    # PHASE 17: REAL IMPLEMENTATIONS BEHIND FLAGS (W181-W188)
    # ════════════════════════════════════════════════════════════════
    (181, "gemini_live_provider", "Gemini Live Provider v1",
     "Real Gemini Live provider behind ENABLE_GEMINI_LIVE flag. Connect/disconnect, stream transcript, interruption handling, tool calling hooks. DEMO uses simulator only.",
     [("provider_id", "str"), ("provider_name", "str"), ("enabled", "bool"),
      ("has_api_key", "bool"), ("config", "dict"),
      ("connection_status", "str"), ("transcript_events", "list"),
      ("tool_calls_issued", "list"), ("interruption_count", "int"),
      ("validation_result", "str"), ("error_message", "str|None"),
      ("status", "str"), ("created_at", "str")],
     [("list_providers", "GET", "/api/gemini-live", "List Gemini Live provider configs"),
      ("create_provider", "POST", "/api/gemini-live", "Create Gemini Live provider config"),
      ("get_provider", "GET", "/api/gemini-live/{provider_id}", "Get provider details"),
      ("validate_config", "POST", "/api/gemini-live/{provider_id}/validate", "Validate provider config"),
      ("connect_provider", "POST", "/api/gemini-live/{provider_id}/connect", "Connect provider via simulator shim"),
      ("disconnect_provider", "POST", "/api/gemini-live/{provider_id}/disconnect", "Disconnect provider"),
      ("stream_transcript", "GET", "/api/gemini-live/{provider_id}/transcript", "Get transcript events"),
      ("provider_report", "GET", "/api/gemini-live/report", "Get provider report")]),

    (182, "cloudrun_deploy", "Cloud Run Deploy Automation",
     "GCP Cloud Run deploy scripts for Agent Gateway. Smoke script hits healthz, runs simulator session, exports binder. Scripts are manual-only, never CI.",
     [("deploy_id", "str"), ("deploy_target", "str"), ("script_path", "str"),
      ("config", "dict"), ("smoke_report", "dict"),
      ("smoke_report_hash", "str|None"), ("validated", "bool"),
      ("deploy_mode", "str"), ("region", "str"),
      ("status", "str"), ("created_at", "str")],
     [("list_deploys", "GET", "/api/cloudrun-deploy", "List deploy configs"),
      ("create_deploy", "POST", "/api/cloudrun-deploy", "Create deploy config"),
      ("get_deploy", "GET", "/api/cloudrun-deploy/{deploy_id}", "Get deploy details"),
      ("validate_scripts", "POST", "/api/cloudrun-deploy/{deploy_id}/validate", "Validate deploy scripts structure"),
      ("generate_smoke_plan", "POST", "/api/cloudrun-deploy/{deploy_id}/smoke-plan", "Generate smoke test plan"),
      ("validate_smoke_schema", "POST", "/api/cloudrun-deploy/{deploy_id}/smoke-schema", "Validate smoke report schema"),
      ("deploy_report", "GET", "/api/cloudrun-deploy/report", "Get deploy validation report")]),

    (183, "session_resume", "Session Interruption Resume Safety",
     "Idempotent job keys for live tool calls. Session interruption cannot duplicate side effects. Resume endpoint continues from last checkpoint.",
     [("resume_id", "str"), ("session_id", "str"), ("job_id", "str"),
      ("idempotency_key", "str"), ("checkpoint_index", "int"),
      ("total_steps", "int"), ("side_effects_count", "int"),
      ("binder_hash", "str|None"), ("interrupted", "bool"),
      ("resumed_from", "int"), ("final_hash", "str|None"),
      ("status", "str"), ("created_at", "str")],
     [("list_resumes", "GET", "/api/session-resume", "List session resume records"),
      ("create_session_run", "POST", "/api/session-resume", "Start a resumable session run"),
      ("get_resume", "GET", "/api/session-resume/{resume_id}", "Get resume record details"),
      ("interrupt_session", "POST", "/api/session-resume/{resume_id}/interrupt", "Force interrupt session"),
      ("resume_session", "POST", "/api/session-resume/{resume_id}/resume", "Resume session from checkpoint"),
      ("verify_idempotency", "POST", "/api/session-resume/{resume_id}/verify", "Verify no duplicate side effects"),
      ("resume_report", "GET", "/api/session-resume/report", "Get session resume report")]),

    (184, "airia_finalizer", "Airia Package Finalizer v1",
     "Publish-ready Airia community bundle: tool schema, runbooks, persona config, metadata, deterministic file ordering, checksums. Strict validator.",
     [("bundle_id", "str"), ("bundle_name", "str"), ("tool_schemas", "list"),
      ("runbooks", "list"), ("persona_config", "dict"),
      ("metadata", "dict"), ("file_ordering", "list"),
      ("checksums", "dict"), ("content_hash", "str|None"),
      ("validation_errors", "list"), ("status", "str"),
      ("generated_at", "str")],
     [("list_bundles", "GET", "/api/airia-finalizer", "List Airia bundles"),
      ("generate_bundle", "POST", "/api/airia-finalizer", "Generate publish-ready Airia bundle"),
      ("get_bundle", "GET", "/api/airia-finalizer/{bundle_id}", "Get bundle details"),
      ("validate_bundle", "POST", "/api/airia-finalizer/{bundle_id}/validate", "Validate bundle completeness"),
      ("export_bundle", "POST", "/api/airia-finalizer/{bundle_id}/export", "Export bundle artifact"),
      ("bundle_report", "GET", "/api/airia-finalizer/report", "Get bundle generation report")]),

    (185, "gradient_training", "Gradient Training Spec v1",
     "DigitalOcean Gradient training job spec templates, inference deployment specs, config schema, validator. Deterministic plan output with hashes.",
     [("spec_id", "str"), ("spec_name", "str"), ("spec_type", "str"),
      ("training_config", "dict"), ("inference_config", "dict"),
      ("resource_requirements", "dict"), ("plan_output", "dict"),
      ("plan_hash", "str|None"), ("validation_errors", "list"),
      ("status", "str"), ("created_at", "str")],
     [("list_specs", "GET", "/api/gradient-training", "List Gradient training specs"),
      ("create_spec", "POST", "/api/gradient-training", "Create Gradient training spec"),
      ("get_spec", "GET", "/api/gradient-training/{spec_id}", "Get spec details"),
      ("validate_spec", "POST", "/api/gradient-training/{spec_id}/validate", "Validate spec config"),
      ("render_plan", "POST", "/api/gradient-training/{spec_id}/render", "Render deterministic would-run plan"),
      ("spec_report", "GET", "/api/gradient-training/report", "Get training spec report")]),

    (186, "gradient_inference", "Gradient Inference Adapter v1",
     "Inference adapter behind ENABLE_GRADIENT_INFERENCE flag. DEMO uses local frozen artifacts. Safe fallback if live unavailable. Deterministic routing.",
     [("adapter_id", "str"), ("adapter_name", "str"), ("enabled", "bool"),
      ("inference_endpoint", "str"), ("fallback_mode", "bool"),
      ("local_artifact_ref", "str"), ("input_hash", "str|None"),
      ("output_hash", "str|None"), ("confidence", "float"),
      ("routing_decision", "str"), ("fallback_used", "bool"),
      ("status", "str"), ("created_at", "str")],
     [("list_adapters", "GET", "/api/gradient-inference", "List inference adapter configs"),
      ("create_adapter", "POST", "/api/gradient-inference", "Create inference adapter config"),
      ("get_adapter", "GET", "/api/gradient-inference/{adapter_id}", "Get adapter details"),
      ("validate_adapter", "POST", "/api/gradient-inference/{adapter_id}/validate", "Validate adapter config"),
      ("run_inference", "POST", "/api/gradient-inference/{adapter_id}/infer", "Run inference with fallback"),
      ("check_fallback", "POST", "/api/gradient-inference/{adapter_id}/fallback", "Check fallback behavior"),
      ("adapter_report", "GET", "/api/gradient-inference/report", "Get adapter report")]),

    (187, "connector_runbooks", "Connector Runbooks Anti-CI Guard",
     "QBO/Xero/Plaid real-mode runbooks with explicit ENABLE flags and NEVER IN CI guard. Meta-test hard fails if CI env detected with ENABLE flags on.",
     [("runbook_id", "str"), ("provider", "str"), ("enable_flag", "str"),
      ("ci_guard_active", "bool"), ("ci_env_detected", "bool"),
      ("flag_value", "bool"), ("guard_result", "str"),
      ("runbook_content", "str"), ("validation_errors", "list"),
      ("status", "str"), ("checked_at", "str")],
     [("list_runbooks", "GET", "/api/connector-runbooks", "List connector runbooks"),
      ("create_runbook", "POST", "/api/connector-runbooks", "Create connector runbook"),
      ("get_runbook", "GET", "/api/connector-runbooks/{runbook_id}", "Get runbook details"),
      ("check_ci_guard", "POST", "/api/connector-runbooks/{runbook_id}/ci-guard", "Check CI guard status"),
      ("validate_flags", "POST", "/api/connector-runbooks/{runbook_id}/validate", "Validate ENABLE flags"),
      ("runbook_report", "GET", "/api/connector-runbooks/report", "Get runbook validation report")]),

    (188, "audit_seal", "Live-Mode Audit Sealing v1",
     "Extended Merkle audit integrity including tool_trace and live session events. Binder bundles include integrity proof for tool traces. Tamper detection.",
     [("seal_id", "str"), ("scope", "str"), ("merkle_root", "str"),
      ("tool_trace_included", "bool"), ("session_events_included", "bool"),
      ("node_count", "int"), ("integrity_status", "str"),
      ("tamper_detected", "bool"), ("tampered_nodes", "list"),
      ("proof_artifact", "dict"), ("status", "str"),
      ("sealed_at", "str")],
     [("list_seals", "GET", "/api/audit-seal", "List audit seals"),
      ("create_seal", "POST", "/api/audit-seal", "Create audit seal with Merkle proof"),
      ("get_seal", "GET", "/api/audit-seal/{seal_id}", "Get seal details"),
      ("verify_integrity", "POST", "/api/audit-seal/{seal_id}/verify", "Verify Merkle integrity"),
      ("inject_tamper", "POST", "/api/audit-seal/{seal_id}/tamper", "Inject tamper for testing"),
      ("detect_tamper", "POST", "/api/audit-seal/{seal_id}/detect", "Detect tampering"),
      ("seal_report", "GET", "/api/audit-seal/report", "Get audit seal report")]),

    # ════════════════════════════════════════════════════════════════
    # PHASE 18: EVIDENCE-FIRST DECISION DOSSIER (W189-W194)
    # ════════════════════════════════════════════════════════════════
    (189, "decision_dossier", "Decision Dossier Model API",
     "Decision dossier entity for exception resolutions and approvals: evidence spans, recon scoring, ML confidence, approvals chain, export verification.",
     [("dossier_id", "str"), ("close_period_id", "str"), ("exception_id", "str|None"),
      ("evidence_spans", "list"), ("recon_scoring", "dict"),
      ("ml_confidence", "float"), ("feature_contributions", "dict"),
      ("approvals_chain", "list"), ("export_verification", "dict"),
      ("resolution_type", "str"), ("status", "str"),
      ("created_at", "str")],
     [("list_dossiers", "GET", "/api/decision-dossiers", "List decision dossiers"),
      ("create_dossier", "POST", "/api/decision-dossiers", "Create decision dossier"),
      ("get_dossier", "GET", "/api/decision-dossiers/{dossier_id}", "Get dossier details"),
      ("add_evidence", "POST", "/api/decision-dossiers/{dossier_id}/evidence", "Add evidence span"),
      ("add_approval", "POST", "/api/decision-dossiers/{dossier_id}/approval", "Add approval to chain"),
      ("verify_dossier", "POST", "/api/decision-dossiers/{dossier_id}/verify", "Verify dossier completeness"),
      ("dossier_report", "GET", "/api/decision-dossiers/report", "Get dossier report")]),

    (190, "evidence_highlighter", "Evidence Span Highlighter v2",
     "Multi-page multi-field evidence viewer with deep links from tool trace to dossier. Highlights evidence correctly in viewer.",
     [("highlight_id", "str"), ("dossier_id", "str"), ("doc_id", "str"),
      ("page_number", "int"), ("field_name", "str"),
      ("offset_start", "int"), ("offset_end", "int"),
      ("highlight_text", "str"), ("confidence", "float"),
      ("deep_link", "str"), ("status", "str"),
      ("created_at", "str")],
     [("list_highlights", "GET", "/api/evidence-highlights", "List evidence highlights"),
      ("create_highlight", "POST", "/api/evidence-highlights", "Create evidence highlight"),
      ("get_highlight", "GET", "/api/evidence-highlights/{highlight_id}", "Get highlight details"),
      ("link_to_dossier", "POST", "/api/evidence-highlights/{highlight_id}/link", "Link highlight to dossier"),
      ("open_deep_link", "POST", "/api/evidence-highlights/{highlight_id}/open", "Open deep link from tool trace"),
      ("highlight_report", "GET", "/api/evidence-highlights/report", "Get highlights report")]),

    (191, "explanation_graph", "Explanation Graph v3",
     "Reason DAG linking exception to evidence to model outputs to policy decisions to approvals to final resolution. Every node must reference evidence IDs.",
     [("graph_id", "str"), ("root_exception_id", "str"), ("nodes", "list"),
      ("edges", "list"), ("citation_count", "int"),
      ("uncited_nodes", "list"), ("dag_hash", "str|None"),
      ("serialization_stable", "bool"), ("validation_result", "str"),
      ("status", "str"), ("created_at", "str")],
     [("list_graphs", "GET", "/api/explanation-graphs", "List explanation graphs"),
      ("create_graph", "POST", "/api/explanation-graphs", "Create explanation graph"),
      ("get_graph", "GET", "/api/explanation-graphs/{graph_id}", "Get graph details"),
      ("add_node", "POST", "/api/explanation-graphs/{graph_id}/node", "Add node with citation"),
      ("validate_citations", "POST", "/api/explanation-graphs/{graph_id}/validate", "Validate all nodes have citations"),
      ("serialize_dag", "POST", "/api/explanation-graphs/{graph_id}/serialize", "Serialize DAG deterministically"),
      ("graph_report", "GET", "/api/explanation-graphs/report", "Get explanation graph report")]),

    (192, "policy_engine", "Policy Engine v4",
     "Tool scopes tied to roles and data sensitivity. Approvals required for sensitive actions. Deterministic deny reasons with audit events.",
     [("policy_id", "str"), ("tool_name", "str"), ("role", "str"),
      ("scope", "str"), ("data_sensitivity", "str"),
      ("approval_required", "bool"), ("deny_reason", "str|None"),
      ("approved_by", "str|None"), ("audit_trace_id", "str"),
      ("action_allowed", "bool"), ("status", "str"),
      ("evaluated_at", "str")],
     [("list_policies", "GET", "/api/policy-engine", "List policy evaluations"),
      ("evaluate_policy", "POST", "/api/policy-engine", "Evaluate policy for action"),
      ("get_policy", "GET", "/api/policy-engine/{policy_id}", "Get policy evaluation details"),
      ("approve_action", "POST", "/api/policy-engine/{policy_id}/approve", "Approve sensitive action"),
      ("deny_action", "POST", "/api/policy-engine/{policy_id}/deny", "Deny action with reason"),
      ("check_scope", "POST", "/api/policy-engine/{policy_id}/scope", "Check tool scope for role"),
      ("policy_report", "GET", "/api/policy-engine/report", "Get policy engine report")]),

    (193, "claim_enforcement", "No-Floating-Claim Enforcement",
     "Agent suggestions and decisions must include dossier_id references. Export blocked if any resolution lacks dossier. Guard enforcement.",
     [("enforcement_id", "str"), ("entity_type", "str"), ("entity_id", "str"),
      ("dossier_id", "str|None"), ("has_dossier", "bool"),
      ("claim_text", "str"), ("blocked", "bool"),
      ("block_reason", "str|None"), ("export_allowed", "bool"),
      ("enforcement_result", "str"), ("status", "str"),
      ("checked_at", "str")],
     [("list_enforcements", "GET", "/api/claim-enforcement", "List claim enforcements"),
      ("check_claim", "POST", "/api/claim-enforcement", "Check claim has dossier reference"),
      ("get_enforcement", "GET", "/api/claim-enforcement/{enforcement_id}", "Get enforcement details"),
      ("block_export", "POST", "/api/claim-enforcement/{enforcement_id}/block", "Block export for missing dossier"),
      ("unblock_export", "POST", "/api/claim-enforcement/{enforcement_id}/unblock", "Unblock after dossier attached"),
      ("enforcement_report", "GET", "/api/claim-enforcement/report", "Get claim enforcement report")]),

    (194, "audit_narrative", "Audit Narrative Export v1",
     "Human-readable story with citations: what happened, why, evidence support. Citations link to evidence spans and dossier IDs. Included in binder.",
     [("narrative_id", "str"), ("close_period_id", "str"), ("title", "str"),
      ("sections", "list"), ("citations", "list"),
      ("dossier_refs", "list"), ("evidence_refs", "list"),
      ("content_hash", "str|None"), ("word_count", "int"),
      ("status", "str"), ("generated_at", "str")],
     [("list_narratives", "GET", "/api/audit-narratives", "List audit narratives"),
      ("generate_narrative", "POST", "/api/audit-narratives", "Generate audit narrative"),
      ("get_narrative", "GET", "/api/audit-narratives/{narrative_id}", "Get narrative details"),
      ("add_citation", "POST", "/api/audit-narratives/{narrative_id}/citation", "Add citation to narrative"),
      ("export_narrative", "POST", "/api/audit-narratives/{narrative_id}/export", "Export narrative for binder"),
      ("narrative_report", "GET", "/api/audit-narratives/report", "Get narrative export report")]),

    # ════════════════════════════════════════════════════════════════
    # PHASE 19: DEPLOYMENT PROOF + PRODUCTION HYGIENE (W195-W200)
    # ════════════════════════════════════════════════════════════════
    (195, "cloudrun_deploy_v2", "Cloud Run Deploy v2",
     "Deploy scripts for LedgerLive API+Web and agent gateway on GCP. Smoke script produces deterministic smoke_report.json. Manual only.",
     [("deploy_id", "str"), ("deploy_target", "str"), ("service_name", "str"),
      ("config", "dict"), ("scripts_valid", "bool"),
      ("smoke_report", "dict"), ("smoke_report_hash", "str|None"),
      ("schema_valid", "bool"), ("region", "str"),
      ("status", "str"), ("created_at", "str")],
     [("list_deploys", "GET", "/api/cloudrun-v2", "List Cloud Run v2 deploy configs"),
      ("create_deploy", "POST", "/api/cloudrun-v2", "Create deploy config"),
      ("get_deploy", "GET", "/api/cloudrun-v2/{deploy_id}", "Get deploy details"),
      ("validate_config", "POST", "/api/cloudrun-v2/{deploy_id}/validate", "Validate deploy config + scripts"),
      ("generate_smoke", "POST", "/api/cloudrun-v2/{deploy_id}/smoke", "Generate smoke report schema"),
      ("deploy_report", "GET", "/api/cloudrun-v2/report", "Get deploy validation report")]),

    (196, "do_deploy", "DigitalOcean Deploy Automation v1",
     "DO App Platform/container deployment scripts. Smoke runs health check, sim session, binder export, hackpack export. Deterministic smoke format.",
     [("deploy_id", "str"), ("deploy_target", "str"), ("platform", "str"),
      ("config", "dict"), ("scripts_valid", "bool"),
      ("smoke_report", "dict"), ("smoke_report_hash", "str|None"),
      ("schema_valid", "bool"), ("status", "str"),
      ("created_at", "str")],
     [("list_deploys", "GET", "/api/do-deploy", "List DO deploy configs"),
      ("create_deploy", "POST", "/api/do-deploy", "Create DO deploy config"),
      ("get_deploy", "GET", "/api/do-deploy/{deploy_id}", "Get deploy details"),
      ("validate_config", "POST", "/api/do-deploy/{deploy_id}/validate", "Validate DO deploy config"),
      ("generate_smoke", "POST", "/api/do-deploy/{deploy_id}/smoke", "Generate smoke report schema"),
      ("deploy_report", "GET", "/api/do-deploy/report", "Get DO deploy report")]),

    (197, "release_bundle", "Release Bundle v3",
     "Release bundle includes proof pack pointer, deploy smoke reports, environment provenance. Deterministic bundle generation in DEMO mode.",
     [("bundle_id", "str"), ("bundle_version", "str"), ("proof_pack_ref", "str"),
      ("smoke_reports", "list"), ("environment_provenance", "dict"),
      ("enabled_features", "list"), ("content_hash", "str|None"),
      ("twice_run_match", "bool"), ("metadata", "dict"),
      ("status", "str"), ("generated_at", "str")],
     [("list_bundles", "GET", "/api/release-bundles", "List release bundles"),
      ("generate_bundle", "POST", "/api/release-bundles", "Generate release bundle"),
      ("get_bundle", "GET", "/api/release-bundles/{bundle_id}", "Get bundle details"),
      ("validate_bundle", "POST", "/api/release-bundles/{bundle_id}/validate", "Validate bundle completeness"),
      ("verify_determinism", "POST", "/api/release-bundles/{bundle_id}/determinism", "Verify twice-run hash match"),
      ("bundle_report", "GET", "/api/release-bundles/report", "Get release bundle report")]),

    (198, "chaos_hooks", "Deployed Environment Chaos Hooks",
     "Optional deployed chaos run scripts for GCP/DO. Never executed in CI. Config and validator only in CI. Seeded chaos for deployed environments.",
     [("hook_id", "str"), ("hook_name", "str"), ("target_env", "str"),
      ("chaos_seed", "int"), ("chaos_scenarios", "list"),
      ("script_path", "str"), ("script_valid", "bool"),
      ("ci_safe", "bool"), ("never_in_ci", "bool"),
      ("status", "str"), ("created_at", "str")],
     [("list_hooks", "GET", "/api/chaos-hooks", "List chaos hook configs"),
      ("create_hook", "POST", "/api/chaos-hooks", "Create chaos hook config"),
      ("get_hook", "GET", "/api/chaos-hooks/{hook_id}", "Get hook details"),
      ("validate_hook", "POST", "/api/chaos-hooks/{hook_id}/validate", "Validate hook script exists and is safe"),
      ("check_ci_safety", "POST", "/api/chaos-hooks/{hook_id}/ci-check", "Check hook is CI safe"),
      ("hook_report", "GET", "/api/chaos-hooks/report", "Get chaos hooks report")]),

    (199, "hackpack_v2", "Hackpack v2 Multi-Bundle",
     "Multi-hackathon bundle generator: Gemini bundle skeleton, Airia validated bundle, DO Gradient bundle, Automation Innovation bundle. All deterministic offline.",
     [("hackpack_id", "str"), ("hackpack_name", "str"), ("bundles", "list"),
      ("gemini_bundle", "dict"), ("airia_bundle", "dict"),
      ("do_bundle", "dict"), ("innovation_bundle", "dict"),
      ("bundle_checksums", "dict"), ("content_hash", "str|None"),
      ("status", "str"), ("generated_at", "str")],
     [("list_hackpacks", "GET", "/api/hackpack-v2", "List hackpack v2 bundles"),
      ("generate_hackpack", "POST", "/api/hackpack-v2", "Generate multi-hackathon pack"),
      ("get_hackpack", "GET", "/api/hackpack-v2/{hackpack_id}", "Get hackpack details"),
      ("validate_hackpack", "POST", "/api/hackpack-v2/{hackpack_id}/validate", "Validate all sub-bundles"),
      ("export_hackpack", "POST", "/api/hackpack-v2/{hackpack_id}/export", "Export hackpack archive"),
      ("hackpack_report", "GET", "/api/hackpack-v2/report", "Get hackpack v2 report")]),

    (200, "submit_all", "Submission Hardening v2",
     "Single command generator: make submit-all produces all bundles and index. Docs match Make targets. TOUR >=240s coverage. Twice-run determinism.",
     [("submission_id", "str"), ("check_type", "str"), ("target", "str"),
      ("make_targets_valid", "bool"), ("doc_commands_valid", "bool"),
      ("index_generated", "bool"), ("tour_duration_s", "float"),
      ("determinism_pass", "bool"), ("twice_run_hash_1", "str|None"),
      ("twice_run_hash_2", "str|None"), ("status", "str"),
      ("checked_at", "str")],
     [("list_submissions", "GET", "/api/submit-all", "List submission checks"),
      ("run_submission", "POST", "/api/submit-all", "Run submission hardening check"),
      ("get_submission", "GET", "/api/submit-all/{submission_id}", "Get submission details"),
      ("verify_docs", "POST", "/api/submit-all/{submission_id}/docs", "Verify docs match Make targets"),
      ("verify_determinism", "POST", "/api/submit-all/{submission_id}/determinism", "Verify twice-run determinism"),
      ("submission_report", "GET", "/api/submit-all/report", "Get submission hardening report")]),
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
    print(f"Generating {len(WAVES)} waves (181-200)...")

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
