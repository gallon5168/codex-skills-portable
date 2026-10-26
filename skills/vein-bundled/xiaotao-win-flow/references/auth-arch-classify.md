# Authorization Architecture Classification (P1) -- classify before picking a technique, predict [Y]/[OK]

> **Purpose**: before choosing a bypass technique, classify the target's auth architecture. Category determines feasibility and [Y]/[OK] probability -- don't default to "it can be patched."
> **Origin**: real post-mortem. Skill's catalog used to lean client-side (patch decision point, fake server), but modern software commonly does "server-side verification + delivering data/tokens/flags" -- hard-patching the client often only reaches [Y] or crashes.

---

## I. Three categories (classify first)

| Category | Characteristics | Client-side patch outcome | Examples |
|---|---|---|---|
| **(1) Client-side boolean gate** | Client checks `if(licensed)` itself, or fetches one boolean and caches it | **[OK] genuinely unlockable** | Standalone software, offline serial verification |
| **(2) Server-side data gate** | Login response carries **server data actually consumed by business logic** (not just a boolean: token, config, feature data) | **[Y] or crashes** -- patching the internal decision point often triggers array-out-of-bounds/null-ref from a missing response field; usually fall back to patching the login gate | SaaS, auth delivering config/quota |
| **(3) Server-side feature gate** | Core functionality/compute is remote (each endpoint independently verifies a token, compute on remote node) | **No client-side solution** -- UI can be tricked open, feature itself unobtainable | Cloud rendering, remote inference, thin clients |

**Real confirmation ((2))**: an EPL target's `dword_960898` from the login response was read by 5+ functions. Patching the decision point (`0x402B56`) **crashed** the program -- missing field triggered an EPL array-out-of-bounds (`sub_586FDE __noreturn`); fell back to patching the login gate (`0x401BA3`) instead.

---

## II. Predict [Y]/[OK] from the classification (feeds Stage 2.5 route scoring)

