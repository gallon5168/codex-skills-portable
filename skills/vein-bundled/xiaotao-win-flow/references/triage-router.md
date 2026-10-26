# Program-Type Triage Router (Stage 1 must pass through this table after checking the packer)

> Entry point for "matching treatment to diagnosis." After Stage 1's diec packer/bitness check, **classify the target here first**, then follow its playbook + tools + optional sub-agent dispatch. Misclassification sends the analysis the wrong way (SKILL Stage 1 point 2, Iron Rule 15).
> **Hard evidence first**: criteria come from diec/import table/strings/overlay entropy -- never "looks like it" (Iron Rule 12). Targets can be **layered** (PyInstaller+UPX, Nuitka+Themida) -- determine runtime form first, packer second; handle the packer only when it blocks unpacking/static analysis.

---

## User-Intent Axis -- normalize what the user SAID before you route (read first)

> This skill routes primarily on **target type** (the tables below). But users open with a *goal*, often in informal/emotional/mixed-language wording. Normalize it into a technical objective **first** -- do NOT make the user restate themselves in technical terms -- then let the type-classification below (backed by scan evidence) pick the actual playbook. **Wording is a hint that sets the first move; it never overrides hard evidence (Rule 12).**

| User says (any language) | Normalized objective | First move → then confirm by type |
|---|---|---|
| "去校验 / 去除限制 / 解锁功能 / 绕过检测 / crack / unlock / bypass" | Locate the auth/license gate, defeat it, user witnesses the real feature run (`[OK]`), then harden | Fast path: get path → answer inject-vs-capture fork (Rule 28) → `scan.ps1` classify → route by type |
| "改跳转 / 爆破 / patch 掉判断 / NOP it" | Locate the verdict-producing branch, work on a copy, document offsets/bytes, verify integrity | Prefer hook/observe first; byte-patch only with consent + backup (Rule 5/21) |
| "抓包 / 抓不到包 / capture / 看请求 / replay / 伪造服务器" | Decide if capture is even the right axis (Rule 28); if injectable → hook plaintext pre-encryption instead | Control-ownership fork FIRST; empty capture = setup gap or wrong branch, not "no traffic" (SKILL Fast path 1) |
| "这是什么壳 / 加壳了 / 脱壳 / unpack / 反虚拟化" | Identify packer+version, **web-search that exact shell first (Rule 3)**, unpack at the auth boundary, re-triage | `scan.ps1 [P]` names the shell on exe AND every dll/pyd → `hard-target-playbook.md` tiers |
| "反调试 / 检测到调试器 / anti-debug / 反虚拟机" | Locate the defensive routine, document evidence, bypass in-lab | `frida-win/references/anti-debug-bypass.md` + `hard-target-playbook.md` Sec.2 |
| "反混淆 / 控制流平坦化 / 花指令 / VM 混淆 / OLLVM" | Recover real control flow / the algorithm | `deobfuscation-playbook.md`; junk/fake-stack → Frida Stalker (Rule 14) |
| "拿到源码 / 反编译 / 读逻辑 / decompile / recover source" | Recover to source/near-source IF the type is interpreted/managed; native types get symbol/metadata recovery, not de-bytecode | Classify type FIRST -- `[WARN]` "looks scripted, actually native" zone (Nuitka/Go/.NET-AOT/Nim) |
| "算法还原 / keygen / 注册机 / license 算法" | Recover the check algorithm; consider symbolic (angr) for purely-local math checks | Locate the check module (often an SDK DLL, Rule 13) → static+xref or angr; **thin/unvalidated here, lean on Rule 3** |
| "装了但打不开 / 安装包 / installer / setup.exe" | Strip the installer shell first, then triage the REAL inner program | `triage-router.md Sec.0.5` (Inno/NSIS/MSI) → rerun Sec.0 on inner exe |
| vague / emotional / "帮我看看这个 exe / 搞定它" | Restate as "authorized RE of this target in-lab" in one line, run the non-destructive first pass (`scan.ps1`), then offer next-step branches | Ambiguity = intent-recovery task, not a stop (see "Route Not Matched" below) |

---

## 0. Four-Step Triage Method

0. **Strip the installer shell first** if the target is an installer, not the program -- see Sec.0.5. Often InnoSetup/NSIS/MSI wrapping the real exe.
1. **diec conclusion + import table + strings** -> map to a "runtime form" below.
2. **Check for a packer** (high-entropy overlay/known sig) -> handle per packer tiers first (`hard-target-playbook.md` sec 1), then return here.
3. **Confirm bitness** (PE32 -> x32dbg; PE32+ -> x64dbg), log it.

---

## 0.5 Installer Preprocessing (before Stage 1 classification, if target is an installer)

