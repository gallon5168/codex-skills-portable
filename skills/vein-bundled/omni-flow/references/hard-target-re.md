# Hard Target Reverse Engineering

Use this reference after `advanced-routing.md` selects a protected, virtualized, obfuscated, or anti-analysis target. Do not treat "top protector" as an end state. Decompose it into layers, choose the narrowest viable attack surface, and publish resumable evidence.

## 0. Triage contract

Record before deep work:

```yaml
target:
  sha256: observed-or-pending
  architecture: x86 | x64 | arm | unknown
  runtime: native | dotnet | java | python | electron | unity-il2cpp | unreal | unknown
protection:
  identified: []
  suspected: []
  evidence:
    - artifact: sections.json
      observation: high entropy / nonstandard names
goal:
  scope: whole-binary | single-function | decision-branch | patch | IOC | algorithm
  acceptance: executable proof or reproducible output
environment:
  mode: offline | isolated-vm | emulator | named-lab | remote-service
  snapshot: id-or-pending
```

Minimum first-pass signals: PE/ELF header, section table, entry point/TLS, imports/exports, resources, overlay, per-section entropy, signatures/version metadata, strings, compiler/runtime fingerprints, child processes/files/services, embedded archives, certificates, and known protector signatures. Preserve all outputs under `analysis/static`.

## 1. Protection triage

Classify each layer separately; never call the whole file "packed":

| Layer | Evidence to collect | Consequence |
|---|---|---|
| Packer/crypter | EP section mismatch, tiny stub, high entropy, sparse IAT, known section names | Find OEP or execute in isolation until self-decryption stabilizes |
| Import/IAT protection | unresolved thunks, delayed/reserved imports, API hashing, missing DLL references | Rebuild IAT at OEP or trace resolved APIs dynamically |
| Anti-analysis | TLS callbacks, `IsDebuggerPresent`, `NtQueryInformationProcess`, RDTSC, CPUID, hypervisor/vendor strings, checksum loops | Inventory before bypass; avoid blind patching that corrupts integrity checks |
| Obfuscation | flat dispatcher, opaque predicates, MBA expressions, substituted instructions, dead branches | Recover data flow/constants first; simplify locally before global decompilation |
| Virtualization | interpreter loop, handler table, context structure, bytecode blob, push/pop dispatch, unusual register encoding | Identify guest-to-handler contract; lift only relevant handlers/basic blocks |
| Integrity/service guard | self-hash, parent/process watchdog, driver/service dependency, online heartbeat, encrypted resource fetcher | Map trigger order; separate local repair from required external service |
| Licensing/auth boundary | UI strings/resources, crypto constants, socket/API calls, license files, registry blobs, hardware IDs | Target input transformation/comparison rather than whole-program recovery |

After the first pass, emit a routing decision before choosing tools:

```yaml
route:
  primary_surface: unpack | iat | anti-analysis | deobfuscate | vm-lift | boundary | integrity | external-dependency
  reachable_path: function-address-or-symbol-or-branch-id
  entry_condition: stable-snapshot | passive-trace | known-unpacker | precondition-missing
  stop_condition: oep-found | api-map-complete | check-neutralized-copy | decision-recovered | handler-subset-lifted
  fallback: next-rung-if-dump-invalid | next-surface-if-static-hostile | isolate-dependency-if-server-bound
```

Use these hard rules when several protections overlap:

- **Top packer / SP**: do not attach at EP by default. Run passive child/process/module/file/registry/network telemetry, let a stage settle only in an isolated snapshot, dump per stage, and reject any dump lacking OEP/import/state evidence.
- **Virtualized code**: identify bytecode, PC/IP, context layout, dispatch loop, operand decoder, and exit contract before lifting. Lift only handlers reached from the target path; validate each lifted edge against concrete input/output traces.
- **Top anti-debug / anti-VM**: inventory every probe and its effect before changing bytes. Distinguish silent corruption, delayed decryption, remote reporting, and execution gating; prefer environment normalization or API return shaping on a copy, then re-check dependent integrity paths.
- **Protected core function**: model callers, arguments, return shape, exceptions, timing, memory writes, and observable outputs first. Enter the VM only when boundary tracing/input differential cannot answer the accepted question.
- **Heavy obfuscation / MBA / flattening**: recover constants, tables, comparisons, API calls, and data-flow anchors before global CFG reconstruction. Simplify one function/basic block family and keep unresolved constructs explicit.
- **Integrity guard**: map hash inputs, trigger order, storage location, and failure behavior. Repair must either preserve the expected digest or satisfy the verifier without corrupting key derivation.

## 2. Anti-analysis workflow

1. Build a passive inventory from strings/imports/syscalls/resources; do not patch the first check found.
2. Group checks by effect: debugger presence, breakpoint/hardware registers, timing, virtualization, sandbox artifacts, process/module/window names, integrity, user interaction, network/licensing.
3. Determine whether a check controls execution, corrupts state silently, delays execution, changes decryption keys, or reports remotely.
4. Choose the least invasive handling: environment normalization > API return shaping > conditional bypass on a copy > controlled hook > key-preserving emulation. Record original/new bytes and all dependent integrity paths.
5. Re-run the narrow experiment after each change. If state diverges, restore the snapshot and isolate the new dependency.

Deliverables: anti-analysis matrix, exact trigger/effect, chosen handling, patched-copy hash, and regression observation.

## 3. SP / multi-layer unpacking

