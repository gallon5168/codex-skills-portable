"""
re_progress.py — Measure reverse-engineering cleanup progress in an IDA database.

Operationalizes the "definition of done" from the ida-reverse-engineering skill: it tells you
how much of the database still looks untouched so you know what to work on and don't fool
yourself into thinking you're finished.

WHAT IT REPORTS
  - Functions: total, how many are still auto-named (sub_*, etc.), and the worst offenders.
    Library/thunk functions (usually FLIRT-identified) are reported separately, not counted
    against you.
  - Functions with no comment at all (a rough proxy for "undocumented").
  - DEEP mode (set DEEP = True): decompiles each function and counts default-named local
    variables (v1, a1, ...), listing the functions with the most. Slower on large binaries.

HOW TO RUN
  In IDA:        File > Script file... > re_progress.py
  Via MCP:       paste this whole file into py_eval(code=...), it prints a report.
                 Or call report() / report(deep=True) after pasting.

NOTE
  Decompiler comments are stored separately from function comments; this script's comment check
  looks at function (regular + repeatable) comments, so treat the "no comment" count as a guide,
  not gospel.
"""

import re

try:
    import idautils
    import ida_funcs
    import ida_bytes
    import idc
except ImportError:
    raise SystemExit("This script must be run inside IDA Pro (IDAPython).")

# --- configuration -----------------------------------------------------------
DEEP = False          # True = also decompile every function to count default-named variables
MAX_EXAMPLES = 25     # how many example names to print per category
PROGRESS_EVERY = 500  # progress ping cadence in DEEP mode

_DEFAULT_LVAR_RE = re.compile(r"^(v\d+|a\d+|arg_[0-9A-Fa-f]+|var_[0-9A-Fa-f]+)$")


def _is_default_func_name(ea):
    return ida_bytes.has_dummy_name(ida_bytes.get_flags(ea))


def _func_kind(func):
    """Return 'lib', 'thunk', or 'user'."""
    if func.flags & ida_funcs.FUNC_THUNK:
        return "thunk"
    if func.flags & ida_funcs.FUNC_LIB:
        return "lib"
    return "user"


def _has_comment(func):
    for rep in (False, True):
        c = ida_funcs.get_func_cmt(func, rep)
        if c and c.strip():
            return True
    return False


def _count_default_lvars(ea):
    """Decompile a function and count default-named local variables. Returns int or None."""
    try:
        import ida_hexrays
    except ImportError:
        return None
    try:
        cfunc = ida_hexrays.decompile(ea)
    except Exception:
        return None
    if cfunc is None:
        return None
    n = 0
    for lvar in cfunc.get_lvars():
        name = lvar.name or ""
        if _DEFAULT_LVAR_RE.match(name):
            n += 1
    return n


def report(deep=DEEP):
    user_total = 0
    user_default = 0
    user_nocmt = 0
    lib_total = 0
    thunk_total = 0
    default_examples = []
    nocmt_examples = []
    deep_offenders = []  # (count, name)

    funcs = list(idautils.Functions())
    for idx, ea in enumerate(funcs):
        func = ida_funcs.get_func(ea)
        if func is None:
            continue
        kind = _func_kind(func)
        name = idc.get_func_name(ea)

        if kind == "lib":
            lib_total += 1
            continue
        if kind == "thunk":
            thunk_total += 1
            continue

        user_total += 1
        if _is_default_func_name(ea):
            user_default += 1
            if len(default_examples) < MAX_EXAMPLES:
                default_examples.append("%s  (0x%X)" % (name, ea))
        if not _has_comment(func):
            user_nocmt += 1
            if len(nocmt_examples) < MAX_EXAMPLES:
                nocmt_examples.append("%s  (0x%X)" % (name, ea))

        if deep:
            c = _count_default_lvars(ea)
            if c:
                deep_offenders.append((c, "%s  (0x%X)" % (name, ea)))
            if PROGRESS_EVERY and (idx % PROGRESS_EVERY == 0) and idx:
                print("  ...decompiled %d/%d" % (idx, len(funcs)))

    named = user_total - user_default
    pct = (100.0 * named / user_total) if user_total else 0.0
    cmt_pct = (100.0 * (user_total - user_nocmt) / user_total) if user_total else 0.0

    print("=" * 60)
    print("RE CLEANUP PROGRESS")
    print("=" * 60)
    print("User functions:        %d" % user_total)
    print("  named (not sub_*):   %d  (%.1f%%)" % (named, pct))
    print("  still auto-named:    %d" % user_default)
    print("  with a comment:      %d  (%.1f%%)" % (user_total - user_nocmt, cmt_pct))
    print("Library functions:     %d  (FLIRT/known — not counted)" % lib_total)
    print("Thunk functions:       %d  (not counted)" % thunk_total)

    if default_examples:
        print("\nStill auto-named (first %d):" % len(default_examples))
        for s in default_examples:
            print("  - " + s)

    if nocmt_examples:
        print("\nNo function comment (first %d):" % len(nocmt_examples))
        for s in nocmt_examples:
            print("  - " + s)

    if deep:
        if deep_offenders:
            deep_offenders.sort(reverse=True)
            print("\nMost default-named variables (top %d):" % min(MAX_EXAMPLES, len(deep_offenders)))
            for cnt, s in deep_offenders[:MAX_EXAMPLES]:
                print("  - %3d  %s" % (cnt, s))
        else:
            print("\n(DEEP) No default-named variables found, or decompiler unavailable.")

    print("=" * 60)
    return {
        "user_functions": user_total,
        "named": named,
        "auto_named": user_default,
        "no_comment": user_nocmt,
        "library": lib_total,
        "thunks": thunk_total,
    }


if __name__ == "__main__":
    report(deep=DEEP)
