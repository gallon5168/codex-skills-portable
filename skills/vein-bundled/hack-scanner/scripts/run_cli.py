#!/usr/bin/env python3
"""Run bundled Hack Scanner CLI from any working directory."""
from __future__ import annotations
import argparse, os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "hack_scanner"))

def main() -> int:
    p = argparse.ArgumentParser(description="Hack Scanner CLI wrapper")
    p.add_argument("--url")
    p.add_argument("--file")
    p.add_argument("--both", action="store_true")
    p.add_argument("--output", "-o", default=os.path.join(os.getcwd(), "hack_report"))
    p.add_argument("--deep", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--unsafe", action="store_true")
    p.add_argument("--disable-oob", action="store_true")
    p.add_argument("--ai", action="store_true")
    p.add_argument("--deepsec-matchers", action="store_true")
    p.add_argument("--proxy", default="")
    args = p.parse_args()
    if not args.url and not args.file:
        p.error("provide --url and/or --file")
    cmd = [sys.executable, os.path.join(ROOT, "hack_scanner.py")]
    if args.url: cmd += ["--url", args.url]
    if args.file: cmd += ["--file", args.file]
    if args.both: cmd += ["--both"]
    cmd += ["--output", os.path.abspath(args.output)]
    for name in ("deep", "dry_run", "unsafe", "disable_oob", "ai", "deepsec_matchers"):
        if getattr(args, name): cmd.append("--" + name.replace("_", "-"))
    if args.proxy: cmd += ["--proxy", args.proxy]
    os.makedirs(os.path.abspath(args.output), exist_ok=True)
    return subprocess.call(cmd, cwd=ROOT)

if __name__ == "__main__":
    raise SystemExit(main())
