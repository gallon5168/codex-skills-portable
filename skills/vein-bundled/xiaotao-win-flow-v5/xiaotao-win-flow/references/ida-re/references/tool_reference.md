# IDA Pro MCP — Tool Reference

Complete mapping of IDA Pro MCP tools to reverse-engineering actions, with batch payload
shapes and the legacy↔current name table. Tool names and argument schemas differ across
server versions and forks, so **always confirm against the live tool list** (your client shows
the registered tools and their JSON schemas; or run `ida-pro-mcp --config`). Treat the examples
below as illustrative of intent, not as guaranteed argument keys.

## Contents
- [Two server flavors](#two-server-flavors)
- [Capability → tool map](#capability--tool-map)
- [Batch payload shapes](#batch-payload-shapes)
- [MCP resources (read-only state)](#mcp-resources-read-only-state)
- [Legacy ↔ current name table](#legacy--current-name-table)
- [Enabling the debugger extension](#enabling-the-debugger-extension)
- [py_eval — the escape hatch](#py_eval--the-escape-hatch)

---

## Two server flavors

- **`ida-pro-mcp` (GUI plugin)** — runs inside an interactive IDA session; you see edits live in
  the UI. Being deprecated in favor of idalib but still widely used.
- **`idalib-mcp` (headless)** — runs IDA's `idalib` without a GUI; can open/close arbitrary
  binaries (`idalib_open` / `idalib_close` / `idalib_switch`) and serve multiple databases. Use
  for automation, CI, or driving many samples. Pass `database=` (session id, filename, or path)
  to target a specific DB; with `--isolated-contexts` each connection gets its own binding.

Both expose the same analysis/modification tool surface below.

---

## Capability → tool map

### Reading code
| You want to… | Tool |
|---|---|
| Decompile a function (Hex-Rays) | `decompile(addr)` |
| Disassemble with full detail (args, stack frame) | `disasm(addr)` |
| One-shot bundle: decompile + asm + xrefs + callees + strings + constants + blocks | `analyze_funcs(addrs)` |
| Basic blocks with successors/predecessors | `basic_blocks(addrs)` |
| Build a call graph from roots | `callgraph(roots, max_depth)` |

### Navigating / finding
| You want to… | Tool |
|---|---|
| Resolve a function by name or address (auto-detect) | `lookup_funcs(queries)` |
| List functions (paginated, filtered) | `list_funcs(queries)` |
| List globals (paginated, filtered) | `list_globals(queries)` |
| List imported symbols + module names | `imports(offset, count)` |
| Cross-refs *to* an address | `xrefs_to(addrs)` |
| Cross-refs to a specific struct field | `xrefs_to_field(queries)` |
| Functions called *by* a function | `callees(addrs)` |
| Regex-search strings | `find_regex(queries)` |
| Find a byte pattern, e.g. `48 8B ?? ??` | `find_bytes(patterns, limit, offset)` |
| Find an instruction sequence | `find_insns(sequences, limit, offset)` |
| Advanced search (immediates, strings, data/code refs) | `find(type, targets, limit, offset)` |
| Search structures by name | `search_structs(filter)` |

### Reading data (ground truth — use instead of guessing)
| You want to… | Tool |
|---|---|
| Read raw bytes | `get_bytes(addrs)` |
| Read an integer with explicit type (`i8`/`u32le`/`i16be`/…) | `get_int(queries)` |
| Read a null-terminated string | `get_string(addrs)` |
| Read a global's compile-time value | `get_global_value(queries)` |
| Read struct field values at an address | `read_struct(queries)` |
| Convert hex ↔ dec ↔ bytes ↔ ASCII ↔ binary | `int_convert(inputs)` |

### Writing back (the senior-RE core)
| You want to… | Tool (current) |
|---|---|
| Rename functions / locals / globals / stack vars | `rename(batch)` |
| Apply a type to func/global/local/stack var | `set_type(edits)` |
| Let Hex-Rays/heuristics infer types | `infer_types(addrs)` |
| Declare C types (structs, unions, enums, typedefs) | `declare_type(decls)` |
| Comment in both disasm and pseudocode | `set_comments(items)` |
| Define a function at an address | `define_func(items)` |
| Convert bytes → code | `define_code(items)` |
| Undefine back to raw bytes | `undefine(items)` |
| Create / delete a stack variable | `declare_stack(items)` / `delete_stack(items)` |
| Patch assembly / bytes | `patch_asm(items)` / `patch(patches)` / `put_int(items)` |
| Export functions (json / c_header / prototypes) | `export_funcs(addrs, format)` |

### Stack frames
`stack_frame(addrs)` to inspect; `declare_stack(items)` / `delete_stack(items)` to edit.

---

## Batch payload shapes

The recent API is batch-first: most tools accept a single item or a list, and batch operations
return a parallel list of results, each `{..., "error": null | "message"}`. Search tools paginate
with a `cursor: {next: offset}` or `{done: true}`. Confirm exact keys against the live schema.

**`rename(batch)`** — one call to rename across all four namespaces. Documented to accept a dict
with optional `func`, `data` (globals), `local`, and `stack` keys:
```jsonc
{
  "func":  [{"addr": "0x401000", "name": "validate_license"}],
  "data":  [{"addr": "0x4050A0", "name": "g_config"}],
  "local": [{"func": "0x401000", "old": "v3", "new": "key_index"}],
  "stack": [{"func": "0x401000", "old": "var_18", "new": "decrypted_buf"}]
}
```

**`declare_type(decls)`** — declare C types into the local type library, then apply them:
```jsonc
{ "decls": "struct Config { unsigned int magic; char* name; unsigned int length; void (*cb)(int); };" }
```

**`set_type(edits)`** — apply a type to a target so the decompiler resolves offsets to fields:
```jsonc
{ "edits": [{"func": "0x401000", "local": "a1", "type": "Config*"}] }
```

**`set_comments(items)`** — comment at addresses (shows in both views):
```jsonc
{ "items": [{"addr": "0x40103C", "comment": "RC4 KSA: 256-byte S-box init"}] }
```

**`int_convert(inputs)`** — never do this in your head:
```jsonc
{ "inputs": ["0x6C616D66"] }   // → decimal, little/big-endian bytes, ASCII, binary
```

Typical type-recovery sequence: `infer_types(addr)` → inspect → `declare_type(struct …)` →
`set_type(var → MyStruct*)` → `decompile(addr)` to confirm `*(a1+0x10)` became `a1->length`.

---

## MCP resources (read-only state)

Browsable state is exposed as resources (read these rather than calling tools when you just need state):
`ida://idb/metadata`, `ida://idb/segments`, `ida://idb/entrypoints`, `ida://cursor`,
`ida://selection`, `ida://types`, `ida://structs`, `ida://struct/{name}`, `ida://import/{name}`,
`ida://export/{name}`, `ida://xrefs/from/{addr}`.

---

## Legacy ↔ current name table

Older releases and third-party forks (e.g. `MxIris-Reverse-Engineering/ida-mcp-server`) use
granular names. If a tool below isn't found, look for its counterpart.

| Action | Legacy / granular | Current (mrexodia main) |
|---|---|---|
| Decompile | `decompile_function` | `decompile` |
| Disassemble | `disassemble_function` | `disasm` |
| Function by name/addr | `get_function_by_name`, `get_function_by_address` | `lookup_funcs` |
| List functions | `list_functions` | `list_funcs` |
| Xrefs to | `get_xrefs_to` | `xrefs_to` |
| Rename local | `rename_local_variable` | `rename` (`local`) |
| Rename global | `rename_global_variable` | `rename` (`data`) |
| Rename function | `rename_function` | `rename` (`func`) |
| Rename stack var | `rename_stack_frame_variable` | `rename` (`stack`) |
| Batch rename funcs | `ida_rename_multi_functions` (fork) | `rename` (`func` list) |
| Set function prototype | `set_function_prototype` | `set_type` |
| Set local type | `set_local_variable_type` | `set_type` |
| Set global type | `set_global_variable_type` | `set_type` |
| Declare C type | `declare_c_type` | `declare_type` |
| Comment | `set_comment`, `set_decompiler_comment` | `set_comments` |
| Create stack var | `create_stack_frame_variable` | `declare_stack` |
| Set stack var type | `set_stack_frame_variable_type` | `set_type` / `declare_stack` |
| Delete stack var | `delete_stack_frame_variable` | `delete_stack` |
| Number conversion | `convert_number` | `int_convert` |

---

## Enabling the debugger extension

Debugger tools are hidden by default. Enable by adding `?ext=dbg` to the server URL, e.g.
`http://127.0.0.1:13337/mcp?ext=dbg`. Then: `dbg_start` / `dbg_exit`, `dbg_continue`,
`dbg_run_to(addr)`, `dbg_step_into` / `dbg_step_over`; breakpoints `dbg_bps`, `dbg_add_bp`,
`dbg_delete_bp`, `dbg_toggle_bp`; registers `dbg_regs`, `dbg_gpregs`, `dbg_regs_named` (and
`_all` / `_remote` variants for threads); memory `dbg_read(regions)` / `dbg_write(regions)`;
and `dbg_stacktrace`. Only debug malware in an isolated, disposable VM with no network you care
about.

---

## py_eval — the escape hatch

`py_eval(code)` runs arbitrary IDAPython in IDA's context and returns `{result, stdout, stderr}`
(Jupyter-style: the last expression's value is returned). Use it for anything the dedicated tools
don't cover, and to run the bundled scripts. Examples:
```python
# count functions still auto-named
import idautils, ida_bytes
sum(ida_bytes.has_dummy_name(ida_bytes.get_flags(ea)) for ea in idautils.Functions())
```
```python
# apply a previously-declared struct to a decompiler variable and re-render
import ida_hexrays
# (then re-run decompile() via the MCP to view the result)
```
Prefer the dedicated tools when they exist (they're typed and safer); fall back to `py_eval`
for bulk operations, custom analyses, or APIs with no tool wrapper.
