#!/usr/bin/env python3
"""Start bundled Hack Scanner MCP server over stdio."""
from __future__ import annotations
import os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "hack_scanner"))

if __name__ == "__main__":
    raise SystemExit(subprocess.call([sys.executable, os.path.join(ROOT, "mcp_server.py")], cwd=ROOT))
