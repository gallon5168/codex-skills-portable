---
name: tracealyzer
description: Trace execution (into or over calls) for N steps or until a condition, then analyze the recorded instruction log
allowed-tools: mcp__x64dbg__get_debugger_status, mcp__x64dbg__pause, mcp__x64dbg__trace_into, mcp__x64dbg__trace_over, mcp__x64dbg__eval_expression, mcp__x64dbg__get_symbol, mcp__x64dbg__disassemble, mcp__x64dbg__get_all_registers, mcp__x64dbg__set_comment, mcp__x64dbg__set_label, Read, Bash
---

# tracealyzer

Trace debuggee execution — stepping into or over calls — for a specified number of instructions or until a condition is met. The full instruction log is captured to a file and then analyzed.

## Instructions

Follow these steps exactly:

### 0. Confirm the tool names actually exist in this session

The tool names referenced throughout this skill (`mcp__x64dbg__trace_into`, `trace_over`, `get_debugger_status`, `get_symbol`, `get_all_registers`, etc.) assume a specific x64dbg MCP implementation. **Different x64dbg MCP servers expose different tool names and capabilities** — a connected server might use a different prefix (e.g. `mcp__x64dbg-mcp__*`) and may not expose batch trace-to-file functionality at all, only step-by-step primitives (`debug_step_into`, `debug_step_over`, `debug_get_state`, etc.).

**Before following any step below, check the actual tool list available in this session.** If the trace tools this skill depends on (`trace_into`/`trace_over` with `log_file` output, or equivalent) are not present, **do not attempt to emulate them by looping single-steps manually** — that burns one MCP round-trip per instruction and is impractical for anything beyond a few dozen instructions (e.g. tracing through a decrypt routine or obfuscated/junk-code region can be thousands of instructions). Tell the user this skill's required trace primitive is unavailable in the current MCP connection, and fall back to a process-internal tracer instead — Frida Stalker (`references/frida-win/`, see `references/frida-win/references/frida-docs/stalker.md`) records real executed instructions with zero MCP round-trips and is immune to junk-code/obfuscated-call-stack tricks.

### 1. Verify debugger connection

Call `mcp__x64dbg__get_debugger_status` to confirm the debugger is connected and a debuggee is loaded and **paused**. If it is running, call `mcp__x64dbg__pause`. If no debuggee is loaded, tell the user and stop.

### 2. Gather trace parameters

Ask the user for the following if not already provided:

- **Trace mode**: trace *into* calls or trace *over* calls (default: over)
- **Stop condition** — one of:
  - A maximum number of instructions (e.g. `1000`)
  - An x64dbg expression that stops when true (e.g. `cip == 0x7FF6A0001000`, `rax != 0`)
  - Both (whichever triggers first)

If the user provides a symbol or address for the stop condition, resolve it with `mcp__x64dbg__eval_expression` and build the `break_condition` expression (e.g. `cip == <resolved_addr>`).

When the user only specifies a step count N and no explicit break condition, use break_condition `0` (never true — the trace runs until max_steps is hit).

### 3. Capture starting context

Call `mcp__x64dbg__get_all_registers` and `mcp__x64dbg__disassemble` at the current instruction pointer to record the starting state. Note the starting address.

### 4. Run the trace

Prepare the output log path: `./traces/trace_<timestamp>.log` (create the `traces` directory if it doesn't exist via `Bash`).

Call the appropriate trace tool (`mcp__x64dbg__trace_into` or `mcp__x64dbg__trace_over`) with:

| Parameter | Value |
|-----------|-------|
| `break_condition` | The user's condition, or `0` if only a step count was given |
| `max_steps` | The user's step count, or `50000` if only a condition was given |
| `log_text` | `{p:cip} {i:cip} | Label={label@cip} Comment={comment@cip}` |
| `log_file` | The output log path from above |
| `wait_timeout` | Scale with max_steps — use `max(60, max_steps // 500)` seconds |

### 5. Read and analyze the trace log

Read the trace log file. The log contains one line per executed instruction in the format:

```
<address> <disassembly> | Label=<label> Comment=<comment>
```

*Ignore when Labels or Comments say `[Formatting Error]`, it just means there is no label or comment at that instruction.*

Analyze the trace and present a summary to the user:

- **Trace overview**: total instructions executed, start address → end address, trace mode used
- **Execution flow**: describe the high-level behavior — what the code did, which functions were called, loops observed, and notable control-flow patterns
- **Hot spots**: addresses or regions that appear most frequently (loops, repeated calls)
- **Key observations**: interesting register manipulations, memory accesses, syscalls, API calls, string operations, or anything else that stands out

Use `mcp__x64dbg__get_symbol` to resolve notable addresses to symbol names where possible.

If the trace log is very large (>2000 lines), read it in chunks and summarize progressively.

### 6. Follow-up actions

After presenting the summary, ask the user if they would like any follow-up actions such as:

- **Annotate**: add comments/labels in x64dbg at key addresses using `mcp__x64dbg__set_comment` / `mcp__x64dbg__set_label`
- **Deeper analysis**: re-trace a specific sub-region, or focus on a particular function
- **Deobfuscation**: identify and explain obfuscated patterns found in the trace
- **Export**: the trace log is already saved to disk at the path from step 4
