# Bypass Attempts Memory Log -- <Target Name>

> **Lite vs full (read first)**: on a **fast-path / simple target**, do NOT copy this whole 6-section template up front -- it's overkill. Keep a lightweight inline log instead: target path + type, gate location, one line per attempt with a status tag (`[OK]/[Y]/[X]/[WARN]`), and a patch-ledger line *only if you edit bytes*. Copy this **full template only when you escalate to the heavy route** (packer/VM/obfuscation) or it's a multi-session target where context compaction will lose state. The sections below are the full form for those cases.
>
> **Usage**: copy this template per target into its own record (e.g. `<target>-attempts.md`) in that target's working directory.
> **Iron Rule mapping**:
> - Rule 6: only "success, with on-the-spot evidence" entries feed the hardening document; the mechanism explanation needs single-variable retesting before it's settled causation -- otherwise tag "conjecture, not isolated-verified."
> - Rule 7: update this file every time a method is tested; read it in full before testing anything new. After context compaction, treat it as sole source of truth. Tag every conclusive statement: `[OK] verified` / `[WARN] conjecture, based on XX, unverified` / `[X] disproven` -- never write a guess in a tone that reads like fact.
> - Rule 16: fill in the route planning table below first, score by static evidence, rank by priority, work the top one.

## Target Basic Information

- Target file / service:
- Architecture / bitness:
- Pack-detection result (diec): packer=____ compiler=____ entropy=____
- Authorization form (local / online / hybrid):
- Packet-capture summary (authorization endpoint, key fields):
- Analysis date:

## Route Planning Table (mandatory at Stage 2.5, before acting -- Iron Rule 16)

> Static evidence should answer: (1) plaintext assets/models locally? (2) auth conclusion lands in a local cache/file/registry? (3) responses replayable/signed/session-rotated? (4) interpreter-packaged? Score each route, work the highest; when stuck, return here to decide keep-going vs. switch -- don't improvise randomly.

| Candidate Route | Supporting Evidence | Feasibility Score (1-5) | Expected Difficulty | Priority | Current Status |
|---|---|---|---|---|---|
| Fake the server (Stage 3) | | | | | |
| Local state/file forgery (technique 5) | | | | | |
| Memory/hook decision point (Stage 4B) | | | | | |
| Read source (interpreter packaging, Iron Rule 15) | | | | | |

## Confirmed Authorization Logic Locations

> Confidence: `[OK] verified` / `[WARN] conjecture` (based on XX, unverified) / `[X] disproven`. Never write a guess as if it were fact (Rule 7).

| Location (function/address/endpoint) | Purpose | How Discovered | Confidence | Notes |
|---|---|---|---|---|
| | | | | |

## Attempt Log (append every step immediately; append-only, never edit/delete -- Iron Rule 7)

> Status: [OK] genuinely unlocked (evidence) / [Y] UI unlocked, feature still not working (common with multi-layer gates, not success) / [X] failed / [WAIT] in progress / [WARN] pending verification (theoretical, not witnessed) / [LOOP] overturned (later evidence disproved it)
> **One line per step**, not per method: what was checked, what was concluded, why the next step follows. A hard target can take dozens of steps; skip one and you can't resume after context compaction.
> **Never delete an overturned entry**: keep the original line, append "[LOOP] Overturned #X: evidence + reason." Deleting/rewriting risks re-walking the dead end or mistaking it for fact. **Failed paths and why they were overturned are themselves the most valuable output** -- they tell the next pass what not to retry.

| # | Date | Technique (matches cheatsheet number) | Specific Steps/Location | Status | On-the-spot Evidence | Failure Reason / Next Step |
|---|---|---|---|---|---|---|
| 1 | | e.g. Technique 1: patch je->jmp @0x401A20 | | [X] | | Triggered integrity self-check, exited |
| 2 | | e.g. Technique 2: Frida hook validate_license returns 1 | | [OK] | Screenshot/log: program entered the authorized UI and the feature ran successfully | -- |
| 3 | | e.g. Technique 3: wildcard-forge all token endpoints after login | | [Y] | UI shows Pro edition, but the generation feature hitting the remote :8443 still returns 401 | Gate is verified server-side, can't bypass client-side -> recorded as "client-side cannot bypass" |
| 4 | | e.g. judged `_verify_session_hash` as the blocking point | Inferred purely from the function name | [WARN] | None (not run) | Pending verification by enumeration |
| 5 | | [LOOP] Overturned #4 | After enumerating all gates, confirmed the block is elsewhere | [LOOP] | Capture evidence id 22 | #4 was guessed from the name alone; kept, not deleted -- don't recheck |
| | | | | | | |

## Excluded Methods (don't retry)

> Distilled from the [X] rows above, so a low-context pass doesn't repeat them.

- 
- 

## Patch Ledger (log immediately when modifying the target file/memory; reversibility mandatory)

> **Why mandatory**: modifying an exe/memory without recording address + original bytes means no rollback, no repro, no way to tell the user what changed. Fill in the row before applying any patch, then act.
> **Bytes verbatim in hex**: `74 12` -> `EB 12`, not "changed je to jmp." You need the exact bytes to revert.
> **Back up first**: `Copy-Item target.exe target.exe.bak`; put the restore command directly in the recovery column.

| # | Type (file/memory/register) | Location (module+offset / absolute address) | Original Bytes | New Bytes | Purpose | One-click Restore Command/Method | Related Attempt # |
|---|---|---|---|---|---|---|---|
| 1 | e.g. File | `app.exe + 0x1A20` (.text) | `74 12` | `EB 12` | je->jmp to skip the license-check-failure branch | Write `74 12` back to the 2 bytes at 0x1A20; or `Copy-Item app.exe.bak app.exe` | Attempt 1 |
| 2 | e.g. Memory (x64dbg) | `app.exe + 0x2F00` (runtime) | `00` (al) | `01` (al) | Force validate to return 1 | Change al back at runtime, or don't save (memory patches are lost on restart anyway) | Attempt 2 |
| | | | | | | | |

> **Before delivery**: every row must be "restored" or explicitly listed as "left in place" in the delivery notes. Never modify an exe without telling the user which bytes changed (Rules 5, 6). A kept patch needs a `.bak` or diff.

## Verified-Successful Bypasses (-> feeds Stage 5 hardening document)

> Only entries here reach Stage 5. Each entry: bypass point + on-the-spot evidence + hardening measure.
> **Mechanism isolation (Iron Rule 6)**: if success followed several simultaneous changes, undo each individually and rerun to find which one caused it. Only then write it as settled causation; otherwise "mechanism isolation-verified?" = "No, conjecture."

| Bypass Point | Technique | On-the-spot Evidence | Mechanism Isolation-Verified? | Corresponding Hardening (cheatsheet) |
|---|---|---|---|---|
| | | | | |

## Pending Verification / Open Questions (theoretically feasible, not witnessed)

- 
