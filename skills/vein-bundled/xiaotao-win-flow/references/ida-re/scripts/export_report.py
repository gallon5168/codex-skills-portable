"""
export_report.py — Generate a report.md skeleton from the current state of the database.

Closes the "Document" phase of the workflow. It harvests what you've already done — renamed
functions, their comments, declared structs/enums, file identity — and writes a Markdown report
following the template in references/methodology.md, with TODO placeholders for the prose only a
human (or the agent) can write. Saves you from reinventing the report structure every time.

HOW TO RUN
  In IDA:    File > Script file... > export_report.py   (writes next to the .idb by default)
  Via MCP:   paste into py_eval(code=...); call export_report() or export_report("/path/out.md").
"""

import os
import binascii

try:
    import idautils
    import idaapi
    import idc
    import ida_funcs
    import ida_bytes
    import ida_nalt
    import ida_entry
except ImportError:
    raise SystemExit("This script must be run inside IDA Pro (IDAPython).")


def _hash(fn):
    try:
        h = fn()
        if isinstance(h, (bytes, bytearray)) and h:
            return binascii.hexlify(bytes(h)).decode()
    except Exception:
        pass
    return "?"


def _meta():
    proc, bits = "?", "?"
    try:
        s = idaapi.get_inf_structure()
        proc = s.procname
        bits = "64-bit" if s.is_64bit() else ("32-bit" if s.is_32bit() else "16-bit")
    except Exception:
        try:
            import ida_ida
            proc = ida_ida.inf_get_procname()
            bits = "64-bit" if ida_ida.inf_is_64bit() else "32-bit"
        except Exception:
            pass
    return proc, bits


def _renamed_functions():
    rows = []
    for ea in idautils.Functions():
        f = ida_funcs.get_func(ea)
        if f is None:
            continue
        if f.flags & (ida_funcs.FUNC_LIB | ida_funcs.FUNC_THUNK):
            continue
        if ida_bytes.has_dummy_name(ida_bytes.get_flags(ea)):
            continue  # not analyzed yet
        cmt = ""
        for rep in (False, True):
            c = ida_funcs.get_func_cmt(f, rep)
            if c and c.strip():
                cmt = c.strip().replace("\n", " ")
                break
        rows.append((ea, idc.get_func_name(ea), cmt))
    rows.sort()
    return rows


def _local_types():
    names = []
    try:
        import ida_typeinf
        til = ida_typeinf.get_idati()
        try:
            limit = ida_typeinf.get_ordinal_limit(til)
        except Exception:
            limit = ida_typeinf.get_ordinal_qty(til)
        for ordn in range(1, limit):
            nm = ida_typeinf.get_numbered_type_name(til, ordn)
            if nm:
                names.append(nm)
    except Exception:
        pass
    return names


def export_report(out_path=None):
    proc, bits = _meta()
    in_path = idaapi.get_input_file_path() or "<unknown>"
    base = os.path.splitext(os.path.basename(in_path))[0] or "sample"

    if out_path is None:
        idb = idc.get_idb_path() or ""
        d = os.path.dirname(idb) or os.getcwd()
        out_path = os.path.join(d, base + "_RE_report.md")

    funcs = _renamed_functions()
    types = _local_types()

    md = []
    md.append("# %s — Reverse Engineering Notes\n" % base)
    md.append("## Summary\n\n_TODO: one paragraph — what it is, what it does, key findings._\n")

    md.append("## File identification\n")
    md.append("- Path: `%s`" % in_path)
    md.append("- Processor: %s (%s)" % (proc, bits))
    md.append("- Image base: 0x%X" % idaapi.get_imagebase())
    md.append("- MD5: `%s`" % _hash(ida_nalt.retrieve_input_file_md5))
    md.append("- SHA-256: `%s`\n" % _hash(ida_nalt.retrieve_input_file_sha256))

    md.append("## Capabilities\n\n_TODO: bullet list, each backed by a function + address._\n")

    md.append("## Key functions\n")
    if funcs:
        md.append("| Address | Name | Notes |")
        md.append("|---|---|---|")
        for ea, name, cmt in funcs:
            md.append("| 0x%X | `%s` | %s |" % (ea, name, cmt or "_TODO_"))
        md.append("")
    else:
        md.append("_No functions renamed yet — run the cleanup loop first._\n")

    md.append("## Recovered structures\n")
    if types:
        for t in types:
            md.append("- `%s` — _TODO: describe fields._" % t)
        md.append("")
    else:
        md.append("_No local types declared yet._\n")

    md.append("## Control / data flow\n\n_TODO: entry -> main logic -> exit; a call-graph sketch helps._\n")
    md.append("## Indicators / artifacts\n\n_TODO (if malware analysis): IOCs, C2, mutexes, paths, persistence._\n")
    md.append("## Open questions\n\n_TODO: what's unresolved and where to look next._\n")

    text = "\n".join(md)
    try:
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("Wrote report skeleton: %s" % out_path)
        print("  functions documented: %d | local types: %d" % (len(funcs), len(types)))
    except Exception as e:
        print("Could not write %s: %s" % (out_path, e))
        print("--- report below ---\n")
        print(text)
    return out_path


if __name__ == "__main__":
    export_report()
