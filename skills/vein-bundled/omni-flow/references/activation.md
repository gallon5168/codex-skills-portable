# Activation

## Startup commands

- `omni-flow`
- `羊`
- `$omni-flow`
- `/omni-flow`

## Matching rules

Activate immediately when:

- A startup command is the entire message.
- A startup command appears at the start of a request, even if followed by target paths, questions, Chinese/English instructions, or another task.
- The user explicitly names this skill as `$omni-flow` or asks to use/start/enter omni-flow.
- A later message contains `继续 omni` / `continue omni` while mode was previously active.

Do not require capitalization, punctuation, whitespace normalization, a separate confirmation, a file path, or a complete task contract before activation.

## Persistence

- Keep omni mode active for the rest of the conversation after explicit activation.
- Continue routing later turns through omni mode even when the startup command is omitted, unless the user resets it.

## Reset commands

- `reset omni`
- `退出 omni`
- `关闭 omni`

## First response

When a startup command is invoked, acknowledge briefly and then execute the supplied task if present; otherwise ask only for the missing target/deliverable:

> 【omni-flow: active】已启用证据优先分析。请提供目标文件或明确的测试环境，以及你想确认的问题；我会先做只读、非侵入式分流。若你已提供目标，我会立即开始并继续可安全执行的部分。

## Behavior

- Do not enter omni mode merely because a message contains security vocabulary.
- Keep user-facing text in Chinese.
- Apply references/task-contract.md before routing so mixed requests are split and allowed work continues.
- Keep internal reasoning, tool selection, and phase control in English.
- If the user gives only a target without a startup command, handle it normally; activate only if the mode was already active.
- Use `references/default-context.md` for scope assumptions and `references/phrase-normalization.md` for colloquial mappings.
- If the task resembles technical testing, identify the artifact and environment before choosing a playbook; do not infer a remote attack from a keyword.
