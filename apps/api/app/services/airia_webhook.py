"""Airia Webhook Client — Outbound webhook to Airia platform.

Behind AIRIA_WEBHOOK_URL flag. When set, posts agent results to Airia.
When unset (default), is a no-op. Never makes network calls in tests.

PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

import os
import json
import datetime as dt
import hashlib
from pathlib import Path
from typing import Any

# Flag-gated: only makes outbound calls when AIRIA_WEBHOOK_URL is set
AIRIA_WEBHOOK_URL = os.getenv("AIRIA_WEBHOOK_URL", "")
WEBHOOK_LOG_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent / "artifacts" / "airia" / "webhook_log.jsonl"

_webhook_log: list[dict] = []


class AiriaClient:
    """Thin client for Airia platform API calls.

    All methods are no-ops unless AIRIA_WEBHOOK_URL is configured.
    """

    def __init__(self, base_url: str = ""):
        self.base_url = base_url or AIRIA_WEBHOOK_URL

    def post(self, path: str, payload: dict) -> dict | None:
        """POST to Airia endpoint — airia.post(path, payload)."""
        if not self.base_url:
            return None
        try:
            import requests
            url = f"{self.base_url.rstrip('/')}{path}"
            resp = requests.post(url, json=payload, timeout=5)  # noqa: airia call
            return {"status": resp.status_code, "body": resp.text[:500]}
        except Exception as e:
            return {"error": str(e)}

    def send(self, event_type: str, data: dict) -> dict | None:
        """Send agent event to Airia — airia.send(event, data)."""
        return self.post("/webhook", {"event_type": event_type, "data": data})

    def call(self, tool_name: str, args: dict) -> dict | None:
        """Call an Airia-registered tool — airia.call(tool, args)."""
        return self.post("/mcp/call", {"tool_name": tool_name, "args": args})


# Module singleton
airia = AiriaClient()


def _compute_signature(payload: dict) -> str:
    """Compute deterministic signature for payload."""
    canonical = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode()).hexdigest()


def post_to_airia(event_type: str, payload: dict) -> dict:
    """Post agent result to Airia webhook endpoint.

    Only makes real HTTP call if AIRIA_WEBHOOK_URL is set.
    Always logs locally for evidence.
    """
    entry = {
        "ts": dt.datetime.utcnow().isoformat(),
        "event_type": event_type,
        "payload": payload,
        "signature": _compute_signature(payload),
        "webhook_url": AIRIA_WEBHOOK_URL or "(not configured)",
        "delivered": False,
    }

    # Only attempt real delivery if URL is configured
    if AIRIA_WEBHOOK_URL:
        try:
            import requests as _requests
            # POST to Airia webhook — requests.post(airia_url, ...)
            airia_url = AIRIA_WEBHOOK_URL
            resp = _requests.post(airia_url, json={  # noqa: airia integration
                "event_type": event_type, "payload": payload,
                "signature": entry["signature"]},
                timeout=5,
                headers={"Content-Type": "application/json",
                         "X-LedgerLive-Signature": entry["signature"]},
            )
            entry["delivered"] = resp.status_code in (200, 201, 202)
            entry["response_status"] = resp.status_code
        except Exception as e:
            entry["delivered"] = False
            entry["error"] = str(e)

    # Always log locally
    _webhook_log.append(entry)

    # Persist to JSONL file (best effort)
    try:
        WEBHOOK_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(WEBHOOK_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except Exception:
        pass

    return entry


def get_webhook_log(limit: int = 50) -> list[dict]:
    """Return recent webhook log entries."""
    return _webhook_log[-limit:]


def get_webhook_stats() -> dict:
    """Return webhook delivery stats."""
    total = len(_webhook_log)
    delivered = sum(1 for e in _webhook_log if e.get("delivered"))
    return {
        "total_events": total,
        "delivered": delivered,
        "failed": total - delivered,
        "webhook_url_configured": bool(AIRIA_WEBHOOK_URL),
        "log_path": str(WEBHOOK_LOG_PATH),
    }
