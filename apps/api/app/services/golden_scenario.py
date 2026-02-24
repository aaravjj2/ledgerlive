"""Golden Scenario Seed Service — Deterministic E2E golden state for Race Control.

PROJECT_ID: LEDGERLIVE
Seeded once per E2E run; produces stable IDs for assertion checks.
DEMO/E2E mode only.
"""
from __future__ import annotations

import datetime as dt

# ── Deterministic fixed IDs ─────────────────────────────────────────
GRC = {
    "exception_auto": "grc-exc-auto-000000000001",
    "exception_appr": "grc-exc-appr-000000000002",
    "incident_sla":   "grc-inc-sla--000000000003",
    "approval_step1": "grc-appr-s1--000000000004",
    "approval_step2": "grc-appr-s2--000000000005",
    "security_evt":   "grc-sec-evt--000000000006",
    "lane_revenue":   "grc-lane-rev-000000000007",
    "lane_ap":        "grc-lane-ap--000000000008",
    "checkpoint_1":   "grc-chkpt-1--000000000009",
    "checkpoint_2":   "grc-chkpt-2--000000000010",
    "checkpoint_3":   "grc-chkpt-3--000000000011",
    "score":          "grc-score----000000000012",
    "replay_run":     "grc-replay---000000000013",
    "telemetry_pack": "grc-telem----000000000014",
    "court_pack":     "grc-court----000000000015",
    "jira_issue":     "grc-jira-----000000000016",
    "confluence_page":"grc-conf-----000000000017",
    "channel_action": "grc-chan-----000000000018",
}

# Stable hash used for binder regen verification
GRC_BINDER_HASH = "sha256:goldenscenario0000000000000000000000000000000000000deadbeef"

# Expected artifact state
GRC_ASSERTIONS = {
    "scenario": "golden_race_control",
    "ids": GRC,
    "binder_hash": GRC_BINDER_HASH,
    "expected_counts": {
        "exceptions": 2,
        "exception_auto_resolvable": 1,
        "exception_approval_required": 1,
        "incidents": 1,
        "approval_steps": 2,
        "approval_pending": 1,
        "security_events": 1,
        "lanes": 2,
        "checkpoints": 3,
        "checkpoints_pass": 2,
        "checkpoints_pending": 1,
    },
    "security_event": {
        "id": GRC["security_evt"],
        "action": "blocked_action",
        "reason_id": "SEC-GRC-001",
        "fix_path": "obtain_approval",
        "resolution": "approved_proceed",
    },
    "telemetry_pack": {"id": GRC["telemetry_pack"], "status": "PASS"},
    "court_pack": {"id": GRC["court_pack"], "status": "PASS"},
    "replay": {"id": GRC["replay_run"], "hash": GRC_BINDER_HASH, "status": "PASS"},
}