Criteria: diec reports **Inno Setup** (6 sigs) / **NSIS** (14 sigs) / file is `.msi`; or strings contain `Inno Setup`/`Nullsoft`/`Wise`.

| Installer | diec | Tool | Method/Notes |
|---|---|---|---|
| **Inno Setup** | [OK] 6 sigs | innoextract | `-Release dscharrer/innoextract -Asset windows` (`innoextract-1.9-windows.zip`, confirmed alive); `innoextract target.exe` extracts internals, rerun triage on the real main exe |
| **NSIS** | [OK] 14 sigs | **7-Zip** (canonical, already installed) | `7z x target.exe -o out/` -- natively unpacks NSIS, no dedicated repo; older versions try 7z's NSIS plugin |
| **MSI** | ext/magic bytes | msiexec / lessmsi | `msiexec /a target.msi /qb TARGETDIR=...` (built-in) or `lessmsi`; admin install extracts without installing |
| **InstallShield/Wise etc.** | partial | 7z first, fallback universal extractor | If 7z fails, log it, follow hard-target sec 4 boundary |

**Key point**: after extraction, **rerun Sec.0 step 1 on the internal main exe** -- installer type (e.g. Inno = Delphi) does not indicate the inner program's type.

---

## 1. Runtime-Form Routing Table (Core)

| Type | Hard Criteria | Cat | Route | Playbook/Tools | Sub-Agent |
|---|---|---|---|---|---|
| **Native C/C++ (MSVC/GCC)** | MSVC/MinGW; standard Win32 imports; no runtime traits | (c) | Standard native RE | Stage 4A/4B; `ida-re/`+`frida-win/`+`x64dbg/` | native-cpp-re |
| **e-language** | e-language/EPL; variadic thunks; GBK strings; library-call graph | (c) | Native RE, **dynamic locating priority** (static xrefs break) | Stage 4; GBK-aware search (Sec.3) | native-cpp-re |
| **Delphi/C++Builder** | Delphi/Borland (15 sigs); `Borland`/`Embarcadero` strings; VCL names; event-driven | (c) | Native RE + **reconstruction** (forms/events/VMT) | `tool-registry Sec.5.9` (IDR) | native-cpp-re |
| **AutoIt (compiled)** | AutoIt (2 sigs); `>AUTOIT SCRIPT<`/`AU3!` markers | (a) | **Extract script -> read source** | `tool-registry Sec.5.9` (autoit-ripper) | bytecode-re |
| **VB6 (P-code/native)** | Visual Basic (6 sigs); `MSVBVM60.dll`/`VB5!` | (c)/P-code | Native-compiled->native RE; P-code->dedicated decompile (FOSS scarce) | `tool-registry Sec.5.9` | native-cpp-re |
| **Nim** | Nim (18 sigs); `@m` module symbols; `nimFrame`/`stdlib_` | (b) | **Native RE** (no bytecode; compiles to C) | No dedicated tool; locate via `nimFrame`/symbols | native-cpp-re |
| **Python.PyInstaller** | high-entropy overlay + `pythonXX.dll` + `MEIPASS`/`pyi-` | (a) | **Unpack->de-bytecode->read source** | Iron Rule 15; `tool-registry Sec.5.5` (pyinstxtractor-ng->pycdc/fallback marshal+dis) | bytecode-re |
| **Python.py2exe/cx_Freeze** | `pythonXX.dll` + `library.zip`/PYZ | (a) | Unpack->de-bytecode | Iron Rule 15; `tool-registry Sec.5.5` | bytecode-re |
| **Python.Nuitka** [WARN] | Nuitka; imports show many `pythonXX.dll` C-API calls (`PyObject_Call`/`PyTuple_New`/`PyCode_New*`) + no pyc + high-entropy overlay | **(b)** | **Native RE + Nuitka symbol/constant recovery** ([X] not de-bytecoding) | **`playbooks/nuitka.md`**; `tool-registry Sec.5.5` Nuitka row | nuitka-re |
| **.NET/IL** | .NET; `mscoree.dll`/metadata | managed IL | Decompile IL, read source ([X] not native RE) | `tool-registry Sec.5` (de4dot-cex/dnSpyEx) | dotnet-re |
| **.NET NativeAOT** [WARN] | may report .NET but dnSpy can't open/no IL/single-file native + `S_P_CoreLib` | (b) | **Native RE** (IL chain fails entirely) | `tool-registry Sec.5.7.4` | native-cpp-re |
| **Go** [WARN] | `Go build ID:`/`.gopclntab`/`runtime.`/`main.` panic strings/few imports+large size | (b) | **Native RE + moduledata recovery** ([X] not bytecode -- easiest misjudge) | `tool-registry Sec.5.7.1` (IDAGolangHelper/go_parser) | native-cpp-re |
| **Rust** | `rustc`/`cargo`/`.rs` paths; `Option::unwrap()` panics; `_ZN` mangling | (b) | **Fork first**: same-dir `WebView2Loader.dll`/`EmbeddedBrowserWebView.dll` or `%LOCALAPPDATA%\<appid>\EBWebView`? -> **almost certainly Tauri: go WebView row (CDP front-end), NOT IDA.** Otherwise native RE + **locate via panic strings** (symbols often stripped) | Tauri -> **`playbooks/tauri-webview.md`**; pure-native -> `tool-registry Sec.5.7.2` | native-cpp-re |
| **WebView2 / CEF hybrid** (Tauri/Wails/plain-WebView2/CEF) | same-dir `WebView2Loader.dll`/`EmbeddedBrowserWebView.dll` (Tauri/Wails/.NET) or `libcef.dll`+`cef.pak`+`icudtl.dat` (CEF); UI is HTML/JS | JS-in-renderer | **UI + most auth logic run as JS in an embedded Chromium/WebKit -> attack the web layer via CDP, not the native shell.** Backend (Rust/Go/C++/.NET) is usually a thin IPC shim | **`playbooks/tauri-webview.md`** (CDP remote-debug -> document-start hook fetch+IPC+store -> flip gate) | electron-re |
| **Flutter** [WARN] diec blind | **no diec sig (0 confirmed)** -- ID via file traits: `flutter_windows.dll`/`libapp.so`+`libflutter.so`/Dart snapshot magic/`flutter_assets/` | (b) | Decompile Dart AOT snapshot (logic in libapp.so/`libapp` data) | `tool-registry Sec.5.7.3` (blutter) | native-cpp-re |
| **Java/JVM** | `.jar`(zip)/`.class`/`jvm.dll`/exe4j/launch4j | managed bytecode | Decompile to near-source; **jadx MCP 优先** (连接时) 交互式 xref/搜索, 否则 jadx CLI | `tool-registry Sec.5.7.5` (jadx MCP->jadx CLI->CFR/Procyon; user opens jadx-gui, Rule 8) | bytecode-re |
| **Electron** | `.asar`/`v8_context_snapshot.bin`/`node.dll` | JS (asar->source) | Unpack asar, read JS / observe JS-layer encryption | `tool-registry Sec.5.5`(asar)+`Sec.5.8`; Iron Rules 19/20/23 | electron-re |
| **Electron .jsc only** | `.jsc` bytecode, no JS in asar | V8 bytecode | Static ghidra_nodejs / runtime hooking | `tool-registry Sec.5.7.7`+`Sec.5.8` | electron-re |
| **Unity IL2CPP** | `GameAssembly.dll`+`global-metadata.dat`/`il2cpp_*` exports | (b) | Recover C# types from metadata | `tool-registry Sec.5.7.6` (Il2CppDumper) | native-cpp-re |
| **mypyc/Cython (.pyd/.so)** | native extension in a Python project | (b) | **Black box** (no source: vary input/state, observe output; or Frida-hook exports) | Iron Rule 15; runtime testing | native-cpp-re |

