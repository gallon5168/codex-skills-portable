---
name: c2-operation
description: C2 框架操作手册 — 基于 Rshell C2 架构提炼的通用 C2 操作知识。涵盖认证鉴权、客户端管理、命令执行、文件操作、凭据抓取、浏览器密码提取、内存执行、SOCKS5代理、Web Delivery、植入端生成、交互式终端等完整后渗透操作链。当需要操作C2框架、管理植入端、执行后渗透任务时使用。
---

# C2 操作技能 — 通用后渗透操作指南

> 来源: [Rshell Skills](https://github.com/Rubby2001/Rshell-Skills)  
> 核心理念: AI Agent 即 C2 操作员 — 用自然语言驱动完整后渗透链

## 技能结构

本技能提供三层递进式知识：

| 层级 | 内容 | 适用场景 |
|------|------|----------|
| **L1: 核心流程** | 认证→客户端管理→命令执行→结果获取 | 日常操作 90% 场景 |
| **L2: 高级操作** | 内存执行、凭据抓取、SOCKS5、文件操作 | 后渗透深入阶段 |
| **L3: 完整参考** | 69+ API 路由、故障排查、架构理解 | 异常处理、定制操作 |

详见 [RSHELL_SKILL.md](RSHELL_SKILL.md) 获取完整 API 参考。

## L1: 核心操作流程

### 1. 认证与鉴权

```
POST /api/users/login {"username":"admin","password":"xxx"}
→ JWT Token (24h 有效期)
→ 后续请求: Authorization2: Bearer <JWT>
```

### 2. 客户端管理

```
GET  /api/client/clientslist              → 列出在线客户端
POST /api/client/shell/sendcommand        → 发送命令
GET  /api/client/shell/getshellcontent    → 轮询输出(3-5s间隔)
```

### 3. 命令类型

| 前缀 | 功能 |
|------|------|
| `shell ` | Shell命令执行 |
| `cd ` | 切换目录 |
| `ps` | 进程列表 |
| `download ` | 下载文件 |
| `upload ` | 上传文件 |
| `screenshot` | 截屏 |
| `getsystem` | Windows提权 |
| `mimikatz` | 凭证抓取 |
| `inject ` | 进程注入 |

## L2: 高级后渗透操作

### 内存执行（无文件落地）

- **Windows**: execute-assembly / inline-bin / shellcode-inject / inline-execute (BOF)
- **Linux**: tmp落地→chmod→执行→自动删除

### 凭据收集

- **浏览器密码**: Chrome/Edge/Firefox 密码+Cookie提取
- **LSASS抓取**: mimikatz 内存凭证
- **敏感文件搜索**: 自动扫描指定目录

### 横向移动

- **SOCKS5代理**: 通过植入端建立内网隧道
- **Web Delivery**: HTTP投递新植入端
- **正向连接**: 主动连接目标端口

## L3: 完整API参考

详见 [RSHELL_SKILL.md](RSHELL_SKILL.md) — 69个API路由的请求/响应格式和完整操作示例。

## 操作检查清单

每次C2操作前确认:
- [ ] JWT Token 有效（未过期）
- [ ] 目标客户端 Online 状态为 "1"
- [ ] 命令前缀正确（shell/cd/ps/download等）
- [ ] 长操作(>300s)使用异步模式+轮询
- [ ] 敏感操作后清理日志

## 与 CyberStrikeAI C2 工具映射

| Rshell API | CyberStrikeAI 工具 |
|------------|-------------------|
| 登录 | `c2_listener` (start) |
| 客户端列表 | `c2_session` (list) |
| 发送命令 | `c2_task` (exec/shell) |
| 文件浏览 | `c2_task` (ls/cd) |
| 文件下载 | `c2_task` (download) |
| 文件上传 | `c2_task` (upload) |
| 截屏 | `c2_task` (screenshot) |
| SOCKS5 | `c2_task` (socks_start) |
| 端口转发 | `c2_task` (port_fwd) |
| 植入端生成 | `c2_payload` (build/oneliner) |
| 持久化 | `c2_task` (persist) |
| Kill进程 | `c2_task` (kill_proc) |