- **(1) Boolean gate** -> single-point patch/hook scores high, predicted **[OK]**.
- **(2) Data gate** -> predicted mostly **[Y] or crash**; [OK] needs forging a **complete, legitimate response structure** (every consumed field, per Rule 19's field dictionary) -- high difficulty.
- **(3) Feature gate** -> client **cannot bypass at all**, at most [Y]; tell the user honestly the client is likely unbypassable, only the presentation layer is; deliver "server verifies each endpoint independently + remote compute = effective defense" as Stage 5 hardening evidence (Rule 6).

**[Y]/[OK] definitions** (adding [R], per Rule 19):
- [R] Statically suspicious -- looks right in code, unrun
- [Y] UI-surface unlock -- flow completes, server-dependent feature unverified
- [OK] Feature-level unlock -- user watches the core feature run and produce a result; only externally-reportable done state, only one that proceeds to Stage 5

---

## III. Map channels/trust boundaries first (no "single gate" mental model)

**Root cause**: software often separates auth/telemetry from the core feature, mixes cloud+local, or uses multiple backends. Real case: an app had **two independent channels** -- (1) its own server (EMSG login, global token) (2) Douyin (core feature uses the **user's own Douyin CK**, connecting directly to `live.douyin.com/webcast/luckybox`). Core feature was decoupled from the login token, nearly misjudged under a single-gate assumption.

**Before attempting a bypass, enumerate all trust boundaries/channels** (heavy route: read them off the Stage 0 trust-boundary diagram; **fast path**: no formal diagram exists yet -- enumerate the channels directly from the packet capture + `scan.ps1` import table instead, same result):
- List every outbound endpoint (domain/IP/port).
- For each, its protocol + credential source (own auth token, or user's third-party CK?).
- Determine which gate actually blocks the core feature -- hit that, not habitually the login gate.

---

## IV. Static <-> dynamic is a two-way switch, neither is only-a-fallback (Rules 26 & 14)

**Route by task nature first, not by habit** (Rule 26):

| Task nature | First choice |
|---|---|
| Find a precise constant / comparison value / branch condition / algorithm shape | **Static (IDA + xref)** |
| Observe runtime data / post-decryption plaintext / network content | Dynamic (hook/breakpoint) |
| Confirm a decision point actually executes | Dynamic (breakpoint hit, Rule 4) |
| Locate "which code produced this string / behavior" | **Static (xref that string/API)** |

**Static -> dynamic** (this section's original point): event-driven GUIs, message maps, vtables, COM, delegates/callbacks, jump tables, EPL variadic thunk dispatch -- pure static xrefs frequently dead-end (all data-type links). Real case: caller of login function `sub_40206B` was found only via dynamic step-out. Switch to dynamic when: xrefs to the target are all data-type (no code xrefs), or you hit a runtime dispatcher (variadic thunk/vtable/message loop). Run dynamic localization (breakpoints + call-stack trace + step-out) **alongside** static xrefs, not only after static fails. Nuitka's structural string-xref failure is an extreme case (`playbooks/nuitka.md Sec.2.2`, switch to nuitka-helper anchor).

**Dynamic -> static (the symmetric switch the skill used to lack -- Rule 26)**: live-debugging is *not* the default for native targets, and it has its own dead ends. Dump the decrypted module + go to IDA static+xref the moment any of these fire:
- Same goal sees **2 consecutive runtime-anchor attempts with zero progress** -- switch the method, don't place a 3rd breakpoint.
- **Junk code / linear-disassembly misalignment** (`EB 01` skip-bytes, overlapping/fake jumps, disassembly contradicting control flow) -- linear `disassembly_at` misreads it; IDA recursive-descent is the fix. High-priority trigger on its own.
- **Event storm** -- a UI-API breakpoint fires hundreds of times without user action (real case `hit_count=1094`, all noise), drowning the hit you want. Static is frequency-independent.
- **Decision/display decoupling** -- you keep catching the *error-display/consumer* side (stack bottom = message pump / `OnCmdMsg` / `WindowProc`) while the check that produced it is on a different stack (async `PostMessage`/custom message). **Chase the decision that produces the error, not the popup** -- static-xref the error string's producer.
- **No xref in x64dbg** (reflectively-loaded / unregistered module) -- dump->IDA is the only way to get "who references this".

**Memory-plaintext = static's best moment**: once a native module is confirmed plaintext in memory (shell self-decrypt / reflective load / manual dump), dump-to-file -> IDA is the default next step. Live breakpoints then serve only to *observe runtime data* (decrypted values, network content, confirm a hit -- Rule 4), never to hunt a static fact.

---

## V. Cheap anchor heuristics (short-circuit layer-by-layer step-out)

Anchor on observable side effects instead of chasing layer by layer down the transport stack:
- `MessageBoxW/A` -> login/auth-failure branch.
- `RegQueryValueEx` -> authorization flag.
- `CreateFile`/`ReadFile` -> license key/config/license.
- `socket send` -> protocol entry point.
- `GetSystemTime`/`GetLocalTime` -> trial-period/time verification.
Breakpoints on these APIs beat step-out-ing layer by layer from the entry point.

---

## Tie-in with the main process

| Main process | Role of this reference |
|---|---|
| Before Stage 2.5 route scoring | Sec.I classify, Sec.II predicts [Y]/[OK] into the scoring table |
| Stage 2.5 / before acting | Sec.III enumerate trust boundaries/channels, find the blocking gate |
| Stage 4, stuck (either direction) | Sec.IV two-way static<->dynamic switch (Rules 26/14): xrefs all data-type -> dynamic; live-debug stalls 2x / junk-code / event-storm / decision-display decoupling / plaintext-in-memory -> dump+IDA. Sec.V cheap anchors |
| Stage 5 delivery | (3) feature gate unbypassable = positive hardening evidence (Rule 6) |