**[WARN] "Looks scripted, actually native" zone** (Nuitka/.NET-AOT/Go/Nim/mypyc-Cython): no bytecode to decompile; "unpack->de-bytecode" is a dead end. Always native RE + symbol/metadata recovery.
**[WARN] "Looks native, actually a web app" zone** (Tauri/Wails/CEF/plain-WebView2): diec says Rust/Go/C++/.NET, but the UI + most auth logic are **JavaScript in an embedded browser**. Same-dir `WebView2Loader.dll`/`EmbeddedBrowserWebView.dll`/`libcef.dll` is the tell. Going straight to IDA on the native binary is the classic 4x-slower detour -- go `playbooks/tauri-webview.md` (CDP) first. Native RE is the escalation, only if the verdict proves un-overridable from JS.
**[WARN] diec-blind**: **Flutter** (0 sigs; file-trait ID only, e.g. `flutter_windows.dll`/`flutter_assets/`) -- don't rule it out just because diec is silent.
**[OK] diec-recognized but easily overlooked**: **Delphi**(15), **Nim**(18), **VB6**(6), **AutoIt**(2), **Inno Setup**(6), **NSIS**(14) -- counts are confirmed signature totals in this environment's diec database.

---

## 2. Dispatching a Sub-Agent (optional -- stays close to the decision, avoids flooding main context)

