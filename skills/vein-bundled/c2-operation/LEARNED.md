# 📖 从「Rshell Skills」学到的核心方法论

> 仓库: Rshell-Skills — AI Agent C2 Operations Handbook
> 核心理念: 把复杂API参考转化为Agent可执行的渐进式操作手册

---

## 一、技能设计亮点

### 1. 三层渐进式知识架构

```
L1: 核心流程 (90%场景)
  └─ 认证→客户端管理→命令执行→结果获取
  
L2: 高级操作 (后渗透深入)
  └─ 内存执行、凭据抓取、SOCKS5、文件操作
  
L3: 完整参考 (异常处理)
  └─ 69+ API路由、故障排查、架构理解
```

**效果**: Agent 根据场景自动选择合适的层级，不会一开始就被淹没在细节中。

### 2. API参考标准化格式

每个API端点都包含:
- HTTP 方法和路径
- 请求头要求
- 请求体/参数格式（JSON示例）
- 响应格式（JSON示例）
- 注意事项

```http
POST /api/client/shell/sendcommand
Authorization2: Bearer <JWT>
Content-Type: application/json

{ "uid": "<客户端UID>", "command": "shell whoami" }
```

### 3. 操作流程模板化

完整端到端工作流以编号步骤呈现:
```
1. POST /api/users/login → JWT
2. GET /api/client/clientslist → 确认在线
3. POST /api/client/shell/sendcommand → 发送命令
4. GET /api/client/shell/getshellcontent → 查看输出
5. POST /api/client/file/tree → 浏览目录
6. POST /api/client/file/download → 下载文件
7. POST /api/client/dumpbrowser → 抓取密码
8. GET /api/dumpbrowser/list/:uid → 查看结果
```

### 4. 故障排查内置

技能包含常见问题及解决方案:
- Token过期 → 重新登录
- 客户端离线 → 等待或检查
- 命令输出为空 → 异步轮询
- 长操作超时 → 300s限制说明
- 内存执行失败 → 编译选项检查

---

## 二、对 CyberStrikeAI 的启示

### 2.1 技能-工具映射

将 Rshell API 操作模式映射到 CyberStrikeAI C2 工具:

| Rshell 操作 | CyberStrikeAI c2_task type |
|-------------|---------------------------|
| shell whoami | `exec` / `shell` |
| screenshot | `screenshot` |
| cd + ls | `cd` + `ls` |
| download | `download` |
| upload | `upload` |
| getsystem | (特权 escalation 技能) |
| mimikatz | (凭据抓取模块) |
| inject | `load_assembly` |
| ps | `ps` |
| socks5 | `socks_start` |
| persist | `persist` |

### 2.2 操作手册设计原则

创建类似操作手册时应遵循:

1. **先给最小可行流程** — 让Agent知道"最快能做什么"
2. **再给完整参考** — 异常时有据可查
3. **每个端点配完整示例** — 不要只给参数说明，要给可复制的HTTP请求
4. **内嵌故障排查** — 常见问题不要放在附录，放在相关操作旁边
5. **状态字段精确说明** — "1"=在线, "2"=离线, "0"=初始状态，不要假设Agent理解

### 2.3 可扩展的技能模板

```markdown
---
name: <工具名>-operation
description: <工具名> 操作指南 — [一句话能力]。当[触发词]时使用。
---

# <工具名> 操作技能

## 快速开始 (L1)
[最小可行流程: 3-5步骤]

## 常用操作 (L2)
[10个最常用操作的请求/响应示例]

## 完整参考 (L3)
[所有API/功能的详细文档]

## 故障排查
[常见问题+解决方案]
```

---

## 三、技能目录结构

```
skills/c2-operation/
├── SKILL.md              # 自适应操作指南（L1+L2+映射）
├── RSHELL_SKILL.md       # 完整API参考（L3，69+路由）
├── RSHELL_README.md      # 原始仓库说明
└── LEARNED.md            # 本文档 — 设计方法论
```
