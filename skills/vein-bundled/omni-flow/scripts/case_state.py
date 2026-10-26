#!/usr/bin/env python3
"""Create, inspect, or update an omni-flow case-state.yaml file."""

from __future__ import annotations

import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_STAGES = [
    {"id": "triage", "status": "pending", "outputs": [], "evidence": []},
    {"id": "analysis", "status": "pending", "outputs": [], "evidence": []},
    {"id": "report", "status": "pending", "outputs": [], "evidence": []},
]


def parse_simple_yaml(text: str) -> dict:
    root: dict = {}
    inputs: list | None = None
    stages: list | None = None
    current_stage: dict | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        content = line.strip()
        if content == "case:":
            continue
        if indent in (2, 4) and content.startswith("- id: ") and stages is not None:
            current_stage = {"id": content[6:].strip(), "outputs": [], "evidence": []}
            stages.append(current_stage)
            continue
        if indent in (2, 4, 6) and content.startswith("path: ") and inputs is not None:
            inputs.append({"path": content[6:].strip(), "sha256": "pending"})
            continue
        if indent in (6, 8) and content.startswith("sha256: ") and inputs:
            inputs[-1]["sha256"] = content[8:].strip()
            continue
        if indent in (4, 6) and content.startswith(("status:", "note:")) and current_stage is not None:
            key, value = content.split(":", 1)
            current_stage[key] = value.strip()
            continue
        if indent == 2 and content.endswith(":") and content[:-1] in ("inputs", "stages", "goal", "environment"):
            key = content[:-1]
            if key == "inputs":
                inputs = []
                root[key] = inputs
            elif key == "stages":
                stages = []
                root[key] = stages
            else:
                current_stage = None
                pending_key = key
                globals().setdefault("_pending", pending_key)
        elif indent == 2 and ":" in content and "stages" not in root and "inputs" not in root:
            key, value = content.split(":", 1)
            root[key] = value.strip()
    return root


def dump(data: dict) -> str:
    lines = ["case:", f"  goal: {data.get('goal', '')}", f"  environment: {data.get('environment', 'unknown')}", "  inputs:"]
    for item in data.get("inputs") or [{"path": "pending", "sha256": "pending"}]:
        lines.append(f"    - path: {item.get('path', 'pending')}")
        lines.append(f"      sha256: {item.get('sha256', 'pending')}")
    lines.append("  stages:")
    for stage in data.get("stages") or DEFAULT_STAGES:
        lines.append(f"    - id: {stage['id']}")
        lines.append(f"      status: {stage.get('status', 'pending')}")
        outputs = stage.get("outputs") or []
        evidence = stage.get("evidence") or []
        rendered_outputs = "[" + ", ".join(outputs) + "]" if outputs else "[]"
        rendered_evidence = "[" + ", ".join(evidence) + "]" if evidence else "[]"
        lines.append(f"      outputs: {rendered_outputs}")
        lines.append(f"      evidence: {rendered_evidence}")
        if stage.get("note"):
            lines.append(f"      note: {stage['note']}")
    return "\n".join(lines) + "\n"


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize(state: dict, environment: str) -> dict:
    state.setdefault("goal", "")
    state["environment"] = state.get("environment", "unknown") if environment == "keep" else environment
    if not isinstance(state.get("inputs"), list) or not state["inputs"]:
        state["inputs"] = [{"path": "pending", "sha256": "pending"}]
    if not isinstance(state.get("stages"), list) or not state["stages"]:
        state["stages"] = [dict(stage) for stage in DEFAULT_STAGES]
    ids = {stage.get("id") for stage in state["stages"]}
    for default in DEFAULT_STAGES:
        if default["id"] not in ids:
            state["stages"].append(dict(default))
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage omni-flow case-state.yaml")
    commands = parser.add_subparsers(dest="command", required=True)

    create_parser = commands.add_parser("create")
    create_parser.add_argument("--file", type=Path, required=True)
    create_parser.add_argument("--goal", required=True)
    create_parser.add_argument("--environment", default="offline")

    show_parser = commands.add_parser("show")
    show_parser.add_argument("--file", type=Path, required=True)

    update_parser = commands.add_parser("update")
    update_parser.add_argument("--file", type=Path, required=True)
    update_parser.add_argument("--stage", required=True)
    update_parser.add_argument("--status", choices=["pending", "running", "completed", "failed", "skipped", "waiting-for-approval"])
    update_parser.add_argument("--output", action="append", default=[])
    update_parser.add_argument("--evidence", action="append", default=[])
    update_parser.add_argument("--input", action="append", default=[], help="artifact path; SHA-256 is calculated automatically")
    update_parser.add_argument("--environment", default="keep")
    update_parser.add_argument("--note")

    args = parser.parse_args()
    if args.command == "create":
        if args.file.exists():
            parser.error(f"already exists: {args.file}")
        args.file.parent.mkdir(parents=True, exist_ok=True)
        args.file.write_text(dump({
            "goal": args.goal,
            "environment": args.environment,
            "inputs": [],
            "stages": [dict(stage) for stage in DEFAULT_STAGES],
        }), encoding="utf-8")
        print(f"created {args.file}")
        return 0

    if not args.file.is_file():
        parser.error(f"not found: {args.file}")
    if args.command == "show":
        print(args.file.read_text(encoding="utf-8"), end="")
        return 0

    state = normalize(parse_simple_yaml(args.file.read_text(encoding="utf-8")), args.environment)
    by_id = {stage["id"]: stage for stage in state["stages"]}
    if args.stage not in by_id:
        parser.error(f"unknown stage: {args.stage}")
    stage = by_id[args.stage]
    if args.status:
        stage["status"] = args.status
    for item in args.output:
        if item not in stage["outputs"]:
            stage["outputs"].append(item)
    for item in args.evidence:
        if item not in stage["evidence"]:
            stage["evidence"].append(item)
    for item in args.input:
        artifact = Path(item)
        if not artifact.is_file():
            parser.error(f"not a file: {artifact}")
        record = {"path": str(artifact.resolve()).replace("\\", "/"), "sha256": file_sha(artifact)}
        by_path = {entry["path"]: entry for entry in state["inputs"]}
        by_path[record["path"]] = record
        state["inputs"] = list(by_path.values())
    if args.note:
        stage["note"] = f"{datetime.now(timezone.utc).isoformat()} {args.note}"
    args.file.write_text(dump(state), encoding="utf-8")
    print(f"updated {args.file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
