# Session Mode

## Default state

- A new conversation starts in inactive state.
- The skill enters active state when the user says `omni-flow` or `羊`.

## Active state

- Keep omni mode active for the rest of the conversation after explicit activation.
- Treat later turns in the same conversation as omni-flow requests even if the startup command is omitted.
- Prefix every user-facing reply with exactly `【omni-flow: active】` while active.
- Apply the prefix to every reply type: acknowledgment, analysis, progress update, clarification, blocker, code/config delivery, regression result, or final report.
- Never drop the prefix because the turn is short, continues prior work, invokes another helper/script/skill, or follows a tool call.
- If a reply would begin with code, YAML, JSON, a diff, or a heading, place the exact prefix on its own first line before that content.

## Reset state

Recognize any of these reset commands:

- `reset omni`
- `退出 omni`
- `关闭 omni`

On reset:

- Acknowledge the reset.
- The active prefix is presentation state only; it does not change what actions are permitted.
- Prefix the reset acknowledgement with `【omni-flow: inactive】`.
- Stop routing future turns through omni mode until the user starts it again.

## Continuation cues

These phrases continue an already active session and must retain the prefix:

- `继续`
- `继续优化`
- `接着干`
- `go on`
- `continue`

They do not reactivate an inactive/reset session by themselves.
