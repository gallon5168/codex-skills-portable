---
name: xiaotao-win-flow
description: Windows reverse-engineering pipeline. Identifies target type (native/Nuitka/Go/Rust/.NET/Python-bytecode/Java/Electron/Tauri-WebView/Delphi/AutoIt/e-language/packed), routes to matching tools, reverse-engineers auth/encryption bypasses into hardening advice. Use for: Windows RE, exe/dll analysis, packer detection/unpacking, installer extraction (Inno/NSIS/MSI), packet capture, IDA/x64dbg, PyInstaller/pyc/.NET/Go/Rust unpacking, license-check location, bypass-to-hardening.
compatibility: Windows only. GUI tools (IDA/x64dbg/Reqable/jadx-gui) and the target itself are ALWAYS opened by the user, never auto-started (Rules 8/9). Missing non-GUI tools are NOT auto-installed -- present the tool name + source and let the user install (Rule 5). Bundled: diec. Overseas GitHub lookups need a proxy (科学上网).
---

# xiaotao-win-flow -- Windows Reverse Engineering Pipeline

**Language: follow the user's language; default Chinese for replies/docs/logs.**

**Act on invocation**: no preamble, no plan announcement -- go straight to the **Fast path**. Drop into the heavy staged workflow only when the target is actually packed/protected/stalled.

**No target path yet? Ask, don't stall.** If the skill is invoked (bare, or alongside an unrelated message like a greeting) and the target's absolute path is NOT already in context, the only valid action is to ask the user directly which program/file to analyze -- one short question (e.g. "要分析哪个目标?给我 exe/dll 的绝对路径"), then stop and wait. Never silently attempt Fast path with no path to act on (produces no visible output = looks hung), and never guess/assume a target from the directory name. Once the path is given, proceed to FIRST ACTION below.

