#!/usr/bin/env python3
"""Executable regression tests for omni-flow's deterministic helpers."""

from __future__ import annotations

import importlib.util
import json
import struct
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def make_pe(path: Path, section_name: bytes, payload: bytes, writable_executable: bool = False):
    dos = bytearray(b"MZ" + b"\x00" * 62)
    struct.pack_into("<I", dos, 0x3C, 0x40)
    optional_size = 240
    pe = bytearray()
    pe += b"PE\x00\x00"
    pe += struct.pack("<HHIIIHH", 0x8664, 1, 0, 0, 0, optional_size, 0x0022)
    pe += b"\x00" * optional_size
    raw_pointer = len(dos) + len(pe)
    characteristics = 0x40000040 | (0x20000000 if writable_executable else 0) | (0x80000000 if writable_executable else 0)
    pe += section_name.ljust(8, b"\x00")
    pe += struct.pack("<IIIIIIHHI", len(payload), 0x1000, len(payload), raw_pointer, 0, 0, 0, 0, characteristics)
    data = bytes(dos + pe + payload)
    path.write_bytes(data)
    return data


def test_plain_pe(tempdir: Path):
    target = tempdir / "plain.exe"
    make_pe(target, b".text", b"A" * 4096)
    classifier = load("classifier_plain", SCRIPTS / "classify_protector.py")
    result = classifier.classify(target)
    require(result["format"] == "PE", "plain PE format not recognized")
    require(result["architecture"] == "x64", "plain PE architecture not recognized")
    require(len(result["signals"]["sections"]) == 1, "plain PE section count wrong")
    require(result["signals"]["sections"][0]["name"] == ".text", "plain PE section name wrong")
    require(result["route_class"] in ("standard-reverse-engineering", "protected-suspect"), "unexpected plain route class")
    return result


def test_protected_pe(tempdir: Path):
    target = tempdir / "protected.exe"
    payload = (
        b".vmp0" + b"\x00" * 64 +
        b"VMProtect" + b"\x00" * 16 +
        b"IsDebuggerPresent" + b"\x00" * 8 +
        b"NtQueryInformationProcess" + b"\x00" * 8 +
        b"\x9c\x58\x50\x9d" + b"\x60\xe8\x00\x00\x00\x00\x61" +
        bytes(range(256)) * 16
    )
    make_pe(target, b".vmp0", payload, writable_executable=True)
    classifier = load("classifier_protected", SCRIPTS / "classify_protector.py")
    result = classifier.classify(target)
    names = [item["name"] for item in result["signals"]["known_protectors"]]
    require("VMProtect" in names, f"VMProtect not recognized: {names}")
    require("IsDebuggerPresent" in result["signals"]["anti_analysis_apis"], "anti-analysis API missing")
    require(result["signals"]["virtualization_pattern_hits"] >= 2, "virtualization patterns under-detected")
    require(any(section.get("entropy") is not None and section["entropy"] > 7 for section in result["signals"]["sections"]), "high entropy missed")
    require(result["route_class"] == "hard-target", f"expected hard-target: {result['route_class']}")
    return result


def run_tool(script: Path, arguments: list[str]):
    process = subprocess.run(
        [sys.executable, "-X", "utf8", str(script), *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if process.returncode != 0:
        raise AssertionError(f"{script.name} failed: {process.stderr}\n{process.stdout}")
    return process.stdout


def test_evidence_pack(tempdir: Path):
    target = tempdir / "protected.exe"
    output = tempdir / "pack"
    test_protected_pe_file(target)
    stdout = run_tool(SCRIPTS / "re_evidence_pack.py", [str(target), "--out", str(output)])
    report = json.loads(stdout)
    require(report["schema"] == "omni-flow.re-evidence-pack/1", "wrong evidence schema")
    require(report["route_class"] == "hard-target", "evidence route class wrong")
    require((output / "classification.json").is_file(), "classification.json missing")
    require((output / "strings.txt").is_file(), "strings.txt missing")
    manifest = (output / "manifest.txt").read_text(encoding="utf-8")
    require("target_sha256=" in manifest and "pack_sha256=" in manifest, "manifest incomplete")
    require(report["claims"]["dynamic_execution_performed"] is False, "dynamic claim must remain false")
    return report


def test_protected_pe_file(target: Path):
    payload = (
        b".vmp0" + b"\x00" * 64 +
        b"VMProtect" + b"\x00" * 16 +
        b"IsDebuggerPresent" + b"\x00" * 8 +
        b"NtQueryInformationProcess" + b"\x00" * 8 +
        b"\x9c\x58\x50\x9d" + b"\x60\xe8\x00\x00\x00\x00\x61" +
        bytes(range(256)) * 16
    )
    make_pe(target, b".vmp0", payload, writable_executable=True)


def test_case_state(tempdir: Path):
    state_path = tempdir / "case-state.yaml"
    base = ["python", "-X", "utf8", str(SCRIPTS / "case_state.py")]
    create = subprocess.run(base + ["create", "--file", str(state_path), "--goal", "regression", "--environment", "offline"], capture_output=True, text=True)
    require(create.returncode == 0, f"case create failed: {create.stderr}")
    sample = tempdir / "artifact.bin"
    sample.write_bytes(b"omni-flow-evidence")
    update = subprocess.run(base + [
        "update", "--file", str(state_path), "--stage", "triage", "--status", "completed",
        "--output", "analysis/static/result.json", "--input", str(sample), "--note", "static pass"
    ], capture_output=True, text=True)
    require(update.returncode == 0, f"case update failed: {update.stderr}")
    text = state_path.read_text(encoding="utf-8")
    require("status: completed" in text, "stage status not persisted")
    require("analysis/static/result.json" in text, "output not persisted")
    require(sample.resolve().as_posix() in text, "input path not persisted")
    import hashlib
    digest = hashlib.sha256(sample.read_bytes()).hexdigest()
    require(digest in text, "input hash not persisted")


def test_activation_rules(tempdir: Path):
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    activation = (ROOT / "references" / "activation.md").read_text(encoding="utf-8")
    session = (ROOT / "references" / "session-mode.md").read_text(encoding="utf-8")
    require("$omni-flow" in activation and "/omni-flow" in activation, "command variants missing from activation")
    require("Do not wait for a second turn" in skill_text or "Do not wait for another confirmation" in activation, "immediate activation rule missing")
    require("【omni-flow: active】" in session and "every reply type" in session.lower(), "mandatory prefix rule incomplete")
    for cue in ("继续", "继续优化", "接着干", "continue"):
        require(cue in session, f"continuation cue missing: {cue}")


def main() -> int:
    tests = {
        "plain_pe": test_plain_pe,
        "protected_pe": test_protected_pe,
        "evidence_pack": test_evidence_pack,
        "case_state": test_case_state,
        "activation_rules": test_activation_rules,
    }
    with tempfile.TemporaryDirectory(prefix="omni-regression-") as temporary:
        tempdir = Path(temporary)
        results = {}
        for name, function in tests.items():
            try:
                function(tempdir)
                results[name] = "PASS"
            except Exception as error:
                print(f"FAIL {name}: {error}")
                return 1
        print(json.dumps(results, indent=2))
    print("omni-flow regression tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