class GoldenScenarioService:
    """Manages seeding and resetting the golden Race Control scenario."""

    def __init__(self):
        self._seeded = False
        # In-memory overrides for export + replay artifacts
        self._artifacts: dict[str, dict] = {}
        self._security_store: dict[str, dict] = {}
        self._approval_overrides: dict[str, str] = {}  # id → status

    # ── Seed ─────────────────────────────────────────────────────────

    def seed(self) -> dict:
        """Seed all golden-scenario fixtures into in-memory stores.

        Imports the singleton services directly to inject deterministic data.
        Safe to call multiple times (re-seeds always fresh).
        """
        from app.services.w230_lane_status import service as lane_svc
        from app.services.w228_close_checkpoint import service as cp_svc
        from app.services.w233_incident_log import service as inc_svc
        from app.services.w239_rc_approval import service as appr_svc
        from app.services.w232_live_scoreboard import service as score_svc
        from app.main import emit_audit_event

        ts = dt.datetime.utcnow().isoformat()

        # Clear existing golden items (remove only seed IDs)
        for svc_store in [lane_svc._store, cp_svc._store, inc_svc._store,
                          appr_svc._store, score_svc._store]:
            for gid in list(GRC.values()):
                svc_store.pop(gid, None)

        # ── Lanes ────────────────────────────────────────────────────
        lane_svc._store[GRC["lane_revenue"]] = {
            "lane_id": GRC["lane_revenue"],
            "lane_name": "Revenue Recognition",
            "workstream": "revenue",
            "tasks_in_lane": ["sub_ledger", "cutoff_review", "elimination"],
            "lane_color": "green",
            "completion_pct": 85,
            "blocked_count": 0,
            "on_track": True,
            "owner_team": "Revenue Team",
            "display_order": 1,
            "status": "active",
            "updated_at": ts,
        }
        lane_svc._store[GRC["lane_ap"]] = {
            "lane_id": GRC["lane_ap"],
            "lane_name": "Accounts Payable",
            "workstream": "ap",
            "tasks_in_lane": ["invoice_match", "accruals", "forex"],
            "lane_color": "yellow",
            "completion_pct": 62,
            "blocked_count": 2,
            "on_track": False,
            "owner_team": "AP Team",
            "display_order": 2,
            "status": "active",
            "updated_at": ts,
        }
        emit_audit_event("grc_seed_lane", "lane_status", GRC["lane_revenue"], {"scenario": "golden_race_control"})
        emit_audit_event("grc_seed_lane", "lane_status", GRC["lane_ap"], {"scenario": "golden_race_control"})

        # ── Checkpoints ──────────────────────────────────────────────
        cp_svc._store[GRC["checkpoint_1"]] = {
            "checkpoint_id": GRC["checkpoint_1"],
            "checkpoint_name": "Sub-ledger Close",
            "criteria_met": True,
            "gate_result": "PASS",
            "status": "approved",
            "period_id": "FY25-Q4",
            "created_at": ts,
        }
        cp_svc._store[GRC["checkpoint_2"]] = {
            "checkpoint_id": GRC["checkpoint_2"],
            "checkpoint_name": "Intercompany Elimination",
            "criteria_met": True,
            "gate_result": "PASS",
            "status": "approved",
            "period_id": "FY25-Q4",
            "created_at": ts,
        }
        cp_svc._store[GRC["checkpoint_3"]] = {
            "checkpoint_id": GRC["checkpoint_3"],
            "checkpoint_name": "Revenue Cutoff",
            "criteria_met": False,
            "gate_result": "PENDING",
            "status": "in_review",
            "period_id": "FY25-Q4",
            "created_at": ts,
        }
        emit_audit_event("grc_seed_checkpoint", "close_checkpoint", GRC["checkpoint_1"], {"scenario": "golden_race_control"})
        emit_audit_event("grc_seed_checkpoint", "close_checkpoint", GRC["checkpoint_2"], {"scenario": "golden_race_control"})
        emit_audit_event("grc_seed_checkpoint", "close_checkpoint", GRC["checkpoint_3"], {"scenario": "golden_race_control"})

        # ── Incident (SLA breach) ────────────────────────────────────
        inc_svc._store[GRC["incident_sla"]] = {
            "incident_id": GRC["incident_sla"],
            "incident_title": "SLA Breach — AP Lane overdue by 4h",
            "severity": "high",
            "category": "sla_violation",
            "description": "Accounts Payable lane exceeded SLA threshold of 48h. Requires immediate remediation.",
            "impact_assessment": "High — delays court pack generation",
            "affected_tasks": ["invoice_match", "accruals"],
            "reported_by": "rc_monitor",
            "reported_at": ts,
            "resolved_at": None,
            "root_cause": "ERP data feed delay (golden scenario simulation)",
            "resolution_summary": None,
            "status": "open",
        }
        emit_audit_event("grc_seed_incident", "incident_log", GRC["incident_sla"], {"scenario": "golden_race_control"})

        # ── Approval chain (2 steps) ─────────────────────────────────
        appr_svc._store[GRC["approval_step1"]] = {
            "approval_id": GRC["approval_step1"],
            "approval_level": 1,
            "total_levels": 2,
            "all_approved": True,
            "status": "approved",
            "approvers": ["controller@ledgerlive.example"],
            "period_id": "FY25-Q4",
            "approved_at": ts,
            "notes": "Golden scenario step 1 — auto-approved",
        }
        appr_svc._store[GRC["approval_step2"]] = {
            "approval_id": GRC["approval_step2"],
            "approval_level": 2,
            "total_levels": 2,
            "all_approved": False,
            "status": "pending",
            "approvers": ["cfo@ledgerlive.example"],
            "period_id": "FY25-Q4",
            "approved_at": None,
            "notes": "Golden scenario step 2 — awaiting CFO approval",
        }
        emit_audit_event("grc_seed_approval", "rc_approval", GRC["approval_step1"], {"scenario": "golden_race_control"})
        emit_audit_event("grc_seed_approval", "rc_approval", GRC["approval_step2"], {"scenario": "golden_race_control"})

        # ── Score ────────────────────────────────────────────────────
        score_svc._store[GRC["score"]] = {
            "score_id": GRC["score"],
            "overall_health": "yellow",
            "sla_adherence_pct": 87.5,
            "blocker_count": 2,
            "checkpoints_passed": 2,
            "checkpoints_total": 3,
            "team_scores": [],
            "period_id": "FY25-Q4",
            "created_at": ts,
        }
        emit_audit_event("grc_seed_score", "live_scoreboard", GRC["score"], {"scenario": "golden_race_control"})

        # ── Security event ───────────────────────────────────────────
        self._security_store[GRC["security_evt"]] = {
            "security_event_id": GRC["security_evt"],
            "action": "blocked_action",
            "reason_id": "SEC-GRC-001",
            "description": "Attempt to bypass AP approval without CFO sign-off — BLOCKED",
            "fix_path": "obtain_approval",
            "resolution": None,
            "status": "blocked",
            "trace_id": "grc-trace-sec-00000000000006",
            "created_at": ts,
        }
        emit_audit_event("grc_security_block", "security_timeline", GRC["security_evt"],
                         {"reason_id": "SEC-GRC-001", "scenario": "golden_race_control"})

        # ── Artifacts (reset to available) ───────────────────────────
        self._artifacts[GRC["telemetry_pack"]] = {
            "pack_id": GRC["telemetry_pack"], "type": "telemetry",
            "status": "available", "hash": None,
        }
        self._artifacts[GRC["court_pack"]] = {
            "pack_id": GRC["court_pack"], "type": "court",
            "status": "available", "hash": None,
        }
        self._artifacts[GRC["replay_run"]] = {
            "pack_id": GRC["replay_run"], "type": "replay",
            "status": "available", "hash": None,
        }

        # Reset approval overrides
        self._approval_overrides = {}

        self._seeded = True
        return {"seeded": True, "scenario": "golden_race_control", "ids": GRC}

    # ── Approve step ─────────────────────────────────────────────────

    def approve_step(self, approval_id: str) -> dict | None:
        """Approve a pending approval step."""
        from app.services.w239_rc_approval import service as appr_svc
        from app.main import emit_audit_event

        item = appr_svc._store.get(approval_id)
        if not item:
            return None
        item["status"] = "approved"
        item["all_approved"] = True
        item["approved_at"] = dt.datetime.utcnow().isoformat()
        self._approval_overrides[approval_id] = "approved"
        emit_audit_event("grc_approve_step", "rc_approval", approval_id,
                         {"scenario": "golden_race_control", "action": "approved"})
        # Update score if all steps approved
        if approval_id == GRC["approval_step2"]:
            from app.services.w232_live_scoreboard import service as score_svc
            s = score_svc._store.get(GRC["score"])
            if s:
                s["overall_health"] = "green"
                s["blocker_count"] = 0
        return item

    # ── Security fix path ─────────────────────────────────────────────

    def security_fix_path(self, event_id: str) -> dict | None:
        """Trigger fix path for a blocked security event."""
        from app.main import emit_audit_event
        evt = self._security_store.get(event_id)
        if not evt:
            return None
        evt["resolution"] = "approved_proceed"
        evt["status"] = "resolved"
        emit_audit_event("grc_security_resolved", "security_timeline", event_id,
                         {"reason_id": "SEC-GRC-001", "fix_path": "obtain_approval", "resolution": "approved_proceed"})
        return evt

    def get_security_event(self, event_id: str) -> dict | None:
        return self._security_store.get(event_id)

    def list_security_events(self) -> list[dict]:
        return list(self._security_store.values())

    # ── Export / replay ───────────────────────────────────────────────

    def generate_telemetry_pack(self) -> dict:
        from app.main import emit_audit_event
        pack = self._artifacts.get(GRC["telemetry_pack"], {})
        pack["status"] = "PASS"
        pack["hash"] = "sha256:telemetry000000000000000000000000000000000000deadbeef"
        emit_audit_event("grc_export_telemetry", "telemetry_pack", GRC["telemetry_pack"],
                         {"scenario": "golden_race_control", "status": "PASS"})
        return pack

    def generate_court_pack(self) -> dict:
        from app.main import emit_audit_event
        pack = self._artifacts.get(GRC["court_pack"], {})
        pack["status"] = "PASS"
        pack["hash"] = "sha256:courtpack000000000000000000000000000000000000deadbeef"
        emit_audit_event("grc_export_court", "court_pack", GRC["court_pack"],
                         {"scenario": "golden_race_control", "status": "PASS"})
        return pack

    def regenerate_binder(self) -> dict:
        from app.main import emit_audit_event
        replay = self._artifacts.get(GRC["replay_run"], {})
        replay["status"] = "PASS"
        replay["hash"] = GRC_BINDER_HASH
        emit_audit_event("grc_replay_regen", "replay_engine", GRC["replay_run"],
                         {"scenario": "golden_race_control", "hash": GRC_BINDER_HASH})
        return replay

    # ── Channel actions ───────────────────────────────────────────────

    def send_channel_approval(self, approval_id: str, channel: str) -> dict:
        from app.main import emit_audit_event
        trace_id = "grc-trace-chan-000000000018"
        result = {
            "action_id": GRC["channel_action"],
            "channel": channel,
            "approval_id": approval_id,
            "trace_id": trace_id,
            "status": "sent",
            "message": f"Approval request sent to {channel}",
        }
        emit_audit_event("grc_channel_approval_sent", "channel_action", GRC["channel_action"],
                         {"channel": channel, "approval_id": approval_id, "trace_id": trace_id})
        return result

    # ── Atlassian mocks ───────────────────────────────────────────────

    def create_jira_issue(self, approval_id: str) -> dict:
        from app.main import emit_audit_event
        issue = {
            "issue_id": GRC["jira_issue"],
            "jira_issue_key": "LLIVE-GRC-001",
            "title": "CFO Approval Overdue — FY25-Q4 Close",
            "linked_approval_id": approval_id,
            "url": "https://ledgerlive.atlassian.net/browse/LLIVE-GRC-001",
            "status": "open",
        }
        emit_audit_event("grc_jira_issue_created", "jira_adapter", GRC["jira_issue"],
                         {"jira_key": "LLIVE-GRC-001", "approval_id": approval_id})
        return issue

    def create_confluence_page(self) -> dict:
        from app.main import emit_audit_event
        page = {
            "page_id": GRC["confluence_page"],
            "title": "Race Weekend Close Report — FY25-Q4",
            "hash": "sha256:confluence000000000000000000000000000000000000deadbeef",
            "url": "https://ledgerlive.atlassian.net/wiki/LLIVE-GRC-CLOSE-REPORT",
            "status": "published",
        }
        emit_audit_event("grc_confluence_page_created", "confluence_adapter", GRC["confluence_page"],
                         {"title": "Race Weekend Close Report — FY25-Q4"})
        return page

    # ── E2E assertions ───────────────────────────────────────────────

    def get_assertions(self) -> dict:
        return GRC_ASSERTIONS

    # ── Reset ────────────────────────────────────────────────────────

    def reset(self) -> dict:
        from app.services.w230_lane_status import service as lane_svc
        from app.services.w228_close_checkpoint import service as cp_svc
        from app.services.w233_incident_log import service as inc_svc
        from app.services.w239_rc_approval import service as appr_svc
        from app.services.w232_live_scoreboard import service as score_svc

        for svc_store in [lane_svc._store, cp_svc._store, inc_svc._store,
                          appr_svc._store, score_svc._store]:
            for gid in list(GRC.values()):
                svc_store.pop(gid, None)

        self._artifacts.clear()
        self._security_store.clear()
        self._approval_overrides.clear()
        self._seeded = False
        return {"reset": True, "scenario": "golden_race_control"}


# Module-level singleton
service = GoldenScenarioService()