**FIRST ACTION (before anything else, unconditional): create the anchor `.claude/CLAUDE.md` in the target's directory.** The instant you have the target's absolute path, create `<target-dir>/.claude/CLAUDE.md` from `templates/target-claude-md-template.md` -- as a **skeleton** (fill in the skill's absolute path + the "re-activate skill" instruction + the core iron rules now; leave the shell-layer map / progress blank and populate them as you discover them). Do this **before** scan/analysis, not after a shell is detected -- so if you get disconnected/interrupted one turn in, the anchor already exists and auto-reloads next time (Rule 7). Then proceed to Fast path step 1.

## Two hard stops (these gate everything -- never work around them)

1. **GUI action = STOP and hand off to the user.** Every open/launch tool (IDA, x64dbg, Reqable, jadx-gui) and the target itself is opened by the **user**, given a verified absolute path; every real interaction with the target (clicking, typing, login flow) is done by the **user**. You never launch or drive them. Flow: stop -> give exact absolute path -> user opens/acts -> user says done -> confirm the matching `mcp__*` is live (Rule 1) -> continue (Rules 8/9).
2. **Missing tool = STOP and let the user install it.** Do NOT auto-install anything. When a needed tool is absent: name the **most suitable** tool for *this* target (per `tool-registry.md`, not just whatever's already local -- Rule 3), give its download source, and stop for the user to install (Rule 5). `bootstrap-tools.ps1` is a **health-check only** (prints what's missing + where to get it); it never installs.

## Routing contract (classify before you commit a route)

Run this read-only classification immediately, as the first action -- never "grind a tool, figure out the type later."

```text
1. Get target absolute path → create the anchor (FIRST ACTION, above).
2. Answer the control-ownership fork FIRST (Rule 28): "can I inject into this process?"
   -- prove it with a ~30s read-only attach, don't guess. This picks the axis (hook vs capture).
3. scan.ps1 → bitness + packer + classify via triage-router.md (MANDATORY, all 3 axes:
   target type + normalized user intent + toolchain). Read the [P] per-module map.
4. Packed? Engage the shell at the auth boundary -- web-search the exact shell+version FIRST
   (Rule 3), then unpack, then RE-TRIAGE the clean output. Don't dodge the shell.
5. Route by TYPE to the matching playbook; pick WHICH module (often an auth DLL/pyd, not the exe, Rule 13).
6. Route not matched → gather one more evidence round, then propose a table row or fall back to
   black-box boundary -- never force-fit (triage-router.md Sec.5).
7. Only after routing: open the target/tool (user does it, Rules 8/9) and ACT.
```

Read order: `SKILL.md (this) → triage-router.md (User-Intent Axis + type table) → PRIMARY playbook → tool-registry / rules.md on demand`.

## Layout (progressive load: thin skeleton, details on demand)

Detail lives in `references/`, loaded only when read. Confirm a path exists before using it (Rule 1).

```
xiaotao-win-flow/
|- SKILL.md / EVAL.md
|- scripts/  scan.ps1 (Stage1) | netcheck.ps1 | bootstrap-tools.ps1 (health-check) | fetch-tool.ps1 (probe)
|- templates/  target-claude-md-template.md (Stage0 anchor) | attempts-log-template.md | mitm-observer.js | electron-node-harness.js
|- tools/die/  (diec.exe portable, no MCP needed)
`- references/
   rules.md (full rule write-up) | heavy-route-workflow.md (Stage 0-5, heavy targets only)
   triage-router.md | env-recon.md | auth-arch-classify.md
   known-pitfalls.md | case-studies.md | auth-bypass-cheatsheet.md | tool-registry.md
   hard-target-playbook.md | deobfuscation-playbook.md | playbooks/nuitka.md | playbooks/tauri-webview.md
   ida-re/ (static) | frida-win/ (dynamic) | x64dbg/ (unpack + dynamic)
```

## Scope

Authorized RE only: own software, authorized targets, CTF, security research -- to reconstruct the bypass and harden it. If the real goal is cracking someone else's software, refuse and explain.

## Core goal -- bypass first, harden second

The deliverable is a **real bypass the user personally witnessed running (`[OK]`)**, not a document. Order is non-negotiable: (1) land the bypass -- locate the auth gate, defeat it, user watches the real feature produce a result; (2) then, per `[OK]` point, cross-reference `auth-bypass-cheatsheet.md` and deliver `{bypass -> location -> hardening}`. No `[OK]` = no hardening doc; "bypass could not be reproduced, defense held" is a valid positive result (Rule 6). Never harden off a `[Y]` UI-trick or a `[static inference only]` guess.

## Posture -- own software, direct but not reckless

- **Never dodge the shell.** Locate the license/auth boundary first (which module, which check), then unpack or hook *at that boundary* -- never fake-server/passive-capture/patch-outside-the-shell as a "cheaper" substitute (Rules 16/27).
- **Proxy capture needs active setup, not a passive system-proxy toggle.** Force traffic into the proxy (Proxifier/TUN, `tool-registry.md Sec.4.5`) and install+trust the interceptor's CA (defeat pinning first, `env-recon.md`). For a local injectable target, skip capture entirely and hook pre-encryption plaintext (Rule 28).
- **Batch all read-only probes in parallel without asking** (CDP reads, memory scans, disasm, `scan.ps1`, module dumps -- Rule 25); confirm only the irreversible (byte-patching, editing local auth state -- Rule 5).
- **Batch every observation into ONE injection / one user action** -- install all hooks at once, harvest in one walk, never make the user re-login per probe.
- **Kill dead ends on paper before spending a round**: ask "can this even work?"; a `[static inference only]` guess is not a bypass.
- **Commit to the top-scored route (Stage 2.5)**; switch only on a real 2x-zero-evidence stall, not first friction.
- **Never**: fake a result, skip evidence tags, patch without consent, or drive the target yourself.

## Fast path (default -- ~80% of targets; action-first)

1. **Get the target's absolute path, then answer the control-ownership fork FIRST (Rule 28): "can I inject into this process?"** -- this shapes step 1; don't reflexively open a proxy.
   - **Local rich client we own + Frida/x64dbg injects (common case)** -> **in-process Hook is the primary first move**; capture is parallel secondary. Run `scripts/scan.ps1 -Target <path>`; its **step [4] network-DLL pre-judgment** tells you in ~30s if a self-contained stack (Cronet/BoringSSL/Go `net`/Qt Network) makes proxy-capture already dead -- if so, hook the target's own SSL/network/decision fns for pre-encryption plaintext (recipes §4.9), don't waste a login round on capture.
   - **Process out of reach** (mobile/remote/PPL/injection-refused/black-box HTTP) -> capture is first, and it is a **hard STOP + handoff, never done on assumption (Rules 8/9)**:
     - **STOP the session and hand capture to the user.** Tell them plainly: start the interceptor + proxy *before* opening the target, then walk one full auth flow, and **report back whether records appeared or not**. Then **wait** -- do not proceed to step 4, do not assume records exist. Never capture on their behalf.
     - **If they report they CAN'T capture (empty/nothing) -> that's my cue to handle it, not to give up.** Now I work out *why* and drive the fix for the user to execute: force the traffic into the interceptor (**Proxifier / TUN**, `tool-registry.md Sec.4.5`) + install & trust the **CA cert** for HTTPS MITM + **defeat pinning first** if present (`env-recon.md`); verify with `openssl s_client -proxy` that it's really decrypted. Empty capture = a setup gap I resolve, not proof there's no traffic.
     - **If it's actually a local injectable target, an empty capture means I was on the wrong branch** -- go back to the fork and hook the pre-encryption plaintext instead (Rule 28), don't keep fighting the proxy.
   - Either way, `scan.ps1` gives bitness + packer + classify (`triage-router.md`, mandatory) + the step [4] pre-judgment. It checks the exe AND every same-dir dll/pyd for a named shell in one pass (`case-studies.md` #3) -- read its `[P]` module-by-module map; don't re-scan modules one at a time.
2. **Packed? Engage the shell -- don't dodge it (Posture).** Order, no deviation:
   - **[DETECT RIGHT FIRST] DIE reporting only `(Heur)Generic/Protection` is NOT "no shell".** Commercial shells (Safengine/SProtect/VMProtect/Themida) routinely evade DIE's namer. If DIE can't name it but you see random section names (`.sp0/.5w44`) / high entropy / anti-debug -> have the user run **Exeinfo PE** (`tool-registry.md Sec.0.9`) on that module. Still unnamed -> search the **hard features** (section names, signature strings `SPBegin/SPEnd`, exports, sibling driver) *verbatim* via ddgs. **NEVER pin shell identity on one clue** (real miss: `sprotect.sys` name -> wrongly guessed 深盾Virbox; it was Safengine/SProtect -- cross-confirm from >=2 features/sources).
   - **★★ [STRONG TECHNIQUE -- reach for this reflexively] Protected auth/license SDK DLL -> UNPACK IT: dump the plaintext, don't fight it from outside.** This is the single most powerful move on a cloud-verify/license SDK DLL (e.g. `SPCloud64_Py.dll` = Safengine + NetLicensor). Proven path: tiny `loader.exe` `LoadLibrary`s the DLL -> **x64dbg + ScyllaHide** (exact config: `hard-target-playbook.md` Sec.2.1 SE block) suppresses anti-debug so it survives -> DLL self-decrypts in memory (4.7MB->9.7MB) -> break `kernel32.Sleep` -> `dump_module` (rebuild PE + fix IAT) -> now IDA the DUMP (Rule 30 allows IDA only on plaintext). Beats grinding IDA on packed bytes (Rule 30 forbids) / fighting anti-debug forever / reverse-guessing server data. **Do NOT default to Intel Pin/UnSafengine64** -- version代差 crashes it (Pin 3.31 vs tool's 3.18); ScyllaHide+x64dbg dump is the reliable route.
   - **★ Auth localized to a module => unpacking it IS the route; guessing its I/O from outside is the detour.** If you're iterating return-value/response guesses more than once, STOP and unpack (case: burned ~9 rounds forging a packed SDK's return before unpacking -- `case-studies.md`).
   - Locate the license/auth verdict (which module, which check) first, then unpack *that* layer/module -- often an SDK/auth DLL, not the main exe (`scan.ps1 [P]` maps every packed module). Re-triage the clean output.
   - **(a) SEARCH FIRST (Rule 3, mandatory; search only via ddgs -- Rule 29):** take the exact packer + version from `scan.ps1`/Exeinfo PE and look it up online (看雪/吾爱/GitHub/issues) before touching the binary. Grab the dedicated tool (`tool-registry.md Sec.1` / `hard-target-playbook.md` tiers), unpack, verify (Rule 21), re-triage, continue.
   - **(b)** No public technique/tool -> fall back to your own RE: dynamic OEP-dump (`x64dbg/find-oep/`) -> dump -> IAT repair (Scylla/pe-sieve); for a virtualized core, hook the function boundary and observe I/O black-box (`hard-target-playbook.md` Sec.1 L3).
   - Only a **compression-only packer** (UPX/ASPack) that `upx -d`/find-oep fully restores lets you proceed as unpacked. VM protectors / strong encryption stay on the heavy route.
   - On a hard shell (ASProtect/VMP/Themida), say once that it's slow/fiddly but normal -- not every step.
3. **Go straight to the auth logic by type** -- but **first pick WHICH module to attack; don't default to the exe (Rule 13)**. The exe is often just a launcher/GUI shell -- the real auth/crypto/license logic lives in an SDK/core DLL or `.pyd`, and attacking that module is usually *easier* (smaller, **named exports** hand you the entry point, sometimes weaker anti-debug). Pick by evidence (Rule 12): which module carries the auth **exports**, which the exe **imports its check from**, which **references the auth strings/APIs**, or the **packed module from `scan.ps1 [P]`**.
   - **ORDER: web-search technique FIRST -- for the HOOK/inject route too, not only "which module to open" (Rule 3 + Rule 13).** Before committing to *any* approach -- static (which module to open) OR **dynamic (how to hook/monkeypatch/inject)** -- search how others do it for **whatever runtime/framework/toolkit this target uses** (any stack: .NET/CLR, Electron/JS, JVM, Qt, WinForms/WPF, Delphi, Go, native C++...). Query template = `<runtime-or-framework> <symptom-or-API> hook/patch` (e.g. `<GUI toolkit> splash won't dismiss`, `<runtime> block <exit-API>`, `<instrumentation tool> <framework> hook`). Guessing hook points / attribute names / completion logic from scratch is the banned move -- search framework+symptom first, then hook. (Applies equally when a hook STALLS: don't re-guess, search how this class is hooked -- Rule 14/23 stop-loss.)
   - Point IDA at the chosen DLL itself / attach x64dbg and `bp` its export -- not reflexively the exe.
   - Managed/interpreted (.NET-IL/Java/Python-bytecode/Electron-asar) -> decompile, **read source**, enumerate *every* gate (Rule 15).
   - **WebView/CEF hybrid FIRST** (Tauri/Wails/Electron/CEF/WebView2 -- same-dir `WebView2Loader.dll`/`libcef.dll`, flagged by `scan.ps1` step [5]) -> UI + most auth logic are **JS in an embedded browser** -> `playbooks/tauri-webview.md` (CDP remote-debug -> one document-start injection hooking fetch+IPC+store -> flip the gate live). **Do NOT route a Rust/Go GUI to IDA on sight.**
   - Native (C/C++/Go/Rust/Nuitka/e-lang) -> **route by task nature (Rule 26)**: hunting a *static fact* (constant/branch/algorithm shape/who-references-a-string) + plaintext in memory -> **IDA static+xref first** (dump the module if reflectively-loaded); *observing runtime data* -> hook/x64dbg. Static and dynamic run **alongside** each other. Don't grind linear MCP disassembly on an obfuscated body.
