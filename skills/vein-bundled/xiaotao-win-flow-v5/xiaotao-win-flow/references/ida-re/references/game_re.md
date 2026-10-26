# Game Binary Reverse Engineering (the playbook)

Reversing a game binary is a different sport from malware triage. Games are usually *not*
obfuscated in the malware sense (no string encryption, no API hashing) — but they're enormous,
overwhelmingly C++, packed with vtables, and frequently wrapped in DRM/anti-tamper. Crucially,
they often ship the metadata needed to reconstruct almost everything: RTTI, reflection systems,
assert strings, sometimes leaked PDBs. The highest-leverage move is rarely "rename `sub_*` by
hand" — it's "find the metadata and let it name thousands of functions at once."

Read the section you need; you don't have to read it all at once.

## Contents
- [Ethics for games specifically](#ethics-for-games-specifically)
- [Step 0: fingerprint the engine FIRST](#step-0-fingerprint-the-engine-first)
- [Unity / IL2CPP](#unity--il2cpp)
- [Unreal Engine](#unreal-engine)
- [RTTI recovery (all native C++ games)](#rtti-recovery-all-native-c-games)
- [Symbols hiding in plain sight](#symbols-hiding-in-plain-sight)
- [Math and SIMD as readable types](#math-and-simd-as-readable-types)
- [DRM / anti-tamper recognition](#drm--anti-tamper-recognition)
- [Entities, structs, and offset hunting](#entities-structs-and-offset-hunting)
- [Byte signatures that survive updates](#byte-signatures-that-survive-updates)
- [Embedded scripting VMs](#embedded-scripting-vms)
- [Recommended order](#recommended-order)

---

## Ethics for games specifically

Reversing games is overwhelmingly legitimate: modding, interoperability, game preservation,
single-player tools/trainers, learning, and security research. The skill's general ethics frame
applies directly — *understanding and documenting* a game is fine. What's out of scope: building
cheats for online/multiplayer games (they degrade the experience for others and usually breach
both law and the ToS), and stripping DRM to enable piracy. The reason this section exists is that
"reverse this game" sits right next to cheating in practice, so the line is worth stating plainly:
analyze freely; don't weaponize against other players or against the publisher's rights.

---

## Step 0: fingerprint the engine FIRST

This single decision reshapes the entire analysis — do it before touching any `sub_*`. Identify
the engine and middleware from strings, imports, exports, and section names:

- **Unity (IL2CPP):** `il2cpp_*` exports, a `GameAssembly.dll`, a `global-metadata.dat` file in
  the build, strings like `Assembly-CSharp`. → jump to the IL2CPP section; this is the biggest win.
- **Unity (Mono):** `mono_*` imports, `mono-2.0-bdwgc.dll`, managed `.dll`s alongside. Managed
  code is in the assemblies — decompile those with a C# decompiler (dnSpy/ILSpy), not IDA.
- **Unreal Engine:** `/Game/…` and `/Engine/…` asset paths, strings `UObject`, `UClass`, `FName`,
  `GNames`, `GUObjectArray`, `StaticClass`, mangled `UFunction` names. → Unreal section.
- **Source / Source 2:** `vphysics`, `studiomdl`, `.vpk`, Valve-style interface strings
  (`VEngineClient`, `CreateInterface`).
- **BigWorld (Wargaming):** a C++/Python MMO engine — powers World of Tanks / World of Warships
  (and their Lesta forks). Tells: an embedded **CPython 2.7** runtime (`python27.dll`-style imports,
  `Py_*` exports), `res/scripts/client/…` paths, `.pyc` files and `.wotmod`/`res_mods` packaging,
  entity-system strings (`Vehicle`, `Avatar`, `Account`, `PlayerAvatar`), `BigWorld`/`BWPersonality`
  symbols. The decisive point: **most gameplay logic lives in Python, not in the native binary.**
  Don't grind the C++ in IDA first — see the BigWorld note in "Embedded scripting VMs" below.
- **Other AAA engines:** idTech, CryEngine, RE Engine, Frostbite, Decima, REDengine, Anvil —
  each has telltale strings/section layouts; search the engine name + characteristic exports.
- **Middleware (orthogonal to engine):** Wwise / FMOD (audio), PhysX / Havok / Bullet (physics),
  Bink (video), RakNet / GameNetworkingSockets (net), Mono / Lua / AngelScript (scripting),
  Scaleform / RmlUi (UI). Recognizing these folds away huge swaths of code as "known library,"
  exactly like FLIRT does for the CRT — don't reverse PhysX internals by hand.

Knowing the engine tells you *where the game's own logic lives* versus engine/middleware
boilerplate, and which metadata-recovery tool will name everything for you.

---

## Unity / IL2CPP

If the game is IL2CPP, this is the first thing you do, not the last. IL2CPP compiles C# to native
C++, but the build ships `global-metadata.dat`, which still contains every class name, method
name, and field name. Tools reconstruct the full managed type system and apply it back to the IDB:

- **Il2CppDumper / Il2CppInspector** take `GameAssembly.dll` + `global-metadata.dat` and emit a
  C# `dump.cs` (the full API surface) plus IDA/Ghidra scripts (`ida_with_struct.py`, header files)
  that rename functions and apply struct types wholesale.
- After running the script, `sub_18004A2C0` becomes `PlayerController$$TakeDamage` and method
  metadata gives you real argument types. You go from staring at sludge to reading near-source.
- If `global-metadata.dat` is encrypted/obfuscated (some anti-cheat builds do this), you may need
  to dump it from memory at runtime after the loader decrypts it — pivot to dynamic analysis,
  breakpoint after the metadata-load, and dump.

The rest of the skill's loop still applies to the C++ glue (the VM, the runtime, native plugins),
but the gameplay logic is named for you. Don't skip this and grind manually.

---

## Unreal Engine

Unreal's reflection system means the binary knows its own type names. Recover the reflection
roots and you can resolve almost everything:

- **`GNames` / `FNamePool`** — the global name table. `FName` values you see everywhere are indices
  into it; resolve them to strings and the code becomes readable. Find it via the string-pool
  init or known byte patterns for the engine version.
- **`GUObjectArray`** — the global object array; walking it enumerates every live `UObject`,
  `UClass`, `UFunction`, `UProperty` with names, offsets, and class hierarchy.
- **SDK generators** (Dumper-7, UnrealFinderTool, and version-specific forks) automate this:
  they locate the reflection globals, dump a full C++ SDK (classes, members, function offsets),
  and give you typed structs to apply. This is the Unreal equivalent of the IL2CPP dumper.
- Engine version matters — offsets to `GNames`/`GUObjectArray` and struct layouts shift between
  UE4 minor versions and UE5; match the generator/config to the version (often in a version string
  or the `.pdb` path left in the binary).

`UFunction`s are reflected, so even Blueprint-callable native functions recover their names and
signatures. Native-only helpers still need the manual loop, but the skeleton is handed to you.

---

## RTTI recovery (all native C++ games)

Unlike malware (which usually strips it), shipping games almost always retain C++ RTTI. This is a
gift: it reconstructs real class names and the vtable→class mapping, so an entire inheritance
hierarchy names itself.

- **MSVC (Windows):** RTTI lives in `.rdata` as `RTTICompleteObjectLocator` → `TypeDescriptor`
  (holding the mangled `.?AV` class name) and `ClassHierarchyDescriptor` (base classes). IDA's
  own RTTI analysis, or plugins/scripts (classic `classinformer`, modern equivalents), parse these
  and name vtables `ClassName::vftable`, then you can name the virtual methods underneath.
- **Itanium (Linux/macOS, GCC/Clang):** `_ZTV*` (vtable), `_ZTI*` (typeinfo), `_ZTS*` (type-name
  string) symbols, demangled with the standard demangler.
- Once vtables are named, set accurate prototypes on the virtual methods so types propagate through
  every virtual call site — exactly the "prototypes matter transitively" point from the main
  methodology, but now seeded by RTTI instead of guessed by hand.

Recover RTTI *before* manually rebuilding any vtable struct; it does the work for you and gives the
true class names rather than your invented ones.

---

## Symbols hiding in plain sight

Games leak their own function names through strings far more than malware does. Mine them:

- **Assert / check macros** embed `__FILE__` and often the function or expression:
  `"d:\\build\\Source\\Player\\PlayerController.cpp"`, `"Assertion failed: health >= 0"`. The path
  and line tell you which source file (and often function) you're in.
- **Log strings**: `"PlayerController::Respawn: no spawn point"`, verbose category tags. These map
  string → function directly; `scripts/string_xref_map.py` is built for exactly this pivot.
- **Shader / material / asset names**, script-error messages, console-command registrations
  (`RegisterConCommand("noclip", …)`) — each ties a string to the function that uses it.
- **Leaked PDB path** in the debug directory (e.g. `Z:\\…\\Game.pdb`) — occasionally the PDB itself
  is fetchable or was shipped, restoring *all* symbols. Always check.

Treat the strings inventory as a naming oracle, not just an IOC list (the malware framing).

---

## Math and SIMD as readable types

Games are linear algebra: positions, rotations, transforms, physics. The decompiler renders these
as walls of `XMM` register math. Recognize the shapes and type them so Hex-Rays collapses the
intrinsics:

- **Recognizable operations:** dot product (multiply + horizontal add), normalize (dot → rsqrt →
  multiply), matrix×matrix / matrix×vector, quaternion multiply and slerp, cross product.
- **Type the operands** as `Vector2`/`Vector3`/`Vector4`/`Quaternion`/`Matrix4x4` (`float[4]`,
  `float[16]`) via `declare_type` + `set_type`. Once a function's params are `Vector3*`, dozens of
  shuffles and `movups` turn into field access and the intent becomes obvious.
- A small library of these math structs, declared once, pays off across the entire binary — most
  gameplay code touches transforms.

---

## DRM / anti-tamper recognition

Recognize the protector, then decide statically-impossible vs worth-it — don't burn hours on a
VM-protected stub:

- **Common protectors:** Denuvo (anti-tamper, heavy), VMProtect / Themida / WinLicense (code
  virtualization), Arxan / GuardIT, Enigma. **Anti-cheat (kernel/user):** EasyAntiCheat (EAC),
  BattlEye, Vanguard, nProtect — these also wrap/encrypt and resist analysis.
- **Tells:** huge high-entropy sections, a tiny real `.text` behind a packer stub, abnormal entry
  flow, TLS-callback tricks, virtualized regions where the decompiler produces nonsense dispatch
  loops, integrity-check threads.
- **Strategy:** virtualized/packed code is generally not worth static analysis. Let it unpack in
  memory and dump the real image at OEP (`scripts/dump_region.py` after a breakpoint), then analyze
  the dump. This is the deobfuscation pre-pass from the main skill, with game-specific names.
- **Caution:** anti-cheat may be kernel-mode and actively hostile to debuggers; only ever run such
  a sample in an isolated, disposable VM, and never attach a debugger to an online game you don't
  own the right to analyze.

---

## Entities, structs, and offset hunting

The central technique of game RE: recover the entity/actor/object struct (the thing holding
position, health, state, flags, the component list), and a huge amount of logic becomes legible at
once because every gameplay function reads and writes it.

- Find a hot object (the player, an actor) by following what `xrefs_to` the most-referenced globals
  touch, or what survives across frames. Map its fields with `struct_recovery.py` and `set_type`.
- "Offset hunting" — locating the displacement of `health`, `position`, `team`, etc. within that
  struct — is the same struct-recovery loop from the main methodology, just framed as the modder's
  goal. Once typed, `*(player + 0x1A0)` reads as `player->health` everywhere.
- Component / ECS engines: recover the component-array layout and the component-type ids; one
  struct unlocks many systems.

---

## Byte signatures that survive updates

A recurring modding/tooling task: find *the same function* in a future patched build. Game updates
shift addresses but rarely rewrite logic, so a relocation-independent signature re-locates it:

- `scripts/function_fingerprint.py` exports normalized per-function fingerprints (mnemonics +
  operand types, address-independent) — run it on two builds to diff versions or to re-find a
  function after a patch.
- For pinpoint hooks, derive a byte/mask **AOB signature** (`48 8B ?? ?? E8 ?? ?? ?? ??` with
  wildcards over relocatable operands) for the function's prologue or a unique mid-body sequence,
  and verify it's unique with `find_bytes`. This is what mod loaders use to stay version-resilient.

---

## Embedded scripting VMs

Many games embed a scripting runtime — Lua (very common), AngelScript, Squirrel, or a bespoke
bytecode VM. If you see one:

- Identify the interpreter dispatch (a big switch/computed-goto over an opcode), then reverse the
  opcode handlers one at a time — each handler is small and the dispatch tells you the opcode set.
- Recover the script value/object struct (tagged union of number/string/table/function) and the
  call/stack convention; from there, embedded script logic and the native↔script boundary
  (registered C functions) open up.
- For stock Lua/AngelScript, identify the version and lean on its known VM structure rather than
  reversing from scratch.

**BigWorld (World of Tanks / World of Warships) — go to the Python, not the C++.** This is the
canonical "scripting-first" engine: the native `WorldOfTanks.exe`/`WorldOfWarships.exe` is mostly
the engine and CPython 2.7 host, while the game logic ships as compiled Python.

- **Find and decompile the `.pyc`.** Game logic lives under `res/scripts/client/…` (and Python
  packages inside `.pkg`/`res` archives); mods live in `res_mods/` and `.wotmod` (zip) files.
  Decompile the bytecode with a Python-2.7-capable decompiler (`decompyle3`/`uncompyle6`, or
  `unpyc37`-class tools for the exact version) rather than reversing native code that just hosts it.
  This recovers near-source — class names, methods, the entity definitions — for free.
- **Map the entity model from Python:** `Vehicle`, `Avatar`/`PlayerAvatar`, `Account` and their
  methods describe gameplay directly; the native side mostly marshals between the network layer and
  these Python objects.
- **The native↔Python boundary** is the part worth reversing in IDA: the `BigWorld` module's C
  functions exposed to Python (entity property sync, the `BWPersonality` callbacks, network entity
  method dispatch). Recover those to understand replication and where native enforcement happens.
- **Dynamic option:** because there's a live embedded interpreter, an in-process Python REPL (the
  community `wot-debugserver`/`replserver` mods open a local TCP console into the running engine)
  lets you introspect modules, objects, and offsets at runtime — far faster than static guessing.
- **Ethics reminder:** WoT/WoWs are online games. Reading the Python to understand or build benign
  client mods is one thing; anything that yields a multiplayer advantage (or breaches the ToS) is
  the cheating line this skill stays on the right side of.

---

## Recommended order

1. **Fingerprint the engine and middleware** (Step 0) — decides everything below.
2. **Run the metadata recoverer for that engine** — IL2CPP dumper (Unity), SDK generator (Unreal),
   or RTTI recovery (native C++). This names thousands of things before you touch the manual loop.
3. **Apply library signatures** (FLIRT/Lumina) for engine/middleware and CRT/STL.
4. **Mine strings** for assert paths, logs, console commands → more names.
5. **Declare the math types and the core entity struct** — the two highest-leverage type recoveries.
6. **Now run the per-function loop from SKILL.md** on the game's own logic, which is what's left
   once the boilerplate is named and typed away.
7. If wrapped in DRM/anti-tamper, **dump from memory first** and analyze the dump.

The throughline: don't reverse a game like malware. Find the metadata, let it name the world, fold
away engine/middleware, and reserve the manual senior-RE loop for the genuinely custom gameplay code.
