# Deobfuscation / Devirtualization Methodology (Making Sense of Protected Code)

> **Positioning**: covers "once strong obfuscation is identified, how do you tear it apart" -- not "switch to Frida black-box observation." Iron Rule 14's escape hatch (2 signals -> Frida Stalker trace) suffices for **pure bypass** (observe input/output, patch the branch consuming a value); but when the deliverable requires **understanding the algorithm inside the VM** (keygen, algorithm-level forgery of request signing/challenge-response -- cheatsheet 4b/6), a black-box boundary can't give you the algorithm and genuine deconstruction is required.
> **[WARN]** general RE methodology + public tool guidance, not tested within this project or verified against this skill's historical targets. Confirm tool availability per Rule 1, pick the best tool per Rule 3, tag deconstruction confidence per Rules 6/7.
> **Cost judgment first**: devirtualization/de-CFF is high-cost. Just need the program to let it through (patch a branch, hook a return value) -> **no deconstruction, go black-box** (Iron Rule 14 + hard-target black-box boundary). Need to reproduce the algorithm (keygen, request signing, compute a legitimate response) -> **only then is deconstruction worth it**. Black-box first if it solves it; deconstruct only when there's no other way.

## 1. Master decision tree: black-box vs. deconstruction

```
Obfuscated code is blocking you
        |
        v
 Need to "understand the algorithm," or just "get it to let you through"?
        |
   .----+-----.
 Just need to pass      Need the algorithm (keygen/signing/challenge-response)
   |              |
   v              v
 Black box:          First determine obfuscation type (diec/yara-sigs/static observation):
 - hook the boundary     |- Control-flow flattening (CFF) -> [2], medium cost, mature tools (d810/HexRaysDeob)
   observe input/output  |- Code virtualization (VM)   -> [3], high cost, off-the-shelf devirtualizer first, then manual
 - patch the branch    |- Opaque predicates/junk code -> [4], low cost, scriptable cleanup
   that consumes it   `- Encrypted strings/APIs  -> [5], low cost, runtime dump or scripted decryption
 - Frida Stalker
   trace the real flow
 (Iron Rule 14)
