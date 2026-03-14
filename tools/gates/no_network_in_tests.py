#!/usr/bin/env python3
"""Gate: ensure test files do not make outbound network calls.

Scans test files for forbidden patterns that indicate real HTTP/network
calls (urllib, requests.get, httpx, aiohttp, socket.connect).
Mocked/patched calls are allowed.

Exit 0 = clean, Exit 1 = violations found.
"""
import os, re, sys, pathlib

FORBIDDEN_PATTERNS = [
    r'\brequests\.(get|post|put|patch|delete)\s*\(',
    r'\bhttpx\.(get|post|put|patch|delete|AsyncClient|Client)\s*\(',
    r'\baiohttp\.ClientSession\s*\(',
    r'\burllib\.request\.urlopen\s*\(',
    r'\bsocket\.connect\s*\(',
    r'\bsocket\.create_connection\s*\(',
]

SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache"}

ALLOW_PATTERNS = [
    r'mock', r'patch', r'monkeypatch', r'MagicMock', r'AsyncMock',
    r'@pytest\.fixture', r'httpx\.AsyncClient\(.*app=',
    r'httpx\.AsyncClient\(.*transport=',
]

ROOT = pathlib.Path(__file__).resolve().parents[2]

def scan():
    forbidden_re = re.compile("|".join(FORBIDDEN_PATTERNS))
    allow_re = re.compile("|".join(ALLOW_PATTERNS), re.IGNORECASE)
    violations = []

    test_dirs = [ROOT / "apps" / "api" / "tests", ROOT / "tests"]
    for test_dir in test_dirs:
        if not test_dir.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(test_dir):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fname in filenames:
                if not fname.endswith(".py"):
                    continue
                fpath = pathlib.Path(dirpath) / fname
                try:
                    text = fpath.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                for i, line in enumerate(text.splitlines(), 1):
                    if forbidden_re.search(line) and not allow_re.search(line):
                        rel = fpath.relative_to(ROOT)
                        violations.append((str(rel), i, line.strip()[:120]))
    return violations

if __name__ == "__main__":
    violations = scan()
    if violations:
        print(f"GATE FAIL: {len(violations)} potential network call(s) in tests:\n")
        for path, lineno, snippet in violations[:30]:
            print(f"  {path}:{lineno}")
            print(f"    {snippet}\n")
        sys.exit(1)
    else:
        print("GATE PASS: No outbound network calls in tests.")
        sys.exit(0)