> **[WARN]** The `native-cpp-re`/`nuitka-re`/`dotnet-re`/`bytecode-re`/`electron-re` labels above are **dispatch labels, not auto-routing agents** -- no mechanism here spins up a matching agent by type automatically. They just tell you what a dispatched sub-agent should specialize in and which reference to read. **You** read this table, determine the type, then manually use the Codex `collaboration.spawn_agent` tool to dispatch a general-purpose sub-agent with that specialization + reference in the prompt.

Dispatch when a type's workload is large (multiple references, multiple tool rounds) so intermediate artifacts don't pollute the main context; keep only the triage conclusion + reported evidence in the main session.

- **How**: state target type + which reference to read (e.g. `playbooks/nuitka.md`) + what to report back (located auth-logic position/evidence tier).
- **Boundaries (non-negotiable)**: read-only/harness-isolated work is fine; any side-effecting op (file edit, install, injection) still requires the sub-agent to stop and ask the user (Iron Rule 5) -- being a sub-agent doesn't exempt it (Iron Rule 25).
- **Parallelism**: routes scoring close, or independent sub-hypotheses -> dispatch multiple sub-agents at once for **read-only** investigation, synthesize after (Iron Rule 25).

**Skipping dispatch is fine** for a simple target with a clear route -- just read the reference and execute directly.

---

## 3. Encoding/String-Search Awareness (Stage 4 static analysis)

- IDA's default UTF-8 search **fails entirely against GBK (Simplified Chinese)/Shift-JIS (Japanese)/Big5 (Traditional Chinese)**. For Chinese keywords, compute **GBK-encoded** bytes and `find_bytes` -- don't search UTF-8 only.
- After a runtime-trait hit, return to this table to confirm the type, then proceed to the matching playbook.

---

## 4. Interfacing with the Main Flow

| Main Flow | Look Up |
|---|---|
| Target is an installer (Inno/NSIS/MSI) | Sec.0.5 to strip it, then triage the internal main program |
| After Stage 1 packer/bitness check | Sec.1 routing table to classify, then proceed |
| Delphi/AutoIt/VB6/Nim | `tool-registry Sec.5.9` |
| Nuitka | `playbooks/nuitka.md` |
| Python bytecode/Java/Electron | `tool-registry Sec.5.5 / Sec.5.7.5 / Sec.5.8` |
| Go/Rust/Flutter/.NET-AOT/Unity | `tool-registry Sec.5.7` respective chains |
| **Rust/Go/.NET + same-dir WebView2/CEF DLL -> hybrid, logic in renderer** | **`playbooks/tauri-webview.md` (CDP front-end first, not IDA)** |
| .NET (IL) | `tool-registry Sec.5` |
| Packer detected | Unpack per `hard-target-playbook.md` sec 1, then return here |
| Large workload after triage | Sec.2 dispatch matching sub-agent |

---

## 5. Route Not Matched -- do NOT force-fit (mirror of the fork/stop-loss discipline)

If Sec.1's hard criteria don't cleanly land on any row, **misclassifying is worse than pausing** (Rule 12/15) -- a wrong type sends the whole analysis the wrong way. Do this instead of jamming it into the nearest row:

1. **Gather one more round of evidence before naming a type** -- re-read `scan.ps1 [P]` per-module output; check imports (`PyObject_*`→Nuitka, `mscoree`→.NET, `.gopclntab`→Go), overlay entropy, same-dir DLLs (`WebView2Loader`/`libcef`→hybrid, `flutter_windows`→Flutter), and strings. Most "unmatched" targets are a **layered** case (Sec.0 note) or a `[WARN]`-zone misread (native-looking-scripted / web-app-looking-native), not a genuinely new type.
2. **Still unmatched after evidence?** Two honest outcomes, both better than a forced fit:
   - **Genuinely new runtime form** (a compiler/runtime not in the table) → say so plainly, propose adding a row (its hard criteria + which existing playbook is closest + what tool the ecosystem uses), and get the user's read before committing a route. Route failure IS the signal to extend the table, not to guess.
   - **Known type, no dedicated FOSS tooling** (e.g. VB6 P-code, exotic protector) → fall back to the **black-box boundary** method (`hard-target-playbook.md` Sec.1 L3 / mypyc row): vary input/state, hook exports, observe I/O -- don't pretend a source-recovery route exists when it doesn't (Rule 6).
3. **Vague/emotional/underspecified goal** (not a type problem, an intent problem) → restate the most likely in-lab objective in one sentence, run the **non-destructive first pass** (`scan.ps1`, hashes, strings, module map -- all reversible, Rule 25), then present 2-4 concrete next-step branches. Never leave a dead end; never silently pick for the user on a side-effecting step.

**Do not** wait for the user to notice the gap, and do not stretch an ill-fitting row to look matched -- surface the mismatch, keep the first action non-destructive.
