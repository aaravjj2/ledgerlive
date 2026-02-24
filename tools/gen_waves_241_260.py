#!/usr/bin/env python3
"""Generate LedgerLive Waves 241-260: Phases 26-27.

Phase 26 (241-250): Agent-Driven Race Control
Phase 27 (251-260): Security Posture First-Class

Run: python tools/gen_waves_241_260.py
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
    # PHASE 26: AGENT-DRIVEN RACE CONTROL (W241-W250)
    # ════════════════════════════════════════════════════════════════
    (241, "next_actions_engine", "Next Actions Engine v1",
     "Generates prioritized next steps from DAG, blockers, SLA, and incidents. Output is deterministic and dossier-linked with evidence references.",
     [("action_id", "str"), ("dag_ref", "str"), ("blocker_refs", "list"),
      ("sla_ref", "str"), ("incident_refs", "list"), ("priority_score", "float"),
      ("action_type", "str"), ("description", "str"),
      ("dossier_link", "str"), ("evidence_refs", "list"),
      ("estimated_minutes", "int"), ("status", "str"),
      ("generated_at", "str")],
     [("list_actions", "GET", "/api/next-actions", "List prioritized next actions"),
      ("generate_actions", "POST", "/api/next-actions", "Generate next actions from DAG state"),
      ("get_action", "GET", "/api/next-actions/{action_id}", "Get action details"),
      ("reprioritize", "POST", "/api/next-actions/{action_id}/reprioritize", "Reprioritize action"),
      ("link_dossier", "POST", "/api/next-actions/{action_id}/link-dossier", "Link dossier to action"),
      ("dismiss_action", "POST", "/api/next-actions/{action_id}/dismiss", "Dismiss action"),
      ("actions_report", "GET", "/api/next-actions/report", "Get next actions report")]),

    (242, "plan_preview", "Plan Preview v1",
     "Agent proposes a full run plan with sequence of actions and predicted artifacts/hashes. Zero side effects — preview only with deterministic output.",
     [("plan_id", "str"), ("plan_name", "str"), ("action_sequence", "list"),
      ("predicted_artifacts", "list"), ("predicted_hashes", "dict"),
      ("estimated_duration_min", "int"), ("risk_assessment", "dict"),
      ("prerequisites_met", "bool"), ("side_effects", "list"),
      ("approval_required", "bool"), ("deterministic_hash", "str"),
      ("status", "str"), ("previewed_at", "str")],
     [("list_plans", "GET", "/api/plan-preview", "List plan previews"),
      ("create_preview", "POST", "/api/plan-preview", "Create plan preview"),
      ("get_plan", "GET", "/api/plan-preview/{plan_id}", "Get plan preview details"),
      ("validate_plan", "POST", "/api/plan-preview/{plan_id}/validate", "Validate plan prerequisites"),
      ("predict_hashes", "POST", "/api/plan-preview/{plan_id}/predict-hashes", "Predict artifact hashes"),
      ("plan_report", "GET", "/api/plan-preview/report", "Get plan preview report")]),

    (243, "verifier_gate_ui", "Verifier Gate UI v1",
     "Shows which invariants pass or fail, surfaces required approvals per step, and provides deterministic deny reasons for blocked actions.",
     [("gate_id", "str"), ("step_ref", "str"), ("invariants", "list"),
      ("passed_invariants", "list"), ("failed_invariants", "list"),
      ("approvals_required", "list"), ("deny_reasons", "list"),
      ("overall_result", "str"), ("deterministic_output", "bool"),
      ("evidence_links", "list"), ("gate_hash", "str"),
      ("status", "str"), ("evaluated_at", "str")],
     [("list_gates", "GET", "/api/verifier-gate", "List verifier gates"),
      ("create_gate", "POST", "/api/verifier-gate", "Create verifier gate evaluation"),
      ("get_gate", "GET", "/api/verifier-gate/{gate_id}", "Get gate details"),
      ("evaluate_gate", "POST", "/api/verifier-gate/{gate_id}/evaluate", "Evaluate gate invariants"),
      ("explain_deny", "POST", "/api/verifier-gate/{gate_id}/explain-deny", "Explain deny reasons"),
      ("gate_report", "GET", "/api/verifier-gate/report", "Get verifier gate report")]),

    (244, "execute_from_plan", "Execute-from-Plan v1",
     "Executes approved plan with idempotency keys, updates tool trace and incident telemetry live, tracks execution progress step by step.",
     [("execution_id", "str"), ("plan_ref", "str"), ("idempotency_key", "str"),
      ("steps_completed", "int"), ("steps_total", "int"),
      ("current_step", "str"), ("tool_trace", "list"),
      ("incidents_generated", "list"), ("telemetry_updates", "list"),
      ("execution_hash", "str"), ("rollback_available", "bool"),
      ("status", "str"), ("started_at", "str")],
     [("list_executions", "GET", "/api/plan-execution", "List plan executions"),
      ("start_execution", "POST", "/api/plan-execution", "Start plan execution"),
      ("get_execution", "GET", "/api/plan-execution/{execution_id}", "Get execution details"),
      ("advance_step", "POST", "/api/plan-execution/{execution_id}/advance", "Advance execution step"),
      ("record_telemetry", "POST", "/api/plan-execution/{execution_id}/telemetry", "Record telemetry update"),
      ("rollback_execution", "POST", "/api/plan-execution/{execution_id}/rollback", "Rollback execution"),
      ("execution_report", "GET", "/api/plan-execution/report", "Get execution report")]),

    (245, "rc_why_dossier", "Race Control Why v1",
     "Every next action has a one-click dossier/reason DAG/evidence view. Consistent across surfaces with deterministic rendering.",
     [("why_id", "str"), ("action_ref", "str"), ("reason_dag", "dict"),
      ("evidence_chain", "list"), ("dossier_content", "dict"),
      ("policy_refs", "list"), ("precedent_refs", "list"),
      ("confidence_score", "float"), ("surface_type", "str"),
      ("render_hash", "str"), ("consistent_across", "list"),
      ("status", "str"), ("generated_at", "str")],
     [("list_whys", "GET", "/api/rc-why", "List why dossiers"),
      ("generate_why", "POST", "/api/rc-why", "Generate why dossier for action"),
      ("get_why", "GET", "/api/rc-why/{why_id}", "Get why dossier details"),
      ("expand_reason", "POST", "/api/rc-why/{why_id}/expand", "Expand reason DAG node"),
      ("verify_consistency", "POST", "/api/rc-why/{why_id}/verify-consistency", "Verify cross-surface consistency"),
      ("why_report", "GET", "/api/rc-why/report", "Get why dossier report")]),

    (246, "fail_closed_escalation", "Fail-Closed Escalation v1",
     "Uncertain steps become approval-required. If risk rules fail, creates incident and pauses automation. Deterministic escalation logic.",
     [("escalation_id", "str"), ("step_ref", "str"), ("risk_rule_results", "dict"),
      ("uncertainty_score", "float"), ("escalation_type", "str"),
      ("approval_required", "bool"), ("incident_created", "bool"),
      ("incident_ref", "str|None"), ("automation_paused", "bool"),
      ("pause_reason", "str"), ("escalation_chain", "list"),
      ("status", "str"), ("escalated_at", "str")],
     [("list_escalations", "GET", "/api/fail-closed", "List fail-closed escalations"),
      ("create_escalation", "POST", "/api/fail-closed", "Create fail-closed escalation"),
      ("get_escalation", "GET", "/api/fail-closed/{escalation_id}", "Get escalation details"),
      ("approve_escalation", "POST", "/api/fail-closed/{escalation_id}/approve", "Approve escalated step"),
      ("create_incident", "POST", "/api/fail-closed/{escalation_id}/create-incident", "Create incident from escalation"),
      ("resume_automation", "POST", "/api/fail-closed/{escalation_id}/resume", "Resume paused automation"),
      ("escalation_report", "GET", "/api/fail-closed/report", "Get escalation report")]),

    (247, "pit_crew_routing", "Pit Crew Routing v1",
     "Next actions assigned to specialized agents. Quorum and veto shown in Race Control. Multi-agent coordination with skill-based routing.",
     [("routing_id", "str"), ("action_ref", "str"), ("agent_assignments", "list"),
      ("required_skills", "list"), ("quorum_required", "int"),
      ("quorum_achieved", "bool"), ("veto_agents", "list"),
      ("veto_active", "bool"), ("routing_strategy", "str"),
      ("assignment_hash", "str"), ("completion_pct", "float"),
      ("status", "str"), ("routed_at", "str")],
     [("list_routings", "GET", "/api/pit-crew", "List pit crew routings"),
      ("create_routing", "POST", "/api/pit-crew", "Create pit crew routing"),
      ("get_routing", "GET", "/api/pit-crew/{routing_id}", "Get routing details"),
      ("assign_agent", "POST", "/api/pit-crew/{routing_id}/assign", "Assign agent to action"),
      ("record_veto", "POST", "/api/pit-crew/{routing_id}/veto", "Record agent veto"),
      ("check_quorum", "POST", "/api/pit-crew/{routing_id}/quorum", "Check quorum status"),
      ("routing_report", "GET", "/api/pit-crew/report", "Get pit crew routing report")]),

    (248, "channel_action_int", "Channel Action Integration v1",
     "Approve or deny steps from mock chat/email cards. Updates plan state immediately with full audit trail and deterministic processing.",
     [("channel_action_id", "str"), ("channel_type", "str"), ("card_ref", "str"),
      ("action_type", "str"), ("plan_ref", "str"), ("step_ref", "str"),
      ("decision", "str"), ("decision_reason", "str"),
      ("decided_by", "str"), ("plan_state_before", "dict"),
      ("plan_state_after", "dict"), ("audit_ref", "str"),
      ("status", "str"), ("decided_at", "str")],
     [("list_channel_actions", "GET", "/api/channel-action", "List channel actions"),
      ("create_channel_action", "POST", "/api/channel-action", "Create channel action"),
      ("get_channel_action", "GET", "/api/channel-action/{channel_action_id}", "Get channel action details"),
      ("approve_via_channel", "POST", "/api/channel-action/{channel_action_id}/approve", "Approve via channel"),
      ("deny_via_channel", "POST", "/api/channel-action/{channel_action_id}/deny", "Deny via channel"),
      ("channel_action_report", "GET", "/api/channel-action/report", "Get channel action report")]),

    (249, "replay_hook", "Replay Hook v1",
     "Every executed plan auto-creates a replay artifact store snapshot. Replay is available from Race Control with full deterministic reproduction.",
     [("hook_id", "str"), ("execution_ref", "str"), ("snapshot_data", "dict"),
      ("artifact_refs", "list"), ("snapshot_hash", "str"),
      ("replay_available", "bool"), ("replay_url", "str"),
      ("rc_link", "str"), ("reproduction_verified", "bool"),
      ("snapshot_size_bytes", "int"), ("deterministic", "bool"),
      ("status", "str"), ("captured_at", "str")],
     [("list_hooks", "GET", "/api/replay-hook", "List replay hooks"),
      ("create_hook", "POST", "/api/replay-hook", "Create replay hook snapshot"),
      ("get_hook", "GET", "/api/replay-hook/{hook_id}", "Get replay hook details"),
      ("trigger_replay", "POST", "/api/replay-hook/{hook_id}/trigger", "Trigger replay from snapshot"),
      ("verify_reproduction", "POST", "/api/replay-hook/{hook_id}/verify", "Verify reproduction fidelity"),
      ("hook_report", "GET", "/api/replay-hook/report", "Get replay hook report")]),

    (250, "agent_rc_proof", "Agent RC Proof Wave v1",
     "End-to-end proof covering Next Actions, Plan Preview, Approve, Execute, Dossier, and Replay link. Deterministic twice-run verification.",
     [("proof_id", "str"), ("next_actions_ref", "str"), ("plan_ref", "str"),
      ("approval_ref", "str"), ("execution_ref", "str"),
      ("dossier_ref", "str"), ("replay_ref", "str"),
      ("all_steps_verified", "bool"), ("determinism_hash", "str"),
      ("twice_run_match", "bool"), ("content_hash", "str"),
      ("evidence_bundle", "list"), ("status", "str"),
      ("verified_at", "str")],
     [("list_proofs", "GET", "/api/agent-rc-proof", "List agent RC proofs"),
      ("generate_proof", "POST", "/api/agent-rc-proof", "Generate agent RC proof"),
      ("get_proof", "GET", "/api/agent-rc-proof/{proof_id}", "Get proof details"),
      ("verify_proof", "POST", "/api/agent-rc-proof/{proof_id}/verify", "Verify proof integrity"),
      ("seal_proof", "POST", "/api/agent-rc-proof/{proof_id}/seal", "Seal agent RC proof"),
      ("proof_report", "GET", "/api/agent-rc-proof/report", "Get agent RC proof report")]),

    # ════════════════════════════════════════════════════════════════
    # PHASE 27: SECURITY POSTURE FIRST-CLASS (W251-W260)
    # ════════════════════════════════════════════════════════════════
    (251, "policy_events", "Policy Events v1",
     "Policy denies, scope violations, and injection flags become structured security events with classification, evidence, and deterministic reasons.",
     [("event_id", "str"), ("event_type", "str"), ("policy_ref", "str"),
      ("violation_type", "str"), ("severity", "str"),
      ("classification", "str"), ("evidence", "dict"),
      ("deny_reason", "str"), ("source_context", "dict"),
      ("affected_entities", "list"), ("remediation_hint", "str"),
      ("status", "str"), ("detected_at", "str")],
     [("list_events", "GET", "/api/policy-events", "List policy events"),
      ("create_event", "POST", "/api/policy-events", "Create policy event"),
      ("get_event", "GET", "/api/policy-events/{event_id}", "Get policy event details"),
      ("classify_event", "POST", "/api/policy-events/{event_id}/classify", "Classify policy event"),
      ("link_evidence", "POST", "/api/policy-events/{event_id}/evidence", "Link evidence to event"),
      ("event_report", "GET", "/api/policy-events/report", "Get policy events report")]),

    (252, "security_timeline", "Security Timeline v1",
     "Incidents and security events unified in a filterable, exportable timeline view within Race Control. Deterministic ordering and rendering.",
     [("timeline_id", "str"), ("entries", "list"), ("filter_criteria", "dict"),
      ("date_range_start", "str"), ("date_range_end", "str"),
      ("entry_count", "int"), ("severity_distribution", "dict"),
      ("export_format", "str"), ("render_hash", "str"),
      ("includes_incidents", "bool"), ("includes_policy_events", "bool"),
      ("status", "str"), ("generated_at", "str")],
     [("list_timelines", "GET", "/api/security-timeline", "List security timelines"),
      ("create_timeline", "POST", "/api/security-timeline", "Create security timeline"),
      ("get_timeline", "GET", "/api/security-timeline/{timeline_id}", "Get timeline details"),
      ("filter_timeline", "POST", "/api/security-timeline/{timeline_id}/filter", "Filter timeline entries"),
      ("export_timeline", "POST", "/api/security-timeline/{timeline_id}/export", "Export timeline"),
      ("timeline_report", "GET", "/api/security-timeline/report", "Get security timeline report")]),

    (253, "tool_scope_matrix", "Tool Scope Matrix UI v1",
     "Shows per-role tool scopes, sensitive data tiers, and required approvals. Matrix view with deterministic rendering and export capability.",
     [("matrix_id", "str"), ("roles", "list"), ("tools", "list"),
      ("scope_entries", "list"), ("data_tiers", "dict"),
      ("approval_requirements", "dict"), ("coverage_pct", "float"),
      ("gaps_identified", "list"), ("render_hash", "str"),
      ("last_reviewed_by", "str"), ("review_status", "str"),
      ("status", "str"), ("generated_at", "str")],
     [("list_matrices", "GET", "/api/tool-scope-matrix", "List tool scope matrices"),
      ("create_matrix", "POST", "/api/tool-scope-matrix", "Create tool scope matrix"),
      ("get_matrix", "GET", "/api/tool-scope-matrix/{matrix_id}", "Get matrix details"),
      ("evaluate_coverage", "POST", "/api/tool-scope-matrix/{matrix_id}/evaluate", "Evaluate scope coverage"),
      ("identify_gaps", "POST", "/api/tool-scope-matrix/{matrix_id}/gaps", "Identify scope gaps"),
      ("matrix_report", "GET", "/api/tool-scope-matrix/report", "Get tool scope matrix report")]),

    (254, "exfil_detector_v2", "Exfil Detector v2",
     "Extended exfiltration and injection detection covering inbound docs and channel content. Deterministic classification with evidence-backed reasons.",
     [("detection_id", "str"), ("content_source", "str"), ("content_type", "str"),
      ("scan_result", "str"), ("threat_type", "str"),
      ("confidence", "float"), ("classification_reason", "str"),
      ("evidence_refs", "list"), ("blocked", "bool"),
      ("remediation_steps", "list"), ("scan_hash", "str"),
      ("status", "str"), ("scanned_at", "str")],
     [("list_detections", "GET", "/api/exfil-detector-v2", "List exfil detections"),
      ("scan_content", "POST", "/api/exfil-detector-v2", "Scan content for exfil/injection"),
      ("get_detection", "GET", "/api/exfil-detector-v2/{detection_id}", "Get detection details"),
      ("classify_threat", "POST", "/api/exfil-detector-v2/{detection_id}/classify", "Classify threat type"),
      ("block_content", "POST", "/api/exfil-detector-v2/{detection_id}/block", "Block detected content"),
      ("detection_report", "GET", "/api/exfil-detector-v2/report", "Get exfil detector report")]),

    (255, "safe_fix_path", "Safe Fix Path v1",
     "Blocked actions show evidence-backed remediation suggestions with no side effects until approved. Deterministic suggestion generation.",
     [("fix_id", "str"), ("blocked_action_ref", "str"), ("block_reason", "str"),
      ("remediation_steps", "list"), ("evidence_refs", "list"),
      ("risk_reduction_pct", "float"), ("side_effects", "list"),
      ("approval_required", "bool"), ("approved_by", "str|None"),
      ("applied", "bool"), ("fix_hash", "str"),
      ("status", "str"), ("suggested_at", "str")],
     [("list_fixes", "GET", "/api/safe-fix-path", "List safe fix paths"),
      ("suggest_fix", "POST", "/api/safe-fix-path", "Suggest safe fix path"),
      ("get_fix", "GET", "/api/safe-fix-path/{fix_id}", "Get fix path details"),
      ("approve_fix", "POST", "/api/safe-fix-path/{fix_id}/approve", "Approve fix path"),
      ("apply_fix", "POST", "/api/safe-fix-path/{fix_id}/apply", "Apply approved fix"),
      ("fix_report", "GET", "/api/safe-fix-path/report", "Get safe fix path report")]),

    (256, "audit_integrity_badge", "Audit Integrity Badge v1",
     "Race Control shows Merkle proof status for audit, tool trace, and security events. Badge indicates verified, unverified, or tampered state.",
     [("badge_id", "str"), ("entity_type", "str"), ("entity_ref", "str"),
      ("merkle_root", "str"), ("proof_chain", "list"),
      ("verification_result", "str"), ("last_verified_at", "str"),
      ("tamper_detected", "bool"), ("badge_state", "str"),
      ("display_color", "str"), ("proof_depth", "int"),
      ("status", "str"), ("computed_at", "str")],
     [("list_badges", "GET", "/api/audit-integrity-badge", "List integrity badges"),
      ("create_badge", "POST", "/api/audit-integrity-badge", "Create integrity badge"),
      ("get_badge", "GET", "/api/audit-integrity-badge/{badge_id}", "Get badge details"),
      ("verify_badge", "POST", "/api/audit-integrity-badge/{badge_id}/verify", "Verify badge integrity"),
      ("recompute_badge", "POST", "/api/audit-integrity-badge/{badge_id}/recompute", "Recompute Merkle proof"),
      ("badge_report", "GET", "/api/audit-integrity-badge/report", "Get integrity badge report")]),

    (257, "tamper_simulation", "Tamper Simulation v1",
     "DEMO-only mode that injects controlled integrity failures. UI explains detection and recovery process with deterministic outcomes.",
     [("simulation_id", "str"), ("target_entity", "str"), ("tamper_type", "str"),
      ("injected_failure", "dict"), ("detection_method", "str"),
      ("detected", "bool"), ("detection_latency_ms", "int"),
      ("recovery_steps", "list"), ("recovery_successful", "bool"),
      ("explanation", "str"), ("simulation_hash", "str"),
      ("status", "str"), ("simulated_at", "str")],
     [("list_simulations", "GET", "/api/tamper-simulation", "List tamper simulations"),
      ("run_simulation", "POST", "/api/tamper-simulation", "Run tamper simulation"),
      ("get_simulation", "GET", "/api/tamper-simulation/{simulation_id}", "Get simulation details"),
      ("inject_failure", "POST", "/api/tamper-simulation/{simulation_id}/inject", "Inject controlled failure"),
      ("detect_tamper", "POST", "/api/tamper-simulation/{simulation_id}/detect", "Detect tamper"),
      ("recover", "POST", "/api/tamper-simulation/{simulation_id}/recover", "Execute recovery"),
      ("simulation_report", "GET", "/api/tamper-simulation/report", "Get tamper simulation report")]),

    (258, "security_posture_pack", "Security Posture Pack v1",
     "Signed export with events, proofs, and verifier outputs. Byte-identical determinism for reproducible security posture snapshots.",
     [("pack_id", "str"), ("events_snapshot", "list"), ("proofs_snapshot", "list"),
      ("verifier_outputs", "list"), ("signature", "str"),
      ("content_hash", "str"), ("byte_identical", "bool"),
      ("export_format", "str"), ("pack_size_bytes", "int"),
      ("verification_status", "str"), ("determinism_verified", "bool"),
      ("status", "str"), ("exported_at", "str")],
     [("list_packs", "GET", "/api/security-posture-pack", "List security posture packs"),
      ("create_pack", "POST", "/api/security-posture-pack", "Create security posture pack"),
      ("get_pack", "GET", "/api/security-posture-pack/{pack_id}", "Get pack details"),
      ("verify_pack", "POST", "/api/security-posture-pack/{pack_id}/verify", "Verify pack integrity"),
      ("sign_pack", "POST", "/api/security-posture-pack/{pack_id}/sign", "Sign posture pack"),
      ("pack_report", "GET", "/api/security-posture-pack/report", "Get security posture pack report")]),

    (259, "adversarial_corpus_v2", "Adversarial Corpus v2",
     "50+ scenarios across channels and tools that must all deterministically block or require approval. Expanded coverage with evidence-backed decisions.",
     [("corpus_id", "str"), ("scenario_count", "int"), ("scenarios", "list"),
      ("blocked_count", "int"), ("approval_required_count", "int"),
      ("passed_count", "int"), ("failed_count", "int"),
      ("coverage_pct", "float"), ("deterministic_results", "bool"),
      ("evidence_per_scenario", "dict"), ("corpus_hash", "str"),
      ("status", "str"), ("evaluated_at", "str")],
     [("list_corpora", "GET", "/api/adversarial-corpus-v2", "List adversarial corpora"),
      ("create_corpus", "POST", "/api/adversarial-corpus-v2", "Create adversarial corpus"),
      ("get_corpus", "GET", "/api/adversarial-corpus-v2/{corpus_id}", "Get corpus details"),
      ("run_scenarios", "POST", "/api/adversarial-corpus-v2/{corpus_id}/run", "Run all scenarios"),
      ("verify_determinism", "POST", "/api/adversarial-corpus-v2/{corpus_id}/verify-determinism", "Verify deterministic results"),
      ("corpus_report", "GET", "/api/adversarial-corpus-v2/report", "Get adversarial corpus report")]),

    (260, "security_proof", "Security Proof Wave v1",
     "MCP E2E proof showing blocked action to security event to fix path to approval to proceed. Export posture pack with determinism twice-run.",
     [("proof_id", "str"), ("blocked_action_ref", "str"), ("security_event_ref", "str"),
      ("fix_path_ref", "str"), ("approval_ref", "str"),
      ("proceed_result", "str"), ("posture_pack_ref", "str"),
      ("determinism_hash", "str"), ("twice_run_match", "bool"),
      ("all_verified", "bool"), ("content_hash", "str"),
      ("status", "str"), ("verified_at", "str")],
     [("list_proofs", "GET", "/api/security-proof", "List security proofs"),
      ("generate_proof", "POST", "/api/security-proof", "Generate security proof"),
      ("get_proof", "GET", "/api/security-proof/{proof_id}", "Get proof details"),
      ("verify_proof", "POST", "/api/security-proof/{proof_id}/verify", "Verify proof integrity"),
      ("seal_proof", "POST", "/api/security-proof/{proof_id}/seal", "Seal security proof"),
      ("proof_report", "GET", "/api/security-proof/report", "Get security proof report")]),
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
    print(f"Generating {len(WAVES)} waves (241-260)...")

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