```

Quick characterization: **CFF** decompiles into one giant `while(1){ switch(state){...} }`; each case ends by assigning `state` a new constant and jumping back to the dispatcher. IDA graph view: star/comb shape, one central node fanning to dozens of blocks, each jumping back to center. **Code virtualization** decompiles into "fetch opcode -> index a jump table -> execute a small chunk -> return to fetch point," with an obvious **VIP (virtual instruction pointer)** increment and a **handler table**; native instructions translated into custom bytecode. **Opaque predicates/junk code**: local always-true/always-false jumps (`xor eax,eax; jz` always taken), `push imm; ret` in place of `jmp`, meaningless arithmetic between real instructions; disassembly misaligns within a small range (Iron Rule 14 signal). **Encrypted strings/APIs**: string scans find no plaintext, decrypted only at runtime; `GetProcAddress` replaced by a hash loop.

## 2. Control-flow flattening (CFF) reconstruction

CFF is the **most common** obfuscation for commercial license checks (cheaper than full virtualization): rewrites sequential/branching flow into a "dispatcher + state variable" loop where execution order is decided by `state`'s value, not code layout.

Signature: (1) **Dispatcher** -- a central block, usually `switch(state)` or a `cmp state, imm / je` chain. (2) **State variable** -- rewritten by every real block at its end to the constant for the next block. (3) **Real blocks** -- scattered original code, each doing real work, then updating `state` and jumping back to the dispatcher.

Manual reconstruction (understand the principle; prefer tools in practice): (1) find the variable every block writes and the dispatcher reads -- that's `state`; (2) enumerate state-value -> block mapping from each block's ending `mov state, 0x1234`; (3) a branching block **conditionally** assigns one of two values to state (`cmov`) -- that's the original `if/else`, use it to rebuild the star shape into the real CFG; (4) output the real CFG, or annotate/patch in IDA so the decompiler outputs normal pseudocode.

### Tools (prefer over manual work -- Iron Rule 3; confirm IDA/Ghidra version per Rule 1, ask before downloading per Rule 5)

| Scenario | Tool | Repository | Notes |
|---|---|---|---|
| Hex-Rays de-CFF/de-OLLVM plugin (first choice) | **d810** | `joydo/d810` | Deobfuscates at IDA microcode layer; works well against OLLVM-family (CFF, opaque predicates, fake control flow); configure rules, run decompiler once, usually comes out clean |
| Hex-Rays microcode deobfuscation (classic) | HexRaysDeob | `RolfRolles/HexRaysDeob` | Paper-grade microcode deobfuscator, handles opaque predicates/CFF |
| Ghidra-side deobfuscation | OOAnalyzer / gorillafuzz-style | search "ghidra deflatten" | Ghidra P-code layer scripts; several community CFF-deflattening scripts |
| Source-level symbolic deobfuscation (e.g. Tigress) | Tigress_protection | `JonathanSalwan/Tigress_protection` | Symbolic execution + taint analysis + LLVM, automatic (already in tool-registry Sec.1) |
| Custom deflatten script base | miasm / Triton / angr | (canonical) | CFG recovery + symbolic solving of state transitions |

**Practical advice**: try **d810** first (install into IDA, run decompiler once) -- 80% of OLLVM-family CFF flattens to normal pseudocode with zero manual work. Hand-roll miasm/Triton only for what d810 can't handle (custom CFF, hybrid VM).

## 3. Code virtualization (VMProtect/Themida) handler analysis

Translates native x86 instructions into custom bytecode, executed instruction-by-instruction via an interpreter (VM) -- the strongest obfuscation form, since original x86 instructions no longer exist in the binary, only VM bytecode + handlers.

Reconfirm it's worth it first: full-function virtualization can take days per function to manually deconstruct. Bypass only: hook the VM function's **boundary** (entry params, exit return value), observe black-box (hard-target black-box boundary + Iron Rule 14) -- the VM protects the "process," input/output stay plaintext. Need the algorithm: prefer an off-the-shelf devirtualizer first, go manual only if all fail.

### Off-the-shelf devirtualizers (first choice -- already in tool-registry Sec.1, this fills in method)
| Target | Tool | Key prerequisite |
|---|---|---|
| VMProtect x64 3.x | **NoVmp** (`can1357/NoVmp`) | Depends on VTIL; strongly tied to VMP version -- mismatch fails outright (tool-registry Sec.0.4) |
| VMProtect pure functions (no side effects) | Triton-VMP (`JonathanSalwan/VMProtect-devirtualization`) | Symbolic execution; suited to math/keygen-type pure functions |
| Lifting VMProtect to LLVM | MogVMP (`eversinc33/MogVMP`) | Depends on Remill |
| Themida 3.x devirtualization (WIP) | bobalkkagi | Experimental, unstable |

Manual steps (only once all off-the-shelf tools fail -- unsupported version/custom VM): (1) locate the VM entry (vmenter) -- native code jumps in via `push`es saving context then a jump to the dispatch loop; (2) locate the dispatch loop -- find the **VIP** and the jump it drives, typical form `movzx eax, byte [VIP]; inc VIP; jmp [handler_table + eax*8]`; (3) extract the handler table -- the opcode-indexed table of handler addresses (usually a few dozen to one-two hundred); (4) reverse each handler's semantics -- small, one "virtual instruction" each, its effect on the VM context (virtual registers = a memory/stack block: add? load? push? branch?), building an `opcode -> semantics` table; (5) dump the bytecode -- break on the VIP at runtime, or statically extract from the data segment; (6) disassemble bytecode -> recover native semantics via the step-4 table; (7) optionally recompile and verify against the VM's real output (Iron Rule 6's side-by-side check).

Leverage: symbolic execution instead of by-hand (Triton/miasm auto-derive a handler's semantics -- NoVmp/Triton-VMP are built on this); only deconstruct the path you need (a keygen exercises a single data-flow path -- trace it with Frida Stalker/Pin, recover only that path -- cheapest route to algorithm-level forgery); the VM context is a struct (recover virtual registers as a struct per methodology.md's technique, turning `*(ctx+0x18)` into `ctx->vreg3`).

## 4. Static cleanup of opaque predicates / junk code

**Local** obfuscation, lowest cost, cleaned up in bulk via scripts.
- **Opaque predicates**: always-true/always-false conditions looking like real checks (`(x*x) >= 0` always true, `(x & 1) && !(x & 1)` always false), inserting never-executed fake branches. Cleanup: identify the constant condition -> replace the conditional jump with unconditional (or delete the fake branch) -> patch to NOP/jmp. d810/HexRaysDeob do this automatically at the microcode layer.
- **Junk code (disassembly misalignment)**: `push imm; ret` for `jmp`, `EB 00` (jmp+0 no-op), `E8` followed by garbage bytes to misalign linear disassembly. Iron Rule 14 covers recognizing the signals; cleanup: once true instruction boundaries are determined, NOP the garbage and straighten fake jumps, using the stackstring/de-junk scripts in `references/ida-re/scripts/` plus manual undefine/re-analyze.
- **Principle**: cleanup exists to get the decompiler outputting normal pseudocode. Afterward, re-analyze (IDA re-analyze) and confirm function boundaries/xrefs come back normal (echoes Iron Rule 13's "wait for IDA's auto-analysis to finish").

## 5. Decrypting encrypted strings/APIs

Plaintext is hidden to raise the bar for static analysis (not the defense itself, but it blocks reading the logic).

**String encryption**: recognize by string scans finding no URLs/field names, code has "grab ciphertext -> call decryption function -> use plaintext." Static: reverse the decryption function (often XOR/RC4/homegrown), reimplement in Python, batch-decrypt the data segment, annotate in IDA. Dynamic (cheaper): break at the decryption function's return point and dump plaintext directly, or Frida-hook it to print every plaintext -- much faster than statically reversing the algorithm.

**API encryption/hashing**: malware and strong packers skip the static import table, resolving APIs at runtime via a hash loop -- walk a DLL's export table, hash each name, compare against a constant, take the address on match. Recognize by `LoadLibrary` plus a loop doing character-by-character `ror/add` on a string (ROR13/CRC32/DJB2) compared against a constant (shellcode-analyzer names this at line 107). Solution A (hash->name table): identify the algorithm -> pre-compute the hash for every export name of the target DLL -> build a `hash -> API name` dict -> replace/annotate hash constants with real names (search "hashdb" / OALabs HashDB for ready-made scripts). Solution B (runtime dump): hook the return point of the resolution function, record hash -> resolved address -> API name; one pass labels every dynamically-resolved API. **Tool**: **OALabs HashDB** (`OALabs/hashdb`, IDA/Ghidra plugin) -- de facto standard, automatic algorithm identification + table-based recovery.

## 6. Dynamic fallback: symbolic execution / trace-driven

When static deconstruction won't budge (custom VM, heavy CFF+VM hybrid):
1. **Frida Stalker trace of the real path** (first choice, Iron Rule 14): records every instruction/basic block walked during one real execution -- naturally immune to junk code/fake stacks/CFF since it follows actual execution flow regardless of physical layout. Analyze only the chain actually walked.
2. **Symbolic-execution solving** (Triton/angr/miasm): treat input as symbolic, let the engine auto-derive the input->output constraint relationship -- can directly solve a keygen's inverse (given a target output, solve for a valid input). Suited to math-type/pure-function authorization algorithms.
3. **Pin/DynamoRIO instrumentation**: instruction-level trace + memory-access recording, a data-collection foundation for devirtualization (input for tools like NoVmp).

**Key discipline**: dynamic findings must be written back into the static repository (methodology.md's static<->dynamic section) -- the real call chain from a trace, the algorithm solved via symbolic execution, both need naming, annotation, and verification (Iron Rule 6) in IDA, not left at "got it working once."

## 7. Hooking into the main workflow

| When to come here | Which section to read |
|---|---|
| Stage 4 triage: decompiles into a giant `while+switch`, star-shaped CFG | [2] CFF reconstruction (try d810 first) |
| Stage 4 triage: VIP increment + handler table | [3] VM analysis (off-the-shelf devirtualizer first) |
| Iron Rule 14 signal fired but you need to understand the algorithm (not just bypass it) | [3]/[6] -- black-box alone won't do |
| Local disassembly misalignment, constant jumps | [4] Opaque predicate/junk code cleanup |
| No plaintext in strings / APIs resolved via hash | [5] (prefer dynamic dump, OALabs HashDB) |
| All off-the-shelf tools fail, manual deconstruction required | [3] manual steps + [6] symbolic execution |

**Relationship to Iron Rule 14**: Rule 14 says "2 signals -> Stalker trace," the default for bypass-oriented work. This file is the understanding-oriented supplement -- when the deliverable requires reproducing the algorithm/keygen/signing (cheatsheet 4b/6), black-box trace can't give you the algorithm, and that's when you escalate to the deconstruction techniques here. No conflict: black-box first, deconstruct only when there's no other way, and even then prefer off-the-shelf tools first.

> Tools fetched via `scripts/fetch-tool.ps1` (Iron Rule 5, ask the user first); for devirtualization/de-CFF tools see `references/tool-registry.md` Sec.1 and the tables in [2]/[3] above.
