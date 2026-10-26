# Reverse Engineering Methodology (the deeper playbook)

How an experienced reverse engineer actually works a binary, beyond the core loop in SKILL.md.
Read the section you need; you don't have to read it all at once.

## Contents
- [Triage checklist](#triage-checklist)
- [Naming conventions](#naming-conventions)
- [Type and struct recovery](#type-and-struct-recovery)
- [Calling conventions cheat sheet](#calling-conventions-cheat-sheet)
- [Common code patterns](#common-code-patterns)
- [Platform notes](#platform-notes)
- [Static vs dynamic — when to switch](#static-vs-dynamic--when-to-switch)
- [Dynamic tactics — finding the variable when static is too slow](#dynamic-tactics--finding-the-variable-when-static-is-too-slow)
- [Documentation structure](#documentation-structure)

---

## Triage checklist

Before deep analysis, build a mental map. (`scripts/ida_triage.py` automates most of this.)

- **File facts:** format (PE/ELF/Mach-O/raw), architecture, bitness, endianness, image base, compiler/toolchain hints, entry point(s) and TLS callbacks.
- **Segments & entropy:** high-entropy (>~7.0) sections suggest packing/encryption/compression. A tiny `.text` with a huge high-entropy blob is a packer tell.
- **Imports:** what capabilities does the binary even have? Networking, crypto, process/thread manipulation, file/registry, service/persistence, debugging/anti-debugging. A binary with no networking imports probably isn't a C2 client (unless it resolves APIs dynamically — see patterns).
- **Exports:** for DLLs/shared objects, exports are your entry points into the interesting logic.
- **Strings:** URLs, IPs, domains, file paths, registry keys, mutex names, format strings, error messages, command-line flags, embedded scripts. Strings are the single fastest route to "what does this do."
- **Anti-analysis tells:** `IsDebuggerPresent`/`CheckRemoteDebuggerPresent`/`NtQueryInformationProcess`, timing checks (`GetTickCount`, `rdtsc`), `PEB.BeingDebugged` reads, exception-based tricks, suspiciously few imports (dynamic resolution), section names like `UPX0`.
- **Known code:** run FLIRT/Lumina to fold away the runtime and libraries so you focus on author code.

From the triage, pick your first targets: usually `main`/`WinMain`/`DllMain`, the code around the most interesting strings, and exported functions.

---

## Naming conventions

Consistent names make the database self-documenting and make later passes faster. Suggested scheme:

- **Functions:** `verb_noun`, purpose-first: `decrypt_config`, `resolve_imports`, `send_beacon`, `is_vm_present`. Prefix families: `crypt_*`, `net_*`, `anti_*`, `parse_*`. Use `sub_*` only for genuinely-unanalyzed code.
- **Globals:** `g_` prefix: `g_config`, `g_aes_key`, `g_socket`. Tables/arrays get plural or `_table`: `g_api_table`.
- **Locals:** semantic, short: `i`/`j`/`n` for indices/counts, `len`, `buf`, `key`, `ctx`, `hfile`, `pProc`. Loop bound becomes the thing it bounds (`num_entries`, not `v7`).
- **Structures:** `PascalCase` type names (`Config`, `BeaconPacket`); field names describe content (`magic`, `length`, `payload`, `next`). When you don't yet know a field, name it by offset (`field_10`) so the slot is reserved.
- **Constants/enums:** decode magic numbers into named enums (`enum MsgType { MSG_HELLO = 1, ... }`) and apply them; the decompiler will then show the symbol.

Rename as soon as you're reasonably sure — a slightly-wrong name you fix later beats `v14` forever. Re-decompiling after a batch of renames often reveals the next layer.

---

## Type and struct recovery

This is the highest-leverage skill and the thing LLM agents most often skip. Raw decompiler
output is full of `*(_DWORD *)(a1 + 0x10)` because IDA doesn't know the layout. Give it the
layout and the math collapses into readable field access everywhere at once.

**Technique:**
1. Spot a candidate object: a pointer that's repeatedly dereferenced at fixed offsets, or that's passed around together. `xrefs_to_field` and the access pattern reveal the offsets in use.
2. Infer field widths from the access size (`BYTE`/`WORD`/`DWORD`/`QWORD` in the pseudocode, or operand size in disasm). `scripts/struct_recovery.py` collects these and drafts a skeleton.
3. `declare_type` the struct (pad gaps you don't understand yet with `char fieldN[size];` or unknown fields).
4. `set_type` it onto the variable/argument as `MyStruct*`.
5. Re-decompile. `*(a1 + 0x10)` becomes `a1->length`. Iterate: the cleaner view often exposes more fields, nested structs, or function-pointer table entries.

**Function pointers & vtables:** C++ objects start with a vtable pointer; recover the vtable as a struct of function pointers and the call sites become named virtual calls. Set accurate prototypes on the targets so arguments are typed through the call.

**Prototypes matter transitively:** fixing one function's prototype (argument count/types, calling convention, return type) improves the decompilation of *every caller*, because types propagate across calls. Fix prototypes early on heavily-called helpers.

---

## Calling conventions cheat sheet

Knowing where arguments live lets you sanity-check the decompiler and read disassembly directly.

**x86-64 — Windows x64:** integer/pointer args in `RCX, RDX, R8, R9`, then stack; floats in `XMM0–3`; return in `RAX`. 32-byte "shadow space" reserved by caller. Callee-saved: `RBX, RBP, RDI, RSI, R12–R15`.

**x86-64 — System V (Linux/macOS):** integer/pointer args in `RDI, RSI, RDX, RCX, R8, R9`, then stack; floats in `XMM0–7`; return in `RAX`(/`RDX`). No shadow space; 128-byte red zone below `RSP`. Callee-saved: `RBX, RBP, R12–R15`.

**x86 (32-bit):**
- `cdecl` — args on stack right-to-left, **caller** cleans up (varargs use this). Return in `EAX`.
- `stdcall` — args on stack right-to-left, **callee** cleans up (`ret N`). Common in Win32 API.
- `fastcall` — first two args in `ECX, EDX`, rest on stack.
- `thiscall` — C++ member fns: `this` in `ECX` (MSVC), args on stack.

**ARM (AArch32):** args in `R0–R3`, then stack; return in `R0`(/`R1`). **ARM64 (AArch64):** args in `X0–X7`, then stack; return in `X0`; `X8` is the indirect-result register.

If the decompiler's argument list looks wrong (too few/many, wrong types), set the correct prototype/convention with `set_type` and re-decompile.

---

## Common code patterns

Recognizing these speeds everything up:

- **Loops:** an induction variable compared against a bound, incremented each pass. Name the variable `i`, the bound `count`/`len`. `memcpy`/`memset`-style loops often get folded by the decompiler — if not, recognize the shape.
- **Switch / jump tables:** a bounded index into a table of targets. IDA usually recovers these; if it shows raw indirect jumps, you may need to mark the jump table. Decode the cases into an enum.
- **String operations:** length scans (`while (*p) p++` → `strlen`), copies, comparisons. Watch for inlined CRT.
- **Stack strings / string building:** characters or dword chunks written to a local buffer one at a time — a common obfuscation to hide strings from `strings`. Reconstruct the literal (use `int_convert` to turn the dwords into ASCII) and comment it.
- **Dynamic API resolution:** `LoadLibrary`/`GetProcAddress` (or hash-based resolution walking the export table) instead of static imports. Recover the resolver, then label each resolved pointer with its real API. Hashing loops compare a computed hash against a constant — identify the algorithm (often a simple rotate-add) and map hashes to names.
- **Crypto:** look for fixed S-boxes/constants. RC4 = 256-byte identity-permutation init then a swap loop. AES = T-tables or `aesenc` intrinsics and round constants. SHA/MD5 = recognizable round constants. XOR loops are the simplest "encryption." Don't reimplement — identify, name, and note key/IV/mode.
- **Non-crypto algorithms (no S-box, so `crypto_const_scan.py` misses them — recognize by shape):**
  - **CRC (checksum, common in integrity/anti-tamper checks):** a per-byte loop indexing a **256-entry `u32` table**, XOR-ing and shifting (`crc = table[(crc ^ byte) & 0xFF] ^ (crc >> 8)`). The table's first entries are the tell (CRC32: `00000000, 77073096, EE0E612C…`). Table-less variants shift-and-XOR with a polynomial constant (`0xEDB88320` reflected, `0x04C11DB7` normal). CRC in a "license" path usually = tamper detection; note it, it's a hardening point.
  - **FNV / djb2 / sdbm (string hashing, common in API-hash resolution & fast lookups):** a tight per-char loop, **no table**, multiply-add or shift-add with a magic constant. FNV-1a: `hash = (hash ^ byte) * 0x01000193` (32-bit) / `* 0x100000001B3` (64-bit), seed `0x811C9DC5` / `0xCBF29CE484222325`. djb2: `hash = hash*33 + byte` (`hash*33` = `(hash<<5)+hash`), seed `5381`. sdbm: `hash = byte + (hash<<6) + (hash<<16) - hash`. Seeing these = likely API hashing (map hash→name, see deobfuscation-playbook §5) or a dictionary key.
  - **LZ-family decompression (LZ77/LZ4/LZSS/zlib-inflate — config/resources unpacked at runtime):** a loop reading **(offset,length) back-references** and copying from **earlier in the same output buffer** (`dst[i] = dst[i-offset]`), interleaved with literal copies, driven by a bit/flag stream. zlib/deflate: Huffman tables + the `78 9C`/`78 DA` header on the input. LZ4: token byte split into literal-len/match-len nibbles. Recognizing it means "this blob is compressed, not encrypted" — decompress with the standard lib, don't try to "decrypt."
  - **Base64 / custom alphabets:** a 64-char alphabet string and `<<6`/`>>2` bit-shuffling. Watch for **reordered alphabets** (custom Base64) — same shape, different table; extract the table and decode with it.
  - **General move:** when a loop transforms bytes with a magic constant or a 256-entry table but it isn't a known cipher, identify the *family* by the constant/table shape above, then find the reference implementation (铁律3) and confirm by matching output on a known input rather than fully reading the asm.
- **C++ objects:** vtable pointer at offset 0, constructors that populate it, virtual calls as `(*(ptr + 8*idx))(this, ...)`. Recover the vtable struct (see type recovery).
- **Error/return-code ladders:** chains of comparisons returning small ints — often map cleanly to a status enum.

---

## Platform notes

- **Windows (PE):** PEB/TEB access via `FS:[...]` (x86) or `GS:[...]` (x64) is common for anti-debug and API-less library location. Know the Win32/Native API split (`kernel32` vs `ntdll`); SSDT/syscall stubs in `ntdll`. Reference *Windows Internals* for structures.
- **Linux (ELF):** PLT/GOT for dynamic calls; `syscall` instruction with the number in `RAX` (and the System V arg registers). Static binaries inline libc — FLIRT helps a lot.
- **macOS (Mach-O):** Objective-C uses `objc_msgSend(receiver, selector, ...)`; the selector (a string) tells you the method. Swift demangling helps for Swift binaries. `__TEXT`/`__DATA` segments; LC_ load commands.
- **Embedded / firmware:** often raw binary (no headers) — you must set the correct processor, load address, and entry by hand, and locate the vector table. Memory-mapped I/O appears as fixed-address reads/writes; datasheets turn those addresses into peripheral registers. Watch for ARM Thumb vs ARM mode.

---

## Static vs dynamic — when to switch

Static analysis is the default. Switch to (or supplement with) dynamic analysis via the
debugger extension when:
- code is packed/self-modifying and the real payload only exists after unpacking in memory;
- strings/config are decrypted at runtime (breakpoint after the decrypt call and dump);
- a value is computed at runtime in a way that's painful to follow statically;
- you want to confirm a hypothesis cheaply by watching execution.

Always feed dynamic findings back into the static database: name the decrypted buffer, comment
the recovered key, set the struct you saw populated. Run untrusted samples only in an isolated,
disposable VM.

---

## Dynamic tactics — finding the variable when static is too slow

Static reading tells you *what the code could do*; these tactics find *where a specific runtime
value lives* and *who touches it* — the fastest route to a license boolean, a countdown, or a
trial flag when you don't want to read every function. (General technique; pair with the debugger
extension — x64dbg `memory_search` + hardware breakpoints, or Cheat Engine.)

### Memory scanning — locate an unknown variable by its value (Cheat Engine style)
When you know a value's *meaning* but not its *address* (the "days remaining" counter, the
"isActivated" flag, a credit balance):
1. **First scan** for the current value (e.g. scan for `30` = days left; for a bool, scan `1`/`0`;
   for an unknown float, use "unknown initial value").
2. **Change it in the app** (let a day tick, toggle the state) and **next-scan** for the new value
   (or "increased/decreased/changed" when you don't know the exact number). Each pass narrows the
   candidate set.
3. Repeat until a handful of addresses remain. Those are your variable (and its aliases/copies).
4. **Freeze or edit** the address to test the hypothesis (freeze days at 30, flip the bool) — if
   behavior changes, you found the decision variable. This is the dynamic equivalent of the
   single-variable isolation the main skill requires before claiming causation.

"Unknown initial value + changed/unchanged" scans handle encrypted or non-obvious encodings: you
never need to know the value, only that it *changed when the thing you care about changed*.

### "Who wrote this?" — hardware write breakpoint backtrace
Once you have the variable's address, find the code that **decides** it:
1. Set a **hardware breakpoint on write** (x64dbg: `bph <addr>, w`; or CE "Find out what writes to
   this address") on the variable.
2. Trigger the state change in the app. The breakpoint fires **in the function that sets the
   value** — that's the authorization decision point (or one hop from it).
3. Walk the call stack up: the caller chain leads from "the flag got set" back to "the check that
   set it." This is often faster than reading forward from `main` through obfuscated control flow.
4. Symmetric move: **hardware breakpoint on read/access** finds every consumer of the value — every
   place that gates behavior on the license flag, i.e. every patch candidate.

Write-breakpoint backtrace and value-scan are complementary: scan finds *where*, the write
breakpoint finds *who decides*, the read/access breakpoint finds *who enforces*.

### Choosing the hook frame (not just "hook it")
When several functions in a call chain touch the value, hook the frame that gives the cleanest
signal:
- **Hook the decision, not the symptom.** Hooking the UI function that greys out a button is the
  symptom; hook the function whose return value the UI reads. Follow the data backward (read
  breakpoint) to the deepest frame that still has the meaningful value in a register/argument.
- **Hook at the API boundary when the internals are obfuscated** — if the check is inside a VM/CFF
  blob but calls `GetSystemTime`/`RegQueryValue`/a network recv, hook that boundary and read the
  inputs/outputs without touching the obfuscated core (pairs with the black-box strategy in the
  main skill's 铁律14 / deobfuscation-playbook.md).
- **Prefer the frame where the value is still typed/plaintext.** Deeper is not always better: once a
  value is packed into a struct or encrypted, a shallower frame that still has the clean value is
  the better hook point.

---

## Documentation structure

Keep a living report so the analysis is reusable and shareable. A workable template:

```
# <Sample> Reverse Engineering Notes

## Summary
One paragraph: what it is, what it does, key findings.

## File identification
Hashes, format, arch, compiler, packer, signatures.

## Capabilities
Bulleted, evidence-backed (function + address per claim).

## Key functions
| Address | Name | Purpose |
Per major function: what it does, how, notable details.

## Recovered structures
The structs/enums you declared and what each field means.

## Control / data flow
How the pieces fit (entry → main logic → exit). A call-graph sketch helps.

## Indicators / artifacts (if malware analysis)
IOCs, C2, mutexes, file paths, registry keys, persistence.

## Open questions
What's still unresolved and where to look next.
```

Update it as you go, not at the end — and let the cleaned IDB and this report be the deliverable.
