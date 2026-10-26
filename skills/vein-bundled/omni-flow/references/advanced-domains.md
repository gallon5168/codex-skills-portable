# Advanced Domains

These are bounded sub-workflows. Read only the section selected by `advanced-routing.md`.

## Windows runtimes

1. Identify container/runtime before deep disassembly: native PE, Nuitka/PyInstaller, `.pyc`, CLR/.NET, Go, Rust, Electron, Tauri, Delphi, AutoIt, e-language, Java, installer, or packer.
2. Record format magic, imports, sections, entropy, signatures, version resources, embedded archives, and obvious launcher strings.
3. Extract on a copy: PyInstaller → `pyinstxtractor`; .NET → ILSpy/dnSpyEx metadata; Java → CFR/Procyon; Electron → ASAR/archive inspection; installers → Inno/NSIS/MSI extraction.
4. Re-triage extracted payloads; do not assume the outer EXE contains the real logic.
5. Locate auth/license/validation boundary through strings, resource IDs, imports, cross-references, or decompiled symbols.
6. Prefer minimal static patch + test over broad dynamic work. Preserve original bytes and provide exact offset/original/new-byte tables.

Minimum artifacts: runtime classification, extraction command/output, key function/file references, validation-flow summary, and reproducible patch/test plan.

## Game engines

1. Detect engine/build: Unity Mono, Unity IL2CPP, Unreal, Godot, custom engine.
2. For Unity Mono, inspect managed assemblies and recover classes/methods. For IL2CPP, correlate global metadata and generated bindings.
3. For Unreal, locate engine object stores such as GNames/GObjects and reconstruct relevant structures only as needed by the question.
4. Use supplied PDBs, symbols, config files, logs, and public SDK knowledge before guessing offsets.
5. Validate candidate structures/functions with at least two independent anchors: string/xref, vtable/layout, constant pattern, runtime state, or observable behavior.
6. Report named functions, structure layouts, confidence levels, and exact reproduction steps.

Minimum artifacts: engine/version classification, anchor evidence, recovered names/structures, uncertainty list, and next validation step.

## Code audit

1. Build a small threat model: trust boundaries, authentication/authorization, input sinks, deserialization, file/path handling, command/process execution, SSRF, crypto, secrets, and privilege changes.
2. Run available scanners as candidate generators; never report scanner output without reachability review.
3. Trace user-controlled data from entry point to sensitive sink; identify guards and bypass/precondition states.
4. Verify with the strongest available local proof: unit/integration test, fixture parser, debugger trace, request replay against a named lab, or code-level invariant proof.
5. Deliver location, data flow, impact conditions, minimal patch, regression test, and actual test output.

Minimum artifacts: reviewed scope, scanner command/results, human-verified findings, patches/tests, and remaining false-positive candidates.

## Active Directory

Use only a clearly identified lab/staging scope.

1. Start with identity/exposure enumeration and graph paths before any exploit attempt.
2. Map accounts, groups, ACLs, delegation, SPNs, certificate templates, trust relationships, and reachable services.
3. Rank paths by precondition, blast radius, persistence/noise, and reversibility.
4. Prefer read-only enumeration and harmless proof of control. Separate credential-material handling from path analysis.
5. Record sanitized commands, scope boundaries, observed outputs, and cleanup steps.

Minimum artifacts: scope note, identity/graph evidence, ranked paths with preconditions, safe validation result, remediation mapping.

## Cloud and Kubernetes

Use only a clearly identified account/project/namespace/lab.

1. Establish current identity and effective permissions first (`whoami`/caller identity/`auth can-i --list` equivalents).
2. Inventory exposed storage, roles/policies, secrets handling, network exposure, workload privileges, host mounts/capabilities, admission controls, and image provenance.
3. Distinguish misconfiguration evidence from exploitable chain evidence.
4. Prefer API reads and non-destructive probes. Never scan outside the stated boundary.
5. Deliver least-privilege fixes, policy controls, and verification commands.

Minimum artifacts: identity context, permission inventory, configuration findings, exploitability assessment, least-privilege remediation.

## Digital forensics

1. Preserve originals; verify hashes and work on mounted/copied evidence.
2. Build source taxonomy and timeline from filesystem, registry, logs, prefetch/shimcache/amcache or platform equivalents, browser data, memory process/network artifacts, and file metadata.
3. Correlate at least two independent sources for material events.
4. Track anomalies through process/file/user/network pivots; mark unsupported attribution as hypothesis.
5. Export IOCs, affected assets, execution/persistence evidence, containment candidates, and gaps.

Minimum artifacts: acquisition hashes, timeline excerpt, correlated evidence table, IOC list, confidence-rated conclusions, and collection gaps.

## Custom protocols

1. Segment frames using length prefixes, delimiters, fixed headers, magic values, sequence numbers, checksums, compression, and timing/reconnection boundaries.
2. Align multiple similar messages to identify invariant fields, counters, flags, opcodes, endianness, padding, and checksum placement.
3. Recover serialization formats; for protobuf/gRPC use raw decode, schema recovery, HTTP/2 framing, and client/library correlation.
4. Locate crypto/key derivation in the client when payload entropy blocks decoding.
5. Produce a message table, annotated hex evidence, decoder script/command, and state-machine diagram or equivalent textual model.

Minimum artifacts: frame layout, message type table, reproducible decode, state transitions, and unresolved encrypted/unknown fields.