"SP壳"/sealed or run-time-unpacking protectors require stage separation:

1. Snapshot clean state; capture loader stages with process/thread/module/file/registry/network monitoring before attaching a debugger.
2. Let each layer finish its own initialization where safe, then dump memory regions and reconstruct the likely OEP using call/ret balance, import resolution, resource initialization, exception-registration changes, and transition to high-level code.
3. Dump per layer, not once globally. Record base/size/protection, reconstructed imports, relocated pointers, TLS/state dependencies, stolen bytes, and checksummed regions.
4. Repair copies independently: rebuild imports, fix relocations/tls/callbacks, restore stolen prologues, remove or satisfy integrity guards, and preserve any value derived from original bytes.
5. Re-triage every dumped child; a later layer may contain another packer/runtime/virtual machine.
6. If a layer depends on server state/device identity/time, mark it as an external precondition and continue with all independent layers.

Minimum artifacts: stage timeline, memory maps/dumps with hashes, OEP evidence, repaired-copy diff/hash, import map, failed-layer reason, and next isolated experiment.

## 4. Code obfuscation and devirtualization

For flattened/obfuscated code, prefer local simplification over heroic full lifting:

1. Normalize representation: disassemble raw bytes, resolve jumps/calls, remove junk/non-returning branches, propagate constants/stack values, and collect MBA/bitwise identities.
2. Recover data-flow anchors before control flow: constants, tables, buffers, comparisons, crypto round patterns, error codes, imported calls, and observable outputs.
3. For flattening, identify real dispatcher state variables, predecessor/successor edges, loop bounds, and invariant blocks; reconstruct a reduced CFG for the target function only.
4. For virtualization, locate bytecode blob, PC/IP register, context layout, handler dispatch mechanism, operand decoding, and exit semantics. Lift one handler family at a time and validate against traces.
5. Use differential tracing: same function with selected input pairs reveals arithmetic, comparison, branching, and key derivation even when static CFG is hostile.
6. Symbolic/constraint tools may assist bounded goals, but validate models against concrete executions; do not present unsolved constraints as recovered logic.

Minimum artifacts: simplified function/CFG, lifted handler subset if applicable, anchor evidence, concrete trace comparison, confidence rating, and unresolved constructs.

## 5. Protected boundary workflow

When a top-tier product protects only core functions, do not attempt whole-program defeat:

1. Enumerate callers, arguments, return shape, side effects, imported APIs, exceptions, timing, and observable outputs around the protected function.
2. Decide whether the question can be answered by pre/post observation, input/output differential, partial emulation, selective instrumentation, or protocol/config recovery instead of entering the VM.
3. Instrument boundaries only after establishing a stable snapshot: entry/exit hooks, memory watchpoints, API breakpoints, exception filters, or syscall traces.
4. If entry into the VM is unavoidable, map only reachable handlers for the requested path. Stop when the decision/key/result is recovered.
5. Preserve server-side or hardware-bound facts as external dependencies; never invent local results for them.

Minimum artifacts: boundary signature, caller/argument model, observation method, recovered transformation/decision, external dependencies, and reproducibility limits.

## 6. Escalation ladder

Use the cheapest successful rung and stop as soon as acceptance is met:

1. Static triage + known unpacker/protector-specific extraction.
2. Isolated execution to self-decryption + memory dump/import repair.
3. Anti-analysis normalization/bypass on a copied target.
4. Boundary tracing/input-output differential around protected function.
5. Local simplification/deobfuscation of target function.
6. Handler-level virtual-machine lifting for reachable path.
7. Emulation/instrumentation of missing hardware/server dependencies.
8. Broad whole-program reconstruction only if the user explicitly requires it.

At each failure, record the exact failing assumption, tool/version, command, expected vs observed state, and switch rung or surface. Never repeat an identical failing strategy without changing evidence or environment.

## 7. Failure-to-route protocol

A failed experiment must change the next action:

| Observed failure | Do not retry | Next route |
|---|---|---|
| Dump crashes or imports unresolved | Global dump / guessed OEP | Re-run to stable import/resource init; reconstruct per-stage OEP with call balance and API resolution evidence |
| Breakpoint/hook silently changes result | Blind byte patch | Trace integrity/hash dependency first, normalize environment/API returns on a copy, satisfy rather than delete checks |
| Static CFG is flattened or unreadable | Full decompilation loop | Extract anchors/constants/differentials, simplify reachable blocks, then lift only unresolved handlers |
| VM trace has hundreds of unrelated handlers | Whole-guest lifting | Pin context/PC/handler table, trace target entry/exit, lift reachable handler families and compare outputs |
| Result depends on server/device/time | Local invention | Record exact request/precondition, continue offline/static/boundary work, isolate replayable dependencies |
| Protector detects tooling | Same debugger/plugin repeat | Change observation layer (kernel/user/API/emulation), minimize footprint, use staged snapshots and passive telemetry |

Every route change records: failing command/tool/version, expected versus observed state, preserved artifacts and hashes, new surface, acceptance still outstanding.

## 8. Report additions

Add to reverse-engineering reports:

```markdown
## Protection Matrix
| Layer | Identified/Suspected | Evidence | Handling | Confidence |
|---|---|---|---|---|

## Stage Timeline
| Stage | Trigger | Memory/File/Registry/Network State | Artifact Hash | Result |
|---|---|---|---|---|

## Recovery Limits
| Goal | Recovered | External/Hardware Bound | Next Experiment |
|---|---|---|---|
```
