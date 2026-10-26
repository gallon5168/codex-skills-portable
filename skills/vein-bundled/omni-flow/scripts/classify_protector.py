#!/usr/bin/env python3
"""Classify hard-target reverse-engineering signals for a supplied artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path


SECTION_ENTROPY_THRESHOLD = 7.0

PROTECTOR_MARKERS = {
    "UPX": [b"UPX0", b"UPX1", b"UPX!", b"UPX2"],
    "VMProtect": [b".vmp0", b".vmp1", b".vmp2", b"VMProtect", b".vmp"],
    "Themida/WinLicense": [b"Themida", b"WinLicense", b".themida", b".winlice", b"Tls0"],
    "Enigma": [b"Enigma", b".enigma", b"E Protector"],
    "ASProtect": [b"ASProtect", b".aspack", b".adata"],
    "StarForce": [b"StarForce", b"sforce", b".sfk"],
    "SafeEngine": [b"SafeEngine", b"Safengine", b".sedata"],
    "Denuvo": [b"Denuvo", b".denuvo", b"denuvo"],
}

RUNTIME_MARKERS = {
    ".NET": [b"mscoree.dll", b"_CorExeMain", b"BSJB"],
    "Python/PyInstaller": [b"pyi-", b"PYZ-00.pyz", b"python3", b"python37", b"python38", b"python39", b"python310", b"python311", b"python312"],
    "Java": [b"P K\x03\x04", b"META-INF/", b"classes.dex", b"dex\n"],
    "Electron": [b"electron.asar", b"app.asar", b"Electron"],
    "Go": [b"go.buildid", b"go:buildid", b"runtime.main"],
    "Rust": [b"rust_begin_unwind", b"/rust/", b".rustc"],
    "Unity/Mono": [b"mono.dll", b"GameAssembly.dll", b"global-metadata.dat", b"unity3d"],
    "Unreal": [b"UnrealEngine", b"GNames", b"GObjects", b"FNamePool"],
}

ANTI_ANALYSIS_APIS = [
    b"IsDebuggerPresent",
    b"CheckRemoteDebuggerPresent",
    b"NtQueryInformationProcess",
    b"OutputDebugString",
    b"CreateToolhelp32Snapshot",
    b"Process32First",
    b"Process32Next",
    b"EnumWindows",
    b"GetTickCount",
    b"QueryPerformanceCounter",
    b"rdtsc",
]

VIRTUALIZATION_PATTERNS = [
    b"\x9c\x58\x50\x9d",   # pushfd/pop eax/push eax/popfd sequence
    b"\x60\xe8\x00\x00\x00\x00\x61",  # pushad/call near/pushad epilogue pattern
    b"\x64\xa1\x30\x00",   # fs:[30] PEB access
    b"\x65\x48\x8b",       # gs-segment x64 TEB access
    b"\x0f\x31",           # RDTSC
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    frequencies = Counter(data)
    size = len(data)
    return -sum((count / size) * math.log2(count / size) for count in frequencies.values())


def read_pe(path: Path) -> tuple[bytes | None, dict]:
    data = path.read_bytes()
    info = {"format": "unknown"}
    if not data.startswith(b"MZ"):
        return None if not data else data, info

    info["format"] = "PE"
    if len(data) < 0x40:
        info["format"] = "PE-truncated"
        return data, info

    e_lfanew = int.from_bytes(data[0x3C:0x40], "little")
    pe = data[e_lfanew:e_lfanew + 4096] if 0 <= e_lfanew < len(data) - 24 else b""
    if pe[:4] != b"PE\x00\x00":
        info["format"] = "PE-invalid"
        return data, info

    if len(pe) < 24:
        info["format"] = "PE-header-truncated"
        return data, info

    machine = int.from_bytes(pe[4:6], "little")
    number_of_sections = int.from_bytes(pe[6:8], "little")
    optional_size = int.from_bytes(pe[20:22], "little")
    architecture = {
        0x014C: "x86",
        0x8664: "x64",
        0x01C0: "ARM",
        0xAA64: "ARM64",
    }.get(machine, f"machine-0x{machine:04X}")
    info.update(architecture=architecture, sections_declared=number_of_sections)

    size_of_optional_header_field = pe[20:22]
    optional_header_size = int.from_bytes(size_of_optional_header_field, "little")
    section_offset = e_lfanew + 24 + optional_header_size
    raw = data
    sections = []
    for index in range(number_of_sections):
        start = section_offset + index * 40
        chunk = raw[start:start + 40]
        if len(chunk) < 40:
            break
        name = chunk[:8].rstrip(b"\x00").decode("latin-1", errors="replace")
        virtual_size = int.from_bytes(chunk[8:12], "little")
        virtual_address = int.from_bytes(chunk[12:16], "little")
        raw_size = int.from_bytes(chunk[16:20], "little")
        raw_pointer = int.from_bytes(chunk[20:24], "little")
        characteristics = int.from_bytes(chunk[36:40], "little")
        if raw_pointer == 0 or raw_pointer >= len(raw):
            continue
        if name:
            sample = raw[raw_pointer:raw_pointer + min(raw_size, 262144)]
            valid = True
        else:
            sample = b""
            valid = False
        sections.append(
            {
                "name": name,
                "virtual_address": virtual_address,
                "virtual_size": virtual_size,
                "raw_size": raw_size,
                "raw_pointer": raw_pointer,
                "executable": valid and bool(characteristics & 0x20000000),
                "writable": valid and bool(characteristics & 0x80000000),
                "entropy": round(entropy(sample), 3) if valid else None,
            }
        )
    info["sections"] = sections
    return data, info


def classify(path: Path) -> dict:
    data, pe = read_pe(path)
    lower = data.lower()
    result = {
        "path": str(path.resolve()),
        "size": len(data),
        "sha256": sha256(data),
        "architecture": pe.get("architecture", "unknown"),
        "format": pe.get("format", "unknown"),
        "routes": [],
        "signals": {},
    }

    protectors = []
    for protector, markers in PROTECTOR_MARKERS.items():
        hits = sorted({marker.decode("latin-1") for marker in markers if marker.lower() in lower})
        if hits:
            protectors.append({"name": protector, "hits": hits})
    runtime_hits = []
    for runtime, markers in RUNTIME_MARKERS.items():
        hits = sorted({marker.decode("latin-1", errors="replace") for marker in markers if marker.lower() in lower})
        if hits:
            runtime_hits.append({"name": runtime, "hits": hits})
    anti_analysis_hits = sorted({api.decode("latin-1") for api in ANTI_ANALYSIS_APIS if api.lower() in lower})
    virtualization_hits = sum(1 for pattern in VIRTUALIZATION_PATTERNS if pattern in data)

    sections = pe.get("sections", [])
    high_entropy_sections = [
        section for section in sections
        if section["entropy"] is not None and section["entropy"] >= SECTION_ENTROPY_THRESHOLD
    ]
    executable_writable = [section for section in sections if section["executable"] and section["writable"]]

    signals = {
        "known_protectors": protectors,
        "runtimes": runtime_hits,
        "anti_analysis_apis": anti_analysis_hits,
        "virtualization_pattern_hits": virtualization_hits,
        "high_entropy_sections": high_entropy_sections,
        "executable_and_writable_sections": executable_writable,
        "sections": sections,
    }
    result["signals"] = signals

    score = 0
    if protectors:
        score += 3
        result["routes"].append("hard-target-re.md § protection triage / SP-multi-layer unpacking")
    if high_entropy_sections:
        score += 2
        result["routes"].append("static packer/crypter triage; dynamic dump only if self-decryption blocks recovery")
    if anti_analysis_hits:
        score += 2
        result["routes"].append("hard-target-re.md § anti-analysis workflow")
    if virtualization_hits >= 2 and (protectors or high_entropy_sections or executable_writable):
        score += 2
        result["routes"].append("boundary tracing first; lift only reachable handlers if necessary")
    if executable_writable:
        score += 1
        result["routes"].append("self-modifying/integrity-guard hypothesis; confirm before instrumentation")
    if any(item["name"] == ".NET" for item in runtime_hits):
        result["routes"].append(".NET metadata/decompiler workflow before native assumptions")
    if any(item["name"] == "Python/PyInstaller" for item in runtime_hits):
        result["routes"].append("extract child payload and re-triage before unpacking outer PE")
    if any(item["name"] in ("Unity/Mono", "Unreal") for item in runtime_hits):
        result["routes"].append("advanced-domains.md § game engines")
    result["hard_target_score"] = score
    result["route_class"] = (
        "hard-target" if score >= 5 else
        "protected-suspect" if score >= 3 else
        "standard-reverse-engineering"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify protected/virtualized target signals")
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--json", action="store_true", help="print JSON only")
    args = parser.parse_args()

    if not args.artifact.is_file():
        parser.error(f"not a file: {args.artifact}")

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

    report = classify(args.artifact)
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    print(rendered)

    output = args.artifact.with_suffix(args.artifact.suffix + ".protection.json")
    output.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
