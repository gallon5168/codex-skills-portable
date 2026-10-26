"""
ida_triage.py — Recon pass over a binary loaded in IDA Pro.

Run this FIRST on any new sample. It orients you before you touch code: what the binary is, how
it's laid out, what capabilities its imports imply, what its strings reveal, and whether it shows
anti-analysis behavior. It only reads and reports — it changes nothing.

This is a defensive/analytical triage aid (the same inventory a malware analyst builds by hand).
Use it to understand a sample, not to operate one.

WHAT IT REPORTS
  - Metadata: input path, architecture, bitness, image base, entry points.
  - Segments with Shannon entropy (high entropy ~> 7.0 suggests packing/encryption/compression).
  - Imports grouped by module, with commonly-abused APIs highlighted for your attention.
  - Notable strings: URLs, IPs, paths, registry keys, and other interesting substrings.
  - Anti-analysis indicators present in the import table.

HOW TO RUN
  In IDA:    File > Script file... > ida_triage.py
  Via MCP:   paste into py_eval(code=...); it prints the report. Or call triage().
"""

import math
import re

try:
    import idautils
    import idaapi
    import idc
    import ida_segment
    import ida_bytes
    import ida_nalt
    import ida_entry
except ImportError:
    raise SystemExit("This script must be run inside IDA Pro (IDAPython).")

ENTROPY_SAMPLE_CAP = 1024 * 1024   # bytes per segment used for entropy (cap for huge segments)
ENTROPY_FLAG = 7.0                 # entropy at/above this is flagged
MAX_STRINGS_SHOWN = 60

# APIs worth a second look, grouped by what they tend to indicate. Presence is a prompt to
# investigate, not a verdict.
SUSPICIOUS_APIS = {
    "process/injection": [
        "VirtualAllocEx", "WriteProcessMemory", "CreateRemoteThread", "NtCreateThreadEx",
        "QueueUserAPC", "SetThreadContext", "GetThreadContext", "NtUnmapViewOfSection",
        "RtlCreateUserThread", "OpenProcess", "VirtualProtect", "VirtualProtectEx",
    ],
    "exec/loader": [
        "CreateProcess", "WinExec", "ShellExecute", "LoadLibrary", "GetProcAddress",
        "LdrLoadDll", "system", "execve", "fork", "dlopen", "dlsym",
    ],
    "networking": [
        "socket", "connect", "send", "recv", "WSAStartup", "InternetOpen", "InternetConnect",
        "HttpSendRequest", "URLDownloadToFile", "WinHttpOpen", "WinHttpConnect", "getaddrinfo",
        "gethostbyname", "bind", "listen", "accept",
    ],
    "crypto": [
        "CryptEncrypt", "CryptDecrypt", "CryptAcquireContext", "CryptGenKey", "BCryptEncrypt",
        "BCryptDecrypt", "CryptHashData", "CryptDeriveKey",
    ],
    "persistence/registry": [
        "RegSetValue", "RegCreateKey", "RegOpenKey", "CreateService", "StartService",
        "schtasks", "CopyFile", "MoveFile",
    ],
    "anti-analysis": [
        "IsDebuggerPresent", "CheckRemoteDebuggerPresent", "NtQueryInformationProcess",
        "OutputDebugString", "GetTickCount", "GetTickCount64", "QueryPerformanceCounter",
        "NtSetInformationThread", "CreateToolhelp32Snapshot", "Process32First", "Process32Next",
        "NtQuerySystemInformation", "GetAdaptersInfo", "Sleep", "SetUnhandledExceptionFilter",
    ],
}
ANTI_ANALYSIS = set(SUSPICIOUS_APIS["anti-analysis"])

