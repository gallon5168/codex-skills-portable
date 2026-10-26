# Experience Zone / Case Studies

> `SKILL.md` no longer inlines case studies -- all collected here. Users can add their own (specific packers, common auth patterns, tricks for identifying encryption schemes, etc.).

---

## Case Study 1: PyInstaller (Py3.14) AI Writing Tool -- Two-Layer Authorization

Strings together several iron rules -- a playbook to follow:

1. **Pack detection (Stage 1)**: diec reports PyInstaller -> interpreter packaging, **don't touch IDA/x64dbg**, go straight to `tool-registry.md Sec.5.5`'s unpacking chain.
2. **Unpacking + de-bytecoding (Rule 15)**: `pyinstxtractor-ng` extracts `_build_standard_edition.pyc` etc; every Py3.14 decompiler failed -> downloaded the 3.14 embeddable Python, disassembled with `marshal`+`dis`. Constant pool exposed `SERVER_URL='http://.../'`, `AICLEAR_API_URL='http://127.0.0.1:5001'`, `ACTIVATION_FILE='activation.json'`, plus `'permanent'`/`'expired'` strings.
3. **Enumerate every gate (Rule 15)** revealed **two layers**:
   - Main-program: `check_authorized()` hits remote `/auth`; on failure falls back to local `load_activation_state()`, reading `activation.json` (passes when `is_active` + `expire_type=='permanent'`).
   - Engine: a local subprocess on `127.0.0.1:5001`; `_is_aiclear_activated()` GETs `/api/status` checking `isActivated`.
4. **Two pitfalls in Stage 3's server-side forgery**:
   - Forging the remote response failed first ("all connection methods failed"). A **proxy-reachability precheck** (traffic capture filtered by app) revealed the restarted process wasn't going through the proxy -- only 4 old records existed. Not the guessed "secondary verification" -- traffic simply never reached the proxy.
   - Engine layer is `127.0.0.1` loopback, which **Reqable can't intercept** -- abandoned, switched to local forgery (cheatsheet technique 5).
5. **Local forgery**: Engine -- changed `activated:true` in `server_v3\license_state.json`, curl-verified `isActivated` flipped true. Main-program -- `_safe_read_json` opens `'activation.json'` (relative path) -> **per Rule 12, read the process's PEB for real CWD**, confirmed `...\Gulang\`, created `activation.json` there (`is_active:true, expire_type:'permanent'`).
6. **Lessons**: (1) judge interpreter packaging early, saves time; (2) fall back to `marshal`+`dis` when decompilers lag; (3) don't waste effort on loopback capture; (4) prove traffic reached the proxy before forging, don't over-attribute; (5) get hard CWD evidence for relative-path files. Either layer unbypassed keeps everything locked.

---

## Case Study 2: Electron Desktop Client (Windows) -- RSA+AES Hybrid Encryption Authorization Protocol

Strings together Rules 19/20/21, reproduced live to feature-level unlock [OK]:

1. **Pack detection**: diec found `.asar`/`v8_context_snapshot` -> Electron, auth logic at the JS layer.
2. **Passive observation (Rule 19 step 1)**: hooked only to record, without altering return values, via `templates/mitm-observer.js` on Node's native `crypto`+`crypto-js`+`jsencrypt`+`http/https` **all at once** (Rule 20), letting the program talk to the real server while the user manually walked the full login flow (Rule 9). Logs to a file, not stdout (Rule 21).
3. **Pitfalls confirmed**:
   - Hooked only `crypto-js` initially, assuming response decryption used it too -> actually Node's native `crypto`, needing an extra round. -> Origin of Rule 20's "hook all libraries at once."
   - One-login sample nearly mistook a **session-level random key** for a fixed one -- caught only because a second login got clicked too, revealing the key had changed. -> Origin of Rule 20's ">=2 independent samples" requirement.
4. **Offline verification (Rule 19 step 2)**: captured key/IV/mode plus ciphertext, verified offline with Python (PyCryptodome) in seconds that real plaintext decrypted -- confirmed the protocol before forging, catching the misunderstanding before going live.
5. **Field dictionary (Rule 19)**: curl'd/captured a real response first to build a field-mapping table -- had previously guessed a backend field name (`lineId`) from a frontend variable, getting stuck on "please select a line first," wasting 2 repackage rounds. Forged structure exactly copied the real one, only values swapped.
6. **Single-layer changes + post-repackage verification (Rule 21)**: each round changed only one layer (render forgery / main-process HTTP forgery, verified separately, never together); repackaged asar with official `@electron/asar`, confirmed the process fully exited first (a locked `.node` file once silently produced a corrupted 8MB package while still exiting code 0); re-extracted key files afterward to verify the change took and size was sane -- never trusting exit code. Target had asar integrity fuse -> switched to a Frida runtime hook instead of edit-and-repackage.
7. **Lessons**: (1) encrypted responses: observe passively -> verify offline -> forge, don't skip steps; (2) once encryption confirmed, hook all candidate libraries at once; (3) "key is fixed" needs >=2 independent samples; (4) build a field dictionary from a real response before forging; (5) zero tolerance for the process not exiting before repackaging, mandatory post-repackage integrity checks, check Electron's integrity fuse first.

---

## Positive Example: the "Minimal Non-Crash Condition" in a Catch Block

A cost-saving methodology worth preserving:

Analyzing `Card.getData`/`Pack.send`, instead of "forge a response passing full signature verification" (heavy work needing a dynamically computed per-request nonce), the approach read the error-handling path first -- `Pack.send` only returns null inside its catch block, and the caller never null-checks it, causing the NPE crash. So as long as the response decrypts and parses into the expected top-level field structure, the function returns a non-null error string even if signature verification fails, and no crash triggers. An order of magnitude cheaper than a fully correct response, same result: crash eliminated, target observation point reached.

