#!/usr/bin/env python3
"""Build a bounded reverse-engineering evidence pack for a supplied artifact."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ASCII_RE = re.compile(rb"[\x20-\x7e]{6,}")
UTF16LE_RE = re.compile(rb"(?:[\x20-\x7e]\x00){5,}")
URL_RE = re.compile(rb"https?://[\x21-\x7e]+", re.IGNORECASE)
IPV4_RE = re.compile(rb"\b(?:\d{1,3}\.){3}\d{1,3}\b")
REGISTRY_RE = re.compile(
    rb"(?:HKEY_[A-Z_]+|SOFTWARE\\\\|CurrentVersion\\\\)[\x20-\x7e]{3,}",
    re.IGNORECASE,
)

ANTI_ANALYSIS_MARKERS = [
    "IsDebuggerPresent",
    "CheckRemoteDebuggerPresent",
    "NtQueryInformationProcess",
    "OutputDebugString",
    "CreateToolhelp32Snapshot",
    "Process32First",
    "Process32Next",
    "EnumWindows",
    "GetTickCount",
    "QueryPerformanceCounter",
    "rdtsc",
]

VALIDATION_MARKERS = [
    "license", "serial", "activation", "register", "registerkey",
    "valid", "invalid", "expire", "trial", "auth", "token", "hwid",
]

CRYPTO_MARKERS = [
    "CryptAcquireContext", "CryptDecrypt", "CryptEncrypt", "CryptHashData",
    "BCryptDecrypt", "BCryptEncrypt", "AES", "RSA", "SHA", "MD5", "base64",
]


def hashes(data: bytes) -> dict[str, str]:
    return {
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    size = len(data)
    return -sum((n / size) * math.log2(n / size) for n in counts.values())


def load_classifier(script_dir: Path) -> object | None:
    path = script_dir / "classify_protector.py"
    spec = importlib.util.spec_from_file_location("omni_classify_protector", path)
    if not spec or not spec.loader:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def unique(values: list[bytes], limit: int = 100) -> list[str]:
    return list(dict.fromkeys(value.decode("latin-1", errors="replace") for value in values))[:limit]


def build_pack(target: Path, output: Path) -> dict:
    data = target.read_bytes()
    output.mkdir(parents=True, exist_ok=True)
    script_dir = Path(__file__).resolve().parent
    classifier = load_classifier(script_dir)

    classification = classifier.classify(target) if classifier else None
    if classification:
        (output / "classification.json").write_text(
            json.dumps(classification, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    strings_ascii = ASCII_RE.findall(data)
    strings_utf16 = [item.replace(b"\x00", b"") for item in UTF16LE_RE.findall(data)]
    all_strings = strings_ascii + strings_utf16
    lower_strings = [item.lower() for item in all_strings]

    markers = {
        "anti_analysis": ANTI_ANALYSIS_MARKERS,
        "validation": VALIDATION_MARKERS,
        "crypto": CRYPTO_MARKERS,
    }
    marker_hits: dict[str, list[str]] = {}
    for category, names in markers.items():
        hits = []
        for name in names:
            needle = name.encode("ascii").lower()
            if any(needle in item for item in lower_strings):
                hits.append(name)
        marker_hits[category] = sorted(set(hits))

    string_evidence = {
        "counts": {
            "ascii_min6": len(strings_ascii),
            "utf16le_min5": len(strings_utf16),
        },
        "urls": unique(URL_RE.findall(data)),
        "ipv4_candidates": unique(IPV4_RE.findall(data), 50),
        "registry_candidates": unique(REGISTRY_RE.findall(data), 50),
        "marker_hits": marker_hits,
    }

    section_entropy = []
    sections = classification["signals"]["sections"] if classification else []
    for section in sections:
        section_entropy.append({
            "name": section.get("name"),
            "entropy": section.get("entropy"),
            "raw_size": section.get("raw_size"),
            "raw_pointer": section.get("raw_pointer"),
        })

    report = {
        "schema": "omni-flow.re-evidence-pack/1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "target": {
            "path": str(target.resolve()),
            "size": len(data),
            **hashes(data),
        },
        "route_class": classification.get("route_class") if classification else "unclassified",
        "routes": classification.get("routes") if classification else [],
        "section_entropy": section_entropy,
        "strings": string_evidence,
        "claims": {
            "classification_state": "candidate" if classification else "not-observed",
            "dynamic_execution_performed": False,
        },
        "limitations": [
            "This is a static evidence package; it does not prove runtime behavior.",
            "String and pattern hits are candidate indicators, not confirmed capabilities.",
            "Protected or virtualized code requires boundary tracing or isolated dynamic validation.",
        ],
    }

    strings_path = output / "strings.txt"
    strings_path.write_text(
        "\n".join(unique(all_strings, len(all_strings) or 1)) + "\n",
        encoding="utf-8",
        errors="replace",
    )
    (output / "evidence-pack.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    pack_hash = hashlib.sha256((output / "evidence-pack.json").read_bytes()).hexdigest()
    (output / "manifest.txt").write_text(
        f"target_sha256={hashes(data)['sha256']}\npack_sha256={pack_hash}\n",
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a static reverse-engineering evidence pack")
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if not args.artifact.is_file():
        parser.error(f"not a file: {args.artifact}")
    report = build_pack(args.artifact, args.out)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
