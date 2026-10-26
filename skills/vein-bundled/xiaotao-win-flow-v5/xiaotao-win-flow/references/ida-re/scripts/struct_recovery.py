"""
struct_recovery.py — Draft a C struct skeleton from a function's memory-access patterns.

Accelerates the highest-leverage step of the RE loop: turning `*(a1 + 0x10)` into `a1->length`.
For the chosen function it collects simple `[base_register + constant]` memory accesses, infers
each field's width from the operand size, and prints a C `struct` you can hand to the MCP's
declare_type, then apply to the base pointer with set_type. Re-decompile and the offset math
collapses into named fields.

HEURISTIC — review before applying:
  - Only simple `[reg + const]` accesses are considered. Indexed forms (`[rax+rcx*4+8]`),
    negative offsets, and named stack vars (`var_8`, `arg_0`) are skipped on purpose.
  - Stack/base pointers (rsp/rbp/esp/ebp) are skipped — they're frames, not objects.
  - Field widths come from the access size actually seen; a field accessed as both DWORD and
    QWORD will show the larger. Gaps are padded with byte arrays.
  - It does not detect nested structs or unions; treat the output as a starting skeleton.

HOW TO RUN
  In IDA:    put the cursor in the target function, then File > Script file... > struct_recovery.py
             (or pass an address as the first script argument).
  Via MCP:   paste into py_eval(code=...) and call recover(0xADDRESS) (or recover() for the
             current function).
"""

import re

try:
    import idautils
    import idaapi
    import idc
    import ida_funcs
    import ida_ua
    import ida_kernwin
except ImportError:
    raise SystemExit("This script must be run inside IDA Pro (IDAPython).")

SKIP_BASE = {"rsp", "esp", "sp", "rbp", "ebp", "bp"}
_SIZE_PREFIXES = ("xmmword ptr ", "qword ptr ", "dword ptr ", "word ptr ", "byte ptr ", "ptr ")
_SEG_PREFIXES = ("ds:", "es:", "ss:", "cs:", "fs:", "gs:")
_REG_RE = re.compile(r"^[a-z][a-z0-9]*$")


def _ctype(size):
    return {1: "unsigned __int8", 2: "unsigned __int16",
            4: "unsigned int", 8: "unsigned __int64"}.get(size)


def _parse_displ(text):
    """Parse a simple [base+const] operand. Return (base_reg, offset) or None."""
    if not text:
        return None
    t = text.strip().lower()
    for p in _SIZE_PREFIXES:
        if t.startswith(p):
            t = t[len(p):]
            break
    for p in _SEG_PREFIXES:
        if t.startswith(p):
            t = t[len(p):]
            break
    lb, rb = t.find("["), t.find("]")
    if lb == -1 or rb == -1 or rb < lb:
        return None
    inner = t[lb + 1:rb]
    if "*" in inner or "-" in inner or "var_" in inner or "arg_" in inner:
        return None
    parts = [p.strip() for p in inner.split("+")]
    if len(parts) == 1:
        reg, off = parts[0], 0
    elif len(parts) == 2:
        reg = parts[0]
        tok = parts[1].rstrip("h")
        try:
            off = int(tok, 16) if (tok.startswith("0x") or re.fullmatch(r"[0-9a-f]+", tok)) else int(tok)
        except ValueError:
            return None
    else:
        return None
    if not _REG_RE.match(reg) or reg in SKIP_BASE:
        return None
    return reg, off


def recover(ea=None):
    if ea is None:
        ea = ida_kernwin.get_screen_ea()
    func = ida_funcs.get_func(ea)
    if func is None:
        print("No function at 0x%X" % ea)
        return None

    fname = idc.get_func_name(func.start_ea)
    # base register -> { offset -> max access size }
    accesses = {}
    insn = ida_ua.insn_t()
    for item_ea in idautils.FuncItems(func.start_ea):
        if ida_ua.decode_insn(insn, item_ea) == 0:
            continue
        for n in range(len(insn.ops)):
            op = insn.ops[n]
            if op.type == ida_ua.o_void:
                break
            if op.type != ida_ua.o_displ:
                continue
            parsed = _parse_displ(idc.print_operand(item_ea, n))
            if not parsed:
                continue
            reg, off = parsed
            size = ida_ua.get_dtype_size(op.dtype) or 1
            d = accesses.setdefault(reg, {})
            d[off] = max(d.get(off, 0), size)

    candidates = {r: offs for r, offs in accesses.items() if len(offs) >= 2}
    if not candidates:
        print("No struct-like access patterns found in %s (0x%X)." % (fname, func.start_ea))
        print("Tip: the object pointer may be copied into another register, or accesses may be")
        print("indexed. Inspect the decompilation and try the function that allocates the object.")
        return None

    print("=" * 60)
    print("STRUCT CANDIDATES in %s (0x%X)" % (fname, func.start_ea))
    print("=" * 60)
    results = {}
    for reg in sorted(candidates):
        offs = candidates[reg]
        struct_name = "Struct_%s_%X" % (reg, func.start_ea)
        lines = ["struct %s" % struct_name, "{"]
        cursor = 0
        for off in sorted(offs):
            if off > cursor:
                lines.append("    char gap_%X[0x%X];" % (cursor, off - cursor))
            size = offs[off]
            ct = _ctype(size)
            if ct:
                lines.append("    %s field_%X;" % (ct, off))
                cursor = off + size
            else:
                lines.append("    char field_%X[0x%X];" % (off, size))
                cursor = off + size
        lines.append("};")
        decl = "\n".join(lines)
        results[reg] = decl
        print("\n// base register seen: %s   (max offset 0x%X)" % (reg, max(offs)))
        print(decl)
        print("// apply with the MCP, then re-decompile:")
        print("//   declare_type(<the struct above>)")
        print("//   set_type(<the variable holding %s> -> %s*)" % (reg, struct_name))

    print("=" * 60)
    return results


if __name__ == "__main__":
    arg = None
    try:
        if len(idc.ARGV) > 1:
            arg = int(idc.ARGV[1], 0)
    except Exception:
        arg = None
    recover(arg)
