# 📖 从「顶级编程 Skill」仓库学到的核心方法论

> 仓库: Matt Pocock / Skills for Real Engineers
> 核心理念: 小型、可组合、模型无关的 AI Agent 技能设计

---

## 一、技能设计范式

### 1.1 YAML 前置元数据

```yaml
---
name: skill-name
description: Brief description. Use when [specific triggers].
argument-hint: "Optional: What will this session be used for?"
---
```

**关键**: `description` 是 Agent 决定加载哪个技能的唯一依据，必须包含：
- 技能提供的能力
- 具体触发词/场景（"Use when user says X / mentions Y"）
- ≤1024 字符

### 1.2 指令-背景分离模式

```markdown
<what-to-do>
[Agent 必须执行的指令，简洁明了]
</what-to-do>

<supporting-info>
[背景知识、参考规则、格式要求]
</supporting-info>
```

**效果**: Agent 先读指令（快速理解任务），需要时再查阅背景信息。

### 1.3 渐进式披露

```
skill-name/
├── SKILL.md           # 主指令（<100行）
├── REFERENCE.md       # 详细文档（按需加载）
├── EXAMPLES.md        # 使用示例
└── scripts/           # 工具脚本
    └── helper.sh
```

- 主文件保持简洁（≤100行）
- 详细内容链到独立文件
- 脚本用于确定性操作（节省 tokens + 提高可靠性）

---

## 二、核心工程原则

### 2.1 反馈环优先 (Feedback Loop First)

> "Build the right feedback loop, and the bug is 90% fixed."

**任何问题的解决第一步**: 建立快速、确定性、Agent可运行的通过/失败信号。

反馈环优先级：
1. 失败的测试 → 2. Curl/HTTP脚本 → 3. CLI调用 → 4. 浏览器脚本 → 5. 回放Trace → ... → 10. 人机协作脚本

反馈环质量标准：
- 速度：2秒 > 30秒 > 无环
- 信号清晰度：精确断言 > "没崩溃"
- 确定性：可复现 > 偶尔复现 > 不复现

### 2.2 纵向切片 > 横向切片

```
❌ 横向（错误）:
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

✅ 纵向（正确）:
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
```

每次只写一个测试+一个实现，根据上一轮学到的反馈调整下一轮。

### 2.3 领域语言统一 (Ubiquitous Language)

- 用项目自身的术语（CONTEXT.md）
- 不用通用词（"service"、"component"、"handler"）
- 好的术语可直接成为函数/变量/文件名
- 减少 Agent 的 token 消耗和认知负荷

### 2.4 深度模块 (Deep Modules)

- **深度** = 大量功能通过简单接口暴露
- **浅度** = 接口几乎和实现一样复杂
- **删除测试**: 想象删除模块，复杂度消失=浅度，复杂度分散到N个调用者=深度
- 目标是提升 **杠杆率**（调用者受益）和 **局部性**（维护者受益）

---

## 三、对安全测试的启示

### 3.1 反馈环映射

| 安全活动 | 反馈环 |
|----------|--------|
| 漏洞验证 | 构造确定性PoC→运行→确认(成功/失败) |
| Fuzzing | 自动化输入→观测崩溃→缩小复现 |
| 渗透测试 | 侦察→假设→验证→记录（类比诊断6阶段） |
| 代码审计 | 静态规则→发现→人工确认→报告 |

### 3.2 技能设计改造建议

将 `diagnose` 技能改造为 **安全漏洞诊断技能**:
- Phase 1: 建立PoC反馈环（可复现利用链）
- Phase 2: 确认漏洞真实存在
- Phase 3: 假设利用路径（3-5条）
- Phase 4: 逐条验证（单变量测试）
- Phase 5: 构造完整利用链 + 回归验证
- Phase 6: 清理痕迹 + 事后分析

将 `grill-with-docs` 改造为 **安全需求评审技能**:
- 访谈范围定义
- 威胁建模对齐
- 攻击面确认
- 输出威胁模型文档 + 安全ADR

将 `improve-codebase-architecture` 改造为 **安全架构加固技能**:
- 发现安全薄弱模块
- 提出纵深防御改进
- 验证改进后的可测试性（安全测试覆盖）

---

## 四、技能目录规范

### 4.1 分桶策略

```
skills/
├── engineering/    # 日常代码工作
├── productivity/   # 非代码工作流
├── misc/           # 偶尔使用
├── personal/       # 个人配置（不推广）
├── in-progress/    # 开发中的草稿
└── deprecated/     # 已废弃
```

### 4.2 文档要求

| 层级 | 文档 | 内容 |
|------|------|------|
| 仓库根 | README.md | 所有技能链接+一句话描述 |
| 分桶 | README.md | 桶内技能清单 |
| 技能 | SKILL.md | 技能指令（<100行） |
| 技能 | REFERENCE.md | 详细参考（可选） |

### 4.3 质量检查清单

- [ ] description 包含触发词（"Use when..."）
- [ ] SKILL.md 控制在 100 行以内
- [ ] 无时间敏感信息
- [ ] 术语一致性
- [ ] 包含具体示例
- [ ] 引用不超过一层深度

---

## 五、关键技能速查

| 场景 | 使用技能 |
|------|----------|
| 遇到复杂 Bug | `diagnose` → 6阶段结构化调试 |
| 开始新功能前 | `grill-with-docs` → 对齐需求+更新文档 |
| 写测试 | `tdd` → 红绿重构循环 |
| 代码越来越乱 | `improve-codebase-architecture` → 深化模块 |
| 需要理解陌生代码 | `zoom-out` → 系统视角 |
| 分解需求 | `to-issues` → 拆分为独立Issue |
| 创建新技能 | `write-a-skill` → 按规范创建 |
| 交接任务 | `handoff` → 压缩会话为文档 |
| Token 太多 | `caveman` → 压缩通信 ~75% |
