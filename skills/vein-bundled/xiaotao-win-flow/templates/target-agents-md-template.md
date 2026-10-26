<!--
  xiaotao-win-flow target anchor for Codex.
  Stage 0: after the target absolute path is known, copy this file to
  <target-dir>\AGENTS.md and fill the real values. Codex loads AGENTS.md
  files from the current project tree; when the session is outside the target
  directory, explicitly read this file before continuing.
  Keep the shell map and progress evidence-based. Detailed attempts belong in
  <target>-attempts.md. Do not overwrite an existing AGENTS.md; merge these
  sections into it and preserve its unrelated instructions.
-->

# 逆向工程会话锚点 — <目标名>

> **Codex 使用方式:**尽量在【本目标程序所在目录】启动任务,这样本文件会随项目指令自动加载。若当前工作目录不在目标目录,每次动作前显式读取本文件 + `<目标>-attempts.md`。
> **本文件不是技能本身。** 上下文压缩、断开或新任务后,先确认 `$xiaotao-win-flow` 已激活；否则显式调用 `$xiaotao-win-flow` 或读取技能目录中的 `SKILL.md`。

## ★★ 强制更新触发器(机械规则,不靠自觉)★★

> 下列任一事件发生,必须在同一轮更新本文件对应段 + attempts.md:
>
> | 触发事件 | 必更新 |
> |---|---|
> | 拿到任一 `[OK]` / `[X]` | 进度段 + attempts.md 追加带证据条目 |
> | 换方法层(静态↔动态、脱壳→hook、DLL→字节码…) | 当前阶段 + 已排除别重试 |
> | 确认/修正壳名·版本·打包方式·保护类型 | 壳分层图 |
> | 发现新授权门/校验点/退出点 | 已确认的授权门 + attempts.md |
> | 部署/替换/patch 产物 | attempts.md 补丁账 + 进度 |
> | 上下文压缩恢复 | 先读本文件 + attempts.md,再行动 |

## ★第一件事:确保 `$xiaotao-win-flow` 已激活

1. 判断本轮上下文里是否已有该技能的 `SKILL.md` / Fast path / 铁律。
2. 未激活时,显式调用 `$xiaotao-win-flow`,或读取 `<技能绝对路径>\SKILL.md`（按需再读 `references\rules.md`）。
3. 然后重读本文件 + `<目标>-attempts.md`,恢复壳分层图和进度。

## 铁律(压缩后不许飘)

- 以 `<技能目录>\references\rules.md` 为准,下面只列最容易忘的核心。
- 找到卡密/授权边界,由边界决定脱壳或 hook 的位置,不要绕开已确认的壳层。
- 带壳先搜该壳+版本的技法,再脱壳/调试;不要在未脱壳文件上做静态结论。
- 抓包需要用户启动拦截器、代理、目标并走一遍完整流程;回报结果后再继续,不要假设记录存在。
- 缺工具就停下,给出工具名和来源,由用户安装;不自动安装。
- GUI 工具(IDA/x64dbg/Reqable)和目标本身由用户手动打开/操作;助手只提供核实后的绝对路径和后续分析。
- 授权是多道串联防线;只有用户亲眼看到真实功能跑起来才记 `[OK]`。
- 每一步立即记入 `<目标>-attempts.md`,不删除被推翻的条目,追加 `[X]`/`[LOOP]` 与证据。

## 目标基本信息

- 目标绝对路径:
- **xiaotao-win-flow skill 绝对路径**: `<技能绝对路径>`
- 位数 / 分类(triage-router):
- 工作目录 / attempts 日志文件: `<目标目录>\<目标>-attempts.md`

## 壳分层图(scan.ps1 [P] 段结果)

| 模块(文件名) | 壳名 + 版本 | 状态 | 备注 |
|---|---|---|---|
| <exe 或 dll/pyd> |  | 未脱/已脱/脱壳中 |  |

- 无具名壳的模块:
- 已就该壳搜到的技法/工具:

## 当前进度

- 当前阶段:
- 已确认的授权门(位置 + 置信度 `[OK]/[WARN]/[X]`):
- 下一步:
- 未决/待验证:

## 已排除、别重试

-