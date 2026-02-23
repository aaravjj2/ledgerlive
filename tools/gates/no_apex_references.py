#!/usr/bin/env python3
"""Gate: ensure ZERO Apex Terminal references exist in the working tree.

Scans apps/, tools/, docs/, tests/ and root-level text files for any
forbidden keywords that would indicate Apex Terminal content leaked
into the LedgerLive project.

Exit 0 = clean, Exit 1 = violations found.
"""
import os, re, sys, pathlib

FORBIDDEN = [
    "apex.terminal", "apex_terminal", "ApexTerminal", "APEX_TERMINAL",
    "autopilot", "backtest", "broker", "alpaca",
    "strategy_id", "trading", "portfolio_value",
    "positions_table", "orders_table", "fills_table",
    "swing", "sentiment_score", "elasticsearch",
    "ws_status", "ui2", "candles", "pnl_chart",
    "slippage", "e2e_apex",
]

SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache",
             "test-results", "playwright-report", "artifacts"}

EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".md", ".html",
              ".css", ".yaml", ".yml", ".toml", ".cfg", ".ini", ".sql", ".txt"}

ROOT = pathlib.Path(__file__).resolve().parents[2]

def scan():
    pattern = re.compile("|".join(re.escape(f) for f in FORBIDDEN), re.IGNORECASE)
    violations = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            fpath = pathlib.Path(dirpath) / fname
            if fpath.suffix.lower() not in EXTENSIONS:
                continue
            # Skip this gate file itself
            if fpath.resolve() == pathlib.Path(__file__).resolve():
                continue
            try:
                text = fpath.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                matches = pattern.findall(line)
                if matches:
                    rel = fpath.relative_to(ROOT)
                    violations.append((str(rel), i, matches, line.strip()[:120]))
    return violations

if __name__ == "__main__":
    violations = scan()
    if violations:
        print(f"GATE FAIL: {len(violations)} Apex reference(s) found:\n")
        for path, lineno, matches, snippet in violations[:50]:
            print(f"  {path}:{lineno}  {matches}")
            print(f"    {snippet}\n")
        if len(violations) > 50:
            print(f"  ... and {len(violations) - 50} more")
        sys.exit(1)
    else:
        print("GATE PASS: Zero Apex references found.")
        sys.exit(0)