4. **After the user confirms capture done -> route splits** (wait for their word): records exist = online (forge/replay/fake-server, but first classify the arch -- a server *feature* gate can't be client-bypassed, `auth-arch-classify.md`); no records = local/offline (patch/hook/local-file per cheatsheet 1/2/5); loopback/raw-socket = local hook, not proxy.
5. **Bypass the gate -> user watches the real feature run = `[OK]`.** Only now write hardening.
   - **Enumerate ALL auth gates, not just the first** (defense-in-depth is the norm, `case-studies.md` #4): list every check function/exit branch/state file/second verification (heartbeat, machine-code, integrity self-check); after each bypass, trace with faulthandler/monkeypatch/signals/log-proxy for the *next* termination point until the real feature runs. `[gate]` flipped < `[alive]` survives < `[OK]` usable -- only `[OK]` counts (Rule 6/15).
   - **★ Process alive but window blank/stuck = a mount/exit-gate problem to HOOK, not data to forge.** When a gate makes init self-terminate (`exit`/`abort`) before the UI mounts: intercept the exit call (runtime hook, detach-persistent), then finish the mount from the runtime -- **GUI toolkits require this on the UI/main thread** (else callbacks never fire). Introspect the live window for the REAL attribute/method names before writing the completion; don't guess or forge the gated data. **On any self-exit / crash / stuck-window symptom, read `references/crash-exit-handling.md` FIRST** (step 0 = read the target's OWN log; exit-interception order; exit-gate != mount-gate; never freeze the main thread). **For embedded-interpreter / frozen / Nuitka-compiled targets that are live and injectable, read `references/runtime-injection-hooking.md`** (in-process `PyRun_SimpleString`+GIL, replace compiled functions wholesale, excepthook/settrace observe, cross-thread GUI mount).

**Escalate to the heavy route when**: VM-protected/strong-encryption core, obfuscated, anti-debug fires, junk-code/fake-stack (Rule 14), a route stalls 2x with zero evidence (Rules 14/23/26), a dynamic->static stop-loss trigger fires (Rule 26), or a multi-session hard target needs the full memory log. **An ordinary packer is NOT an escalation trigger** -- unpack it inline per step 2 and stay fast.

**Logging on the fast path**: lightweight inline log (target path/type, gate location, each attempt + status tag, a patch-ledger line only if you edit bytes). Copy the full `templates/attempts-log-template.md` only when escalated or multi-session.
**★ Mechanical write-back triggers (Rule 7 -- "log when I remember" silently desyncs; make it event-driven).** Any ONE of these events = update attempts.md + the `.claude/CLAUDE.md` anchor's matching section **in the SAME turn**, before replying: (a) got an `[OK]`/`[X]` (verified/disproven); (b) switched method layer (static<->dynamic, unpack->hook, DLL->bytecode); (c) confirmed/corrected shell name·version·packaging·protection; (d) found a new gate/check/exit-point; (e) deployed/patched/replaced an artifact; (f) recovered from context compaction (read anchor+attempts FIRST). Self-check before every user-facing reply: "did any trigger fire this turn? fired-but-not-logged -> log now." The anchor template ships this as a table at its top.

## Iron rules (grouped one-liners; full rationale + coverage calibration in `references/rules.md` -- that file wins on conflict)

**Always-on core (both paths)**: **1** confirm MCP exists before use; **2** web lookups via `netcheck.ps1` -- overseas proxy-first, domestic CN forums direct; **search specific (exact shell+version/verbatim error), not generic; a page blocked by anti-scraping = STOP after one try, hand the user the URL to open/download (tool-registry 0.95)**; **3** pick the *best* tool per target (`tool-registry.md`), never settle for local -- and for packed/protected targets, **search online for the specific shell+version first** before acting; **4** code-exists != running (tag `[static inference only]`); **5** consent before any change/download/install; **6** no hardening without a witnessed bypass; **7** log every step immediately, never delete a disproven entry, reconcile after compaction; **8** user opens all GUI/launch tools; **9** user drives the target; **10** single-line output; **11** red-team zero-credentials.

**★ IRON tooling rules (absolute, no exceptions -- full text in `rules.md`)**:
- **29 No `ddgs` = NO search**: every web lookup goes through the `ddgs` lib (`pip install ddgs`); not installed -> STOP + tell user to install, WAIT. Banned: built-in `web_search`, curl/PS scraping search engines. (Still route by destination per Rule 2.)
- **30 Packed = IDA FORBIDDEN until unpacked**: target/module confirmed packed (Safengine/SProtect/VMProtect/Themida/any commercial shell) -> NEVER open in IDA / call `mcp__ida__*` (packed bytes are stubs/zero/VM -- proven dead end). IDA only on a **plaintext dump** (unpack first per Rule 3). Before unpack, inspect via memory-dump+capstone / proxy-DLL logging / Frida read-only.

**Heavy-route rules (kick in as their situation arises; one-line pointer only -- full write-up + rationale is in `rules.md`, that file wins on conflict)**:
- **Stop-loss family (14 / 23 / 26)**: 2 zero-evidence attempts on a strategy = structurally dead -> switch the method layer, never place a 3rd breakpoint / retry a 3rd channel.
- **VM-core family (16 / 27)**: score routes before acting; a VM protector on the core vetoes "fake the server"; attack a confirmed VM'd verdict at its boundary, never flee to fake-server/registry-diff/network-capture.
- **Others**: 12 attribution needs hard evidence; 13 pick WHICH module to open, not reflexively the exe; 15 interpreted->unpack->de-bytecode->read source (Go/Rust/Nuitka/.NET-AOT are native RE, not this); 17 no modal dialog open before injection; 18 grade an unknown fn by name prefix before blind-calling; 19 build a real-response field dictionary before forging; 20 hook every candidate crypto lib at once; 21 edit->repack->restart, one layer per round; 22 DLL hijacking is an independent route; 24 runtime path args pure ASCII; 25 batch independent read-only sub-hypotheses in parallel; 28 control-ownership fork decides Hook-vs-capture before any default action, prove with a ~30s read-only attach.
- **Generic gotchas (this class of target -- full text `known-pitfalls.md`)**: **read the target's OWN log first** on any crash/exit (`crash-exit-handling.md` step 0); **exit-interception order = runtime-layer no-op before native `ExitProcess`; never sleep/loop on the main thread** (freezes UI -> "Not Responding"); **blocking exit != entering UI** (mount is positively gated -> call the mount fn from runtime); **a fake/proxy SDK DLL must fill the caller's output buffer in the exact parsed shape, not just return a code** -- proxy-forward to the REAL DLL + log its buffer to learn the shape; **non-ASCII paths are a toolchain-wide minefield** -> keep all scripts/logs/injected-source/build-output in an ASCII-only scratch dir, `\uXXXX`-escape CJK, copy back; **kill the target's whole process tree (elevating if a requireAdministrator manifest denies it) before replacing any loaded DLL/file** -- fixed pre-deploy step; **`QTimer.singleShot` on an injected thread never fires** -> Signal+`moveToThread(main)`+QueuedConnection (or the framework's post-to-UI-thread call).