**Reusable methodology**: for any "will this call chain crash" question, locate every `catch`/exception block's return value along the chain and the caller's null-check logic, and find the minimal sufficient condition for not crashing -- often far cheaper than a fully correct input/response. You don't need to pass verification, only avoid the null/None branch.

---

## Case Study 3: Shell on the SDK DLL, not the main exe

A real run scanning only the main exe found it clean and burned many rounds hunting for a shell before anyone thought to scan the same-dir DLLs -- the Safengine shell was actually sitting on `SPCloud64_Py.dll`. **Origin of the rule**: `scan.ps1` must check the exe AND every same-dir dll/pyd for a named shell in one pass; the packed module -- often an SDK DLL, not the main exe -- decides what you attack.

---

## Case Study 4: Defense-in-depth auth with three sequential gates

A real run's auth stack had three gates in series, each only becoming visible after the previous was defeated: (1) a login boolean, (2) a PIC/machine-code check calling `os._exit(0)` in init, (3) GUI content gated on init completing. **Origin of the rule**: don't declare victory at the first gate -- enumerate every check function/exit branch/state file/second verification, and after each bypass, trace for the next termination point until the real feature actually runs.

---

## Case: 灵播AI (Safengine cloud-verify + PyArmor + Nuitka) -- the WINNING playbook

Three shells, all guarding only the **launcher outer layer**; every bypass landed **outside** the shell (ctypes boundary / Python runtime / backend). This is the reference success path -- contrast it against the pitfalls above (the losing session brute-forced a proxy DLL's cloud-compute return for ~9 rebuilds before this playbook was found).

**Structure**: `灵播AI.exe` (Python3.12+PySide6, Nuitka-compiled, custom packer, requireAdministrator) + `digital/` (AI backend, 4 PyArmor-9.2.3 .py + own `heyi\python.exe` venv) + `SPCloud64_Py.dll` (**Safengine Shielden VM shell + NetLicensor** cloud SDK, strongest layer).

**Detection (why "查壳不准" bit us)**: DIE reported only `(Heur)Generic/Protection` on the main exe (high-entropy `.n2f/.i8cf` = Nuitka packed payload, NOT a crypto shell). The real shell only shows on `SPCloud64_Py.dll`: random sections `.sp0/.58a4/.5w44/.93c` (`.93c` entropy 7.86), strings `SProtectSDK64.dll`/`SPBegin`/`SPEnd`/`SPBeginVMFastAntiDump`, 57 `SP_Cloud_*` exports -> Safengine/SProtect + NetLicensor. **Identity confirmed by section-names + strings + exports crossed, NOT one clue** (the `sprotect.sys`-driver-name-alone guess of "深盾Virbox" was wrong).

**Winning moves (in order of cleanliness)**:
1. **Cleanest -- backend runs standalone, zero auth**: `cd digital && heyi\python.exe server.py` -> local Flask :5080 -> `GET /api/status` 200. The auth shell never guarded the backend功能.
2. **Full GUI bypass**: proxy DLL forces `SP_CloudLogin`=1 (auth = a **client boolean gate**, not server data) + Frida intercepts the `os._exit(0)` **exit-gate** (2nd gate = PIC machine-code check `sp_PIC_Func_*`/`BuildPack_*`/`SP_GetCpuid`) + main-thread QTimer补 `addSubInterface`+`splashScreen.finish()` (界面对象已建但init被os._exit中断没挂上) -> real main window.
3. **DLL unpack (strong technique)**: `loader.exe` LoadLibrary the DLL -> ScyllaHide (VMProtect profile + DRx/**KiUserExceptionDispatcher** all on) suppresses SE anti-debug -> memory 4.7MB->9.7MB self-decrypted -> break `kernel32.Sleep` -> `dump_module` -> plaintext DLL for IDA (Rule 30: IDA only on the dump).

**Key anti-debug fact (SE)**: read-only Frida attach/enumerate is safe (doesn't trip SE); **inline hook / byte-patch trips SE's memory-CRC thread -> killed in ~166s**. So: forge at the ctypes boundary (proxy DLL) + monkeypatch the Python runtime (os._exit, detach-persistent) -- never inline-hook the shell's bytes. PyArmor solved separately with **Pyarmor-Static-Unpack-1shot** (static, no execution, no anti-debug tripped).

**The two failures that cost the most (now hard rules in SKILL.md Fast path steps 2 & 5)**:
1. **Not committing to the unpack.** Auth was confirmed inside `SPCloud64_Py.dll`, yet ~9 rounds were burned brute-forcing the proxy-DLL's `SP_CloudComputing` *return value* and trying to forge the CBC server packet (spKey known, table known, but the algorithm is inline in Nuitka + no valid sample => unforgeable). The DLL should have been unpacked-and-read the moment auth was localized to it. **Lesson: auth localized to a module => unpacking that module is THE route; guessing its I/O from outside is the detour. >1 return-value-guess iteration = STOP, unpack.**
2. **Treating "blank window" as a data problem.** After login flipped, the window stuck on the splash logo. Rounds were wasted trying to make `initNavigation`'s decrypt "succeed" by forging its server data / faking `spCloud` returns / matching buffer lengths. **The real fix was pure runtime hooking**: intercept `os._exit(0)` (the PIC machine-code gate's exit) + on the **main thread** finish the UI mount (`addSubInterface` each `*Interface` + `splashScreen.finish()`, via `QTimer.moveToThread(app.thread())`+`invokeMethod`). **Lesson: "window exists but empty" = mount/exit-gate problem solved by hook + main-thread completion, never by forging the gated data.** Also: introspect the live object for REAL attribute names (`homeInterface`, not guessed `home_interface`) before writing the completion.
