"""
function_fingerprint.py — Export per-function fingerprints for diffing and variant matching.

Builds a relocation-independent fingerprint of each function by hashing its normalized
instruction stream (mnemonics + operand *types*, no addresses or immediates). Use it to:
  - find identical functions inside one binary (shared/library/duplicated code), and
  - diff two binaries: export both, compare fingerprints to see what changed between samples,
    versions, or a patched vs unpatched build.
Read-only; writes a JSON file.

HOW TO RUN
  In IDA:    File > Script file... > function_fingerprint.py  (writes next to the .idb)
  Via MCP:   paste into py_eval(code=...); call fingerprint() or fingerprint("/path/out.json").

DIFFING TWO DATABASES
  Run in each, then compare the JSON: equal fingerprints = unchanged functions; fingerprints
  present in only one side = added/removed/modified.
"""

import os
import json
import hashlib

try:
    import idautils
    import idc
    import ida_funcs
    import ida_ua
    import idaapi
except ImportError:
    raise SystemExit("This script must be run inside IDA Pro (IDAPython).")

_OPTYPE = {
    ida_ua.o_reg: "r", ida_ua.o_mem: "m", ida_ua.o_phrase: "p",
    ida_ua.o_displ: "d", ida_ua.o_imm: "i", ida_ua.o_far: "f",
    ida_ua.o_near: "n",
}


def _func_tokens(func):
    toks = []
    insn = ida_ua.insn_t()
    for ea in idautils.FuncItems(func.start_ea):
        if ida_ua.decode_insn(insn, ea) == 0:
            continue
        mnem = (idc.print_insn_mnem(ea) or "").lower()
        if not mnem:
            continue
        optypes = []
        for n in range(len(insn.ops)):
            op = insn.ops[n]
            if op.type == ida_ua.o_void:
                break
            optypes.append(_OPTYPE.get(op.type, "?"))
        toks.append(mnem + ":" + "".join(optypes))
    return toks


def fingerprint(out_path=None):
    if out_path is None:
        idb = idc.get_idb_path() or ""
        d = os.path.dirname(idb) or os.getcwd()
        base = os.path.splitext(os.path.basename(idaapi.get_input_file_path() or "sample"))[0]
        out_path = os.path.join(d, base + "_fingerprints.json")

    entries = []
    by_fp = {}
    for ea in idautils.Functions():
        f = ida_funcs.get_func(ea)
        if f is None:
            continue
        toks = _func_tokens(f)
        if not toks:
            continue
        digest = hashlib.sha256(";".join(toks).encode()).hexdigest()
        name = idc.get_func_name(ea)
        entries.append({
            "address": "0x%X" % ea,
            "name": name,
            "instr_count": len(toks),
            "fingerprint": digest,
        })
        by_fp.setdefault(digest, []).append(name)

    try:
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump({"functions": entries}, fh, indent=2)
        print("Wrote %d fingerprints: %s" % (len(entries), out_path))
    except Exception as e:
        print("Could not write %s: %s" % (out_path, e))

    dups = {fp: names for fp, names in by_fp.items() if len(names) > 1}
    if dups:
        print("\nIdentical functions within this binary (%d group(s)):" % len(dups))
        shown = 0
        for fp, names in dups.items():
            print("  %s..  %s" % (fp[:12], ", ".join(names[:8]) + ("..." if len(names) > 8 else "")))
            shown += 1
            if shown >= 20:
                print("  ... (more)")
                break
    return out_path


if __name__ == "__main__":
    fingerprint()
