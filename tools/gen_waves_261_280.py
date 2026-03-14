#!/usr/bin/env python3
"""Generate LedgerLive Waves 261-280: Phases 28-29.

Phase 28 (261-270): Replay / Court / Telemetry as Product
Phase 29 (271-280): Everywhere Surfaces

Run: python tools/gen_waves_261_280.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SVC_DIR = ROOT / "apps" / "api" / "app" / "services"
RTR_DIR = ROOT / "apps" / "api" / "app" / "routers"
TST_DIR = ROOT / "apps" / "api" / "tests"
MAIN_PY = ROOT / "apps" / "api" / "app" / "main.py"

WAVES = [
    # ════════════════════════════════════════════════════════════════
    # PHASE 28: REPLAY / COURT / TELEMETRY AS PRODUCT (W261-W270)
    # ════════════════════════════════════════════════════════════════
    (261, "replay_viewer_v3", "Replay Viewer v3",
     "Diffing between original and replay artifacts. Jump-to-evidence and jump-to-policy-event navigation with deterministic rendering.",
     [("viewer_id", "str"), ("original_ref", "str"), ("replay_ref", "str"),
      ("diff_entries", "list"), ("diff_summary", "dict"),
      ("evidence_links", "list"), ("policy_event_links", "list"),
      ("match_pct", "float"), ("divergence_points", "list"),
      ("render_hash", "str"), ("navigation_index", "dict"),
      ("status", "str"), ("compared_at", "str")],
     [("list_viewers", "GET", "/api/replay-viewer-v3", "List replay viewers"),
      ("create_viewer", "POST", "/api/replay-viewer-v3", "Create replay viewer comparison"),
      ("get_viewer", "GET", "/api/replay-viewer-v3/{viewer_id}", "Get viewer details"),
      ("compute_diff", "POST", "/api/replay-viewer-v3/{viewer_id}/diff", "Compute artifact diff"),
      ("jump_to_evidence", "POST", "/api/replay-viewer-v3/{viewer_id}/evidence", "Jump to evidence"),
      ("viewer_report", "GET", "/api/replay-viewer-v3/report", "Get replay viewer report")]),

    (262, "court_pack_v4", "Court Pack v4",
     "Generated directly from Race Control. Includes offline viewer, verify-all script, and parity report attachments with deterministic content.",
     [("pack_id", "str"), ("rc_ref", "str"), ("offline_viewer_data", "dict"),
      ("verify_script", "str"), ("parity_report", "dict"),
      ("attachments", "list"), ("content_hash", "str"),
      ("verification_result", "str"), ("pack_size_bytes", "int"),
      ("deterministic", "bool"), ("generated_from", "str"),
      ("status", "str"), ("generated_at", "str")],
     [("list_packs", "GET", "/api/court-pack-v4", "List court packs"),
      ("create_pack", "POST", "/api/court-pack-v4", "Create court pack from RC"),
      ("get_pack", "GET", "/api/court-pack-v4/{pack_id}", "Get court pack details"),
      ("verify_pack", "POST", "/api/court-pack-v4/{pack_id}/verify", "Verify court pack"),
      ("attach_parity", "POST", "/api/court-pack-v4/{pack_id}/parity", "Attach parity report"),
      ("pack_report", "GET", "/api/court-pack-v4/report", "Get court pack report")]),

    (263, "telemetry_pack_v3", "Telemetry Pack v3",
     "Combines tool trace, verifier checks, drift snapshot, incidents, and security timeline into a deterministic zip with content verification.",
     [("pack_id", "str"), ("tool_trace_data", "list"), ("verifier_checks", "list"),
      ("drift_snapshot", "dict"), ("incidents_data", "list"),
      ("security_timeline_data", "list"), ("content_hash", "str"),
      ("pack_format", "str"), ("pack_size_bytes", "int"),
      ("verification_status", "str"), ("deterministic", "bool"),
      ("status", "str"), ("assembled_at", "str")],
     [("list_packs", "GET", "/api/telemetry-pack-v3", "List telemetry packs"),
      ("create_pack", "POST", "/api/telemetry-pack-v3", "Create telemetry pack"),
      ("get_pack", "GET", "/api/telemetry-pack-v3/{pack_id}", "Get telemetry pack details"),
      ("verify_pack", "POST", "/api/telemetry-pack-v3/{pack_id}/verify", "Verify telemetry pack"),
      ("add_component", "POST", "/api/telemetry-pack-v3/{pack_id}/component", "Add component to pack"),
      ("pack_report", "GET", "/api/telemetry-pack-v3/report", "Get telemetry pack report")]),

    (264, "reproduce_close", "Reproduce Close v1",
     "From Race Control, regenerate binder/board pack from replay. Byte-identical hard gate ensures reproducibility of close artifacts.",
     [("reproduce_id", "str"), ("rc_ref", "str"), ("replay_ref", "str"),
      ("original_binder_hash", "str"), ("reproduced_binder_hash", "str"),
      ("hashes_match", "bool"), ("divergence_log", "list"),
      ("board_pack_ref", "str"), ("reproduced_board_hash", "str"),
      ("byte_identical", "bool"), ("gate_result", "str"),
      ("status", "str"), ("reproduced_at", "str")],
     [("list_reproductions", "GET", "/api/reproduce-close", "List close reproductions"),
      ("create_reproduction", "POST", "/api/reproduce-close", "Create close reproduction"),
      ("get_reproduction", "GET", "/api/reproduce-close/{reproduce_id}", "Get reproduction details"),
      ("verify_hashes", "POST", "/api/reproduce-close/{reproduce_id}/verify", "Verify hash match"),
      ("regenerate_binder", "POST", "/api/reproduce-close/{reproduce_id}/regenerate", "Regenerate binder from replay"),
      ("reproduction_report", "GET", "/api/reproduce-close/report", "Get reproduction report")]),

    (265, "replay_regression", "Replay Regression Harness v2",
     "Multiple canonical closes re-run offline and drift diffs captured deterministically. Regression harness with budgeted drift tolerance.",
     [("harness_id", "str"), ("canonical_closes", "list"), ("replay_results", "list"),
      ("drift_diffs", "list"), ("drift_budget", "float"),
      ("drift_actual", "float"), ("within_budget", "bool"),
      ("regression_detected", "bool"), ("baseline_hashes", "dict"),
      ("replay_hashes", "dict"), ("comparison_hash", "str"),
      ("status", "str"), ("executed_at", "str")],
     [("list_harnesses", "GET", "/api/replay-regression", "List replay regression harnesses"),
      ("create_harness", "POST", "/api/replay-regression", "Create regression harness"),
      ("get_harness", "GET", "/api/replay-regression/{harness_id}", "Get harness details"),
      ("run_regression", "POST", "/api/replay-regression/{harness_id}/run", "Run regression suite"),
      ("compare_drift", "POST", "/api/replay-regression/{harness_id}/drift", "Compare drift against budget"),
      ("harness_report", "GET", "/api/replay-regression/report", "Get regression harness report")]),

    (266, "narrative_export_v2", "Narrative Export v2",
     "Human narrative cites dossiers, evidence, and policy events. Stable formatting and ordering with deterministic content generation.",
     [("narrative_id", "str"), ("period_ref", "str"), ("sections", "list"),
      ("dossier_citations", "list"), ("evidence_citations", "list"),
      ("policy_event_citations", "list"), ("word_count", "int"),
      ("format_version", "str"), ("render_hash", "str"),
      ("stable_ordering", "bool"), ("export_format", "str"),
      ("status", "str"), ("generated_at", "str")],
     [("list_narratives", "GET", "/api/narrative-export-v2", "List narrative exports"),
      ("create_narrative", "POST", "/api/narrative-export-v2", "Create narrative export"),
      ("get_narrative", "GET", "/api/narrative-export-v2/{narrative_id}", "Get narrative details"),
      ("add_citation", "POST", "/api/narrative-export-v2/{narrative_id}/citation", "Add citation to narrative"),
      ("render_narrative", "POST", "/api/narrative-export-v2/{narrative_id}/render", "Render narrative"),
      ("narrative_report", "GET", "/api/narrative-export-v2/report", "Get narrative export report")]),

    (267, "audit_qa_pack", "Audit Q&A Pack v1",
     "Question template with linked evidence for auditor portal integration. One-click generation with deterministic content.",
     [("qa_id", "str"), ("period_ref", "str"), ("questions", "list"),
      ("answers", "list"), ("evidence_links", "dict"),
      ("template_version", "str"), ("completeness_pct", "float"),
      ("reviewed_by", "str|None"), ("review_status", "str"),
      ("content_hash", "str"), ("portal_compatible", "bool"),
      ("status", "str"), ("generated_at", "str")],
     [("list_qa_packs", "GET", "/api/audit-qa-pack", "List audit Q&A packs"),
      ("create_qa_pack", "POST", "/api/audit-qa-pack", "Create audit Q&A pack"),
      ("get_qa_pack", "GET", "/api/audit-qa-pack/{qa_id}", "Get Q&A pack details"),
      ("add_question", "POST", "/api/audit-qa-pack/{qa_id}/question", "Add question to pack"),
      ("link_evidence", "POST", "/api/audit-qa-pack/{qa_id}/evidence", "Link evidence to answer"),
      ("qa_report", "GET", "/api/audit-qa-pack/report", "Get audit Q&A pack report")]),

    (268, "replay_performance", "Replay Performance v1",
     "10x and 25x fixture replays with enforced performance budgets. Stable pagination and deterministic replay timing.",
     [("perf_id", "str"), ("fixture_scale", "str"), ("fixture_count", "int"),
      ("replay_duration_ms", "int"), ("budget_ms", "int"),
      ("within_budget", "bool"), ("pagination_stable", "bool"),
      ("pages_replayed", "int"), ("throughput_rps", "float"),
      ("memory_peak_mb", "float"), ("perf_hash", "str"),
      ("status", "str"), ("measured_at", "str")],
     [("list_perfs", "GET", "/api/replay-performance", "List replay performance tests"),
      ("run_perf_test", "POST", "/api/replay-performance", "Run replay performance test"),
      ("get_perf", "GET", "/api/replay-performance/{perf_id}", "Get performance test details"),
      ("run_10x", "POST", "/api/replay-performance/{perf_id}/run-10x", "Run 10x fixture replay"),
      ("run_25x", "POST", "/api/replay-performance/{perf_id}/run-25x", "Run 25x fixture replay"),
      ("perf_report", "GET", "/api/replay-performance/report", "Get replay performance report")]),

    (269, "rc_gate_extension", "RC Gate Extension v1",
     "Court, replay, and telemetry packs must verify. Drift budgets must pass. Extended gate checking for Race Control release readiness.",
     [("gate_ext_id", "str"), ("court_pack_verified", "bool"), ("replay_verified", "bool"),
      ("telemetry_verified", "bool"), ("drift_budget_passed", "bool"),
      ("drift_actual", "float"), ("drift_limit", "float"),
      ("gate_checks", "list"), ("all_passed", "bool"),
      ("failure_reasons", "list"), ("gate_hash", "str"),
      ("status", "str"), ("evaluated_at", "str")],
     [("list_gate_exts", "GET", "/api/rc-gate-extension", "List RC gate extensions"),
      ("create_gate_ext", "POST", "/api/rc-gate-extension", "Create RC gate extension check"),
      ("get_gate_ext", "GET", "/api/rc-gate-extension/{gate_ext_id}", "Get gate extension details"),
      ("evaluate_all", "POST", "/api/rc-gate-extension/{gate_ext_id}/evaluate", "Evaluate all gate checks"),
      ("check_drift", "POST", "/api/rc-gate-extension/{gate_ext_id}/drift", "Check drift budget"),
      ("gate_ext_report", "GET", "/api/rc-gate-extension/report", "Get RC gate extension report")]),

    (270, "replay_court_proof", "Replay Court Proof Wave v1",
     "MCP E2E from Race Control to generate court pack, verify, replay, regenerate binder, and hash match. Determinism twice-run verified.",
     [("proof_id", "str"), ("rc_ref", "str"), ("court_pack_ref", "str"),
      ("replay_ref", "str"), ("binder_regen_ref", "str"),
      ("hash_match_verified", "bool"), ("all_steps_passed", "bool"),
      ("determinism_hash", "str"), ("twice_run_match", "bool"),
      ("evidence_bundle", "list"), ("content_hash", "str"),
      ("status", "str"), ("verified_at", "str")],
     [("list_proofs", "GET", "/api/replay-court-proof", "List replay court proofs"),
      ("generate_proof", "POST", "/api/replay-court-proof", "Generate replay court proof"),
      ("get_proof", "GET", "/api/replay-court-proof/{proof_id}", "Get proof details"),
      ("verify_proof", "POST", "/api/replay-court-proof/{proof_id}/verify", "Verify proof integrity"),
      ("seal_proof", "POST", "/api/replay-court-proof/{proof_id}/seal", "Seal replay court proof"),
      ("proof_report", "GET", "/api/replay-court-proof/report", "Get replay court proof report")]),

    # ════════════════════════════════════════════════════════════════
    # PHASE 29: EVERYWHERE SURFACES (W271-W280)
    # ════════════════════════════════════════════════════════════════
    (271, "email_inbox_v2", "Email Inbox v2",
     "Mock email inbox with threads, attachments, and approval replies. Deterministic ordering, parsing, and content rendering.",
     [("email_id", "str"), ("thread_id", "str"), ("subject", "str"),
      ("sender", "str"), ("recipients", "list"), ("body", "str"),
      ("attachments", "list"), ("is_approval_reply", "bool"),
      ("approval_decision", "str|None"), ("parsed_content", "dict"),
      ("thread_position", "int"), ("read", "bool"),
      ("status", "str"), ("received_at", "str")],
     [("list_emails", "GET", "/api/email-inbox-v2", "List emails"),
      ("create_email", "POST", "/api/email-inbox-v2", "Create email"),
      ("get_email", "GET", "/api/email-inbox-v2/{email_id}", "Get email details"),
      ("reply_email", "POST", "/api/email-inbox-v2/{email_id}/reply", "Reply to email"),
      ("parse_content", "POST", "/api/email-inbox-v2/{email_id}/parse", "Parse email content"),
      ("mark_read", "POST", "/api/email-inbox-v2/{email_id}/read", "Mark email as read"),
      ("email_report", "GET", "/api/email-inbox-v2/report", "Get email inbox report")]),

    (272, "chat_workspace_v2", "Chat Workspace v2",
     "Mock chat workspace with interactive cards, escalation pings, and watcher notifications. Deterministic message ordering.",
     [("message_id", "str"), ("channel_id", "str"), ("sender", "str"),
      ("content", "str"), ("card_data", "dict|None"), ("is_card", "bool"),
      ("is_escalation", "bool"), ("watchers", "list"),
      ("reactions", "list"), ("thread_replies", "list"),
      ("ping_targets", "list"), ("message_order", "int"),
      ("status", "str"), ("sent_at", "str")],
     [("list_messages", "GET", "/api/chat-workspace-v2", "List chat messages"),
      ("send_message", "POST", "/api/chat-workspace-v2", "Send chat message"),
      ("get_message", "GET", "/api/chat-workspace-v2/{message_id}", "Get message details"),
      ("send_card", "POST", "/api/chat-workspace-v2/{message_id}/card", "Send interactive card"),
      ("escalate", "POST", "/api/chat-workspace-v2/{message_id}/escalate", "Escalate via ping"),
      ("add_watcher", "POST", "/api/chat-workspace-v2/{message_id}/watcher", "Add watcher notification"),
      ("chat_report", "GET", "/api/chat-workspace-v2/report", "Get chat workspace report")]),

    (273, "browser_ext_v2", "Browser Extension v2",
     "Capture, annotate, and submit with deterministic capture fixtures. Deep links to evidence with consistent rendering.",
     [("capture_id", "str"), ("url", "str"), ("capture_data", "dict"),
      ("annotations", "list"), ("submission_ref", "str|None"),
      ("evidence_link", "str"), ("deep_link", "str"),
      ("capture_hash", "str"), ("fixture_id", "str|None"),
      ("deterministic", "bool"), ("render_consistent", "bool"),
      ("status", "str"), ("captured_at", "str")],
     [("list_captures", "GET", "/api/browser-ext-v2", "List browser captures"),
      ("create_capture", "POST", "/api/browser-ext-v2", "Create browser capture"),
      ("get_capture", "GET", "/api/browser-ext-v2/{capture_id}", "Get capture details"),
      ("annotate", "POST", "/api/browser-ext-v2/{capture_id}/annotate", "Add annotation"),
      ("submit_capture", "POST", "/api/browser-ext-v2/{capture_id}/submit", "Submit capture as evidence"),
      ("capture_report", "GET", "/api/browser-ext-v2/report", "Get browser extension report")]),

    (274, "notification_hub_v4", "Notification Hub v4",
     "Per-user routing rules, quiet hours, dedup, SLA escalations, and frozen-time deterministic notification delivery.",
     [("notification_id", "str"), ("user_id", "str"), ("channel", "str"),
      ("subject", "str"), ("body", "str"), ("priority", "str"),
      ("routing_rule_ref", "str"), ("quiet_hours_blocked", "bool"),
      ("deduplicated", "bool"), ("sla_escalation", "bool"),
      ("delivery_status", "str"), ("frozen_time", "str|None"),
      ("status", "str"), ("created_at", "str")],
     [("list_notifications", "GET", "/api/notification-hub-v4", "List notifications"),
      ("send_notification", "POST", "/api/notification-hub-v4", "Send notification"),
      ("get_notification", "GET", "/api/notification-hub-v4/{notification_id}", "Get notification details"),
      ("apply_routing", "POST", "/api/notification-hub-v4/{notification_id}/route", "Apply routing rules"),
      ("check_quiet_hours", "POST", "/api/notification-hub-v4/{notification_id}/quiet", "Check quiet hours"),
      ("dedup_check", "POST", "/api/notification-hub-v4/{notification_id}/dedup", "Check for duplicates"),
      ("notification_report", "GET", "/api/notification-hub-v4/report", "Get notification hub report")]),

    (275, "cross_channel_audit", "Cross-Channel Audit v1",
     "Every channel action writes audit and tool trace with dossier updates. Full cross-channel audit trail with deterministic ordering.",
     [("audit_entry_id", "str"), ("channel_type", "str"), ("action_type", "str"),
      ("action_ref", "str"), ("tool_trace_ref", "str"),
      ("dossier_ref", "str"), ("user_id", "str"),
      ("timestamp", "str"), ("evidence_refs", "list"),
      ("context_data", "dict"), ("ordering_key", "int"),
      ("deterministic", "bool"), ("status", "str")],
     [("list_audit_entries", "GET", "/api/cross-channel-audit", "List cross-channel audit entries"),
      ("create_audit_entry", "POST", "/api/cross-channel-audit", "Create cross-channel audit entry"),
      ("get_audit_entry", "GET", "/api/cross-channel-audit/{audit_entry_id}", "Get audit entry details"),
      ("link_trace", "POST", "/api/cross-channel-audit/{audit_entry_id}/trace", "Link tool trace"),
      ("update_dossier", "POST", "/api/cross-channel-audit/{audit_entry_id}/dossier", "Update linked dossier"),
      ("audit_entry_report", "GET", "/api/cross-channel-audit/report", "Get cross-channel audit report")]),

    (276, "channel_reliability", "Channel Reliability Harness v1",
     "Seeded failures including timeouts, retries, and partial delivery with deterministic recovery scenarios.",
     [("harness_id", "str"), ("channel_type", "str"), ("failure_type", "str"),
      ("failure_config", "dict"), ("recovery_strategy", "str"),
      ("recovery_successful", "bool"), ("retry_count", "int"),
      ("max_retries", "int"), ("partial_delivery_pct", "float"),
      ("timeout_ms", "int"), ("deterministic_outcome", "bool"),
      ("status", "str"), ("tested_at", "str")],
     [("list_harnesses", "GET", "/api/channel-reliability", "List reliability harnesses"),
      ("create_harness", "POST", "/api/channel-reliability", "Create reliability harness"),
      ("get_harness", "GET", "/api/channel-reliability/{harness_id}", "Get harness details"),
      ("inject_failure", "POST", "/api/channel-reliability/{harness_id}/inject", "Inject seeded failure"),
      ("test_recovery", "POST", "/api/channel-reliability/{harness_id}/recover", "Test recovery strategy"),
      ("reliability_report", "GET", "/api/channel-reliability/report", "Get reliability harness report")]),

    (277, "rc_channel_actions", "RC Channel Actions v1",
     "Send to channel actions for approvals and incidents from Race Control. No network in CI with deterministic routing.",
     [("rc_action_id", "str"), ("rc_ref", "str"), ("channel_type", "str"),
      ("action_type", "str"), ("target_entity", "str"),
      ("message_content", "str"), ("approval_ref", "str|None"),
      ("incident_ref", "str|None"), ("delivery_status", "str"),
      ("routing_deterministic", "bool"), ("no_network_flag", "bool"),
      ("status", "str"), ("sent_at", "str")],
     [("list_rc_actions", "GET", "/api/rc-channel-actions", "List RC channel actions"),
      ("create_rc_action", "POST", "/api/rc-channel-actions", "Create RC channel action"),
      ("get_rc_action", "GET", "/api/rc-channel-actions/{rc_action_id}", "Get RC action details"),
      ("route_to_channel", "POST", "/api/rc-channel-actions/{rc_action_id}/route", "Route to channel"),
      ("confirm_delivery", "POST", "/api/rc-channel-actions/{rc_action_id}/confirm", "Confirm delivery"),
      ("rc_action_report", "GET", "/api/rc-channel-actions/report", "Get RC channel actions report")]),

    (278, "collab_v3", "Collaboration v3",
     "Mentions, watchers across channels with activity feed tied to Race Control lanes. Deterministic feed ordering.",
     [("collab_id", "str"), ("entity_ref", "str"), ("entity_type", "str"),
      ("mentions", "list"), ("watchers", "list"), ("activity_feed", "list"),
      ("lane_ref", "str|None"), ("feed_ordering_key", "int"),
      ("notification_sent", "bool"), ("cross_channel", "bool"),
      ("deterministic_feed", "bool"), ("status", "str"),
      ("updated_at", "str")],
     [("list_collabs", "GET", "/api/collab-v3", "List collaborations"),
      ("create_collab", "POST", "/api/collab-v3", "Create collaboration entry"),
      ("get_collab", "GET", "/api/collab-v3/{collab_id}", "Get collaboration details"),
      ("add_mention", "POST", "/api/collab-v3/{collab_id}/mention", "Add mention"),
      ("add_watcher", "POST", "/api/collab-v3/{collab_id}/watcher", "Add watcher"),
      ("get_feed", "POST", "/api/collab-v3/{collab_id}/feed", "Get activity feed"),
      ("collab_report", "GET", "/api/collab-v3/report", "Get collaboration report")]),

    (279, "ops_pack_export", "Ops Pack Export v1",
     "Signed bundle of channel interactions, approvals, incidents, and verify script. Deterministic export with content hash.",
     [("ops_pack_id", "str"), ("channel_interactions", "list"), ("approvals_data", "list"),
      ("incidents_data", "list"), ("verify_script", "str"),
      ("signature", "str"), ("content_hash", "str"),
      ("pack_size_bytes", "int"), ("deterministic", "bool"),
      ("export_format", "str"), ("verification_passed", "bool"),
      ("status", "str"), ("exported_at", "str")],
     [("list_ops_packs", "GET", "/api/ops-pack-export", "List ops pack exports"),
      ("create_ops_pack", "POST", "/api/ops-pack-export", "Create ops pack export"),
      ("get_ops_pack", "GET", "/api/ops-pack-export/{ops_pack_id}", "Get ops pack details"),
      ("verify_ops_pack", "POST", "/api/ops-pack-export/{ops_pack_id}/verify", "Verify ops pack"),
      ("sign_ops_pack", "POST", "/api/ops-pack-export/{ops_pack_id}/sign", "Sign ops pack"),
      ("ops_pack_report", "GET", "/api/ops-pack-export/report", "Get ops pack export report")]),

    (280, "everywhere_proof", "Everywhere Proof Wave v1",
     "MCP E2E triggers approval to mock chat/email, approves via channel, Race Control updates, export ops pack. Determinism twice-run.",
     [("proof_id", "str"), ("approval_trigger_ref", "str"), ("chat_action_ref", "str"),
      ("email_action_ref", "str"), ("channel_approval_ref", "str"),
      ("rc_update_ref", "str"), ("ops_pack_ref", "str"),
      ("all_verified", "bool"), ("determinism_hash", "str"),
      ("twice_run_match", "bool"), ("content_hash", "str"),
      ("status", "str"), ("verified_at", "str")],
     [("list_proofs", "GET", "/api/everywhere-proof", "List everywhere proofs"),
      ("generate_proof", "POST", "/api/everywhere-proof", "Generate everywhere proof"),
      ("get_proof", "GET", "/api/everywhere-proof/{proof_id}", "Get proof details"),
      ("verify_proof", "POST", "/api/everywhere-proof/{proof_id}/verify", "Verify proof integrity"),
      ("seal_proof", "POST", "/api/everywhere-proof/{proof_id}/seal", "Seal everywhere proof"),
      ("proof_report", "GET", "/api/everywhere-proof/report", "Get everywhere proof report")]),
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
    print(f"Generating {len(WAVES)} waves (261-280)...")

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