## Workflow (heavy route -- packed/protected/stalled targets only)

The fast path *is* a compressed pass through these stages (Stage 0 Kickoff/anchor -> Stage 1 Triage -> Stage 2 User captures -> Stage 2.5 Route planning -> Stage 3 Fake-the-server -> Stage 4 Deep analysis -> Stage 5 Hardening). **Only read the full stage-by-stage write-up in `references/heavy-route-workflow.md` once a target actually escalates** (per the escalation triggers above) -- don't load it for an ordinary Fast-path target.

## Dependencies (user installs these -- you never auto-install; Rule 5 + hard stop 2)

| Stage | Tool | MCP/CLI | If missing |
|---|---|---|---|
| 0 | uv/7z/upx/capa/angr/frida | none | `bootstrap-tools.ps1` health-check -> present tool+source -> user installs |
| 1 | diec | none (bundled) | -- |
| 1 unpack | x64dbg + unpacker | x64dbg MCP | present + ask user to install |
| 2/3 | x32/x64dbg + Reqable | x64dbg / Reqable MCP | present + ask user to install |
| 4 static | IDA Pro | IDA MCP | present + ask user to install |
| 4 dynamic | x32/x64dbg / Frida | x64dbg MCP / Frida CLI | present + ask user to install |
| 0.5 installer | innoextract/7-Zip/msiexec | -- | `fetch-tool.ps1 -Probe` -> present + user installs |
| 4 other (unpack/.NET/Nuitka/Delphi/AutoIt/VB6/Nim) | see `tool-registry.md` | -- | present the matching tool + source -> user installs |

