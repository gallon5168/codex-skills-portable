# Tool Registry (Encounter X -> Which Tool -> Repo -> Install)

> Check this table first instead of ad-hoc searching -- get a confirmed tool name + repo + install method, then **present the tool name + source/command to the user and let them install it** (you never auto-install -- Rule 5 + SKILL.md hard stop 2). `scripts/fetch-tool.ps1` only *probes aliveness and prints the install command / download link* for the user to run -- it does NOT download or install. Aligned with Rule 3: search "how to handle this packer/algorithm," never "crack this software" -- every entry maps to a packer/obfuscation/algorithm type, not a specific piece of software.
> Star counts marked with a number were measured via the GitHub API this session; `(canonical)` entries are community-recognized stable repos not re-measured due to rate limiting. Re-confirm aliveness with `fetch-tool.ps1 -Probe` before use.

---

## 0. General usage rules

1. **Classify before picking a tool**: use `scripts/scan.ps1` (diec) + `references/x64dbg/yara-sigs/` to classify the target first. A wrong classification wastes every tool installed after it.
2. **Don't unpack if you don't have to**: for L3 virtualization packers on VM-ized functions, prefer black-box hooking of inputs/outputs (Stage 4B) over forcing an unpack.
3. **You never install -- present the tool + source, the user installs** (Rule 5 + SKILL.md hard stop 2): `fetch-tool.ps1` only probes and prints the install command / download link; hand that to the user and stop. The user runs it themselves.
4. **Stop on version mismatch**: dedicated unpackers depend heavily on the packer's exact version (e.g. unlicense only covers Themida/WinLicense 2.x-3.x). If it doesn't match, tell the user honestly per hard-target-playbook Sec.4 rather than forcing it.

### Four ways to obtain a tool

| Release form | fetch-tool parameter | Example |
|---|---|---|
| PyPI package | `-Pip "pkg"` / `-Uv "pkg"` | `pyinstxtractor-ng`, `autoit-ripper`, `angr` |
| Source repo (clone, build/run yourself) | `-Repo "owner/name"` | `NoVmp`, `nuitka-helper` |
| **Release-only (compiled exe/zip/rar, no PyPI, clone gets no binary)** | `-Release "owner/name" -Asset "keyword"` | `dnSpyEx/dnSpy`, `de4dot-cex`, `Scylla`, `innoextract`, `Magicmida` |
| System package manager | `-Winget "id"` | `upx` |
| **Commercial/official-site (not GitHub)** | user installs manually, not via `fetch-tool.ps1` | `Proxifier` (Sec.4.5), IDA Pro, Reqable |

> Usage for release-only tools: run `-Release "owner/name"` without `-Asset` first to list assets -> pick a substring (`win64`/`zip`) with `-Asset` to print that asset's download link -> **give the link to the user to download themselves** (the script does not download). Some releases ship source only; the script will suggest `-Repo` instead.

---

## 0.9. Packer detection + web search (do these BEFORE unpacking/analysis)

