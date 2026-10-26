"""
stackstring_recover.py — Reconstruct strings built on the stack from immediate stores.

A common way to hide strings from `strings`/static scanners is to write them into a local buffer
one chunk at a time (`mov [rbp+var_20], 'h'; mov [rbp+var_1F], 't'; ...` or dword/qword chunks).
This script finds runs of immediate stores to contiguous stack offsets, decodes the bytes, and
prints the reconstructed literal so you can comment it. Read-only.

SCOPE / HEURISTIC
  - Targets x86/x64 `mov`-style immediate stores to stack destinations ([rbp/rsp+...], var_*).
  - Joins stores at contiguous offsets into one string; flushes on a gap.
  - Keeps candidates with >= MIN_LEN printable characters. It will miss register-built or
    obfuscated-then-decrypted strings — review the output.

HOW TO RUN
  In IDA:    cursor in a function then File > Script file...  (or pass an address argument);
             with no argument it scans ALL functions.
  Via MCP:   paste into py_eval(code=...); call recover() (all) or recover(0xADDR) (one function).
"""

import re

try:
    import idautils
    import idc
    import ida_funcs
    import ida_ua
except ImportError:
    raise SystemExit("This script must be run inside IDA Pro (IDAPython).")

MIN_LEN = 4            # minimum printable chars to report a candidate
PRINTABLE = set(range(0x20, 0x7f)) | {0x09, 0x0a, 0x0d}
_STACK_RE = re.compile(r"\[(?:r|e)?(?:bp|sp)|var_|arg_", re.I)


def _is_stack_dest(ea, n):
    t = idc.print_operand(ea, n) or ""
    return bool(_STACK_RE.search(t))


def _printable_ratio(bs):
    if not bs:
        return 0.0
    return sum(1 for b in bs if b in PRINTABLE) / len(bs)


def _flush(run_bytes, run_start, out):
    # strip trailing NULs then evaluate
    bs = run_bytes.rstrip(b"\x00")
    if len(bs) >= MIN_LEN and _printable_ratio(bs) >= 0.8:
        try:
            text = bs.decode("latin-1")
        except Exception:
            text = repr(bs)
        out.append((run_start, text))


def _scan_func(func):
    out = []
    insn = ida_ua.insn_t()
    run = bytearray()
    run_start = None
    next_off = None

    for item_ea in idautils.FuncItems(func.start_ea):
        if ida_ua.decode_insn(insn, item_ea) == 0:
            continue
        mnem = (idc.print_insn_mnem(item_ea) or "").lower()
        matched = False
        if mnem.startswith("mov") and len(insn.ops) >= 2:
            dst, src = insn.ops[0], insn.ops[1]
            if src.type == ida_ua.o_imm and dst.type in (ida_ua.o_displ, ida_ua.o_mem) \
                    and _is_stack_dest(item_ea, 0):
                size = ida_ua.get_dtype_size(dst.dtype) or 1
                off = dst.addr
                try:
                    chunk = (src.value & ((1 << (8 * size)) - 1)).to_bytes(size, "little")
                except Exception:
                    chunk = b""
                if chunk:
                    if next_off is not None and off == next_off:
                        run += chunk
                        next_off = off + size
                    else:
                        _flush(run, run_start, out)
                        run = bytearray(chunk)
                        run_start = item_ea
                        next_off = off + size
                    matched = True
        if not matched and run:
            # any non-store instruction breaks the run (conservative)
            if mnem and not mnem.startswith(("mov", "lea", "nop")):
                _flush(run, run_start, out)
                run = bytearray()
                run_start = None
                next_off = None

    _flush(run, run_start, out)
    return out


def recover(ea=None):
    if ea is not None:
        funcs = [ea]
    else:
        funcs = list(idautils.Functions())

    print("=" * 64)
    print("STACK STRING RECOVERY")
    print("=" * 64)
    total = 0
    for fea in funcs:
        func = ida_funcs.get_func(fea)
        if func is None:
            continue
        found = _scan_func(func)
        if found:
            print("\n%s (0x%X)" % (idc.get_func_name(func.start_ea), func.start_ea))
            for at, text in found:
                print("   0x%X  \"%s\"" % (at, text))
            total += len(found)

    if total == 0:
        print("No stack strings found with current thresholds (MIN_LEN=%d)." % MIN_LEN)
    else:
        print("\nFound %d candidate(s). Comment them at the listed addresses." % total)
    print("=" * 64)
    return total


if __name__ == "__main__":
    arg = None
    try:
        if len(idc.ARGV) > 1:
            arg = int(idc.ARGV[1], 0)
    except Exception:
        arg = None
    recover(arg)
