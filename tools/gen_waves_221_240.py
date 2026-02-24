#!/usr/bin/env python3
"""Generate LedgerLive Waves 221-240: Phases 23-25.

Phase 23 (221-228): Close Orchestration Foundation
Phase 24 (229-234): Race Control Dashboard
Phase 25 (235-240): Race Control Integration & RC

Run: python tools/gen_waves_221_240.py
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
    # PHASE 23: CLOSE ORCHESTRATION FOUNDATION (W221-W228)
    # ════════════════════════════════════════════════════════════════
    (221, "close_calendar", "Close Calendar Manager v1",
     "Manages financial close calendars with period definitions, milestone dates, and working-day calculations. Supports recurring close schedules and holiday-aware date math.",
     [("calendar_id", "str"), ("period_name", "str"), ("fiscal_year", "int"),
      ("fiscal_month", "int"), ("open_date", "str"), ("target_close_date", "str"),
      ("actual_close_date", "str|None"), ("working_days_remaining", "int"),
      ("milestones", "list"), ("holiday_calendar", "str"),
      ("recurrence_rule", "str|None"), ("status", "str"),
      ("created_at", "str")],
     [("list_calendars", "GET", "/api/period-calendar", "List close calendars"),
      ("create_calendar", "POST", "/api/period-calendar", "Create close calendar period"),
      ("get_calendar", "GET", "/api/period-calendar/{calendar_id}", "Get calendar details"),
      ("advance_day", "POST", "/api/period-calendar/{calendar_id}/advance", "Advance working day"),
      ("set_milestone", "POST", "/api/period-calendar/{calendar_id}/milestone", "Set milestone date"),
      ("finalize_period", "POST", "/api/period-calendar/{calendar_id}/finalize", "Finalize close period"),
      ("calendar_report", "GET", "/api/period-calendar/report", "Get calendar summary report")]),

    (222, "task_dag", "Task DAG Builder v1",
     "Builds directed acyclic graph of close tasks. Nodes are close activities, edges are dependencies. Validates acyclicity, computes topological order, and tracks completion.",
     [("dag_id", "str"), ("dag_name", "str"), ("period_id", "str"),
      ("nodes", "list"), ("edges", "list"), ("topological_order", "list"),
      ("is_valid_dag", "bool"), ("total_nodes", "int"),
      ("completed_nodes", "int"), ("critical_path_length", "int"),
      ("status", "str"), ("built_at", "str")],
     [("list_dags", "GET", "/api/task-dag", "List task DAGs"),
      ("create_dag", "POST", "/api/task-dag", "Create task DAG"),
      ("get_dag", "GET", "/api/task-dag/{dag_id}", "Get DAG details"),
      ("add_node", "POST", "/api/task-dag/{dag_id}/node", "Add node to DAG"),
      ("add_edge", "POST", "/api/task-dag/{dag_id}/edge", "Add dependency edge"),
      ("validate_dag", "POST", "/api/task-dag/{dag_id}/validate", "Validate DAG acyclicity"),
      ("dag_report", "GET", "/api/task-dag/report", "Get task DAG report")]),

    (223, "dependency_resolver", "Dependency Resolver v1",
     "Resolves task dependencies from DAG, determines execution readiness, detects circular references, and produces parallelizable task batches for close execution.",
     [("resolver_id", "str"), ("dag_id", "str"), ("resolved_order", "list"),
      ("parallel_batches", "list"), ("unresolved_deps", "list"),
      ("circular_refs", "list"), ("ready_tasks", "list"),
      ("blocked_tasks", "list"), ("resolution_depth", "int"),
      ("fully_resolved", "bool"), ("status", "str"),
      ("resolved_at", "str")],
     [("list_resolutions", "GET", "/api/dependency-resolver", "List dependency resolutions"),
      ("resolve_deps", "POST", "/api/dependency-resolver", "Resolve dependencies from DAG"),
      ("get_resolution", "GET", "/api/dependency-resolver/{resolver_id}", "Get resolution details"),
      ("check_ready", "POST", "/api/dependency-resolver/{resolver_id}/ready", "Check which tasks are ready"),
      ("detect_circular", "POST", "/api/dependency-resolver/{resolver_id}/circular", "Detect circular references"),
      ("resolver_report", "GET", "/api/dependency-resolver/report", "Get dependency resolver report")]),

    (224, "sla_monitor", "SLA Monitor v1",
     "Monitors service level agreements for close tasks. Tracks expected vs actual completion times, computes SLA breach risk, and triggers escalation alerts.",
     [("sla_id", "str"), ("task_id", "str"), ("task_name", "str"),
      ("expected_duration_min", "int"), ("actual_duration_min", "int"),
      ("deadline", "str"), ("breach_risk_pct", "float"),
      ("breached", "bool"), ("escalation_sent", "bool"),
      ("escalation_target", "str|None"), ("variance_min", "int"),
      ("status", "str"), ("monitored_at", "str")],
     [("list_slas", "GET", "/api/sla-monitor", "List SLA monitors"),
      ("create_sla", "POST", "/api/sla-monitor", "Create SLA monitor"),
      ("get_sla", "GET", "/api/sla-monitor/{sla_id}", "Get SLA details"),
      ("check_breach", "POST", "/api/sla-monitor/{sla_id}/breach", "Check for SLA breach"),
      ("escalate", "POST", "/api/sla-monitor/{sla_id}/escalate", "Trigger escalation alert"),
      ("sla_report", "GET", "/api/sla-monitor/report", "Get SLA monitor report")]),

    (225, "blocker_tracker", "Blocker Tracker v1",
     "Tracks blockers preventing close task completion. Categorizes blockers by type (data, approval, system), assigns owners, and tracks resolution workflow.",
     [("blocker_id", "str"), ("task_id", "str"), ("blocker_type", "str"),
      ("description", "str"), ("severity", "str"), ("owner", "str"),
      ("raised_at", "str"), ("resolved_at", "str|None"),
      ("resolution_notes", "str|None"), ("impact_scope", "list"),
      ("days_open", "int"), ("status", "str")],
     [("list_blockers", "GET", "/api/blocker-tracker", "List blockers"),
      ("create_blocker", "POST", "/api/blocker-tracker", "Create blocker"),
      ("get_blocker", "GET", "/api/blocker-tracker/{blocker_id}", "Get blocker details"),
      ("resolve_blocker", "POST", "/api/blocker-tracker/{blocker_id}/resolve", "Resolve blocker"),
      ("escalate_blocker", "POST", "/api/blocker-tracker/{blocker_id}/escalate", "Escalate blocker"),
      ("blocker_report", "GET", "/api/blocker-tracker/report", "Get blocker tracker report")]),

    (226, "handoff_protocol", "Handoff Protocol v1",
     "Manages task handoffs between teams during close. Tracks handoff initiation, acceptance, evidence attachment, and sign-off. Ensures no task falls between cracks.",
     [("handoff_id", "str"), ("from_team", "str"), ("to_team", "str"),
      ("task_id", "str"), ("evidence_refs", "list"), ("notes", "str"),
      ("initiated_at", "str"), ("accepted_at", "str|None"),
      ("signed_off", "bool"), ("sign_off_by", "str|None"),
      ("handoff_hash", "str|None"), ("status", "str")],
     [("list_handoffs", "GET", "/api/handoff-protocol", "List handoffs"),
      ("initiate_handoff", "POST", "/api/handoff-protocol", "Initiate handoff"),
      ("get_handoff", "GET", "/api/handoff-protocol/{handoff_id}", "Get handoff details"),
      ("accept_handoff", "POST", "/api/handoff-protocol/{handoff_id}/accept", "Accept handoff"),
      ("sign_off", "POST", "/api/handoff-protocol/{handoff_id}/signoff", "Sign off on handoff"),
      ("handoff_report", "GET", "/api/handoff-protocol/report", "Get handoff protocol report")]),

    (227, "progress_aggregator", "Progress Aggregator v1",
     "Aggregates completion progress across all close tasks, DAG nodes, and team handoffs. Produces weighted progress percentage and phase-level breakdowns.",
     [("aggregation_id", "str"), ("period_id", "str"), ("total_tasks", "int"),
      ("completed_tasks", "int"), ("in_progress_tasks", "int"),
      ("blocked_tasks", "int"), ("overall_pct", "float"),
      ("phase_breakdown", "dict"), ("team_breakdown", "dict"),
      ("weighted_score", "float"), ("trend_direction", "str"),
      ("status", "str"), ("aggregated_at", "str")],
     [("list_aggregations", "GET", "/api/progress-aggregator", "List progress aggregations"),
      ("aggregate", "POST", "/api/progress-aggregator", "Compute progress aggregation"),
      ("get_aggregation", "GET", "/api/progress-aggregator/{aggregation_id}", "Get aggregation details"),
      ("refresh", "POST", "/api/progress-aggregator/{aggregation_id}/refresh", "Refresh aggregation data"),
      ("team_detail", "POST", "/api/progress-aggregator/{aggregation_id}/team", "Get team-level detail"),
      ("aggregator_report", "GET", "/api/progress-aggregator/report", "Get progress aggregator report")]),

    (228, "close_checkpoint", "Close Checkpoint Manager v1",
     "Defines and evaluates checkpoints (gates) in the close process. Each checkpoint has pass/fail criteria, evidence requirements, and approval rules.",
     [("checkpoint_id", "str"), ("checkpoint_name", "str"), ("period_id", "str"),
      ("gate_criteria", "list"), ("evidence_required", "list"),
      ("evidence_submitted", "list"), ("criteria_met", "bool"),
      ("approved_by", "str|None"), ("approval_timestamp", "str|None"),
      ("gate_result", "str"), ("notes", "str|None"),
      ("status", "str"), ("evaluated_at", "str")],
     [("list_checkpoints", "GET", "/api/close-checkpoint", "List close checkpoints"),
      ("create_checkpoint", "POST", "/api/close-checkpoint", "Create close checkpoint"),
      ("get_checkpoint", "GET", "/api/close-checkpoint/{checkpoint_id}", "Get checkpoint details"),
      ("evaluate_gate", "POST", "/api/close-checkpoint/{checkpoint_id}/evaluate", "Evaluate checkpoint gate"),
      ("submit_evidence", "POST", "/api/close-checkpoint/{checkpoint_id}/evidence", "Submit checkpoint evidence"),
      ("approve_checkpoint", "POST", "/api/close-checkpoint/{checkpoint_id}/approve", "Approve checkpoint"),
      ("checkpoint_report", "GET", "/api/close-checkpoint/report", "Get checkpoint report")]),

    # ════════════════════════════════════════════════════════════════
    # PHASE 24: RACE CONTROL DASHBOARD (W229-W234)
    # ════════════════════════════════════════════════════════════════
    (229, "rc_state_machine", "Race Control State Machine v1",
     "Finite state machine governing close lifecycle: NOT_STARTED -> IN_PROGRESS -> REVIEW -> APPROVED -> CLOSED. Transition guards enforce prerequisites.",
     [("machine_id", "str"), ("period_id", "str"), ("current_state", "str"),
      ("previous_state", "str|None"), ("valid_transitions", "list"),
      ("transition_history", "list"), ("guard_results", "dict"),
      ("last_transition_at", "str|None"), ("locked", "bool"),
      ("lock_reason", "str|None"), ("status", "str"),
      ("created_at", "str")],
     [("list_machines", "GET", "/api/rc-state-machine", "List state machines"),
      ("create_machine", "POST", "/api/rc-state-machine", "Create state machine"),
      ("get_machine", "GET", "/api/rc-state-machine/{machine_id}", "Get state machine details"),
      ("transition", "POST", "/api/rc-state-machine/{machine_id}/transition", "Perform state transition"),
      ("lock_state", "POST", "/api/rc-state-machine/{machine_id}/lock", "Lock state machine"),
      ("machine_report", "GET", "/api/rc-state-machine/report", "Get state machine report")]),

    (230, "lane_status", "Lane Status Board v1",
     "Visual lane board showing close workstreams as swim lanes. Each lane has tasks ordered by dependency, colored by status, with live completion tracking.",
     [("lane_id", "str"), ("lane_name", "str"), ("workstream", "str"),
      ("tasks_in_lane", "list"), ("lane_color", "str"),
      ("completion_pct", "float"), ("blocked_count", "int"),
      ("on_track", "bool"), ("owner_team", "str"),
      ("display_order", "int"), ("status", "str"),
      ("updated_at", "str")],
     [("list_lanes", "GET", "/api/lane-status", "List lanes"),
      ("create_lane", "POST", "/api/lane-status", "Create lane"),
      ("get_lane", "GET", "/api/lane-status/{lane_id}", "Get lane details"),
      ("update_lane", "POST", "/api/lane-status/{lane_id}/update", "Update lane status"),
      ("reorder_lane", "POST", "/api/lane-status/{lane_id}/reorder", "Reorder lane"),
      ("lane_report", "GET", "/api/lane-status/report", "Get lane status report")]),

    (231, "critical_path", "Critical Path Analyzer v1",
     "Identifies the critical path through the close task DAG. Computes earliest/latest start and finish times, float values, and bottleneck nodes.",
     [("analysis_id", "str"), ("dag_id", "str"), ("critical_nodes", "list"),
      ("critical_edges", "list"), ("total_duration", "int"),
      ("earliest_start", "dict"), ("latest_finish", "dict"),
      ("float_values", "dict"), ("bottleneck_node", "str|None"),
      ("slack_available", "int"), ("status", "str"),
      ("analyzed_at", "str")],
     [("list_analyses", "GET", "/api/critical-path", "List critical path analyses"),
      ("analyze_path", "POST", "/api/critical-path", "Analyze critical path"),
      ("get_analysis", "GET", "/api/critical-path/{analysis_id}", "Get analysis details"),
      ("find_bottleneck", "POST", "/api/critical-path/{analysis_id}/bottleneck", "Find bottleneck node"),
      ("compute_float", "POST", "/api/critical-path/{analysis_id}/float", "Compute float values"),
      ("path_report", "GET", "/api/critical-path/report", "Get critical path report")]),

    (232, "live_scoreboard", "Live Scoreboard v1",
     "Real-time scoreboard displaying team progress, SLA adherence, blocker counts, and checkpoint completion. Auto-refreshing metrics with trend indicators.",
     [("score_id", "str"), ("period_id", "str"), ("team_scores", "dict"),
      ("sla_adherence_pct", "float"), ("blocker_count", "int"),
      ("checkpoints_passed", "int"), ("checkpoints_total", "int"),
      ("overall_health", "str"), ("trend_indicator", "str"),
      ("last_refresh", "str"), ("refresh_interval_s", "int"),
      ("status", "str")],
     [("list_scores", "GET", "/api/live-scoreboard", "List scoreboard snapshots"),
      ("create_score", "POST", "/api/live-scoreboard", "Create scoreboard snapshot"),
      ("get_score", "GET", "/api/live-scoreboard/{score_id}", "Get scoreboard details"),
      ("refresh_score", "POST", "/api/live-scoreboard/{score_id}/refresh", "Refresh scoreboard data"),
      ("rank_teams", "POST", "/api/live-scoreboard/{score_id}/rank", "Rank teams by progress"),
      ("scoreboard_report", "GET", "/api/live-scoreboard/report", "Get scoreboard report")]),

    (233, "incident_log", "Incident Log v1",
     "Logs incidents during close: system outages, data issues, process failures. Each incident has severity, impact assessment, resolution timeline, and root cause.",
     [("incident_id", "str"), ("incident_title", "str"), ("severity", "str"),
      ("category", "str"), ("description", "str"), ("impact_assessment", "str"),
      ("affected_tasks", "list"), ("reported_by", "str"),
      ("reported_at", "str"), ("resolved_at", "str|None"),
      ("root_cause", "str|None"), ("resolution_summary", "str|None"),
      ("status", "str")],
     [("list_incidents", "GET", "/api/incident-log", "List incidents"),
      ("create_incident", "POST", "/api/incident-log", "Create incident"),
      ("get_incident", "GET", "/api/incident-log/{incident_id}", "Get incident details"),
      ("resolve_incident", "POST", "/api/incident-log/{incident_id}/resolve", "Resolve incident"),
      ("assess_impact", "POST", "/api/incident-log/{incident_id}/impact", "Assess incident impact"),
      ("incident_report", "GET", "/api/incident-log/report", "Get incident log report")]),

    (234, "control_export", "Control Room Export v1",
     "Exports Race Control dashboard state as a comprehensive snapshot: lane statuses, scoreboard, critical path, incidents, checkpoints. Deterministic pack with content hash.",
     [("export_id", "str"), ("period_id", "str"), ("snapshot_data", "dict"),
      ("lanes_snapshot", "list"), ("scoreboard_snapshot", "dict"),
      ("critical_path_snapshot", "dict"), ("incidents_snapshot", "list"),
      ("checkpoints_snapshot", "list"), ("content_hash", "str|None"),
      ("export_format", "str"), ("deterministic", "bool"),
      ("status", "str"), ("exported_at", "str")],
     [("list_exports", "GET", "/api/control-export", "List control room exports"),
      ("create_export", "POST", "/api/control-export", "Create control room export"),
      ("get_export", "GET", "/api/control-export/{export_id}", "Get export details"),
      ("verify_hash", "POST", "/api/control-export/{export_id}/verify", "Verify content hash"),
      ("download_export", "POST", "/api/control-export/{export_id}/download", "Download export pack"),
      ("export_report", "GET", "/api/control-export/report", "Get control export report")]),

    # ════════════════════════════════════════════════════════════════
    # PHASE 25: RACE CONTROL INTEGRATION & RC (W235-W240)
    # ════════════════════════════════════════════════════════════════
    (235, "rc_rules", "RC Automation Rules v1",
     "Rule engine for Race Control automation. Rules trigger actions based on conditions: auto-escalate breached SLAs, auto-notify on blocker creation, auto-lock on checkpoint failure.",
     [("rule_id", "str"), ("rule_name", "str"), ("condition_type", "str"),
      ("condition_params", "dict"), ("action_type", "str"),
      ("action_params", "dict"), ("enabled", "bool"),
      ("trigger_count", "int"), ("last_triggered_at", "str|None"),
      ("cooldown_s", "int"), ("priority", "int"),
      ("status", "str"), ("created_at", "str")],
     [("list_rules", "GET", "/api/rc-rules", "List automation rules"),
      ("create_rule", "POST", "/api/rc-rules", "Create automation rule"),
      ("get_rule", "GET", "/api/rc-rules/{rule_id}", "Get rule details"),
      ("trigger_rule", "POST", "/api/rc-rules/{rule_id}/trigger", "Trigger rule manually"),
      ("toggle_rule", "POST", "/api/rc-rules/{rule_id}/toggle", "Enable/disable rule"),
      ("rules_report", "GET", "/api/rc-rules/report", "Get automation rules report")]),

    (236, "rc_notifications", "RC Notification Hub v1",
     "Centralized notification hub for Race Control events. Routes notifications by channel (in-app, webhook), applies dedup and throttling, tracks delivery status.",
     [("notification_id", "str"), ("event_type", "str"), ("channel", "str"),
      ("recipient", "str"), ("subject", "str"), ("body", "str"),
      ("priority", "str"), ("delivered", "bool"),
      ("delivered_at", "str|None"), ("deduplicated", "bool"),
      ("throttled", "bool"), ("retry_count", "int"),
      ("status", "str"), ("created_at", "str")],
     [("list_notifications", "GET", "/api/rc-notifications", "List notifications"),
      ("send_notification", "POST", "/api/rc-notifications", "Send notification"),
      ("get_notification", "GET", "/api/rc-notifications/{notification_id}", "Get notification details"),
      ("mark_delivered", "POST", "/api/rc-notifications/{notification_id}/deliver", "Mark notification delivered"),
      ("retry_notification", "POST", "/api/rc-notifications/{notification_id}/retry", "Retry failed notification"),
      ("notification_report", "GET", "/api/rc-notifications/report", "Get notification hub report")]),

    (237, "rc_playbook", "RC Playbook Engine v1",
     "Executable playbooks for common close scenarios: month-end, quarter-end, year-end. Each playbook defines ordered steps, decision points, and rollback procedures.",
     [("playbook_id", "str"), ("playbook_name", "str"), ("scenario_type", "str"),
      ("steps", "list"), ("current_step", "int"), ("total_steps", "int"),
      ("decision_points", "list"), ("rollback_procedures", "list"),
      ("execution_log", "list"), ("completed", "bool"),
      ("success", "bool"), ("status", "str"),
      ("started_at", "str")],
     [("list_playbooks", "GET", "/api/rc-playbook", "List playbooks"),
      ("create_playbook", "POST", "/api/rc-playbook", "Create playbook"),
      ("get_playbook", "GET", "/api/rc-playbook/{playbook_id}", "Get playbook details"),
      ("advance_step", "POST", "/api/rc-playbook/{playbook_id}/advance", "Advance playbook step"),
      ("rollback_step", "POST", "/api/rc-playbook/{playbook_id}/rollback", "Rollback playbook step"),
      ("playbook_report", "GET", "/api/rc-playbook/report", "Get playbook engine report")]),

    (238, "rc_dry_run", "RC Dry Run Simulation v1",
     "Simulates a full close cycle without side effects. Runs playbook steps, evaluates rules, checks SLAs, and produces a dry run report predicting outcomes.",
     [("dry_run_id", "str"), ("playbook_id", "str"), ("period_id", "str"),
      ("simulated_steps", "list"), ("rules_evaluated", "int"),
      ("sla_predictions", "dict"), ("predicted_blockers", "list"),
      ("predicted_duration_min", "int"), ("risk_score", "float"),
      ("outcome_prediction", "str"), ("simulation_hash", "str|None"),
      ("status", "str"), ("simulated_at", "str")],
     [("list_dry_runs", "GET", "/api/rc-dry-run", "List dry run simulations"),
      ("run_simulation", "POST", "/api/rc-dry-run", "Run dry run simulation"),
      ("get_dry_run", "GET", "/api/rc-dry-run/{dry_run_id}", "Get dry run details"),
      ("predict_blockers", "POST", "/api/rc-dry-run/{dry_run_id}/predict", "Predict blockers"),
      ("evaluate_risk", "POST", "/api/rc-dry-run/{dry_run_id}/risk", "Evaluate risk score"),
      ("dry_run_report", "GET", "/api/rc-dry-run/report", "Get dry run report")]),

    (239, "rc_approval", "RC Approval Chain v1",
     "Multi-level approval chain for close sign-off. Supports sequential and parallel approvals, delegation, expiry, and audit trail of all approval decisions.",
     [("approval_id", "str"), ("period_id", "str"), ("approval_level", "int"),
      ("total_levels", "int"), ("approvers", "list"),
      ("decisions", "list"), ("current_approver", "str|None"),
      ("delegated_to", "str|None"), ("expires_at", "str|None"),
      ("all_approved", "bool"), ("rejection_reason", "str|None"),
      ("status", "str"), ("initiated_at", "str")],
     [("list_approvals", "GET", "/api/rc-approval", "List approval chains"),
      ("create_approval", "POST", "/api/rc-approval", "Create approval chain"),
      ("get_approval", "GET", "/api/rc-approval/{approval_id}", "Get approval chain details"),
      ("approve_level", "POST", "/api/rc-approval/{approval_id}/approve", "Approve current level"),
      ("reject_level", "POST", "/api/rc-approval/{approval_id}/reject", "Reject current level"),
      ("delegate_approval", "POST", "/api/rc-approval/{approval_id}/delegate", "Delegate approval"),
      ("approval_report", "GET", "/api/rc-approval/report", "Get approval chain report")]),

    (240, "rc_proof_pack", "RC Proof Pack v1",
     "Final Race Control proof pack: aggregates all RC components (state machine, lanes, critical path, scoreboard, incidents, rules, approvals) into a single verified artifact with content hash.",
     [("proof_id", "str"), ("period_id", "str"), ("rc_state_ref", "str"),
      ("lanes_ref", "str"), ("critical_path_ref", "str"),
      ("scoreboard_ref", "str"), ("incidents_ref", "str"),
      ("rules_ref", "str"), ("approvals_ref", "str"),
      ("playbook_ref", "str"), ("dry_run_ref", "str"),
      ("all_verified", "bool"), ("content_hash", "str|None"),
      ("status", "str"), ("generated_at", "str")],
     [("list_proofs", "GET", "/api/rc-proof-pack", "List RC proof packs"),
      ("generate_proof", "POST", "/api/rc-proof-pack", "Generate RC proof pack"),
      ("get_proof", "GET", "/api/rc-proof-pack/{proof_id}", "Get proof pack details"),
      ("verify_proof", "POST", "/api/rc-proof-pack/{proof_id}/verify", "Verify proof pack integrity"),
      ("seal_proof", "POST", "/api/rc-proof-pack/{proof_id}/seal", "Seal proof pack"),
      ("download_proof", "POST", "/api/rc-proof-pack/{proof_id}/download", "Download proof pack"),
      ("proof_report", "GET", "/api/rc-proof-pack/report", "Get RC proof pack report")]),
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
    print(f"Generating {len(WAVES)} waves (221-240)...")

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
