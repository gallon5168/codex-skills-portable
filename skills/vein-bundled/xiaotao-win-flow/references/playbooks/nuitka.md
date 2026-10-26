# Nuitka Reverse-Engineering Playbook

> Gap-filler for **Nuitka-compiled targets**: mechanism, three dead ends, verified experience, vetted toolchain. `triage-router.md` routes Nuitka to "(b) native compilation" -> here. Triage entry: Stage 1 diec reports Nuitka (or `pythonXX.dll` C-API imports + no pyc + high-entropy overlay) -> route here, **not "unpack -> de-bytecode"** (dead end, Sec.2.1).
> Evidence tiers (Iron Rules 6/7): `[OK]` verified this session on target (Chinese-named launcher "chuanshanjia"/pangolin launcher, 294MB Nuitka onefile, embedded python39.dll). `[WARN]` candidate/unverified. `[DOC]` tool capability per README, not necessarily run on this target category.

## 0. Nuitka != PyInstaller -- no de-bytecode route

PyInstaller/py2exe package **real pyc bytecode** -- unpack -> decompile reads source in minutes (`tool-registry.md Sec.5.5`). **Nuitka compiles Python to native C -> machine code; no reversible bytecode exists.** Treating it as interpreter packaging is a dead end, confirmed twice this session (Sec.2.1). Correct route: **native RE + Nuitka-specific symbol/constant recovery**.

## 1. Runtime mechanism (understand before reversing)

[OK] this session reverse-engineered `sub_14F55F540` + cross-confirmed against dynamic memory; [DOC] matches nuitka-helper/Nuitka-Dumper READMEs:
1. **Every Python function = one native C function.** Real logic is machine code in `.text`.
2. **Constants (strings/numbers/tuples/code objects) packed into one blob** in the PE's **RCDATA resource (commonly type=10, id=3)**, restored to a Python object pool at startup by a **generic deserializer** (marshal-like recursive decoding, single-char type tags: `u`/`a`=string, `C`=code object, `T`=tuple, `l`/`q`=integer, `D`=dict...). Blob header has a **checksum**: decoder branch like `puts("Error, corrupted constants object"); abort();` ([DOC] Nuitka-Dumper README; [OK] equivalent seen this session).
3. **Code objects are empty shells**: deserializer always builds `PyCodeObject.co_code` from the same fixed placeholder (this session: `unk_15191F0F0`) -- never real bytecode; at runtime it points to CPython's shared empty `b''` singleton.
4. Strings/constants are accessed via a **compile-time constant-pool index** (`base + index`), not a direct address reference.

> These 4 points cause the three dead ends below and why Sec.3 needs dedicated tooling.

## 2. Three dead ends (avoid up front, they burn turns)

**2.1 [X] Don't dump PyCodeObject from memory -- co_code is an empty shell.** `[OK]` on target, `co_code` of `_check_with_server`/`launch_main_after_auth`/`on_login` all point to CPython's shared empty `b''` singleton (very high `ob_refcnt`, `ob_size=0`, `ob_type==PyBytes_Type`). Real logic exists only as machine code -- no extractable bytecode. Memory does hold code objects with non-empty `co_code`, but their `co_filename` is always Python stdlib (`<frozen importlib._bootstrap>`/`codecs.py`), never app logic.

**2.2 [X] String->xref is structurally broken -- IDA xrefs all zero.** `[OK]` `xrefs_to`/`find_xref_signatures`/`find_bytes`/`trace_data_flow` against app strings (`_check_with_server`/`AuthDialog`) -- all four returned zero results. Root cause: Sec.1.4, constant-pool index access leaves no direct address reference. **`references/ida-re/`'s `string_xref_map` does not apply to Nuitka; use a different anchor (Sec.3).**

**2.3 [WARN] App functions aren't exported -- Frida can only hook Qt/C-API.** `[OK]` the exe exports/imports only standard symbols (KERNEL32/USER32/python39.dll C-API/Qt); app functions like `_check_with_server` have no export symbol, so `Module.getExportByName` can't reach them. Frida can only attach to Qt (`QDialog::exec`) or Python C-API (`PyObject_Call`) -- generic layers far from actual decision points. Black-box/Frida-hook-on-exports is largely dead here.

## 3. Toolchain (verified to exist + capability checked against README)

> [WARN] All below are `[DOC]` -- exist, README claims the capability, not actually run on the "chuanshanjia" target. Confirm deps per Rule 1, consent before downloading per Rule 5. Liveness/stars: Nuitka row of `tool-registry.md Sec.5.5`.