Check the session tool list for `mcp__reqable__*`/`mcp__ida__*`/`mcp__x64dbg__*` -- absent = not installed (Rule 1). All GUI tools opened by the user (Rule 8).

## Pointer index (loaded only when read)

- Full iron-rule write-up -> `references/rules.md`
- Heavy-route Stage 0-5 workflow -> `references/heavy-route-workflow.md` (read only once escalated)
- Program-type triage -> `references/triage-router.md`
- Env recon / auth-arch -> `references/env-recon.md` / `references/auth-arch-classify.md`
- Bypass x hardening -> `references/auth-bypass-cheatsheet.md` | Tool registry -> `references/tool-registry.md`
- Hard targets / de-obfuscation -> `references/hard-target-playbook.md` / `references/deobfuscation-playbook.md`
- Nuitka -> `references/playbooks/nuitka.md` | **Tauri/WebView2/CEF hybrid -> `references/playbooks/tauri-webview.md` (CDP front-end, not IDA)**
- **Crash / self-exit / stuck-window -> `references/crash-exit-handling.md`** (read on any exit/abort/闪退/未响应 symptom; step 0 = target's own log)
- **Runtime injection & hook (embedded interpreter / frozen / compiled, live process) -> `references/runtime-injection-hooking.md`** (GIL+PyRun in-process, replace compiled_function, cross-thread GUI mount)
- Sub-skills -> `references/ida-re/`, `references/frida-win/`, `references/x64dbg/`
- Known pitfalls / case studies -> `references/known-pitfalls.md` / `references/case-studies.md`
- **Target anchor (Stage0, compaction-surviving) -> `templates/target-claude-md-template.md`** (copy to `<target-dir>/.claude/CLAUDE.md`)
- Memory-log template / observer / harness -> `templates/attempts-log-template.md` / `templates/mitm-observer.js` / `templates/electron-node-harness.js`

Each sub-skill has its own MCP/CLI dependency -- confirm before use (Rule 1).
