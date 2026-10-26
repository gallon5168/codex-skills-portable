"""
dump_region.py — Dump a memory region or segment to disk.

A debugging helper for capturing data that only exists at runtime: an unpacked or decrypted
payload after you've broken past the stub, a decoded config buffer, a staged second stage, etc.
It reads bytes from the current view (debugger-aware while a debug session is active) and writes
them to a file, reporting size and entropy so you can tell whether the result is still packed.

Run untrusted samples only inside an isolated, disposable VM. To debug via MCP, enable the
debugger extension (server URL with `?ext=dbg`).

HOW TO RUN
  In IDA:    File > Script file... > dump_region.py, then call dump(start, size) /
             dump_segment("name") from the Output window, or set the constants below and run.
  Via MCP:   paste into py_eval(code=...); call dump(0xADDR, 0xSIZE) or dump_segment(".text").
"""

import os
import math

try:
    import idautils
    import idaapi
    import idc
    import ida_bytes
    import ida_segment
except ImportError:
    raise SystemExit("This script must be run inside IDA Pro (IDAPython).")

# Optional defaults for running the file directly without calling a function:
START = None   # e.g. 0x401000
SIZE = None    # e.g. 0x2000


def _shannon(data):
    if not data:
        return 0.0
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    n = len(data)
    h = 0.0
    for c in counts:
        if c:
            p = c / n
            h -= p * math.log(p, 2)
    return h


def _read(start, size):
    data = ida_bytes.get_bytes(start, size)
    if data:
        return data
    # fall back to live debugger memory if available
    try:
        data = idaapi.dbg_read_memory(start, size)
        if data:
            return data
    except Exception:
        pass
    return None


def _outdir():
    idb = idc.get_idb_path() or ""
    return os.path.dirname(idb) or os.getcwd()


def dump(start, size, path=None):
    data = _read(start, size)
    if not data:
        print("Could not read 0x%X bytes at 0x%X (not mapped? start the debugger?)." % (size, start))
        return None
    if path is None:
        path = os.path.join(_outdir(), "dump_0x%X_0x%X.bin" % (start, len(data)))
    try:
        with open(path, "wb") as fh:
            fh.write(data)
    except Exception as e:
        print("Could not write %s: %s" % (path, e))
        return None
    ent = _shannon(data)
    print("Dumped %d bytes from 0x%X -> %s" % (len(data), start, path))
    print("Entropy: %.2f%s" % (ent, "  (still high — likely packed/encrypted)" if ent >= 7.0 else ""))
    return path


def dump_segment(name, path=None):
    for seg_ea in idautils.Segments():
        seg = ida_segment.getseg(seg_ea)
        if seg and ida_segment.get_segm_name(seg) == name:
            return dump(seg.start_ea, seg.end_ea - seg.start_ea, path)
    print("No segment named %r." % name)
    return None


if __name__ == "__main__":
    if START is not None and SIZE is not None:
        dump(START, SIZE)
    else:
        print("Set START/SIZE at the top of the script, or call dump(start, size) / "
              "dump_segment(name) from the Output window.")
