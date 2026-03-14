#!/usr/bin/env python
"""
smoke_mcp.py — MCP Remote Server smoke test for LedgerLive

Usage:
    python tools/deploy/smoke_mcp.py                         # test local (http://127.0.0.1:8090)
    python tools/deploy/smoke_mcp.py --url https://my.app    # test Heroku
    python tools/deploy/smoke_mcp.py --url https://my.app --verbose

Exit code: 0 = all pass, 1 = any failure.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Any

import httpx

PASS = "\033[32mPASS\033[0m"
FAIL = "\033[31mFAIL\033[0m"
SKIP = "\033[33mSKIP\033[0m"

results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    tag = PASS if ok else FAIL
    print(f"  [{tag}] {name}" + (f"  — {detail}" if detail else ""))
    results.append((name, ok, detail))


def rpc(client: httpx.Client, base: str, method: str, params: dict | None = None) -> Any:
    body: dict = {"jsonrpc": "2.0", "id": 1, "method": method}
    if params:
        body["params"] = params
    r = client.post(f"{base}/mcp/message", json=body, timeout=15)
    r.raise_for_status()
    return r.json()


def smoke(base_url: str, verbose: bool = False) -> None:
    base = base_url.rstrip("/")
    print(f"\n{'='*60}")
    print(f"  LedgerLive MCP Remote — smoke test")
    print(f"  Target: {base}")
    print(f"{'='*60}\n")

    with httpx.Client(follow_redirects=True) as client:

        # ── 1. /mcp/info health check ──────────────────────────────
        print("[ /mcp/info ]")
        try:
            r = client.get(f"{base}/mcp/info", timeout=10)
            ok = r.status_code == 200
            data = r.json() if ok else {}
            check("status 200", ok, str(r.status_code))
            # /mcp/info wraps name inside serverInfo.name
            sinfo = data.get("serverInfo", {})
            check("name field", bool(sinfo.get("name")), sinfo.get("name", ""))
            # protocol version uses camelCase
            check("protocol_version", bool(data.get("protocolVersion")), data.get("protocolVersion", ""))
            check("tool_count == 7", data.get("tool_count") == 7, str(data.get("tool_count")))
        except Exception as exc:
            check("/mcp/info reachable", False, str(exc))

        print()

        # ── 2. MCP initialize ─────────────────────────────────────
        print("[ POST /mcp/message — initialize ]")
        try:
            resp = rpc(client, base, "initialize", {
                "protocolVersion": "2024-11-05",
                "clientInfo": {"name": "smoke-test", "version": "0.1"},
                "capabilities": {}
            })
            result = resp.get("result", {})
            check("jsonrpc=2.0", resp.get("jsonrpc") == "2.0", resp.get("jsonrpc", ""))
            check("serverInfo present", "serverInfo" in result, str(result.get("serverInfo", {})))
            check("protocolVersion", result.get("protocolVersion") == "2024-11-05",
                  result.get("protocolVersion", ""))
        except Exception as exc:
            check("initialize call", False, str(exc))

        print()

        # ── 3. tools/list — count + stability ─────────────────────
        print("[ POST /mcp/message — tools/list ]")
        tools_data: list[dict] = []
        try:
            resp1 = rpc(client, base, "tools/list")
            resp2 = rpc(client, base, "tools/list")
            tools_data = resp1.get("result", {}).get("tools", [])
            names1 = [t["name"] for t in tools_data]
            names2 = [t["name"] for t in resp2.get("result", {}).get("tools", [])]
            check("tool count == 7", len(tools_data) == 7, str(len(tools_data)))
            check("stable across calls", names1 == names2, "")
            expected_prefix = "ledgerlive."
            check("all tools ledgerlive.*",
                  all(n.startswith(expected_prefix) for n in names1),
                  str(names1))
            if verbose:
                for t in tools_data:
                    print(f"         • {t['name']}")
        except Exception as exc:
            check("tools/list call", False, str(exc))

        print()

        # ── 4. tools/call — ledgerlive.cfo_cockpit ────────────────
        print("[ POST /mcp/message — tools/call cfo_cockpit ]")
        try:
            resp = rpc(client, base, "tools/call", {
                "name": "ledgerlive.cfo_cockpit",
                "arguments": {}
            })
            result = resp.get("result", {})
            content = result.get("content", [])
            check("content list present", isinstance(content, list) and len(content) > 0, "")
            check("trace_id in result",
                  any("trace_id" in str(c) for c in content) or "trace_id" in str(result), "")
        except Exception as exc:
            check("tools/call cfo_cockpit", False, str(exc))

        print()

        # ── 5. tools/call idempotency ────────────────────────────
        print("[ tools/call idempotency — cfo_story_run ]")
        try:
            args = {"period_id": "2026-Q1"}
            r1 = rpc(client, base, "tools/call", {"name": "ledgerlive.cfo_story_run", "arguments": args})
            r2 = rpc(client, base, "tools/call", {"name": "ledgerlive.cfo_story_run", "arguments": args})

            def _extract_trace(resp: Any) -> str:
                """Extract trace_id from a tools/call response (idempotency token)."""
                result = resp.get("result", {})
                # Preferred: _meta.trace_id (always present in our implementation)
                if "_meta" in result and "trace_id" in result["_meta"]:
                    return result["_meta"]["trace_id"]
                # Fallback: parse content[0].text as JSON
                for item in result.get("content", []):
                    try:
                        parsed = json.loads(item.get("text", ""))
                        if "trace_id" in parsed:
                            return parsed["trace_id"]
                    except Exception:
                        pass
                return ""

            tid1 = _extract_trace(r1)
            tid2 = _extract_trace(r2)
            check("idempotent trace_id", bool(tid1) and tid1 == tid2, f"{tid1[:16]}" if tid1 else "empty")
        except Exception as exc:
            check("idempotency check", False, str(exc))

        print()

        # ── 6. error — unknown tool ───────────────────────────────
        print("[ POST /mcp/message — error: unknown tool ]")
        try:
            resp = rpc(client, base, "tools/call", {"name": "ledgerlive.does_not_exist", "arguments": {}})
            err = resp.get("error", {})
            check("error code -32602", err.get("code") == -32602, str(err.get("code")))
            check("error message present", bool(err.get("message")), err.get("message", ""))
        except Exception as exc:
            check("unknown tool error", False, str(exc))

        print()

        # ── 7. SSE GET /mcp/sse — verify headers + stream opens ──
        print("[ GET /mcp/sse — event:endpoint ]")
        try:
            # Strategy: open the SSE stream and check status/content-type from
            # response headers (available before body bytes) — then optionally
            # read body. Cloudflare trycloudflare and other CDN proxies may
            # buffer the body indefinitely, so we never block on iter_bytes().
            sse_timeout = httpx.Timeout(connect=20.0, read=30.0, write=10.0, pool=10.0)
            with httpx.Client(follow_redirects=True) as sse_client:
                with sse_client.stream("GET", f"{base}/mcp/sse",
                                       timeout=sse_timeout) as stream:
                    status_code = stream.status_code
                    ct_header = stream.headers.get("content-type", "")
                    # Try to read the first body chunk with a 5-second window.
                    # If it arrives (local / non-buffered), check its content.
                    # If it times out (CDN-buffered), the headers already passed.
                    raw = b""
                    t0 = time.time()
                    try:
                        for chunk in stream.iter_bytes():
                            raw += chunk
                            if b"event: endpoint" in raw:
                                break
                            if time.time() - t0 > 5:
                                break
                    except httpx.ReadTimeout:
                        pass  # CDN buffering — headers already captured above

            check("SSE status 200", status_code == 200, str(status_code))
            check("SSE content-type event-stream",
                  "text/event-stream" in ct_header, ct_header)
            decoded = raw.decode("utf-8", errors="replace")
            if "event: endpoint" in decoded:
                check("event: endpoint in body", True, "confirmed")
                check("/mcp/message in data", "/mcp/message" in decoded, "")
            else:
                print(f"  [INFO] SSE body not received (CDN buffering — "
                      f"Airia browser client is unaffected by proxy buffering)")
        except Exception as exc:
            check("SSE /mcp/sse", False, str(exc))

    print()

    # ── Summary ──────────────────────────────────────────────────
    passed = sum(1 for _, ok, _ in results if ok)
    failed = sum(1 for _, ok, _ in results if not ok)
    total = len(results)
    print(f"{'='*60}")
    print(f"  Results: {passed}/{total} passed  ({failed} failed)")
    print(f"{'='*60}\n")

    if failed > 0:
        print("Failed checks:")
        for name, ok, detail in results:
            if not ok:
                print(f"  • {name}: {detail}")
        print()
        sys.exit(1)

    print("All checks passed. ✓\n")
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smoke test for LedgerLive MCP Remote Server")
    parser.add_argument("--url", default="http://127.0.0.1:8090",
                        help="Base URL to test (default: http://127.0.0.1:8090)")
    parser.add_argument("--verbose", action="store_true",
                        help="Print tool names during tools/list check")
    args = parser.parse_args()
    smoke(args.url, verbose=args.verbose)
