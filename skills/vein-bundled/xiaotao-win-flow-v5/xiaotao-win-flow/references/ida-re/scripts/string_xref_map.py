"""
string_xref_map.py — Map notable strings to the functions that reference them.

Implements the "follow the strings" workflow. ida_triage.py lists interesting strings; this one
takes them the next step and shows which functions use each, so you can jump straight to the code
that handles a URL, a registry key, a file path, or a format string. Read-only.

HOW TO RUN
  In IDA:    File > Script file... > string_xref_map.py
  Via MCP:   paste into py_eval(code=...); it prints the map. Or call string_map().
"""

import re
from collections import defaultdict

try:
    import idautils
    import idc
    import ida_funcs
except ImportError:
    raise SystemExit("This script must be run inside IDA Pro (IDAPython).")

# What counts as "notable". Mirrors ida_triage's classifier.
PATTERNS = [
    ("url", re.compile(r"https?://", re.I)),
    ("ip", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
    ("path", re.compile(r"(?:[A-Za-z]:\\|\\\\)[^\s\"]+")),
    ("registry", re.compile(r"\bHKEY_|\\\\?Software\\\\", re.I)),
    ("shell", re.compile(r"\b(cmd\.exe|powershell|/bin/sh|/bin/bash|rundll32|regsvr32)\b", re.I)),
    ("format", re.compile(r"%[sdxp]")),
    ("mutex/event", re.compile(r"\b(Global|Local)\\", re.I)),
]
MAX_STR_LEN = 90


def _classify(text):
    for label, rx in PATTERNS:
        if rx.search(text):
            return label
    return None


def string_map():
    func_to_strings = defaultdict(list)  # func_ea -> [(label, text)]
    orphan = []                          # notable strings with no direct xref

    for s in idautils.Strings():
        try:
            text = str(s)
        except Exception:
            continue
        label = _classify(text)
        if not label:
            continue
        shown = text if len(text) <= MAX_STR_LEN else text[:MAX_STR_LEN - 3] + "..."
        callers = set()
        for xref in idautils.XrefsTo(s.ea):
            f = ida_funcs.get_func(xref.frm)
            if f:
                callers.add(f.start_ea)
        if callers:
            for fea in callers:
                func_to_strings[fea].append((label, shown))
        else:
            orphan.append((label, s.ea, shown))

    print("=" * 64)
    print("STRING -> FUNCTION MAP")
    print("=" * 64)
    if not func_to_strings and not orphan:
        print("No notable strings found.")
        print("=" * 64)
        return {}

    # functions that reference the most notable strings first
    for fea in sorted(func_to_strings, key=lambda k: len(func_to_strings[k]), reverse=True):
        items = func_to_strings[fea]
        print("\n%s (0x%X)  — %d notable string(s)" %
              (idc.get_func_name(fea), fea, len(items)))
        for label, text in items:
            print("   [%-12s] %s" % (label, text))

    if orphan:
        print("\nNotable strings with no direct code xref (referenced indirectly?):")
        for label, ea, text in orphan:
            print("   [%-12s] 0x%X  %s" % (label, ea, text))
    print("=" * 64)
    return func_to_strings


if __name__ == "__main__":
    string_map()
