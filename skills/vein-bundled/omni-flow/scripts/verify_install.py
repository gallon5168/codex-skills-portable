from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

VERSION = "1.3.0"

FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/activation.md",
    "references/default-context.md",
    "references/router.md",
    "references/session-mode.md",
    "references/task-contract.md",
    "references/behavior-tests.md",
    "references/advanced-routing.md",
    "references/advanced-domains.md",
    "references/hard-target-re.md",
    "references/tooling-matrix.md",
    "references/evidence-reporting.md",
    "scripts/verify_install.py",
    "scripts/install_local.ps1",
    "scripts/create_case.py",
    "scripts/triage_artifact.py",
    "scripts/smoke_check.py",
    "scripts/classify_protector.py",
    "scripts/re_evidence_pack.py",
    "scripts/case_state.py",
    "scripts/regression_tests.py",
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare an omni-flow source tree with an installed copy.")
    parser.add_argument("--version", action="version", version=f"omni-flow {VERSION}")
    parser.add_argument("source", type=Path)
    parser.add_argument("installed", type=Path)
    args = parser.parse_args()
    mismatches: list[str] = []
    for relative in FILES:
        source = args.source / relative
        installed = args.installed / relative
        if not source.exists():
            mismatches.append(f"missing source: {relative}")
        elif not installed.exists():
            mismatches.append(f"missing installed file: {relative}")
        elif digest(source) != digest(installed):
            mismatches.append(f"different: {relative}")
    if mismatches:
        print("omni-flow install differs")
        print("\n".join(mismatches))
        return 1
    print(f"omni-flow {VERSION} install matches source")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
