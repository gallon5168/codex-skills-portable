"""
function_capabilities.py — Rank functions by what their imported API calls imply.

A lightweight, IDA-native take on capability detection (in the spirit of Mandiant's capa). For
each user function it gathers which imported APIs it references, buckets them by behavior, and
ranks functions by how many behavior categories they touch. The function that talks to both the
network and crypto is usually where you want to start. Read-only.

HOW IT WORKS
  Imports are attributed to a function when that function references the import's IAT slot or
  calls a thunk that forwards to it (resolved via XrefsTo, so it's robust across direct calls,
  IAT calls, and j_ thunks).

HOW TO RUN
  In IDA:    File > Script file... > function_capabilities.py
  Via MCP:   paste into py_eval(code=...); it prints the ranking. Or call rank().
"""

from collections import defaultdict

try:
    import idautils
    import idc
    import ida_funcs
    import ida_nalt
except ImportError:
    raise SystemExit("This script must be run inside IDA Pro (IDAPython).")

TOP_N = 40  # how many functions to print

# Behavior taxonomy. Matched as case-insensitive substrings so A/W/Ex suffixes are handled.
CATEGORIES = {
    "net":        ["socket", "connect", "send", "recv", "WSAStartup", "InternetOpen",
                   "InternetConnect", "HttpSendRequest", "URLDownloadToFile", "WinHttp",
                   "getaddrinfo", "gethostbyname", "bind", "listen", "accept"],
    "crypto":     ["Crypt", "BCrypt", "Hash"],
    "inject":     ["VirtualAllocEx", "WriteProcessMemory", "CreateRemoteThread", "NtCreateThreadEx",
                   "QueueUserAPC", "SetThreadContext", "NtUnmapViewOfSection", "RtlCreateUserThread",
                   "VirtualProtect"],
    "exec/loader":["CreateProcess", "WinExec", "ShellExecute", "LoadLibrary", "GetProcAddress",
                   "LdrLoadDll", "system", "execve", "dlopen", "dlsym"],
    "fs":         ["CreateFile", "ReadFile", "WriteFile", "CopyFile", "MoveFile", "DeleteFile",
                   "FindFirstFile", "fopen", "open", "unlink"],
    "registry":   ["RegSetValue", "RegCreateKey", "RegOpenKey", "RegQueryValue", "RegDeleteKey"],
    "persist":    ["CreateService", "StartService", "schtasks", "RegSetValueEx"],
    "anti":       ["IsDebuggerPresent", "CheckRemoteDebuggerPresent", "NtQueryInformationProcess",
                   "OutputDebugString", "GetTickCount", "QueryPerformanceCounter",
                   "NtSetInformationThread", "CreateToolhelp32Snapshot", "Process32"],
}


def _thunk_target(func):
    try:
        res = ida_funcs.calc_thunk_func_target(func)
        if isinstance(res, tuple):
            return res[0]
        return res
    except Exception:
        for t in idautils.CodeRefsFrom(func.start_ea, False):
            return t
    return idc.BADADDR


def _collect_import_map():
    import_ea_to_name = {}
    qty = ida_nalt.get_import_module_qty()
    for i in range(qty):
        def cb(ea, name, ordinal):
            if name:
                import_ea_to_name[ea] = name
            return True
        ida_nalt.enum_import_names(i, cb)
    return import_ea_to_name


def _categorize(api):
    low = api.lower()
    cats = set()
    for cat, keys in CATEGORIES.items():
        if any(k.lower() in low for k in keys):
            cats.add(cat)
    return cats


def rank():
    import_ea_to_name = _collect_import_map()

    # thunks that forward to an import -> the import's name
    thunk_ea_to_name = {}
    for ea in idautils.Functions():
        f = ida_funcs.get_func(ea)
        if f and (f.flags & ida_funcs.FUNC_THUNK):
            tgt = _thunk_target(f)
            if tgt in import_ea_to_name:
                thunk_ea_to_name[f.start_ea] = import_ea_to_name[tgt]

    func_apis = defaultdict(set)

    def attribute(target_ea, api_name):
        for xref in idautils.XrefsTo(target_ea):
            cf = ida_funcs.get_func(xref.frm)
            if cf:
                func_apis[cf.start_ea].add(api_name)

    for ea, name in import_ea_to_name.items():
        attribute(ea, name)
    for tea, name in thunk_ea_to_name.items():
        attribute(tea, name)

    rows = []
    for fea, apis in func_apis.items():
        cats = set()
        for api in apis:
            cats |= _categorize(api)
        if not cats:
            continue
        rows.append((len(cats), len(apis), fea, sorted(cats), sorted(apis)))

    rows.sort(key=lambda r: (r[0], r[1]), reverse=True)

    print("=" * 64)
    print("FUNCTION CAPABILITIES (ranked by behavior categories touched)")
    print("=" * 64)
    if not rows:
        print("No functions reference categorized APIs (dynamic resolution? unresolved imports?).")
        print("=" * 64)
        return []

    for ncat, napi, fea, cats, apis in rows[:TOP_N]:
        print("\n%s (0x%X)  — %d categor%s" %
              (idc.get_func_name(fea), fea, ncat, "y" if ncat == 1 else "ies"))
        print("   categories: %s" % ", ".join(cats))
        print("   apis: %s" % ", ".join(apis))

    if rows:
        top = rows[0]
        print("\nStart here: %s (0x%X) — touches %s." %
              (idc.get_func_name(top[2]), top[2], ", ".join(top[3])))
    print("=" * 64)
    return rows


if __name__ == "__main__":
    rank()
