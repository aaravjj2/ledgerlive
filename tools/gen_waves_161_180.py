#!/usr/bin/env python3
"""Generate LedgerLive Waves 161-180: Phases A-C.

Phase A (161-168): DEMO completeness + agentization
Phase B (169-176): Mocked connectors + ML baseline
Phase C (177-180): Live-ready adapters (no keys)

Run: python tools/gen_waves_161_180.py
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
    # PHASE A: DEMO COMPLETENESS + AGENTIZATION (W161-W168)
    # ════════════════════════════════════════════════════════════════
    (161, "demo_contract", "DEMO Contract",
     "Single authoritative APP_MODE switch with frozen time, seeded RNG, deterministic IDs, stable ordering, outbound network deny.",
     [("contract_id", "str"), ("app_mode", "str"), ("seed", "int"),
      ("frozen_time", "str"), ("network_policy", "str"),
      ("id_policy", "str"), ("ordering_policy", "str"),
      ("invariants_hash", "str"), ("status", "str"),
      ("checked_at", "str")],
     [("list_contracts", "GET", "/api/ops/demo-contracts", "List DEMO contract checks"),
      ("check_contract", "POST", "/api/ops/demo-contracts", "Check DEMO contract invariants"),
      ("get_contract", "GET", "/api/ops/demo-contracts/{contract_id}", "Get contract details"),
      ("verify_invariants", "POST", "/api/ops/demo-contracts/{contract_id}/verify", "Verify invariants hold"),
      ("demo_contract_report", "GET", "/api/ops/demo-contracts/report", "Get DEMO contract report"),
      ("demo_contract_hash", "GET", "/api/ops/demo-contracts/hash", "Get deterministic invariants hash")]),

    (162, "e2e_reset_v2", "E2E Reset Seed State v2",
     "Snapshot-based canonical scenario: POST reset restores DB+storage, POST seed loads canonical close scenario, GET state returns stable IDs.",
     [("snapshot_id", "str"), ("snapshot_type", "str"), ("entity_count", "int"),
      ("close_period_present", "bool"), ("canonical_ids", "dict"),
      ("state_hash", "str"), ("seed_version", "str"),
      ("status", "str"), ("executed_at", "str")],
     [("list_snapshots", "GET", "/api/ops/e2e-snapshots", "List E2E snapshots"),
      ("create_reset", "POST", "/api/ops/e2e-snapshots/reset", "Reset DB and storage to clean snapshot"),
      ("create_seed", "POST", "/api/ops/e2e-snapshots/seed", "Seed canonical multi-entity close scenario"),
      ("get_state", "GET", "/api/ops/e2e-snapshots/state", "Get current state with stable IDs"),
      ("get_snapshot", "GET", "/api/ops/e2e-snapshots/{snapshot_id}", "Get snapshot details"),
      ("verify_state", "POST", "/api/ops/e2e-snapshots/{snapshot_id}/verify", "Verify state hash consistency")]),

    (163, "tool_registry", "Tool Registry v1",
     "Typed versioned audited tool registry with JSON schemas, strict validation, and tool_trace recording.",
     [("tool_id", "str"), ("tool_name", "str"), ("schema_version", "str"),
      ("input_schema", "dict"), ("output_schema", "dict"),
      ("args_hash", "str|None"), ("result_hash", "str|None"),
      ("duration_ms", "float"), ("trace_id", "str"),
      ("idempotency_key", "str|None"), ("status", "str"),
      ("invoked_at", "str")],
     [("list_tools", "GET", "/api/tool-registry", "List registered tools"),
      ("register_tool", "POST", "/api/tool-registry", "Register a tool with schema"),
      ("get_tool", "GET", "/api/tool-registry/{tool_id}", "Get tool details"),
      ("invoke_tool", "POST", "/api/tool-registry/{tool_id}/invoke", "Invoke tool with args"),
      ("get_trace", "GET", "/api/tool-registry/{tool_id}/trace", "Get tool trace history"),
      ("validate_schema", "POST", "/api/tool-registry/{tool_id}/validate", "Validate tool schema"),
      ("tool_registry_export", "GET", "/api/tool-registry/export", "Export tool registry")]),

    (164, "agent_runtime", "Agent Runtime v1",
     "Verifier-first propose/verify/execute runtime producing ProposedAction objects with invariant checks before execution.",
     [("action_id", "str"), ("action_type", "str"), ("proposed_by", "str"),
      ("target_entity", "str"), ("payload", "dict"),
      ("verifier_result", "dict"), ("invariants_checked", "list"),
      ("approval_required", "bool"), ("approved_by", "str|None"),
      ("execution_status", "str"), ("reason_code", "str|None"),
      ("evidence_links", "list"), ("trace_id", "str"),
      ("proposed_at", "str"), ("executed_at", "str|None")],
     [("list_actions", "GET", "/api/agent-runtime/actions", "List proposed actions"),
      ("propose_action", "POST", "/api/agent-runtime/actions", "Propose a new action"),
      ("get_action", "GET", "/api/agent-runtime/actions/{action_id}", "Get action details"),
      ("verify_action", "POST", "/api/agent-runtime/actions/{action_id}/verify", "Run verifier on action"),
      ("approve_action", "POST", "/api/agent-runtime/actions/{action_id}/approve", "Approve action"),
      ("execute_action", "POST", "/api/agent-runtime/actions/{action_id}/execute", "Execute verified action"),
      ("reject_action", "POST", "/api/agent-runtime/actions/{action_id}/reject", "Reject action"),
      ("action_audit", "GET", "/api/agent-runtime/audit", "Get agent runtime audit log")]),

    (165, "session_sim", "Live Session Simulator",
     "Deterministic agent session replay runner: streams transcript events, triggers tool calls, streams verifier outcomes and tool trace updates.",
     [("session_id", "str"), ("session_name", "str"), ("transcript", "list"),
      ("tool_calls", "list"), ("verifier_outcomes", "list"),
      ("transcript_hash", "str|None"), ("tool_trace_hash", "str|None"),
      ("duration_ms", "float"), ("status", "str"),
      ("started_at", "str"), ("completed_at", "str|None")],
     [("list_sessions", "GET", "/api/session-sim", "List simulator sessions"),
      ("start_session", "POST", "/api/session-sim", "Start a simulator session"),
      ("get_session", "GET", "/api/session-sim/{session_id}", "Get session details"),
      ("advance_session", "POST", "/api/session-sim/{session_id}/advance", "Advance session step"),
      ("complete_session", "POST", "/api/session-sim/{session_id}/complete", "Complete session"),
      ("session_transcript", "GET", "/api/session-sim/{session_id}/transcript", "Get session transcript"),
      ("session_report", "GET", "/api/session-sim/report", "Get session simulation report")]),

    (166, "agent_console", "Agent Console UI",
     "Ops-grade agent console: transcript stream, tool trace stream, verifier results, approvals inbox, run status, export links.",
     [("console_id", "str"), ("session_id", "str"), ("transcript_items", "list"),
      ("tool_trace_items", "list"), ("verifier_items", "list"),
      ("approvals_pending", "list"), ("run_status", "str"),
      ("export_links", "list"), ("page_testid", "str"),
      ("created_at", "str")],
     [("list_consoles", "GET", "/api/agent-console", "List agent console states"),
      ("create_console", "POST", "/api/agent-console", "Create agent console session"),
      ("get_console", "GET", "/api/agent-console/{console_id}", "Get console state"),
      ("refresh_console", "POST", "/api/agent-console/{console_id}/refresh", "Refresh console data"),
      ("approve_item", "POST", "/api/agent-console/{console_id}/approve", "Approve item from console"),
      ("export_from_console", "POST", "/api/agent-console/{console_id}/export", "Export from console"),
      ("console_report", "GET", "/api/agent-console/report", "Get console report")]),

    (167, "close_orchestrator", "Close Orchestrator Workflow v1",
     "Full close orchestrator DAG: ingest, OCR, extraction, recon, triage, approvals, binder, verify, board pack. Resumable and idempotent by job_id.",
     [("job_id", "str"), ("workflow_name", "str"), ("dag_steps", "list"),
      ("current_step", "int"), ("total_steps", "int"),
      ("step_outputs", "dict"), ("binder_hash", "str|None"),
      ("board_pack_hash", "str|None"), ("resumable", "bool"),
      ("status", "str"), ("started_at", "str"),
      ("completed_at", "str|None")],
     [("list_jobs", "GET", "/api/close-orchestrator/jobs", "List orchestrator jobs"),
      ("start_job", "POST", "/api/close-orchestrator/jobs", "Start close orchestrator job"),
      ("get_job", "GET", "/api/close-orchestrator/jobs/{job_id}", "Get job details"),
      ("advance_step", "POST", "/api/close-orchestrator/jobs/{job_id}/advance", "Advance to next DAG step"),
      ("resume_job", "POST", "/api/close-orchestrator/jobs/{job_id}/resume", "Resume failed job"),
      ("verify_outputs", "POST", "/api/close-orchestrator/jobs/{job_id}/verify", "Verify all step outputs"),
      ("export_binder", "POST", "/api/close-orchestrator/jobs/{job_id}/binder", "Export binder from job"),
      ("job_report", "GET", "/api/close-orchestrator/report", "Get orchestrator report")]),

    (168, "hackpack_gen", "Hackpack Generator v1",
     "Generates deterministic hackathon pack: architecture diagram, tool schemas, demo script, proof pack pointer, deployment placeholders.",
     [("hackpack_id", "str"), ("pack_name", "str"), ("architecture_ref", "str"),
      ("tool_schemas", "list"), ("demo_script", "str"),
      ("proof_pack_ref", "str"), ("checksums", "dict"),
      ("content_hash", "str|None"), ("deployment_placeholders", "dict"),
      ("status", "str"), ("generated_at", "str")],
     [("list_hackpacks", "GET", "/api/hackpacks", "List generated hackpacks"),
      ("generate_hackpack", "POST", "/api/hackpacks", "Generate hackathon pack"),
      ("get_hackpack", "GET", "/api/hackpacks/{hackpack_id}", "Get hackpack details"),
      ("validate_hackpack", "POST", "/api/hackpacks/{hackpack_id}/validate", "Validate hackpack integrity"),
      ("export_hackpack", "POST", "/api/hackpacks/{hackpack_id}/export", "Export hackpack bundle"),
      ("hackpack_report", "GET", "/api/hackpacks/report", "Get hackpack generation report")]),

    # ════════════════════════════════════════════════════════════════
    # PHASE B: MOCKED CONNECTORS + ML BASELINE (W169-W176)
    # ════════════════════════════════════════════════════════════════
    (169, "connector_mocks", "Connector Mock Servers v1",
     "Local mock servers for QBO/Xero/Plaid simulating pagination, token refresh, 429 backoff, partial responses, dirty data.",
     [("mock_id", "str"), ("provider", "str"), ("mock_type", "str"),
      ("endpoint", "str"), ("response_mode", "str"),
      ("pagination_enabled", "bool"), ("token_refresh_sim", "bool"),
      ("error_rate_pct", "float"), ("status", "str"),
      ("created_at", "str")],
     [("list_mocks", "GET", "/api/connector-mocks", "List mock server configs"),
      ("create_mock", "POST", "/api/connector-mocks", "Create mock server config"),
      ("get_mock", "GET", "/api/connector-mocks/{mock_id}", "Get mock config details"),
      ("toggle_error", "POST", "/api/connector-mocks/{mock_id}/toggle-error", "Toggle error simulation"),
      ("sync_mock", "POST", "/api/connector-mocks/{mock_id}/sync", "Sync data from mock"),
      ("mock_status", "GET", "/api/connector-mocks/status", "Get mock server status"),
      ("mock_report", "GET", "/api/connector-mocks/report", "Get mock sync report")]),

    (170, "connector_realmode", "Connector Real-Mode Interface",
     "Real provider interfaces behind ENABLE_QBO/ENABLE_XERO/ENABLE_PLAID flags. Keys optional, never required. Fail fast without keys.",
     [("config_id", "str"), ("provider", "str"), ("enabled", "bool"),
      ("has_keys", "bool"), ("validation_result", "str"),
      ("error_message", "str|None"), ("fallback_to_mock", "bool"),
      ("status", "str"), ("validated_at", "str")],
     [("list_configs", "GET", "/api/connector-realmode", "List real-mode configs"),
      ("create_config", "POST", "/api/connector-realmode", "Create real-mode config"),
      ("get_config", "GET", "/api/connector-realmode/{config_id}", "Get config details"),
      ("validate_keys", "POST", "/api/connector-realmode/{config_id}/validate", "Validate provider keys"),
      ("test_connection", "POST", "/api/connector-realmode/{config_id}/test", "Test connection safely"),
      ("config_report", "GET", "/api/connector-realmode/report", "Get config validation report")]),

    (171, "ml_dataset", "ML Dataset Builder v1",
     "Deterministic dataset builder from seeded close runs: extraction labels, match labels, exception categories. Output with sha256 manifest.",
     [("dataset_id", "str"), ("dataset_name", "str"), ("dataset_type", "str"),
      ("record_count", "int"), ("label_count", "int"),
      ("seed", "int"), ("content_hash", "str|None"),
      ("manifest", "dict"), ("status", "str"),
      ("generated_at", "str")],
     [("list_datasets", "GET", "/api/ml-datasets", "List ML datasets"),
      ("generate_dataset", "POST", "/api/ml-datasets", "Generate ML dataset from fixtures"),
      ("get_dataset", "GET", "/api/ml-datasets/{dataset_id}", "Get dataset details"),
      ("verify_dataset", "POST", "/api/ml-datasets/{dataset_id}/verify", "Verify dataset hash integrity"),
      ("export_dataset", "POST", "/api/ml-datasets/{dataset_id}/export", "Export dataset artifacts"),
      ("dataset_report", "GET", "/api/ml-datasets/report", "Get dataset generation report")]),

    (172, "ml_baseline", "ML Baseline Models v1",
     "Deterministic baseline models: extraction confidence calibration and match likelihood scoring. Seeded training with stable artifact hashes.",
     [("model_id", "str"), ("model_name", "str"), ("model_type", "str"),
      ("dataset_id", "str"), ("seed", "int"),
      ("artifact_hash", "str|None"), ("calibration_score", "float"),
      ("match_accuracy", "float"), ("metadata", "dict"),
      ("status", "str"), ("trained_at", "str")],
     [("list_models", "GET", "/api/ml-baseline", "List baseline models"),
      ("train_model", "POST", "/api/ml-baseline", "Train baseline model"),
      ("get_model", "GET", "/api/ml-baseline/{model_id}", "Get model details"),
      ("evaluate_model", "POST", "/api/ml-baseline/{model_id}/evaluate", "Evaluate model metrics"),
      ("register_model", "POST", "/api/ml-baseline/{model_id}/register", "Register model artifact"),
      ("model_report", "GET", "/api/ml-baseline/report", "Get model training report")]),

    (173, "ml_inference", "ML Inference Hook v1",
     "Model-driven routing: low-confidence extracts to review, auto-suggest triage, auto-approve low-risk matches with verifier gating and explainability.",
     [("inference_id", "str"), ("model_id", "str"), ("input_hash", "str"),
      ("confidence", "float"), ("routing_decision", "str"),
      ("explanation", "str"), ("evidence_pointers", "list"),
      ("verifier_pass", "bool"), ("fallback_used", "bool"),
      ("status", "str"), ("inferred_at", "str")],
     [("list_inferences", "GET", "/api/ml-inference", "List inference results"),
      ("run_inference", "POST", "/api/ml-inference", "Run ML inference"),
      ("get_inference", "GET", "/api/ml-inference/{inference_id}", "Get inference details"),
      ("explain_decision", "POST", "/api/ml-inference/{inference_id}/explain", "Get explainability report"),
      ("fallback_check", "POST", "/api/ml-inference/{inference_id}/fallback", "Check fallback behavior"),
      ("inference_report", "GET", "/api/ml-inference/report", "Get inference report")]),

    (174, "model_governance", "Model Governance Lite",
     "Model registry, dataset registry, drift snapshot in eval reports. Drift report artifacts with stable ordering and hashes.",
     [("governance_id", "str"), ("model_id", "str"), ("dataset_id", "str"),
      ("drift_detected", "bool"), ("drift_score", "float"),
      ("drift_report_hash", "str|None"), ("eval_metrics", "dict"),
      ("snapshot_stable", "bool"), ("status", "str"),
      ("evaluated_at", "str")],
     [("list_governance", "GET", "/api/model-governance", "List governance records"),
      ("create_eval", "POST", "/api/model-governance", "Create governance evaluation"),
      ("get_governance", "GET", "/api/model-governance/{governance_id}", "Get governance record"),
      ("compute_drift", "POST", "/api/model-governance/{governance_id}/drift", "Compute drift snapshot"),
      ("verify_stability", "POST", "/api/model-governance/{governance_id}/verify", "Verify snapshot stability"),
      ("governance_report", "GET", "/api/model-governance/report", "Get governance report")]),

    (175, "evidence_search", "Evidence Graph Search v2",
     "Local offline index over docs, exceptions, tool traces, and audit with deterministic ordering, pagination, and saved searches.",
     [("search_id", "str"), ("query_text", "str"), ("index_scope", "str"),
      ("result_count", "int"), ("results", "list"),
      ("order_hash", "str|None"), ("saved", "bool"),
      ("deterministic", "bool"), ("status", "str"),
      ("searched_at", "str")],
     [("list_searches", "GET", "/api/evidence-search", "List saved searches"),
      ("execute_search", "POST", "/api/evidence-search", "Execute evidence search"),
      ("get_search", "GET", "/api/evidence-search/{search_id}", "Get search details"),
      ("save_search", "POST", "/api/evidence-search/{search_id}/save", "Save search for reuse"),
      ("open_evidence", "POST", "/api/evidence-search/{search_id}/open", "Open linked evidence"),
      ("search_report", "GET", "/api/evidence-search/report", "Get search report")]),

    (176, "reliability_harness", "Reliability Harness v1",
     "Seeded chaos matrix for connector 429, partial OCR, job interruption, storage failure. Deterministic chaos report with resilience score.",
     [("harness_id", "str"), ("scenario", "str"), ("seed", "int"),
      ("failure_type", "str"), ("injection_point", "str"),
      ("outcome", "str"), ("resilience_score", "float"),
      ("deterministic", "bool"), ("chaos_report_hash", "str|None"),
      ("status", "str"), ("tested_at", "str")],
     [("list_harnesses", "GET", "/api/reliability-harness", "List reliability harness runs"),
      ("run_harness", "POST", "/api/reliability-harness", "Run reliability harness test"),
      ("get_harness", "GET", "/api/reliability-harness/{harness_id}", "Get harness details"),
      ("inject_failure", "POST", "/api/reliability-harness/{harness_id}/inject", "Inject specific failure"),
      ("verify_determinism", "POST", "/api/reliability-harness/{harness_id}/verify", "Verify report determinism"),
      ("harness_report", "GET", "/api/reliability-harness/report", "Get chaos report with resilience score")]),

    # ════════════════════════════════════════════════════════════════
    # PHASE C: LIVE-READY ADAPTERS (NO KEYS) (W177-W180)
    # ════════════════════════════════════════════════════════════════
    (177, "gemini_adapter", "Gemini Live Adapter Skeleton",
     "Adapter interface compatible with Live Session Simulator. DEMO uses simulator; GEMINI provider behind flag with placeholder config.",
     [("adapter_id", "str"), ("adapter_name", "str"), ("provider", "str"),
      ("config", "dict"), ("config_valid", "bool"),
      ("mock_mode", "bool"), ("deploy_scripts", "list"),
      ("validation_result", "str"), ("status", "str"),
      ("created_at", "str")],
     [("list_adapters", "GET", "/api/gemini-adapter", "List Gemini adapter configs"),
      ("create_adapter", "POST", "/api/gemini-adapter", "Create Gemini adapter config"),
      ("get_adapter", "GET", "/api/gemini-adapter/{adapter_id}", "Get adapter details"),
      ("validate_config", "POST", "/api/gemini-adapter/{adapter_id}/validate", "Validate adapter config"),
      ("test_adapter", "POST", "/api/gemini-adapter/{adapter_id}/test", "Test adapter offline"),
      ("adapter_report", "GET", "/api/gemini-adapter/report", "Get adapter report")]),

    (178, "airia_adapter", "Airia Adapter Skeleton",
     "Exporter producing Airia community package artifact: tool schema, runbooks, persona config, screenshots list, metadata. Not published yet.",
     [("package_id", "str"), ("package_name", "str"), ("tool_schemas", "list"),
      ("runbooks", "list"), ("persona_config", "dict"),
      ("screenshots_list", "list"), ("metadata", "dict"),
      ("content_hash", "str|None"), ("status", "str"),
      ("generated_at", "str")],
     [("list_packages", "GET", "/api/airia-adapter", "List Airia packages"),
      ("generate_package", "POST", "/api/airia-adapter", "Generate Airia community package"),
      ("get_package", "GET", "/api/airia-adapter/{package_id}", "Get package details"),
      ("validate_package", "POST", "/api/airia-adapter/{package_id}/validate", "Validate package"),
      ("export_package", "POST", "/api/airia-adapter/{package_id}/export", "Export package artifact"),
      ("package_report", "GET", "/api/airia-adapter/report", "Get package report")]),

    (179, "gradient_adapter", "DigitalOcean Gradient Adapter Skeleton",
     "Config and scripts for Gradient training/inference. DEMO uses local model artifacts. Deterministic would-run plan output.",
     [("plan_id", "str"), ("plan_name", "str"), ("config", "dict"),
      ("training_steps", "list"), ("inference_steps", "list"),
      ("resource_requirements", "dict"), ("plan_hash", "str|None"),
      ("local_artifacts_ref", "str"), ("status", "str"),
      ("created_at", "str")],
     [("list_plans", "GET", "/api/gradient-adapter", "List Gradient adapter plans"),
      ("create_plan", "POST", "/api/gradient-adapter", "Create Gradient adapter plan"),
      ("get_plan", "GET", "/api/gradient-adapter/{plan_id}", "Get plan details"),
      ("validate_plan", "POST", "/api/gradient-adapter/{plan_id}/validate", "Validate plan config"),
      ("simulate_plan", "POST", "/api/gradient-adapter/{plan_id}/simulate", "Simulate plan execution"),
      ("plan_report", "GET", "/api/gradient-adapter/report", "Get plan report")]),

    (180, "submission_harden", "Submission Hardening Wave",
     "One-command local run, docs generator, expanded TOUR coverage. Documentation tests enforce commands exist. MCP E2E twice-run determinism.",
     [("harden_id", "str"), ("check_type", "str"), ("target", "str"),
      ("doc_commands_valid", "bool"), ("make_targets_exist", "bool"),
      ("tour_duration_s", "float"), ("determinism_pass", "bool"),
      ("twice_run_hash_1", "str|None"), ("twice_run_hash_2", "str|None"),
      ("status", "str"), ("checked_at", "str")],
     [("list_checks", "GET", "/api/submission-harden", "List hardening checks"),
      ("run_check", "POST", "/api/submission-harden", "Run hardening check"),
      ("get_check", "GET", "/api/submission-harden/{harden_id}", "Get check details"),
      ("verify_docs", "POST", "/api/submission-harden/{harden_id}/docs", "Verify docs match Make targets"),
      ("verify_determinism", "POST", "/api/submission-harden/{harden_id}/determinism", "Verify twice-run determinism"),
      ("harden_report", "GET", "/api/submission-harden/report", "Get hardening report")]),
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
    print(f"Generating {len(WAVES)} waves (161-180)...")

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
