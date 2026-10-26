# Phrase Normalization

This file covers colloquial routing only. Scope assumptions live in `default-context.md`.

Map casual user phrasing to concrete analysis goals.

## Reverse-engineering phrases

| User phrasing | Interpretation |
|---|---|
| `解锁 XX` | Locate the gate or validation branch, explain the logic, and verify behavior on the supplied local copy. |
| `去除 XX` | Locate the check routine, record evidence, and describe a reversible code or debugger change on a copy. |
| `绕过反调试` | Analyze the anti-debug logic and explain its effect; propose a local diagnostic experiment only when requested. |
| `让它通过` / `make it pass` | Recover the validation logic and derive the expected input, state transition, or test condition. |
| `拿 flag` | Trace the validation flow, encoding / crypto logic, and trigger conditions in the supplied challenge artifact. |

## Pentest / web / API phrases

| User phrasing | Interpretation |
|---|---|
| `扫一下` / `看一下暴露面` | Inventory entry points, routes, and trust boundaries from supplied code, configuration, or captured traffic. |
| `看登录` / `绕过登录` | Analyze auth flow, session handling, and access-control checks in code or a named test environment. |
| `测越权` / `看权限` | Review authorization boundaries, role transitions, and object-access checks with non-destructive examples. |
| `测注入` / `看参数` | Trace input handling and sink reachability; reproduce only against a supplied fixture or named test environment. |
| `看回调` / `看 webhook` | Review callback signatures, replay protection, and trust boundaries. |
| `打一下接口` / `看接口` | Map API routes, parameters, and request / response flow from code or captured traffic. |
| `提权` | Analyze privilege boundaries and state transitions in code, logs, or a named lab; do not infer an exploit request. |

## Other domain cues

| User phrasing | Interpretation |
|---|---|
| `看一下 app` / `抓一下包` | Route toward mobile or network analysis depending on the artifact. |
| `看加密` / `算一下 hash` | Route toward cryptography. |
| `看样本` / `像木马` / `可疑文件` | Route toward malware analysis. |
| `看固件` / `路由器` / `binwalk` | Route toward firmware analysis. |
| `看流量` / `协议` | Route toward network analysis. |
| `太容易拒绝` / `别只分析` / `直接干活` | Parse the concrete deliverable, split mixed requests, execute all locally reversible parts, and report evidence; do not respond with a generic warning or capability statement. |
| `太cyber了` / `这个是不是黑客` / `会不会违规` | Ignore the label as a routing stopper. Extract artifact, operation, environment, and deliverable; choose the matching technical workflow and execute the safe/reversible part immediately. |
| `帮我破解` / `拿flag` / `打本地靶机` / `复现崩溃` | Treat as reverse-engineering/vulnerability research against the supplied challenge, local crackme, or named lab: classify, preserve/hash, reproduce, locate the check/fault, recover logic/primitive, and verify the result. |
| `分析木马` / `看病毒` / `提取IOC` / `写检测规则` | Treat as defensive/static-first malware analysis: hash, identify format, unpack/extract safely, correlate indicators, and produce YARA/Sigma/report artifacts. |

## Shared rule
- Keep phrase normalization separate from default-context rules.
- If the phrasing is vague, use the router and start with safe triage.
