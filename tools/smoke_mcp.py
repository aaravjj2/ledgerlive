#!/usr/bin/env python
"""Convenience entry point — delegates to tools/deploy/smoke_mcp.py.

Usage:
    python tools/smoke_mcp.py --url http://127.0.0.1:8090
    python tools/smoke_mcp.py --url https://<public>.trycloudflare.com
"""
import runpy, sys, os

# Locate the real smoke script relative to this file
_here = os.path.dirname(os.path.abspath(__file__))
_real = os.path.join(_here, "deploy", "smoke_mcp.py")

if not os.path.exists(_real):
    raise FileNotFoundError(f"smoke_mcp.py not found at {_real}")

runpy.run_path(_real, run_name="__main__")