**3.1 Unpacking** (get `__main__` module + constants blob): **nuitka-extractor** (`extremecoders-re/nuitka-extractor`, 238*) unpacks onefile builds, extracts embedded DLL/so/resources and the `__main__` module DLL. Only extracts binary resources, no decompile (README: "doesn't contain pyc file"); signed PE needs cert stripped first.

**3.2 [TARGET] Static anchor recovery** (breaks Sec.2.2) -- highest priority:
| Tool | Repo | Capability | Why it matters |
|---|---|---|---|
| **nuitka-helper** | `Siradankullanici/nuitka-helper` | IDAPython scripts: (1) Library Code Recovery (2) User Code Recovery (name->address map) (3) Constants Recovery (constant -> ref sites -> `constants.log`); ships `nuitka.h` structs, FLIRT sigs, `get_nuitka_version.py`; blog by goatmilkk | Resolves 2.1/2.2 via Nuitka struct layout + constant-pool decoding instead of string xrefs |
| **Nuitka-Dumper** (`nuitka_unstreamer`) | `4equest/Nuitka-Dumper` | Decodes the constants blob, generates IDA script `rename___main__.py` naming every constant + commenting every ref site. Usage: unpack with nuitka-extractor -> extract RCDATA -> `--base-map __main__:0xADDR` | Automates what this session did by hand on `sub_14F55F540`; README hints at a `.bytecode` branch worth exploring |

Finding the base-map address ([DOC] per README): find the (usually unique) xref to `LoadResource`/`LockResource` -> locate the constants-validation function (the "corrupted constants object" abort) -> check its xrefs (module init routines) -> find the call whose argument is `"__main__"` -- its `qword_TARGET` is the entry module's constant base address.

**3.3 Dynamic injection/hooking** (fixes Sec.2.3, anti-injection risk):
| Tool | Repo | Capability | Risk |
|---|---|---|---|
| **nuitka-injector** | `crackalove/nuitka-injector` (15*) | Injects a DLL + inits the Python API in-target, 12 payloads. Most relevant: Mode 8 HTTP Spy (hooks `requests.Session.request`, captures plaintext before HTTPS encryption, bypasses SSL pinning), Mode 11 Nuitka Explorer (compiled functions/code objects on GC heap), Mode 7 MITM Hook (modifies return values), Mode 5 Anti-Anti-Debug (patches `IsDebuggerPresent`), Mode 1 Full Dumper (dumps `__main__` globals) | [WARN] May trigger `anti_inject_scan_fail_closed` (blacklist of specific words like frida/x64dbg); differently-named DLL may not get caught -- unverified |
| **pymodhook** | `ekcbw/pymodhook` (120*) | Records args/return values/derived objects of any Python module's calls, IDA-style call sequence (`pip install pymodhook`); like Android Xposed | Must run inside target's Python context; same risk |

**3.4 Combined/composite/reference**: Nuitka+Themida/VMProtect combo -> `DimaReverse/nuitka-themida-unpacker` (16*), `2M12/DeNuitkanizator` (16*) -- unpack the outer layer first (`hard-target-playbook.md` sec.1 + `tool-registry.md Sec.1`), then return to Sec.3.1. `HydraDragonAntivirus/AutoNuitkaDecompiler` (56*): IDA Pro 9.1 + `stage1idapro.py` (inspired by nuitka-helper), automated malware pipeline; non-IDA variant handles UPX-wrapped targets. `1-3-7/disrobe` (41*): general decompiler/deobfuscator/unpacker, but for Nuitka only fingerprints, doesn't recover symbols (confirmed previously).

## 4. Recommended workflow (static-first)

```
Stage 1 identifies Nuitka (diec + python39.dll C-API imports + no pyc)
   | (outer packer: unpack first via tool-registry Sec.1 / nuitka-themida-unpacker)
   |-[Main: static] Break Sec.2.2's string-xref dead end ----.
   |  1. nuitka-extractor unpacks -> __main__ DLL + RCDATA   |
   |  2. Nuitka-Dumper decodes constants -> rename___main__.py |
   |  3. Run nuitka-helper.py in IDA -> names/library code/constant refs |
   |  4. App named, constants commented -> locate auth-decision branch |
   |  5. Statically patch that jump (show user before changing) |
   `-[Aux: dynamic, read-only, safe] --------------------------'
      - Read-only RPM memory scan (Sec.5.1) to cross-verify static conclusions
      - Need runtime plaintext/params -> nuitka-injector (Sec.3.3, mind anti-injection)