| Scenario | Tool | Repo / Install | Notes |
|---|---|---|---|
| Quick built-in packer/type triage | DIE (diec) | bundled `tools/die/diec.exe` (`scan.ps1`) | Fast first pass, but **often only reports `(Heur)Generic/Protection` on commercial shells (Safengine/SProtect...)** -- do NOT read that as "no shell". |
| **★ Strong packer/protector ID (when DIE can't name the shell)** | **Exeinfo PE** | `ExeinfoASL/Exeinfo` (release exe; GUI, user opens per Rule 8) | Top community detector, richest packer/protector signature DB -- names shells DIE misses. `scan.ps1` says "no named packer" but you suspect a shell (random section names / high entropy) -> have user run Exeinfo PE on that exact module. |
| Shell still unnamed after both | web search on **hard features** | via `ddgs` (below) | Extract features -- **section names** (`.sp0/.5w44`), **signature strings** (`SPBegin/SPEnd/SProtectSDK`), exports, sibling driver files -- search each *verbatim*, cross-confirm from >=2 sources. **NEVER pin shell identity on a single clue** (real miss: guessed "深盾Virbox" from `sprotect.sys` name alone; was Safengine/SProtect). |
| **★ Web search library (Rule 29 -- ONLY sanctioned search channel)** | **ddgs** | `pip install ddgs` (renamed from `duckduckgo_search`; no API key, multi-engine) | Mandatory for all web lookups. Not installed -> STOP, tell user `pip install ddgs`, wait (Rule 5). Banned: built-in `web_search`, curl/PS scraping engines. CLI `ddgs text -q "..." -m N`; API `from ddgs import DDGS; DDGS().text("...", max_results=N)`. Overseas via ddgs; 看雪/52pojie direct via curl.exe (Rule 2). |

> **★★ STRONG TECHNIQUE -- reflexively reach for this on a protected auth/license SDK DLL: UNPACK THE DLL (dump plaintext), don't fight it from outside.** When the packed layer is an SDK DLL (cloud-verify/license, e.g. `SPCloud64_Py.dll` = Safengine + NetLicensor), the single most powerful move is to get its **decrypted plaintext** and then read it (IDA on the DUMP only -- Rule 30). Proven path (real success): write a tiny `loader.exe` that `LoadLibrary`s the DLL -> run under **x64dbg + ScyllaHide** (exact ScyllaHide config: `hard-target-playbook.md` Sec.2.1 SE block + `case-studies.md`) which suppresses the shell's anti-debug so the process survives -> the DLL self-decrypts in memory (disk 4.7MB -> memory 9.7MB) -> break on `kernel32.Sleep` (a loop always hits) -> `dump_module` (rebuild PE + fix IAT). Now you have plaintext to analyze. This beats: grinding IDA on the packed file (Rule 30 forbids), fighting anti-debug forever, or reverse-guessing server data. **Do NOT default to Intel Pin/UnSafengine64 for this** -- version代差 makes it crash (Pin 3.31 vs the tool's 3.18); ScyllaHide+x64dbg dump is the reliable route.

---

## 0.95. Web Search SOP (operational -- Rule 29 + Rule 2 + Rule 3)

Follow in order for any web lookup during RE:

1. **Confirm `ddgs` importable** (`python -c "import ddgs"`). Not installed → STOP, tell user `pip install ddgs`, wait (Rule 29/5). **Never** fall back to the built-in `web_search` tool or curl/PS scraping of Google/Bing/DDG HTML.
2. **Route by destination (Rule 2)**: overseas (GitHub / tool repos / shell-unpack techniques / English) → `ddgs` (goes through the system proxy). Domestic CN forums (看雪 `bbs.kanxue.com`, 吾爱 `52pojie.cn`) → **`curl.exe` direct, NOT proxy** (they TLS-fail through an overseas proxy exit; ddgs may also miss CN forum content -- hit them directly).
3. **★ SEARCH THE SHELL'S NAME, NOT THE VERIFICATION SYSTEM'S NAME** (real miss this session): to find unpack/anti-debug techniques, search the **packer/protector identity** (`Safengine`, `SProtect`, `VMProtect`, `Themida`) -- NOT the license/verify SDK's name (`SPCloud`, `卡密`, `NetLicensor`, `网络验证`, the product name). Searching the verify-SDK name returns vendor marketing for auth systems, never unpacking know-how. Same as Rule 3's "search the packer, never 'crack this software'" -- and the verify-SDK/卡密 name is exactly that banned "software name" in disguise.
4. **Keyword templates + specificity ladder** (the difference between finding the exact writeup vs generic noise -- real weakness this session):
   - Templates: `<shell> <version> 脱壳/反调试/绕过`, `<shell> unpack OEP dump`, `<shell> ScyllaHide 配置`, `<tool> <dependency version> crash/不兼容`, `<verbatim error text>`. Unnamed shell: search section names (`.sp0`) / signature strings (`SPBegin`) *verbatim*.
   - **Worked example -- BAD (too generic, returns marketing/tutorials):** `换脸软件 破解` / `python 网络验证 破解` / `SPCloud 绕过`. **GOOD (specific, finds the actual technique):** `Safengine Shielden 2.3 脱壳 ScyllaHide` / `Safengine SProtect .sp0 dump OEP` / `UnSafengine64 Pin 3.31 crash` / the verbatim error `RECEIVED_ACCESS_FAULT Pin Safengine` / `PyArmor 9.2 static unpack`. **Ladder: start most-specific (exact shell+version+tool / verbatim error/signature string), only widen if empty.** A generic query is a wasted round; every token you add that's *specific to this target* (version, section name, error text, tool+version) sharpens it.
   - **Also mine the RESULT LIST itself, not just page bodies**: ddgs returns titles+URLs -- a 看雪/吾爱 thread title like "Safengine Shielden 2.3.8.0 脱壳" or a GitHub repo name is often enough to (a) confirm the approach exists and (b) hand the user that exact URL (see step 7). You don't always need the body.
5. **Cross-confirm from ≥2 sources** before pinning shell identity or committing to a technique -- one hit is a lead, not a conclusion.
6. **Usage**: CLI `ddgs text -q "<query>" -m <N>`; API `from ddgs import DDGS; DDGS().text("<query>", max_results=N)`. Unsatisfying results → rephrase / let ddgs's multi-engine rotate / hit CN forums via curl -- never revert to the banned channels (Rule 29).
7. **★ [IRON] Content fetch blocked by anti-scraping/JS/enterprise-policy = STOP and hand the user the URL to open/download; do NOT keep fighting the scrape.** Real time-sink this session: 看雪/CSDN/知乎/MDPI page bodies came back empty or WebFetch was refused ("cannot verify domain"/enterprise policy), and rounds were burned retrying curl with UA/gzip/iconv variations. **The moment a specific page won't yield its content after ONE normal attempt, stop: give the user the exact URL(s) (from the ddgs result list) and ask them to open/download it and paste the text or save it to a file you can read.** This mirrors the GUI/tool hard-stop -- the manual fetch is the user's step. `ddgs` search (result titles/URLs) still works and is not "scraping"; this rule is about fetching a *specific page's body* that's protected. Never let an anti-scrape wall stall the flow -- convert it into a one-line handoff.

---

## 1. Unpacking / devirtualization (Stage 1 when packed, or before Stage 4 static)

| Scenario | Tool | Repo | Install | star |
|---|---|---|---|---|
| **Themida/WinLicense 2.x-3.x** dynamic unpack + IAT repair | unlicense | `ergrelet/unlicense` | `pip install git+https://github.com/ergrelet/unlicense.git` or release exe (not on PyPI; 32-bit target needs 32-bit Python) | 1429 |
| Themida alternative (GUI) | Magicmida | `Hendi48/Magicmida` | release exe | 683 |
| Themida 3.x unpack+devirt (WIP) | bobalkkagi | `bobalkkagi/bobalkkagi` | clone + Python | 207 |
| **VMProtect x64 3.x static devirt** | NoVmp | `can1357/NoVmp` | clone + VS build (needs VTIL) | 2166 |
| VMProtect symbolic-exec devirt (pure functions) | Triton-VMP | `JonathanSalwan/VMProtect-devirtualization` | clone + Triton | 1473 |
| VMProtect 1.x-3.x static unpack + PE rebuild | VMPStatic | `notsnakesilent/VMPStatic` | clone + Python | 82 |
| VMProtect 3.0-3.5 lift to LLVM | MogVMP | `eversinc33/MogVMP` | clone (needs Remill) | 306 |
| VMProtect generic devirt | titan | `archercreat/titan` | clone + build | 146 |
| **Generic dynamic unpack** (dump after run) | mal_unpack | `hasherezade/mal_unpack` | release/clone | 828 |
| Intel Pin dynamic unpack | pin_n_sieve | `hasherezade/pin_n_sieve` | clone + Pin | 63 |
| Simple packers (UPX/ASPack) one-click | SimpleUnpacker | `Cr4sh/SimpleUnpacker` | release | 32 |
| **UPX** direct unpack | upx | `upx/upx` | `winget install upx`; `upx -d target` | (canonical) |
| **Enigma Virtual Box** unpack | evbunpack | `mos9527/evbunpack` | `pip install evbunpack`; `evbunpack target.exe out/` ([WARN] archived repo, still had pushes as of 2025-11) | 334 |
| **ASProtect** unpack (specific versions) | ASpirin | `Hendi48/ASpirin` | release (README says narrow target range; stop if version mismatches, per playbook Sec.4) | 22 |
| **Safengine Shielden** (common Chinese VM packer) | UnSafengine64 | `holycall/UnSafengine64` (upstream) / `sctnightcore/UnSafengine64` (fork) | `-Release holycall/UnSafengine64`; Intel-Pin-based dynamic unpack | 26/31 |
| **Steam DRM (SteamStub)** unpack | Steamless | `atom0s/Steamless` | `-Release atom0s/Steamless -Asset zip` | 4939 |
| **IAT rebuild** after unpacking | Scylla | `NtQuery/Scylla` | `-Release NtQuery/Scylla -Asset rar` (latest is `.rar` not `.zip`; or use the plugin bundled with x64dbg) | (canonical) |
| Runtime dump / implant detection | pe-sieve | `hasherezade/pe-sieve` | release exe | (canonical) |

**Tigress obfuscation** (source-level, not a packer): `JonathanSalwan/Tigress_protection` (910) -- deobfuscates via symbolic execution + taint analysis + LLVM.

**[WARN] No FOSS dedicated unpacker exists for**: Obsidium, Enigma Protector (!= Enigma Virtual Box), PELock, ACProtect, Armadillo, ExeCryptor (confirmed via actual searches -- don't waste time). Fall back to generic dynamic unpacking: `find-oep` -> dump -> Scylla IAT fix; or `mal_unpack`/`pe-sieve` runtime dump; for virtualized portions, hook boundaries per L3 rather than force-unpack. If that also stalls, tell the user honestly per playbook Sec.4 -- don't fabricate a tool name.

---

## 2. Anti-debug / anti-anti-debug (Stage 4B when dynamic analysis is blocked)

| Scenario | Tool | Repo | Install | star |
|---|---|---|---|---|
| **One-shot usermode hiding** (IsDebuggerPresent/PEB/NtQuery...) | ScyllaHide | `x64dbg/ScyllaHide` | release, x64dbg/IDA plugin | 4245 |
| **Hypervisor-level anti-anti-debug** | HyperHide | `Air14/HyperHide` | release + driver, x64dbg plugin | 1639 |
| Anti-debug technique checklist (learning) | AntiDBG | `HackOvert/AntiDBG` | reference code for self-testing | 817 |
| Anti-debug bypass practice targets | GH_AntiDebug_Bypass | `guidedhacking/*` | see hard-target-playbook Sec.2 | (canonical) |
| **QEMU-level VM hiding** (Themida/VMProtect/Enigma/Safengine anti-VM checks) | qemu-anti-detection | `zhaodice/qemu-anti-detection` | apply a QEMU patch to alter VM fingerprint | 1611 |

> For specific API-hook bypass (Frida scripts) see `references/frida-win/references/anti-debug-bypass.md` + `anti-debug-db/`. For anti-VM, prefer a physical machine (playbook Sec.2.3) over hardening the VM.

---

## 3. Junk code / control-flow obfuscation / forged call stacks

**Core insight**: junk code + forged call stacks (`push fake-retaddr; jmp` instead of `call`) breaks static disassembly and `step_out` stack-walking (Rule 14). Only in-process instruction-level tracing handles this, not manual single-stepping.

| Scenario | Tool/Technique | Location | Notes |
|---|---|---|---|
| **In-process instruction tracing** (immune to junk code/forged stacks) | **Frida Stalker** | built into Frida, docs at `references/frida-win/references/frida-docs/stalker.md` | records every executed instruction/basic block, follows EB/E9 jumps automatically, zero MCP round-trips. First choice on Windows |
| Stalker usage reference (OLLVM/junk-code) | frida_stalker | `CYRUS-STUDIO/frida_stalker` | 98*; ARM/Android-oriented, borrow ideas only, needs porting for Windows |
| Instruction-trace stack reference | GumTrace / stalker_trace_so | `lidongyooo/GumTrace` / `oacia/stalker_trace_so` | both ARM/Android-oriented, architecture reference only |
| Static de-obfuscation pre-pass in IDA | ida-re scripts | `references/ida-re/scripts/` (stackstring_recover.py etc.) | run before deep analysis |
| x64dbg-side tracing | tracealyzer | `references/x64dbg/tracealyzer/` | confirm the tool actually exists per its SKILL.md step 0; fall back to Frida Stalker if no batch trace |

> For Windows junk code go straight to Frida Stalker; the Android tools above are idea references, not directly runnable against an exe.

---

## 3.5 Symbolic-execution auto-solving of local validation/keygen

**Purpose**: for a purely computational local check (input key -> transform -> compare) with no heavy anti-debug/network dependency, symbolic execution auto-derives a passing input -- an automatic keygen, faster than manual reversal.

| Scenario | Tool | Source | Install | Notes |
|---|---|---|---|---|
| Symbolic exec to solve flag/serial validation | angr | `angr/angr` (PyPI) | `pip install angr` | set `find`=success address, `avoid`=failure address; present the install command, user installs |

> Boundary: works best for pure computation. Networking/syscalls/heavy virtualization cause state explosion -- fall back to x64dbg/Frida black-box (4B.A/B). `angr.Project(exe)` works directly on a Windows PE.

---

## 4. Encryption/signature algorithm identification & recovery

**Workflow**: identify the algorithm -> find a correct third-party library implementation (Rule 3, not a crack) -> decrypt the captured ciphertext with the library -> understand the protocol -> forge legitimate requests/responses per the algorithm (cheatsheet 4b).

| Scenario | Tool/Library | Source | Install | star |
|---|---|---|---|---|
| **Identify crypto constants** (AES S-box/SHA/MD5/Base64) | findcrypt-yara | `polymorf/findcrypt-yara` | IDA plugin | 1731 |
| In-IDA constant scanning (built-in) | crypto_const_scan.py | `references/ida-re/scripts/crypto_const_scan.py` | run via py_eval | -- |
| **Python algorithm implementations** (decrypt/verify yourself) | PyCryptodome | `pycryptodome` (PyPI) | `pip install pycryptodome` | (canonical) |
| Interactive decrypt/encode trial | CyberChef | `gchq/CyberChef` | web version or offline release | (canonical) |
| Curve/big-number/RSA attacks | SageMath / pycryptodome | -- | as needed | (canonical) |
| **Auto-identify crypto/capabilities** (API/behavior rules, not just constants) | capa | `mandiant/capa` | `-Pip capa` or `-Release mandiant/capa` | matches rules for capabilities like "uses AES/RC4/HTTP/anti-debug"; run first to locate where encryption happens |

### Dynamic hooking to locate native C/C++ encryption (when static ID fails -- RC4/custom/no signature)

**Insight**: findcrypt/capa rely on constants/rules and miss RC4, home-grown algorithms, or feature-less implementations. Hooking the encryption function's entry/exit to capture plaintext is faster than grinding static reversal -- the primary approach for native targets (Stage 4B).

| Scenario | Technique | Location/Tool | Notes |
|---|---|---|---|
| **Hook Windows CryptoAPI/CNG** | Frida hook `CryptEncrypt`/`CryptDecrypt`/`BCryptEncrypt`/`BCryptDecrypt` | `references/frida-win/`; `Interceptor.attach` | dump plaintext at entry, ciphertext at exit -- key/IV often in the parameters too |
| **Hook OpenSSL/mbedTLS** (statically linked) | Frida hook `EVP_EncryptUpdate`/`EVP_DecryptUpdate`/`AES_encrypt` | same as above | no export name when static-linked -- ID via AES/SHA round constants (findcrypt) first, then hook that address |
| **Hook custom/home-grown algorithms** | locate the buffer-processing function, hook its entry/exit | Frida `Interceptor` + 4B black-box | don't reverse the algorithm -- capture at the plaintext<->ciphertext boundary, cross-reference against traffic |
| Frida hook reference / memory dump | fridump / brida | `Nightbringer21/fridump`, `federicodotta/brida` | fridump dumps process memory for residual plaintext/keys; brida wires Frida into Burp |

> Once a specific algorithm is identified (`ChaCha20`, `SM4`), search "python/rust library for this algorithm" per Rule 3 -- not a crack. RC4 and other constant-signature-less algorithms rely on dynamic hooking above, not static recognition.

---

## 4.5 Traffic capture forwarding / forced proxying (target ignores the system proxy)

**Scenario**: Stage 2's app-filtered capture shows no new records, and `env-recon.md` Sec.1-Addendum confirms "app ignores the system proxy but is still HTTP(S)." Recoverable by force-forwarding the target's outbound TCP to Reqable.

| Tool | Purpose | Form | Notes |
|---|---|---|---|
| **Proxifier** (commercial) | Force per-app TCP through a designated proxy | official-site trial/paid, not GitHub, manual install | route the target's outbound traffic to `127.0.0.1:<Reqable port>` (HTTP); Reqable chains its own upstream. Primary fix for this scenario |
| ProxyCap / SocksCap64 | Similar forced-forwarding alternative | official-site, not GitHub | fallback when Proxifier unavailable |
| **Reqable's built-in forced proxy** ([WARN] unverified) | might replace Proxifier if it exists | inside Reqable UI | docs were WAF-blocked this session, feature name/port unconfirmed -- check the UI directly, don't assert a menu name from memory |

> **Not applicable here**: TLS pinning -> bypass with Frida first, then return to the proxy; raw sockets with custom binary protocols -> Reqable can't decode raw TCP, use in-process hooking (Sec.4 + Stage 4B); loopback (127.0.0.1) -> nothing intercepts this, switch to a local technique (Stage 4).

---

## 5. .NET-specific targets (diec reports .NET)

The x86 toolchain (IDA/x64dbg) doesn't apply -- switch to the .NET-specific chain:

| Scenario | Tool | Repo | Install | star |
|---|---|---|---|---|
| **General .NET deobfuscation** | de4dot-cex | `ViRb3/de4dot-cex` | release exe | 574 |
| Deobfuscator index/collection | .NET-Deobfuscator | `NotPrab/.NET-Deobfuscator` | pick per packer | 1508 |
| **.NET Reactor** dedicated unpack | NETReactorSlayer | `SychicBoy/NETReactorSlayer` | release | 1247 |
| .NET-version VMProtect dump | VMUnprotect.Dumper | `void-stack/VMUnprotect.Dumper` | clone + build | 454 |
| **Decompile for source reading** | dnSpyEx / ILSpy | `dnSpyEx/dnSpy` / `icsharpcode/ILSpy` | release | (canonical) |
| PyArmor 8 output decrypt | pyarmor-8-decrypt | `vxnetrip/pyarmor-8-decrypt` | clone + Python (Python targets only) | 37 |

---

## 5.5 Interpreter-packaged targets (diec reports PyInstaller/Nuitka/py2exe/cx_Freeze)

A high-entropy overlay carrying `pythonXX.dll` means a Python program, not native C/C++ -- IDA/x64dbg don't apply. Follow unpack->decompile-bytecode->read-source (Rule 15, Stage 1).

> **Rule 3 applies**: pick the decompiler matching the target's exact Python bytecode version -- don't settle for whatever's local. Pin the version first (pyc magic / `python3XX.dll`), match against the table below. Confirm aliveness with `-Probe`, then present the tool + install command to the user (they install).

| Scenario | Tool | Source | Install | star |
|---|---|---|---|---|
| **PyInstaller unpack** (newer, stable, first choice) | pyinstxtractor-ng | PyPI | `pip install pyinstxtractor-ng`; `pyinstxtractor-ng target.exe` (optional `pycryptodome` decrypts the PYZ) | (canonical) |
| PyInstaller unpack (classic, fallback) | pyinstxtractor | `extremecoders-re/pyinstxtractor` | single-file script, `python pyinstxtractor.py target.exe` | (canonical) |
| **pyc decompile** (older Python <=3.8) | uncompyle6 / decompyle3 | `rocky/python-uncompyle6` / `rocky/python-decompile3` | `pip install uncompyle6` | (canonical) |
| pyc decompile (newer, C++ impl) | pycdc (Decompyle++) | `zrax/pycdc` | clone + cmake build; `pycdc target.pyc` | (canonical) |
| **Fallback when decompilers haven't caught up** (3.12/3.13/3.14) | official embeddable Python + `marshal`+`dis` | python.org (exact-matching version) | see fallback steps below | -- |
| **Nuitka (native, symbol/constant recovery not bytecode)** | see Sec.5.6 | -- | go straight to `references/playbooks/nuitka.md` -- no bytecode exists | -- |
| Electron (`.asar`) unpack | asar / npx asar | `electron/asar` | `npx @electron/asar extract app.asar out/` | (canonical) |
| **mypyc/Cython .pyd/.so** | -- (black-box) | -- | already native machine code -- vary inputs/state and observe outputs, or Frida-hook exports (Rule 15) | -- |

**Fallback steps** (verified on Py3.14):
1. Read the pyc header's 4-byte magic, or check `python3XX.dll` in the unpacked dir, to pin the version.
2. Download the matching embeddable Python.
3. `import marshal,dis; code=marshal.loads(open('x.pyc','rb').read()[16:]); dis.dis(code)` (16-byte pyc header for 3.7+, 8/12 for older).
4. `LOAD_CONST`/`LOAD_GLOBAL`/`LOAD_ATTR`/`CALL`/jumps are enough to read auth logic; constants often reveal URLs, field names, `'permanent'`/`'expired'` strings directly.

---

## 5.6 Nuitka-specific chain (native compilation, not bytecode)

> Nuitka compiles Python into native C -> machine code, no bytecode to decompile. Full mechanism/workflow in **`references/playbooks/nuitka.md`**; this section just registers tools. Confirm aliveness with `-Probe`, then present the tool + source to the user (they install).

| Scenario | Tool | Repo | Capability ([DOC] via README, mostly untested here) | star |
|---|---|---|---|---|
| **Unpack onefile** (extract embedded DLL/RCDATA/`__main__`) | nuitka-extractor | `extremecoders-re/nuitka-extractor` | extracts binary resources, does not decompile | 238 |
| **[TARGET] Static anchor recovery** (IDAPython, first choice) | nuitka-helper | `Siradankullanici/nuitka-helper` | Library/User Code Recovery + Constants Recovery + `nuitka.h` structs + FLIRT -- breaks the string-xref dead end | (canonical) |
| **Decode constant blob -> IDA rename script** | Nuitka-Dumper | `4equest/Nuitka-Dumper` | generates `rename___main__.py` naming constants and reference points | (canonical) |
| **Dynamic injection hook** (anti-injection risk) | nuitka-injector | `crackalove/nuitka-injector` | injects DLL + Python API init, 12 payloads (HTTP Spy/MITM/dump globals) | 15 |
| Python call logging (args/returns) | pymodhook | `ekcbw/pymodhook` | `pip install pymodhook`, must run in the target's Python context | 120 |
| **Nuitka+Themida/VMP combo**, unpack outer layer | nuitka-themida-unpacker | `DimaReverse/nuitka-themida-unpacker` | handles the combo, then back to nuitka-extractor | 16 |
| Alternative for combo packers | DeNuitkanizator | `2M12/DeNuitkanizator` | Nuitka unpacking/processing | 16 |
| Automated pipeline reference | AutoNuitkaDecompiler | `HydraDragonAntivirus/AutoNuitkaDecompiler` | IDA Pro 9.1 + `stage1idapro.py`, inspired by nuitka-helper | 56 |

**Key point**: prefer static (nuitka-helper + Nuitka-Dumper, fully offline, zero injection) for anti-injection targets -- dynamic injection hits anti-injection defenses (playbook Sec.2.3/5.2). Unpack an outer packer layer first if present.

---

## 5.7 Natively-compiled runtime chains (Go/Rust/Flutter/.NET-AOT/Java/Unity)

> These are either natively compiled (no bytecode) or use managed bytecode needing specialized tools -- Sec.5.5's "unpack->decompile" doesn't apply (Rule 15). Misclassifying sends the whole analysis the wrong way -- **Go especially**: rich symbols, but recovered via moduledata, not bytecode decompiling. Tools below are public/untested here -- confirm aliveness with `-Probe`, then present the tool + source to the user (they install).

### 5.7.1 Go (native, symbols via pclntab/moduledata)
Indicators: diec reports Go / `Go build ID:` string / `.gopclntab` section / few imports + large binary / `runtime.`/`main.` panic strings.
| Scenario | Tool | Repo | Notes |
|---|---|---|---|
| **Recover Go names/types in IDA** (first choice) | IDAGolangHelper | `sibears/IDAGolangHelper` | parses pclntab/moduledata, batch-recovers function names |
| Go symbol/string/type recovery | go_parser | `0xjiayu/go_parser` | IDAPython, fairly comprehensive |
| Go analysis on Ghidra | GolangAnalyzerExtension | `mooncat-greenpy/Ghidra_GolangAnalyzerExtension` | for Ghidra users |
| Version/build info | `go version -m target.exe` | official Go toolchain | reads Go version + modules, no reversing needed |

**Key point**: native reverse engineering once symbols are recovered -- don't look for bytecode. Struct recovery helps with interface/slice/map types.

### 5.7.2 Rust (native, often stripped)
Indicators: `rustc`/`cargo`/`.rs` path strings, panic strings (`called 'Option::unwrap()'`), mangled symbols (`_ZN...`).
| Scenario | Tool | Source | Notes |
|---|---|---|---|
| Symbol demangling | rustfilt / IDA's demangler | `rust-lang/rustc-demangle` | restores `_ZN4core...` to readable paths |
| Locating logic via panic strings | (technique) | -- | primary approach once stripped -- reverse-lookup from panic/assert strings |
| Folding known crates | FLIRT/Lumina | (canonical) | folds the stdlib/common crates so you focus on author code |

**Key point**: stripped Rust has no metadata system (unlike IL2CPP/Unreal) -- panic strings + constants are the main approach, not symbol-recovery tools.
**[WARN] Fork before you open IDA**: a Rust exe with a same-dir `WebView2Loader.dll`/`EmbeddedBrowserWebView.dll` (or `%LOCALAPPDATA%\<appid>\EBWebView`) is **almost certainly a Tauri app -- its UI + most auth logic are JavaScript in a WebView, not in this binary**. Go `playbooks/tauri-webview.md` (CDP front-end) FIRST; the panic-string native route below is for a genuinely headless/CLI Rust binary or the escalation after the JS layer proves the verdict is computed native-side. This is the single biggest time-sink the post-mortem flagged.

### 5.7.3 Flutter (Dart AOT snapshot inside libapp.so)
Indicators: `libapp.so` + `libflutter.so` / `flutter` strings / Dart snapshot magic.
| Scenario | Tool | Repo | Notes |
|---|---|---|---|
| **Reverse the Dart AOT snapshot** | blutter | `worawit/blutter` | parses `libapp.so`, recovers Dart classes/functions, produces an IDA script; strongly version-dependent |
| Dart snapshot structure reference | Doldecomp / darter-type tools | search "dart snapshot parser" | fallback when blutter's version doesn't match |

**Key point**: business logic lives in Dart inside `libapp.so`, not the native glue layer -- find the matching fork if blutter's version mismatches.

### 5.7.4 .NET NativeAOT (native, no IL)
Indicators: diec may say .NET but dnSpy can't open it / no IL metadata / single-file native exe / `S_P_CoreLib` string.
| Scenario | Tool | Notes |
|---|---|---|
| Recover NativeAOT type/method names | Il2CppDumper-style / bybt-type scripts | search "NativeAOT reversing" -- retained metadata (for reflection) can be parsed |
| Treat as native RE | IDA + methodology.md | AOT is just native machine code -- Sec.5's de4dot/dnSpy don't apply |

**Key point**: NativeAOT != regular .NET -- regular .NET goes through Sec.5's IL deobfuscation, NativeAOT goes native. Don't force dnSpy to open it.

### 5.7.5 Java/JVM (bytecode, decompiles)
Indicators: `.jar`/`.class`/`jvm.dll`/`java` launcher/exe4j-launch4j wrapping.
| Scenario | Tool | Repo | Notes |
|---|---|---|---|
| **Decompile jar/class -- MCP connected (first choice)** | **jadx MCP** (`mcp__jadx__*`) | `skylot/jadx` (jadx-gui + MCP plugin) | **Prefer whenever `mcp__jadx__*` is in the tool list (Rule 1).** Interactive, no full-dump-to-disk: `search_classes_by_keyword` jumps to auth classes (`license`/`verify`/`expired`); **`get_xrefs_to_method` pulls the call chain** -- directly serves Rule 4 (code-exists != running); `get_method_by_name`/`get_class_source`/`rename_*` to read+mark in place. **User opens jadx-gui + loads the target manually (Rule 8), then you confirm the MCP methods are live.** |
| Decompile jar/class -- no MCP | jadx (GUI+CLI) | `skylot/jadx` | same engine, CLI/GUI only; near-source Java directly. Use when MCP not connected. |
| Decompiler alternatives | CFR / Procyon | `leibnitz27/cfr` / `procyon` | switch when jadx stalls, handle different obfuscation |
| Java deobfuscation (name/string encryption) | deobfuscator | `java-deobfuscator/deobfuscator` | targets Zelix/Allatori-style obfuscators |
| Extract jar from exe wrapper | zip/resource extraction | -- | extract first, then decompile |

**Key point**: bytecode decompiles close to source -- the main difficulty is Java-specific obfuscators, preprocess with deobfuscator.
**[WARN] jadx MCP is Android-oriented, desktop-jar smoothness not empirically verified here**: the connected MCP's toolset leans Android (`get_android_manifest`/`get_main_activity_class`/`get_smali_of_class`/resource APIs). jadx's engine *does* decompile plain `.jar`/`.class` (exe4j/launch4j-wrapped desktop Java is the target form here, not APK), but how cleanly *this MCP implementation* drives a desktop jar was not tested -- if a class/xref query misbehaves on a desktop jar, fall back to jadx CLI / CFR / Procyon (the row above), and log it. This mirrors the skill's existing MCP-first posture (IDA/x64dbg/Reqable MCP) -- Java was simply the one type with an available MCP not yet written in.

### 5.7.6 Unity IL2CPP / Unreal
> Game targets: see `references/ida-re/references/game_re.md` (more thorough); non-game Unity/Unreal apps also go through this section.
| Scenario | Tool | Repo | Notes |
|---|---|---|---|
| **Recover C# types from IL2CPP** (first choice) | Il2CppDumper / Il2CppInspector | `Perfare/Il2CppDumper` / `djkaty/Il2CppInspector` | `GameAssembly.dll`+`global-metadata.dat` -> all names + an IDA script |
| Unity Mono (managed dll) | dnSpyEx/ILSpy (Sec.5) | -- | Mono is regular .NET, decompile IL directly |
| Recover Unreal SDK | Dumper-7 | `Encryqed/Dumper-7` | locates GNames/GUObjectArray, dumps the SDK |

**Key point**: `global-metadata.dat` recovers near-source symbols; if encrypted, dump at runtime instead (see game_re).

### 5.7.7 Electron V8 snapshot (bytecode only, no JS source)
> Sec.5.5 covers extracting JS from `.asar`; this covers when only a V8 snapshot/bytecode ships, no JS source.
Indicators: `v8_context_snapshot.bin` / only `.jsc` bytecode / no readable JS in the asar.
| Scenario | Tool | Repo | Notes | star |
|---|---|---|---|---|
| Parsing the V8 snapshot | v8-snapshot parser | search "v8 snapshot parser" | extracts strings/structures | -- |
| **Compile/load `.jsc`** | bytenode | `bytenode/bytenode` | `npm install bytenode`; `require('bytenode')` then `require('x.jsc')` | 2965 |
| **Static disasm/decompile `.jsc`** (Ghidra plugin) | ghidra_nodejs | `PositiveTechnologies/ghidra_nodejs` | [WARN] untested here -- runtime string decryption may still block readability | 385 |
| Fallback when static analysis fails | runtime hooking | see Sec.5.8 | hook `Module._compile`/`require` in the main process to dump loaded JS, or use the Sec.5.8 offline harness | -- |

**Key point**: V8 bytecode decompiling is far less mature than pyc -- if ghidra_nodejs fails, switch to runtime hooking/offline harness, faster than grinding static analysis.

### 5.7.8 WebView2 / CEF hybrid (Tauri/Wails/CEF/plain-WebView2) -- CDP front-end + native-stack plaintext
> Full flow in `playbooks/tauri-webview.md`. This is the tool/recipe index. **Logic is JS in an embedded browser -> CDP is the primary channel, not IDA.** ID: same-dir `WebView2Loader.dll`/`EmbeddedBrowserWebView.dll` (Tauri/Wails/.NET-WebView2) or `libcef.dll`+`cef.pak`+`icudtl.dat` (CEF).

| Scenario | Tool | Source | Notes |
|---|---|---|---|
| **Open the CDP port** | env `WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--remote-debugging-port=9222` (Tauri/Wails/WebView2); `--remote-debugging-port=9222` launch switch (Electron renderer / CEF); `--inspect=9223` (Electron main) | Chromium/WebView2 built-in | user sets + relaunches (Rule 8); no binary patch. Works even when release-build right-click devtools is disabled |
| **Connect + drive CDP** | chrome-remote-interface (npm) / pychrome (py) / Playwright-Puppeteer `connectOverCDP` | `cyrus-and/chrome-remote-interface` / `fate0/pychrome` | list `http://127.0.0.1:9222/json`; **no Frida/native injection needed** |
| **Inject before app scripts** (document-start) | CDP `Page.addScriptToEvaluateOnNewDocument` + `Page.reload` | (protocol) | fixes the "app cached the original fn -> post-load hook missed" bug; install fetch+IPC+store hooks here |
| **Front-end HTTP plaintext** | hook `window.fetch`/`XMLHttpRequest` in the injected script | -- | catches auth calls the JS makes directly, pre-TLS |
| **IPC boundary plaintext** (backend does the networking) | wrap `__TAURI_INTERNALS__.invoke` (Tauri v2) / `__TAURI__.invoke` (v1) / `window.go.*` (Wails) / `ipcRenderer` (Electron) | -- | **plaintext args+return even when Rust `reqwest`/rustls does the TLS** -- first choice for reqwest/rustls targets, beats hooking rustls |
| **Read/flip front-end state** | CDP `Runtime.evaluate` on Vue (`#app.__vue_app__`/Pinia)/React fiber/Vuex + localStorage/sessionStorage/IndexedDB | -- | flip `isVip`/expiry live, verify bypass on the spot = `[OK]` |
| **rustls/reqwest below the IPC** (only if IPC hook insufficient) | SSLKEYLOGFILE (renderer TLS only; rustls usually **not**, verify -- Rule 4) / memory-marker scan / Frida on rustls send-recv | -- | IPC-boundary hook first; these are fallbacks, marker-scan is the harder path |

**Key point**: for this whole class the win is a live JS value-flip after one login, reached via CDP -- not native RE. reqwest/rustls's proxy-immune stack is a non-issue because the **IPC boundary carries the plaintext** above the native TLS.

---

## 5.8 Electron-as-Node offline harness

> **Purpose**: against main-process anti-injection (asar integrity fuse, `--inspect` crash, single-instance-lock kicks the injected process), load the target's own `.jsc`/JS modules decoupled from the real GUI via `ELECTRON_RUN_AS_NODE=1` -- the concrete tooling for Rule 23's "Electron-as-Node offline invocation" tier. Target-specific bits (ee-core's `EE_*` vars, `path.join` patching, jsencrypt public-key autofill) still need hand-writing; for the two generic parts below, prefer these libraries over hand-writing (hand-written versions were the main time sink -- recursion bugs, axios-incompatible mocks):

| Scenario | Library | Repo | Install | star | Replaces |
|---|---|---|---|---|---|
| **Intercept `require('electron')` -> stub** | proxyquire | `thlorenz/proxyquire` | `npm install --save-dev proxyquire` | 2747 | hand-written `Module._load` patch + Proxy stub |
| **Intercept/fake HTTP(S) responses** | nock | `nock/nock` (first choice, axios-compatible) | `npm install --save-dev nock` | 13118 | hand-written `http.request` redirect closure (recursion-prone) + mock `http.createServer` |

**Usage**: `proxyquire('./controller/user.jsc', { electron: fakeElectronStub })` replaces dozens of lines of `Module._load` patching in one line. `nock('http://target-host').post('/v2/login').reply(200, forgedBody)` intercepts axios requests directly, avoiding hand-mock errors like `Cannot read properties of undefined`. Both apply only inside the offline harness process, not the real GUI; loop multiple `nock().reply()` assertions in one script to test candidate keys/formats in one pass (Rule 25).

---

## 5.9 Other runtimes: Delphi / AutoIt / VB6 / Nim

> Triggered when `triage-router.md Sec.1` classifies the target as one of these -- real commercial software commonly uses them but they get mistaken for "an ordinary native exe." Everything here is community/untested except where noted -- confirm with `-Probe`/`-Release`, then present the tool + source/link to the user (they download/install).

### 5.9.1 Delphi/C++Builder (native, form/events/VMT rebuildable)
Indicators: diec reports Delphi/Borland; `Borland`/`Embarcadero`/`Delphi` strings; VCL class names (`TForm`/`TButton`).
| Scenario | Tool | Repo | Install | Notes |
|---|---|---|---|---|
| **Rebuild Delphi symbols/forms/events** (first choice) | IDR (Interactive Delphi Reconstructor) | `crypto2011/IDR` | `-Release crypto2011/IDR` | recovers VMTs/event handlers/string refs; pick the kb library by Delphi version |
| Delphi assistance in IDA | IDA's built-in tools + Delphi FLIRT | (canonical) | -- | folds VCL library functions |

**Key point**: native RE, but event-driven model + VCL makes raw reversal painful -- rebuild forms/events with IDR first.

### 5.9.2 AutoIt (compiled, source extractable)
Indicators: diec reports AutoIt; `>AUTOIT SCRIPT<` / `AU3!EA` in resources/overlay.
| Scenario | Tool | Source | Install | Notes |
|---|---|---|---|---|
| **Extract AutoIt source** (first choice) | autoit-ripper | `nazywam/AutoIt-Ripper` (PyPI) | `-Pip autoit-ripper` | extracts .au3 back out; supports AutoIt 3.26+ |
| Older/GUI extraction | Exe2Aut | `exe2aut.com` (not GitHub) | manual | fallback when autoit-ripper fails on an older version |

**Key point**: extracts back to near-source, the easiest of this group -- try autoit-ripper first.

### 5.9.3 VB6
Indicators: diec reports Visual Basic; depends on `MSVBVM60.dll`; `VB5!` header.
| Scenario | Tool | Source | Notes |
|---|---|---|---|
| P-code decompile/native analysis | VB Decompiler (commercial) | `vb-decompiler.org` | no mature FOSS decompiler exists on GitHub -- rely on this (free Lite version available) for P-code; native-compiled VB6 goes through ordinary native RE |
| Native VB6 | IDA + methodology.md | -- | compiled to native code, no P-code, reverse as native C |

**Key point**: first distinguish P-code vs natively-compiled -- the open-source toolchain here is genuinely thin.

### 5.9.4 Nim
Indicators: diec reports Nim; `@m`-prefixed module symbols; `nimFrame`/`stdlib_` strings.
| Scenario | Technique | Notes |
|---|---|---|
| Treat as native C reversing (no dedicated tool) | IDA + methodology.md | no mature dedicated tool exists -- Nim compiles to C->machine code, no bytecode; locate logic via `nimFrame` calls, `@m<module>` prefixes, stdlib strings |

**Key point**: "looks like a script, is actually native" (triage [WARN]) -- just native RE plus naming via leftover symbols.

---

## 6. Learning resources

> When you hit an unfamiliar technique, check the methodology here before diving in.

- **Anti-debug encyclopedia**: `references/frida-win/references/anti-debug-db/` (bundled locally, Check Point Anti-Debug, MIT).
- **al-khaser**: `ayoubfaouzi/al-khaser` -- comprehensive anti-debug/anti-VM/anti-sandbox demo, see what the target might use.
- **HackTricks -- Reversing**: `book.hacktricks.xyz` -- general RE patterns.
- **unicorn-engine / Triton / miasm**: symbolic execution + emulation frameworks underlying automated deobfuscation/devirtualization.
- **VMProtect/Themida analysis collections**: the various devirtualizer repos' READMEs/issues are the most practical primary sources.
- **ida-re reading list**: `references/ida-re/references/reading_list.md`.

---

## 7. Connection points with the main workflow

| Stage | Look up |
|---|---|
| Stage 1, packed | Sec.1 -- pick an unpacker by packer type |
| Stage 4 pre-triage: junk code | Sec.3 -- Frida Stalker |
| Stage 4 pre-triage: encryption with constant signatures | Sec.4 -- capa/findcrypt then a third-party library |
| Stage 4B: encryption with no signature (RC4/custom) | end of Sec.4 -- dynamic hooking of native crypto |
| Stage 1, installer (Inno/NSIS/MSI) | `triage-router.md Sec.0.5` -- strip the installer first |
| Stage 1, Delphi/AutoIt/VB6/Nim | Sec.5.9 |
| **Stage 2, no capture records (ignores system proxy)** | **Sec.4.5 -- Proxifier forced-forward** (pinning: Frida first; raw sockets/loopback: switch to hooking) |
| Stage 4B blocked by anti-debug | Sec.2 -- ScyllaHide/HyperHide |
| Stage 1/4, .NET | Sec.5 |
| Stage 1, classify first | `references/triage-router.md` |
| **Stage 1, PyInstaller/py2exe (genuine bytecode)** | **Sec.5.5** |
| **Stage 1, Nuitka (native)** | **Sec.5.6 + `references/playbooks/nuitka.md`** |
| **Stage 1, Go/Rust/Flutter/.NET-AOT/Java/Unity** | **Sec.5.7** |
| **Stage 1, WebView2/CEF hybrid (Tauri/Wails/CEF), logic in renderer** | **Sec.5.7.8 + `playbooks/tauri-webview.md` (CDP first, not IDA)** |
| **Stage 4B, main-process anti-injection** | **Sec.5.8 -- proxyquire+nock, with `templates/electron-node-harness.js`** |
| Stage 4, need to reproduce the algorithm (CFF/VM) | `references/deobfuscation-playbook.md` |
| Unfamiliar technique | Sec.6 |

**Probe/locate tools via** `scripts/fetch-tool.ps1` (Sec.0), then present the tool + source to the user -- the user installs, you never auto-install.
