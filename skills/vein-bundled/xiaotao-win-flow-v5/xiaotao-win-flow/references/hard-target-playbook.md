# Hard-Target Playbook (Packers / Anti-Detection / Network Verification)

> **Purpose**: for a strong packer, strong anti-detection, or complex network verification, freely choose a technique based on analysis, paired with the memory log (Rule 7) to decide when to escalate/switch/stop.
> **Defensive stance**: reconstruct red-team techniques -> harden your own (or licensed) software. Per Rule 3, search "how to unpack this specific packer / third-party library for this algorithm," never "how to crack this software."
> **Sources**: al-khaser, CheckPointSW (showstopper/Evasions), guidedhacking GH_AntiDebug_Bypass, ergrelet/unlicense, Magicmida, VMPStatic/birosca, PELock SDK, GuardingPearSoftware, Securitum.

---

## 0. General Unpacking SOP (packer-agnostic -- follow in order, every packed target)

> The step sequence for ANY packed target. Tier-specific tactics are Sec.1; this is the spine that ties detect→search→unpack→verify together. Never skip a step forward.

1. **DETECT the shell precisely (don't trust one tool).**
   - `scan.ps1` (DIE) auto first-pass. **DIE reporting only `(Heur)Generic/Protection` is NOT "no shell"** -- commercial shells routinely evade its namer.
   - Suspect a shell (random section names `.sp0/.5w44` / entropy ~7.8+ / anti-debug behavior) but DIE can't name it → have the user run **Exeinfo PE** (tool-registry Sec.0.9) on that module.
   - **Scan the exe AND every same-dir dll/pyd** -- the shell is often on an SDK DLL, not the main exe (Rule 3 [SCAN ALL MODULES]). The main exe's high entropy may just be a Nuitka/packer *payload*, not a crypto shell.
   - **Confirm shell IDENTITY by ≥2 crossed features** -- section names + signature strings (`SPBegin/SPEnd/SProtectSDK`, `vmp0`, `.themida`, `.enigma`) + exports + sibling driver files. **NEVER pin identity on one clue** (real miss: `sprotect.sys` name alone → wrongly "深盾Virbox"; it was Safengine/SProtect).

2. **SEARCH the exact shell+version FIRST (Rule 3, mandatory; via ddgs only -- Rule 29).** Before touching the binary: 看雪/52pojie (direct curl) + GitHub/issues (proxy) for that shell+version's documented unpack/devirt/anti-debug-config. Keyword templates: `<shell> <ver> 脱壳/反调试/绕过`, `<shell> ScyllaHide 配置`, `<shell> unpack dump OEP`. Un-searched grinding trips CRC/anti-debug and burns rounds.

3. **PICK the route by tier (Sec.1), don't force one tool.**
   - **L1 compression** (UPX/ASPack/PECompact/MPRESS): `upx -d`, or find-oep → dump. Trivial, proceed as unpacked after.
   - **L1.5 container** (Enigma VBox): `evbunpack` extracts embedded files, then re-triage the payload.
   - **L2 encryption/anti-debug** (Themida/Enigma/ASProtect/**Safengine/SProtect**/Steam DRM): dedicated unpacker if version matches (verify first, Rule 3!), else **ScyllaHide-suppress-anti-debug + run-to-self-decrypt + dump** (the reliable general route for SE/SProtect -- Sec.2.1 config + tool-registry Sec.0.9).
   - **L3 virtualization** (VMProtect-VM/Themida-VM/Code Virtualizer/Safengine): generic unpack fails on the VM'd functions -- either a dedicated devirtualizer (NoVmp/Triton-VMP, version-picky), or **don't unpack the VM at all -- black-box hook the virtualized function's input/output at its boundary** (Rule 27, Stage 4B). Key code stays bytecode; you observe/force I/O, not read x86.

4. **VERIFY tool version compatibility with a 5-min smoke test BEFORE heavy integration** (Rule 3): a dedicated unpacker validated on packer vX often crashes on vY (real: UnSafengine64 works on Pin 3.18, crashes on the only-available Pin 3.31). Confirm "does it even run here" before compiling/adapting/wiring it.

5. **UNPACK the packed layer, not reflexively the exe.** The auth/license verdict usually sits in an SDK DLL (named exports hand you the entry point). Unpack THAT module.

6. **DUMP + FIX after decryption.** Once decrypted-in-memory (self-decrypt / reflective / manual): break on an outside API (`kernel32.Sleep` in a loader loop always hits), `dump_module` (rebuild PE) → **Scylla/pe-sieve fix IAT** → **DLL targets also need reloc-table rebuild**. Disk-size→memory-size growth (e.g. 4.7MB→9.7MB) confirms decryption happened.

7. **RE-TRIAGE the clean output + VERIFY** (Rule 21): the unpacked module is a new target -- re-run classification on it. IDA is now allowed (Rule 30: only on the plaintext dump). Confirm the unpack is valid (imports resolve / runs / expected strings present), don't trust "it dumped."

**Anti-debug is the gate for steps 3/6** (see Sec.2.1, esp. the SE/SProtect reproducible block): on shells with memory-CRC (Safengine/SProtect), **never change the shell's bytes** (software bp / inline hook = killed) -- use hardware bp + ScyllaHide, or dump-then-static.

---

## 1. Packer Strength Tiers and Countermeasures (Stage 2)

Identify the packer with `scripts/scan.ps1` (diec) + `references/x64dbg/yara-sigs/`, then pick by tier:

| Tier | Typical Packers | Characteristics | Strategy |
|---|---|---|---|
| **L1 Compression** | UPX, ASPack, PECompact, MPRESS | Pure compression, one decompression pass, jumps to OEP | `references/x64dbg/find-oep/` traces to OEP -> dump; UPX direct via `upx -d` |
| **L1.5 Packaging Container** | **Enigma Virtual Box** (virtual FS bundling deps into one exe) | Not encryption -- a virtual FS container | **`evbunpack` (tool-registry Sec.1) extracts embedded files directly**, then triage the extracted payload's packer |
| **L2 Encryption/Protection** | Themida/WinLicense, Enigma (Protector), VMProtect (packing mode), Obsidium, **ASProtect**, PELock, **Steam DRM (SteamStub)** | Anti-debug + IAT obfuscation + multi-stage decryption | **Prefer a dedicated unpacker** (below), supplement with find-oep to reach OEP dynamically |
| **L3 Virtualization** | VMProtect (virtualization), Themida (VM), Code Virtualizer, **Safengine Shielden** (domestic Chinese) | Key code becomes bytecode, no real x86 OEP | Generic unpacking fails -- use a **dedicated devirtualization tool**, or **only dynamically observe the virtualized key functions** (Stage 4 hook input/output, don't unpack the whole packer) |

**Dedicated unpacking tools** (fetch from web per Rule 3 -- skill doesn't bundle binaries):
- Themida/WinLicense 2.x-3.x -> **ergrelet/unlicense** (dynamic unpacking + IAT repair, auto-recovers OEP; 32-bit target needs 32-bit Python; WinLicense needs a valid license file), **Hendi48/Magicmida**.
- VMProtect -> **VMPStatic / YuroGod-VMPStaticUnpacker** (static, 1.x-3.9.5), **keowu/birosca** (dynamic, 1.x, recovers OEP/fixes PE/IAT/bypasses protection).
- **Enigma Virtual Box -> evbunpack** (`mos9527/evbunpack`, `pip install evbunpack`; [WARN] repo archived but usable).
- **ASProtect -> ASpirin** (`Hendi48/ASpirin`; README says it targets "a very specific target" -- if version mismatches, stop per Sec.4 rather than force it).
- **Safengine Shielden -> UnSafengine64** (`holycall/UnSafengine64` upstream / `sctnightcore/UnSafengine64` fork; Intel Pin-based dynamic unpacking).
- **Steam DRM (SteamStub) -> Steamless** (`atom0s/Steamless`, GUI, `-Release atom0s/Steamless -Asset zip`).
- **[WARN] No FOSS dedicated tool exists**: Obsidium, Enigma Protector (!= Virtual Box), PELock, ACProtect, Armadillo, ExeCryptor -- use generic dynamic unpacking (find-oep -> dump -> Scylla for IAT, or mal_unpack/pe-sieve), hook the boundary for virtualized portions. Don't hunt for a tool name that doesn't exist.
- **Nuitka + Themida/VMP combo -> nuitka-themida-unpacker / DeNuitkanizator** (`references/playbooks/nuitka.md Sec.3.4`) -- unpack outer layer first, then the Nuitka chain.
- Generic workflow: **anpa1200/Unpacker** (UPX/ASPack/Themida/VMProtect detection + unpacking).

### Search prompts for unpacking (Rule 3 -- search the packer, never "crack the software")

When a packer isn't in the table above, or a new/unknown one shows up, search for the technique yourself. **Route by destination per Rule 2 / `netcheck.ps1`** -- overseas via proxy, domestic RE forums direct.

**Overseas (via system proxy)** -- GitHub is the primary source:
- Repo search queries: `<packer> unpacker` / `<packer> devirtualize` / `<packer> dump OEP` / `<packer> static unpack` / `<packer> IAT rebuild`.
- **Always include the version** -- unpackers are version-locked (VMPStatic ≤3.x, birosca 1.x only). Pin it from diec first: `<packer> <version> unpack`.
- GitHub `/search` on a shared proxy IP often 429s -- when it does, open `github.com/<owner>/<repo>` directly (repo pages aren't rate-limited the same way).
- For an *algorithm* (RSA/AES/custom crypto), search a third-party library that implements it, never a "crack".

**Domestic CN forums (direct, NOT via proxy -- prefer `curl.exe`; overseas proxy IPs get TLS-refused, and PowerShell's .NET TLS stack fails their handshake)**:
- 看雪 `bbs.kanxue.com` -- RE technique / 脱壳机 discussion, VMP/Themida/ASProtect writeups.
- 吾爱破解 `52pojie.cn` -- PE 脱壳 tools + step-by-step tutorials, the main CN board for this.
- Scope: **EXE/PE only** -- these two are the PE-unpacking boards; APK/Android forums are out of scope.

**Verified tool anchors** (checked alive via proxy against GitHub repo pages):

**Mainstream -- these two are what you actually hit most; try them first:**

| Packer | Tool (owner/repo) | Field note |
|---|---|---|
| **VMProtect** | `notsnakesilent/VMPStatic` (static 1.x–3.x) · `keowu/birosca` (dynamic 1.x) | Split first: **packing mode** (L2, has real OEP -> unpack) vs **virtualization mode** (L3, no x86 OEP -> don't unpack, hook the VM boundary). diec + Rule 16 veto "fake the server". |
| **ASProtect** | `Hendi48/ASpirin` (specific targets only) | ASpirin is version-picky -- if the version doesn't match, don't force it: fall back to find-oep dump -> Scylla/pe-sieve IAT repair. (This is ASProtect the L2 protector, **not** ASPack the L1 compressor -- ASPack just `find-oep`/dumps trivially.) |

**Less common (still covered):**

| Packer | Tool (owner/repo) |
|---|---|
| Themida/WinLicense | `ergrelet/unlicense` · `Hendi48/Magicmida` |
| Enigma Virtual Box | `mos9527/evbunpack` |
| Steam DRM (SteamStub) | `atom0s/Steamless` |
| Safengine Shielden | `holycall/UnSafengine64` |
| .NET (obfuscator/packer) | `de4dot/de4dot` · `dnSpyEx/dnSpy` |

**No public tool for this packer/version -> fall back to your own RE** (Fast path 2b): find-oep dump -> Scylla/pe-sieve IAT repair; virtualized core -> hook the VM function boundary (key insight below), don't unpack the whole thing.

#### ASProtect unpacking specifics (mainstream -- verified from 52pojie field write-ups)

ASProtect is an OllyDbg-era exception-driven protector. Unpacking is OD + PEiD + OllyScript and is **slow and fiddly by nature** -- tell the user up front it's slow and to be patient (see the reassurance rule in SKILL Fast path step 2). A plain "find OEP + rebuild IAT" is NOT enough here -- these four steps are what actually work:

1. **Reach OEP by exception-counting (not the ESP trick):** OD load, ignore every exception *except* "access violation", press SHIFT+F9 ~20-21 times; after ~20 set a **memory-access breakpoint on the code section**, and the next SHIFT+F9 lands on the real OEP.
2. **The IAT is relocated into the packer's own section (the real work):** ignore all exceptions, set a **memory-write breakpoint on an IAT slot**; when it breaks, `EDX` = the IAT slot being processed, `EAX` = its (processed) value, `ESI` = the API name; follow the CALL to recover the real API address. It's a **loop over every import** -- automate with an OllyScript that anchors on `GetSystemTime` (the packer calls it) to locate the packer section, then binary-searches the processing CALL and batch-restores the IAT. Manual one-by-one repair works too but is brutally slow.
3. **Recover stolen OEP bytes:** ASProtect steals/emulates the first instructions at OEP, so a plain dump lands on incomplete code and crashes -- recover the stolen bytes before finalizing. (Shared with the ACProtect family.)
4. **Version split decides everything:** 1.2x / 1.23 = simple, an OllyScript basically 通杀; **2.1x SKE** (Software Key Encryption, ties in a hardware/machine key) is a harder tier a 1.2 script won't touch. Pin the exact version from diec first -- `Hendi48/ASpirin` is version-picky for the same reason.

**Source (domestic, direct -- Rule 2, NOT via proxy):** `52pojie.cn` has a full ASProtect series (1.2 simple+script, v1.23, 2.1x SKE analysis). Reach it via Baidu (domestic search works via `curl.exe` direct; Bing/DuckDuckGo are blocked/JS-walled in this environment).

**Key insight for L3**: virtualized code often needs no unpacking. When the auth decision is virtualized, Stage 4 hooking the virtualized function's boundary (args/return/memory read-write) to observe authorization black-box is faster than reconstructing bytecode, and gets straight to the bypass point.

---

## 2. Anti-Detection Layered Checklist and Bypasses (Stage 4)

Targets often "detect debugger/VM/dump, then exit or change behavior." Identify by category, then bypass. Verify against practice tools: guidedhacking/GH_AntiDebug_Bypass_Practice_Tool, CheckPointSW/showstopper, meowdiocre/AntiAntiDebuggerExpert (x64dbg + Unicorn emulation bypass).

### 1. Anti-Debug (al-khaser / CheckPoint anti-debug-db checklist)
- **Flag-based**: IsDebuggerPresent, CheckRemoteDebuggerPresent, PEB.BeingDebugged, PEB.NtGlobalFlag, ProcessHeap.Flags/ForceFlags.
- **NtQueryInformationProcess-based**: ProcessDebugPort / ProcessDebugFlags / ProcessDebugObject.
- **Bypass**: in x64dbg, flip the return value after the detection call to "no debugger" (`references/x64dbg/find-oep/` sec 5); or Frida-hook these APIs to always return no-debugger (`references/frida-win/references/anti-debug-bypass.md` + `anti-debug-db/`). ScyllaHide / TitanHide hide most in one shot.

#### ★ Safengine / SProtect (SE) anti-debug -- the reproducible defeat (field-verified)

SE (Safengine Shielden / SProtect, sp0101) is the domestic VM shell this pipeline is most battle-tested on. Its anti-debug is **anti-breakpoint at the core**, run by **multiple persistent background threads** doing continuous integrity/anti-debug checks:
- **Anti hardware-breakpoint**: `SetThreadContext` sets DRx + constructs an exception inside the VM + SEH inspects the DRx values -> a debugger's HW breakpoints are detected/cleared.
- **Anti INT3 software-breakpoint**: memory **hash/CRC over the shell's own code** -- **any byte you change (software bp `0xCC`, inline hook) ends the process** (observed: killed in ~166s after an inline hook).

**Iron takeaway**: on SE, **any "modify the shell's bytes" tactic (software bp, inline hook, byte-patch) is fatal** to the CRC thread. You MUST use a **"don't-change-bytes + suppress-anti-debug"** path. What works vs what dies:
- ✅ Read-only Frida attach/enumerate/memory-read -- safe, doesn't trip SE.
- ✅ ScyllaHide (usermode, hooks Nt* to hide the debugger -- doesn't patch the shell) + x64dbg + HARDWARE breakpoints only (or break on an outside API like `kernel32.Sleep`).
- ✅ Proxy-DLL boundary logging / Python-runtime monkeypatch (changes runtime state, not shell bytes; detach-persistent).
- ❌ Software breakpoint inside shell code, inline hook (Interceptor.attach on a shell fn), byte-patch -- CRC thread kills the process.
- ❌ Naked x64dbg attach/launch with NO ScyllaHide -> SProtect pops a dialog and kills the process immediately.
- ❌ Intel Pin / UnSafengine64 on current Pin 3.31 -> SE anti-DBI crashes it (`RECEIVED_ACCESS_FAULT`); the tool only ever worked on Pin 3.18.

**ScyllaHide config for SE (start from the VMProtect profile, then補勾 -- exact set that worked)**:
- Debugger Hiding: **PEB all 5** (BeingDebugged / HeapFlags / NtGlobalFlag / StartupInfo / OsBuildNumber) + NtSetInformationThread + NtSetInformationProcess + NtQuerySystemInformation + NtQueryInformationProcess + NtQueryObject + NtClose
- **DRx Protection ALL**: NtGetContextThread / NtSetContextThread / NtContinue / **KiUserExceptionDispatcher** ← the core of SE's exception-based anti-debug, MUST be checked
- Timing Hooks all; Misc → **Kill Anti-Attach**
- **NEVER check**: Prevent Thread creation, RunPE Unpacker (they block the shell's own decryption -> DLL never unpacks)
- Plugin install: 3 files (`HookLibraryx64.dll` / `ScyllaHideX64DBGPlugin.dp64` / `scylla_hide.ini`) into `<x64dbg>\release\x64\plugins\` (the layer with the real x64dbg.exe -- not `<x64dbg>\plugins\`).

**Then unpack** (the strong technique, see `tool-registry.md Sec.0.9`): loader.exe LoadLibrary the DLL -> ScyllaHide suppresses anti-debug so it survives -> memory self-decrypts (4.7MB→9.7MB) -> break `kernel32.Sleep` -> `dump_module` (rebuild PE + fix IAT) -> IDA on the DUMP (Rule 30). Note ThreadHideFromDebugger (`NtSetInformationThread` class 0x11) is the specific "SE anti-debug核心" forums cite -- covered by the NtSetInformationThread hook above.

### 2. Anti-Dump
- **Techniques**: erasing the PE header at runtime, PAGE_GUARD memory breakpoints, write-watch.
- **Bypass**: rebuild the PE header before dumping; `references/ida-re/scripts/dump_region.py` to dump post-decryption; repair IAT with an unpacker.

### 3. Anti-VM / Anti-Sandbox
- **Techniques**: VMware/VirtualBox/QEMU/KVM/Hyper-V fingerprinting, CPUID, `NtQueryLicenseValue(Kernel-VMDetection)`, physical memory/disk size, MAC prefix, timing checks (RDTSC+CPUID, Sleep-acceleration detection, GetTickCount).
- **Bypass**: harden VMware with **hzqst/VmwareHardenedLoader**, QEMU with **zhaodice/qemu-anti-detection** (patches QEMU fingerprints, bypasses anti-VM in Themida/VMProtect/Enigma/Safengine); or analyze on physical hardware (least effort); patch out timing checks or use find-oep's evasion. Check your environment's exposure with **NotRequiem/VMAware**, **void-stack/Hypervisor-Detection**.

### 4. Anti-Disassembly / Anti-Frida
- **Techniques**: junk code, control-flow flattening, anti-Frida (detecting `gum-js-loop`/`gmain` thread names, ports, memory signatures).
- **Bypass**: run ida-re's deobfuscation pre-pass first; have Frida rename its threads / use Gadget mode to dodge signatures (frida-win anti-debug-bypass).

### 5. Forged Call Stacks (push+jmp instead of call) -- structurally breaks step_out/stack-walking

**Technique**: instead of a real `call` (leaves a matched return address for `ret`/stack-walking), the obfuscator hand-writes `push <forged return address (immediate)>; jmp <target>` -- same effect, but no real call/ret matched stack frame.

**Recognition signals** (any one confirms this -- stop treating it as operator error and retrying):
- Disassembly repeatedly misaligns -- short-jump chains (`EB00/EB03/EB04`), an `E9` landing implausibly, or `push imm64`'s 8-byte immediate misread as a following instruction.
- Raw bytes at the "return address" show a **literal immediate right before a jump** (not pushed by a real `call`) -- appears as data in the code section.
- `step_out`/stack-walk **times out repeatedly**, or RIP lands somewhere unrelated (message loop, event dispatch) instead of the expected caller.
- Function-boundary lookup returns "not found" for that address.

**Bypass**: solvable only via **instruction-level dynamic trace** (record every executed instruction/block, auto-follow EB/E9 jumps, no call-stack semantics) -- `references/x64dbg/tracealyzer/` (if available this session, see its SKILL.md) or **Frida Stalker** (`references/frida-win/references/frida-docs/stalker.md`, in-process, zero MCP round-trips, immune to this). Don't attempt a 3rd round of step_out/stack-walk retries -- structural limitation, not luck. See Rule 14.

---

## 3. Common Bypass Techniques for Network Verification / License-Key Systems (Stages 1+4)

> Assesses whether your own network verification is hardened. Hardening counterpart to each technique is in `auth-bypass-cheatsheet.md`.

| Technique | Principle | RE Location | Hardening |
|---|---|---|---|
| **Local return-value forgery** | Hook verification function to always return "authorized" | Frida hook the entry; check if call site only does `if(ok)` | Auth result must feed a critical computation, not just a branch check; multi-point verification |
| **Offline/disconnection bypass** | Disconnect network, force "offline grace period" or cached-authorized branch | Capture traffic post-disconnect; find offline-degradation logic | High-value features require active connection; offline mode grants only short-lived, limited functionality |
| **Request replay / tampering** | Replay a legit activation request, or modify a loosely-validated param (machine code/device count) | Capture activation with Reqable, modify device ID and replay | Server must validate every param strictly; HMAC signature + nonce + timestamp against replay |
| **Fake server** | Spin up a fake local server / modify hosts / rewrite to return "authorization succeeded" | Examine response structure, Reqable rewrite to fabricate success and test | Response signed with server's private key, client verifies signature; certificate validation |
| **Machine-code forgery** | Tamper with reported hardware fingerprint to bypass device binding | Hook the API retrieving hardware info (CPUID/disk serial/MAC) | Multi-source fingerprint cross-check + server-side binding + anomalous-concurrency detection |
| **Local key/registry forgery** | Modify local license file/registry authorization flag | Monitor file/registry reads with Procmon/Frida | Sign/encrypt local state; never store final unlock decision in plaintext |
| **Keygen** | Reverse-engineer key-generation algorithm to build a keygen | Locate verification algorithm in IDA, identify crypto constants | Asymmetric signing (client has no private key, can't forge a key) |

**Commercial protection SDKs** (work backward to hardening ideas): PELock, NebulaFox/FoxAuth, AtlasAuthentication provide anti-crack/anti-debug/licensing. Identify the SDK's signature via diec/yara first.

---

## 4. Escalate / Switch Route / Stop Decision (Pair with Memory Log)

**Trigger**: a route hit [X] >= 3 times in `<target>-attempts.md`, or clearly exceeds current tooling's capability. Decide via this table, don't retry indefinitely:

| Situation | Decision |
|---|---|
| Stuck statically (packer/obfuscation/self-modifying code) | -> Switch to dynamic: unpack via find-oep then back to static, or Stage 4 black-box hook |
| Blocked dynamically by anti-debug | -> ScyllaHide/TitanHide; or switch to Frida; or use a physical machine |
| Anti-VM causes an exit | -> Switch to physical-machine analysis, don't burn time hardening the VM |
| Can't unpack an L3 virtualization packer | -> Give up unpacking the whole packer, hook only the virtualized functions' input/output |
| Network verification strictly server-side, no local logic to change | -> Record "no bypassable point client-side" -- a conclusion the software is well-hardened; deliver honestly |
| A dedicated tool clearly doesn't support this version | -> Tell the user "this exceeds current tooling, a dedicated XX tool is needed," stop, don't improvise |

**Ties to Rules 6/7**: log every escalation/give-up in the memory log; only a personally witnessed successful bypass goes into the hardening deliverable; with zero successes, report "bypass could not be reproduced" and treat that as a positive conclusion about good hardening.