```
**Why static-first**: dynamic injection hits anti-injection (Sec.2.3+5.2); static nuitka-helper + Nuitka-Dumper are entirely offline, zero-injection, and break the string-xref dead end directly -- should outscore dynamic hooking in Stage 2.5 route-scoring on anti-injection targets.

## 4b. Runtime route -- live injectable process (complements the static route above)

The Sec.3/4 static route suits an **anti-injection onefile** you analyze offline. But when the target is **already running and injectable** (embedded interpreter, no fatal anti-injection), a runtime route is often faster and is what one full case `[OK]` used end-to-end:
- **A compiled Nuitka function is still a module/class attribute -> replace it wholesale at the Python level.** `Cls.method = my_impl` works even though its `__code__` is a stub (`RuntimeError('Compiled function bytecode used')`, `type()=='compiled_function'`). You cannot edit its bytecode, but you can **swap the whole callable** or **monkeypatch the check it calls**. This defeats "can't patch Nuitka bytecode" without any static extraction.
- **Drive it in-process via the embedded interpreter C-API** (`PyGILState_Ensure`+`PyRun_SimpleString`), **observe with excepthook/settrace/gc-introspect**, and **complete a stalled UI mount from the runtime on the main thread** -- full procedures in `references/runtime-injection-hooking.md` and `references/crash-exit-handling.md`.
- **When to prefer which**: fully-static anti-injection onefile -> Sec.3/4 static. Live, injectable, and you need to flip a gate / mount the UI / read runtime data -> runtime route (this section). They compose: static to understand, runtime to act.

## 5. Verified anti-detection experience ([OK] actually run this session)

**5.1** Read-only memory scanning triggers nothing: `OpenProcess(PROCESS_VM_READ|PROCESS_QUERY_INFORMATION)` + `VirtualQueryEx` + `ReadProcessMemory`, no debugger attach/injection/thread. Scanned repeatedly, never triggered a dialog or self-kill. Pair with **IAT-slot ASLR-resolution**: read a known python39.dll C-API import slot's runtime value to convert IDA static <-> live address (`live = main_base + (static - 0x140000000)`) -- generic to any native target embedding CPython.

**5.2** Process blacklist matches the full cmdline -- a naming trap for scripts. `kill_if_bad_process` uses `psutil.process_iter()` on each process's `.exe` + full cmdline vs: `frida / x64dbg / ida64 / idaq / ollydbg / cheatengine / fiddler / charles / mitmproxy / burpsuite / burp / wireshark / httpdebugger`. **[WARN] Trap actually hit: a blacklisted word in your script's filename gets flagged** -- `frida_enum.py` was judged BAD purely for "frida" in its cmdline, regardless of actual injection. Give injection/analysis scripts and temp files ASCII-neutral names avoiding every blacklist word. Two other layers (trip on attach-style debugging): `anti_inject_scan_fail_closed` (`EnumProcessModules`+`GetModuleFileNameExW` scans loaded modules for the same names); `IsDebuggerPresent`/`CheckRemoteDebuggerPresent`/`NtQueryInformationProcess`/`sys.gettrace()` -- a real debugger like x64dbg always trips this, the worst route on a Nuitka anti-detection target.

**5.3** Full-scope IDA queries time out on a huge onefile: 294MB / 80,000+ functions, `survey_binary(detail)`/`func_profile(addr="*")` hang IDA's main loop until timeout. Use scoped queries (`func_query` with size/count filters, or a specified address range), never a full scan.

## 6. [WARN] Candidate techniques (unverified)

**6.1** Nuitka function object -> native C entry pointer: `Nuitka_Function_Type` internally stores a pointer to the compiled C function. Pull it from memory, subtract live base, add IDA static base -> locate that function's machine code, bypassing Sec.2.2. Not verified this session (struct offset never confirmed); nuitka-helper's User Code Recovery likely already does this -- prefer it (Sec.3.2) over reinventing.

**6.2** Whether nuitka-injector's DLL injection evades anti-injection: blacklist matches specific words so a neutrally-named DLL may not get caught, but fail-closed design needs actual testing. Before injecting, follow Iron Rule 17 (confirm no modal dialog open).

## 7. Connections
- **triage-router**: identified as Nuitka -> route to (b) native compilation -> Sec.4 workflow, never "unpack -> de-bytecode."
- **Stage 2.5 scoring**: static anchor recovery (3.2) > dynamic hooking (3.3) > x64dbg (5.2 always trips it).
- **ida-re sub-skill**: `string_xref_map` fails on Nuitka (2.2); use nuitka-helper's Constants Recovery.
- **tool-registry Sec.5.5**: registers the Nuitka tool row; fetch via `fetch-tool.ps1` (ask first).
- **Iron Rule 6**: every tool here is `[DOC]` only -- no bypass into Stage 5 hardening doc until run and the unlock personally witnessed.
