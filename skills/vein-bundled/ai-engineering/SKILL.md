---
name: ai-engineering
description: AI 工程技能套件 — 来自 Matt Pocock Skills for Real Engineers。涵盖 TDD 测试驱动开发、结构化诊断调试、代码架构优化、需求对齐访谈、原型构建、Issue 分诊、会话交接等核心工程能力。当需要系统化软件开发方法论、调试复杂Bug、改进代码架构、或创建新技能时使用。
---

# AI 工程技能套件 (Skills for Real Engineers)

> 来源: [Matt Pocock / skills](https://github.com/mattpocock/skills)  
> 核心理念: 小型、可组合、模型无关的工程技能——不做 vibe coding，做 real engineering。

## 技能清单

### 🔧 工程类 (engineering/)

| 技能 | 用途 | 触发词 |
|------|------|--------|
| **diagnose** | 6阶段结构化调试循环：复现→缩小→假设→探测→修复→回归测试 | 调试、bug、报错、性能问题 |
| **grill-with-docs** | 需求对齐访谈+领域术语精炼+CONTEXT.md/ADR自动更新 | 需求评审、方案讨论、架构对齐 |
| **improve-codebase-architecture** | 代码架构深度优化：发现浅模块→深化→提升可测试性与AI可导航性 | 重构、架构改进、模块深化 |
| **tdd** | 红-绿-重构循环，纵向切片式测试驱动开发 | TDD、测试驱动、单元测试 |
| **triage** | Issue分诊状态机：按角色流转处理 | Issue管理、Bug分诊 |
| **zoom-out** | 让AI放大视角，从系统整体理解代码 | 代码理解、系统概览 |
| **prototype** | 构建可丢弃原型验证设计（终端/UI双模式） | 原型、验证设计 |

### ⚡ 生产力 (productivity/)

| 技能 | 用途 | 触发词 |
|------|------|--------|
| **caveman** | 超压缩通信模式，砍掉~75% tokens | 长对话、省token |
| **grill-me** | 无文档版需求对齐访谈 | 方案讨论、设计评审 |
| **handoff** | 会话压缩为交接文档 | 会话交接、任务转交 |
| **write-a-skill** | 按规范创建新技能 | 创建技能、写skill |

### 🛠 杂项 (misc/)

| 技能 | 用途 | 触发词 |
|------|------|--------|
| **git-guardrails** | 设置Git危险命令拦截钩子 | Git安全、pre-commit |

## 使用方法

每个技能通过 `skill` 工具加载：

```
skill: "ai-engineering:diagnose"
skill: "ai-engineering:tdd"
skill: "ai-engineering:handoff"
```

## 核心设计模式（从该仓库学到的最佳实践）

1. **`<what-to-do>` + `<supporting-info>` 分离**：指令与背景知识分开，降低认知负荷
2. **渐进式披露**：主文件<100行，详细内容链到参考文件
3. **检查清单驱动**：每阶段有 `[ ]` 可勾选验证项
4. **领域语言一致性**：用项目自己的术语（CONTEXT.md）而非通用词
5. **反馈环优先**：任何调试/开发先建立快速可验证的反馈信号