# Patterns for interesting strings.
STR_PATTERNS = [
    ("url", re.compile(r"https?://", re.I)),
    ("ip", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
    ("unc/path", re.compile(r"(?:[A-Za-z]:\\|\\\\)[^\s\"]+")),
    ("registry", re.compile(r"\bHKEY_|\\\\?Software\\\\", re.I)),
    ("shell", re.compile(r"\b(cmd\.exe|powershell|/bin/sh|/bin/bash|rundll32|regsvr32)\b", re.I)),
    ("format", re.compile(r"%[sdxp]")),
]


def _inf():
    """Return a small dict of binary info, compatible across IDA 8.x and 9.x."""
    info = {}
    try:  # IDA <= 8.x
        s = idaapi.get_inf_structure()
        info["proc"] = s.procname
        info["is64"] = s.is_64bit()
        info["is32"] = s.is_32bit()
        info["min_ea"] = s.min_ea
        info["max_ea"] = s.max_ea
    except Exception:  # IDA 9.x
        import ida_ida
        info["proc"] = ida_ida.inf_get_procname()
        info["is64"] = ida_ida.inf_is_64bit()
        info["is32"] = bool(ida_ida.inf_is_32bit_exactly()) if hasattr(ida_ida, "inf_is_32bit_exactly") else (not ida_ida.inf_is_64bit())
        info["min_ea"] = ida_ida.inf_get_min_ea()
        info["max_ea"] = ida_ida.inf_get_max_ea()
    return info


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


def _perm_str(seg):
    p = seg.perm
    return "%s%s%s" % (
        "r" if p & ida_segment.SEGPERM_READ else "-",
        "w" if p & ida_segment.SEGPERM_WRITE else "-",
        "x" if p & ida_segment.SEGPERM_EXEC else "-",
    )


def _collect_imports():
    """Return {module: [names...]} and a flat set of all import names."""
    modules = {}
    all_names = set()
    qty = ida_nalt.get_import_module_qty()
    for i in range(qty):
        modname = ida_nalt.get_import_module_name(i) or "<unknown>"
        names = []

        def cb(ea, name, ordinal, _names=names):
            if name:
                _names.append(name)
            return True

        ida_nalt.enum_import_names(i, cb)
        modules[modname] = names
        all_names.update(names)
    return modules, all_names


def _match_suspicious(all_names):
    """Return {category: [matched api names]} by substring match (handles A/W/Ex suffixes)."""
    hits = {}
    lowered = [(n, n.lower()) for n in all_names]
    for cat, apis in SUSPICIOUS_APIS.items():
        found = set()
        for api in apis:
            al = api.lower()
            for orig, low in lowered:
                if al in low:
                    found.add(orig)
        if found:
            hits[cat] = sorted(found)
    return hits


def triage():
    info = _inf()
    print("=" * 64)
    print("TRIAGE REPORT")
    print("=" * 64)

    # --- metadata ---
    print("Input file:  %s" % (idaapi.get_input_file_path() or "<unknown>"))
    bits = "64-bit" if info.get("is64") else ("32-bit" if info.get("is32") else "16-bit?")
    print("Processor:   %s   (%s)" % (info.get("proc", "?"), bits))
    print("Image base:  0x%X" % idaapi.get_imagebase())
    print("Range:       0x%X - 0x%X" % (info.get("min_ea", 0), info.get("max_ea", 0)))

    n_ent = ida_entry.get_entry_qty()
    if n_ent:
        print("Entry points (%d):" % n_ent)
        for i in range(n_ent):
            ordn = ida_entry.get_entry_ordinal(i)
            ea = ida_entry.get_entry(ordn)
            nm = ida_entry.get_entry_name(ordn) or idc.get_name(ea) or ""
            print("  - 0x%X  %s" % (ea, nm))

    # --- segments + entropy ---
    print("\nSegments:")
    print("  %-12s %-5s %-18s %-7s %s" % ("name", "perm", "range", "size", "entropy"))
    for seg_ea in idautils.Segments():
        seg = ida_segment.getseg(seg_ea)
        if not seg:
            continue
        name = ida_segment.get_segm_name(seg) or "?"
        size = seg.end_ea - seg.start_ea
        sample = ida_bytes.get_bytes(seg.start_ea, min(size, ENTROPY_SAMPLE_CAP)) or b""
        ent = _shannon(sample)
        flag = "  <== HIGH (packed/encrypted?)" if ent >= ENTROPY_FLAG else ""
        print("  %-12s %-5s 0x%08X-0x%08X %-7d %.2f%s" %
              (name[:12], _perm_str(seg), seg.start_ea, seg.end_ea, size, ent, flag))

    # --- imports ---
    modules, all_names = _collect_imports()
    total_imports = sum(len(v) for v in modules.values())
    print("\nImports: %d across %d module(s)" % (total_imports, len(modules)))
    if total_imports == 0:
        print("  (none resolved — likely dynamic API resolution; look for LoadLibrary/")
        print("   GetProcAddress or hash-based resolvers)")
    else:
        for mod in sorted(modules):
            if modules[mod]:
                print("  %s: %d" % (mod, len(modules[mod])))

    hits = _match_suspicious(all_names)
    if hits:
        print("\nNotable APIs (investigate — presence is a prompt, not a verdict):")
        for cat in sorted(hits):
            print("  [%s] %s" % (cat, ", ".join(hits[cat])))

    present_anti = sorted(n for n in all_names if any(a.lower() in n.lower() for a in ANTI_ANALYSIS))
    if present_anti:
        print("\nAnti-analysis indicators present: %s" % ", ".join(present_anti))

    # --- strings ---
    interesting = []
    total_strings = 0
    for s in idautils.Strings():
        total_strings += 1
        try:
            text = str(s)
        except Exception:
            continue
        for label, rx in STR_PATTERNS:
            if rx.search(text):
                interesting.append((label, s.ea, text))
                break
    print("\nStrings: %d total, %d notable" % (total_strings, len(interesting)))
    for label, ea, text in interesting[:MAX_STRINGS_SHOWN]:
        shown = text if len(text) <= 100 else text[:97] + "..."
        print("  [%-9s] 0x%X  %s" % (label, ea, shown))
    if len(interesting) > MAX_STRINGS_SHOWN:
        print("  ... (%d more)" % (len(interesting) - MAX_STRINGS_SHOWN))

    print("=" * 64)


if __name__ == "__main__":
    triage()
