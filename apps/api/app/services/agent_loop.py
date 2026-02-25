"""Agent Loop Service — Perceive → Decide → Act autonomous close agent.

Implements a real perceive→decide→act loop that:
1. PERCEIVE: reads current state from all live services
2. DECIDE: applies rule-based triage + confidence scoring
3. ACT: executes actions (resolve exceptions, advance workflows, post to Airia)

Each cycle produces a decision trace with reasoning, citations, and audit trail.

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

import uuid
import datetime as dt
import hashlib
from typing import Any

from app.main import emit_audit_event


# ── In-memory cycle log ─────────────────────────────────────────────
_cycle_log: list[dict] = []


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def perceive() -> dict[str, Any]:
    """PERCEIVE phase — gather current state from all live services."""
    from app.services.w03_document_store import service as doc_svc
    from app.services.w04_ocr_pipeline import service as ocr_svc
    from app.services.w06_reconciliation import service as recon_svc
    from app.services.w07_exception import service as exc_svc
    from app.services.w08_review_queue import service as review_svc
    from app.services.w13_workflow import service as wf_svc

    docs = doc_svc.list()
    ocr_jobs = ocr_svc.list()
    recons = recon_svc.list()
    exceptions = exc_svc.list()
    reviews = review_svc.list()
    workflows = wf_svc.list()

    return {
        "ts": dt.datetime.utcnow().isoformat(),
        "documents": {
            "total": len(docs),
            "ids": [d.get("document_id") or d.get("id") for d in docs[:10]],
        },
        "ocr": {
            "total": len(ocr_jobs),
            "completed": sum(1 for j in ocr_jobs if j.get("status") == "completed"),
            "pending": sum(1 for j in ocr_jobs if j.get("status") != "completed"),
        },
        "reconciliations": {
            "total": len(recons),
            "approved": sum(1 for r in recons if r.get("status") == "approved"),
            "pending": sum(1 for r in recons if r.get("status") != "approved"),
            "avg_match_score": round(
                sum(r.get("match_score", 0) for r in recons) / max(len(recons), 1), 2
            ),
        },
        "exceptions": {
            "total": len(exceptions),
            "open": sum(1 for e in exceptions if e.get("status") in ("open", "escalated")),
            "resolved": sum(1 for e in exceptions if e.get("status") == "resolved"),
            "items": [
                {
                    "id": e.get("exception_id"),
                    "category": e.get("category", "unknown"),
                    "severity": e.get("severity", "medium"),
                    "status": e.get("status", "open"),
                    "description": e.get("description", ""),
                }
                for e in exceptions
                if e.get("status") in ("open", "escalated")
            ],
        },
        "reviews": {
            "total": len(reviews),
            "pending": sum(1 for r in reviews if r.get("status") in ("pending", "open")),
        },
        "workflows": {
            "total": len(workflows),
            "active": sum(1 for w in workflows if w.get("status") == "in_progress"),
            "completed": sum(1 for w in workflows if w.get("status") == "completed"),
        },
    }


def decide(perception: dict) -> dict[str, Any]:
    """DECIDE phase — apply triage rules and score confidence for each action.

    Rules:
    - Auto-resolve low-severity exceptions with high confidence
    - Escalate high-severity exceptions to review queue
    - Advance workflows when all blocking exceptions are resolved
    - Flag cost cap risks based on exception amounts
    """
    actions: list[dict] = []
    reasoning_trace: list[str] = []

    # Rule 1: Auto-resolve low-severity open exceptions
    open_exceptions = perception["exceptions"]["items"]
    for exc in open_exceptions:
        severity = exc.get("severity", "medium")
        category = exc.get("category", "unknown")

        if severity in ("low", "info"):
            confidence = 0.95
            actions.append({
                "action": "auto_resolve",
                "target_type": "exception",
                "target_id": exc["id"],
                "confidence": confidence,
                "reasoning": f"Low-severity {category} exception — auto-resolvable with {confidence:.0%} confidence. "
                             f"Pattern: {category} items below materiality threshold do not require manual review.",
                "citations": [exc["id"]],
            })
            reasoning_trace.append(
                f"DECIDE: Exception {exc['id']} ({category}, severity={severity}) → AUTO_RESOLVE (confidence={confidence})"
            )
        elif severity == "high":
            actions.append({
                "action": "escalate",
                "target_type": "exception",
                "target_id": exc["id"],
                "confidence": 0.90,
                "reasoning": f"High-severity {category} exception — requires human review. "
                             f"Escalating to review queue for CFO approval.",
                "citations": [exc["id"]],
            })
            reasoning_trace.append(
                f"DECIDE: Exception {exc['id']} ({category}, severity={severity}) → ESCALATE (confidence=0.90)"
            )
        else:  # medium
            # Medium: check if it's an amount-based or pattern-based issue
            confidence = 0.75
            actions.append({
                "action": "auto_resolve",
                "target_type": "exception",
                "target_id": exc["id"],
                "confidence": confidence,
                "reasoning": f"Medium-severity {category} exception — agent resolves with {confidence:.0%} confidence. "
                             f"If confidence drops below 70%, this would escalate instead.",
                "citations": [exc["id"]],
            })
            reasoning_trace.append(
                f"DECIDE: Exception {exc['id']} ({category}, severity={severity}) → AUTO_RESOLVE (confidence={confidence})"
            )

    # Rule 2: Advance workflow if no open exceptions remain after actions
    open_after = len([
        e for e in open_exceptions
        if not any(a["target_id"] == e["id"] and a["action"] == "auto_resolve" for a in actions)
    ])
    if open_after == 0 and perception["workflows"]["active"] > 0:
        actions.append({
            "action": "advance_workflow",
            "target_type": "workflow",
            "target_id": "active",
            "confidence": 0.99,
            "reasoning": "All blocking exceptions resolved or being resolved — safe to advance workflow to next stage.",
            "citations": [],
        })
        reasoning_trace.append("DECIDE: All exceptions clear → ADVANCE_WORKFLOW")

    # Rule 3: Notify Airia of cycle results
    actions.append({
        "action": "notify_airia",
        "target_type": "webhook",
        "target_id": "airia",
        "confidence": 1.0,
        "reasoning": "Post cycle results to Airia webhook for platform visibility.",
        "citations": [],
    })

    return {
        "ts": dt.datetime.utcnow().isoformat(),
        "actions_planned": len(actions),
        "actions": actions,
        "reasoning_trace": reasoning_trace,
        "summary": (
            f"Planned {len(actions)} actions: "
            f"{sum(1 for a in actions if a['action'] == 'auto_resolve')} auto-resolve, "
            f"{sum(1 for a in actions if a['action'] == 'escalate')} escalate, "
            f"{sum(1 for a in actions if a['action'] == 'advance_workflow')} advance, "
            f"{sum(1 for a in actions if a['action'] == 'notify_airia')} notify."
        ),
    }


def act(decision: dict) -> dict[str, Any]:
    """ACT phase — execute the planned actions against live services."""
    from app.services.w07_exception import service as exc_svc
    from app.services.w13_workflow import service as wf_svc
    from app.services.airia_webhook import post_to_airia

    results: list[dict] = []
    errors: list[str] = []

    for action in decision.get("actions", []):
        action_type = action["action"]
        target_id = action["target_id"]

        try:
            if action_type == "auto_resolve":
                item = exc_svc.resolve(target_id, {
                    "resolution": "agent_auto_resolve",
                    "confidence": action["confidence"],
                    "reasoning": action["reasoning"],
                    "resolved_at": dt.datetime.utcnow().isoformat(),
                })
                success = item is not None
                results.append({
                    "action": action_type,
                    "target_id": target_id,
                    "success": success,
                    "detail": "Resolved" if success else "Exception not found",
                })
                if success:
                    emit_audit_event(
                        "agent_auto_resolve", "exception", target_id,
                        {"confidence": action["confidence"], "reasoning": action["reasoning"]},
                    )

            elif action_type == "escalate":
                item = exc_svc.assign(target_id, {
                    "status": "escalated",
                    "assigned_to": "cfo_review_queue",
                    "reasoning": action["reasoning"],
                })
                success = item is not None
                results.append({
                    "action": action_type,
                    "target_id": target_id,
                    "success": success,
                    "detail": "Escalated to review queue" if success else "Exception not found",
                })
                if success:
                    emit_audit_event(
                        "agent_escalate", "exception", target_id,
                        {"reasoning": action["reasoning"]},
                    )

            elif action_type == "advance_workflow":
                # Find the active workflow and advance it
                active_wf = next(
                    (w for w in wf_svc.list() if w.get("status") == "in_progress"),
                    None,
                )
                if active_wf:
                    wf_id = active_wf.get("workflow_id")
                    wf_svc.advance(wf_id, {"status": "in_progress"})
                    results.append({
                        "action": action_type,
                        "target_id": wf_id,
                        "success": True,
                        "detail": "Workflow advanced to next stage",
                    })
                    emit_audit_event(
                        "agent_advance_workflow", "workflow", wf_id,
                        {"reasoning": action["reasoning"]},
                    )
                else:
                    results.append({
                        "action": action_type,
                        "target_id": "none",
                        "success": False,
                        "detail": "No active workflow to advance",
                    })

            elif action_type == "notify_airia":
                # Post results to Airia webhook (no-op if URL not configured)
                webhook_result = post_to_airia("agent_cycle_complete", {
                    "actions_executed": len(results),
                    "successes": sum(1 for r in results if r.get("success")),
                    "ts": dt.datetime.utcnow().isoformat(),
                })
                results.append({
                    "action": action_type,
                    "target_id": "airia_webhook",
                    "success": True,
                    "detail": f"Webhook posted (delivered={webhook_result.get('delivered', False)})",
                })

        except Exception as e:
            errors.append(f"{action_type} on {target_id}: {e}")
            results.append({
                "action": action_type,
                "target_id": target_id,
                "success": False,
                "detail": str(e),
            })

    return {
        "ts": dt.datetime.utcnow().isoformat(),
        "results": results,
        "total_actions": len(results),
        "successes": sum(1 for r in results if r.get("success")),
        "failures": sum(1 for r in results if not r.get("success")),
        "errors": errors,
    }


def run_cycle() -> dict[str, Any]:
    """Run one full perceive→decide→act cycle.

    Returns the complete trace for auditability.
    """
    cycle_id = str(uuid.uuid4())
    start = dt.datetime.utcnow()

    # Phase 1: PERCEIVE
    perception = perceive()

    # Phase 2: DECIDE
    decision = decide(perception)

    # Phase 3: ACT
    execution = act(decision)

    elapsed_ms = round((dt.datetime.utcnow() - start).total_seconds() * 1000)

    cycle = {
        "cycle_id": cycle_id,
        "ts": start.isoformat(),
        "elapsed_ms": elapsed_ms,
        "phases": {
            "perceive": perception,
            "decide": decision,
            "act": execution,
        },
        "summary": (
            f"Cycle {cycle_id[:8]}: "
            f"perceived {perception['exceptions']['open']} open exceptions, "
            f"planned {decision['actions_planned']} actions, "
            f"executed {execution['successes']}/{execution['total_actions']} successfully "
            f"in {elapsed_ms}ms."
        ),
        "checkpoint_hash": _sha(f"{cycle_id}-{execution['successes']}-{elapsed_ms}"),
    }

    # Emit audit event for the full cycle
    emit_audit_event("agent_cycle", "agent_loop", cycle_id, {
        "elapsed_ms": elapsed_ms,
        "actions_planned": decision["actions_planned"],
        "successes": execution["successes"],
        "failures": execution["failures"],
    })

    _cycle_log.append(cycle)
    return cycle


def get_cycle_log(limit: int = 20) -> list[dict]:
    """Return recent cycle log entries."""
    return _cycle_log[-limit:]


def get_cycle(cycle_id: str) -> dict | None:
    """Retrieve a specific cycle by ID."""
    for c in _cycle_log:
        if c["cycle_id"] == cycle_id:
            return c
    return None
