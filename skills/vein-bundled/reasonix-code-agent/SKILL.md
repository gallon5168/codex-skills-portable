---
name: reasonix-code-agent
description: Reasonix — DeepSeek 原生 AI 编程代理。支持交互式编码、项目搜索/编辑、子代理委派(4并发)、HTTP+SSE/ACP协议、MCP工具集成、多模型切换(deeseek-flash/deepseek-pro/deepseek-reasoner)。effort=max 模式确保最强推理+全量代码搜索。用于渗透测试代码生成(exploit/POC/scanner/shellcode)、代码审计、项目重构。触发词：reasonix、代码生成、AI编程、deepseek coding、代码审计。
version: 1.0.0
---

# Reasonix — DeepSeek AI 编程代理

## 概述

Reasonix 是 DeepSeek 推出的原生 AI 编程代理（对标 Claude Code），可自主完成代码生成、项目分析、安全审计等任务。

## 安装位置

| 资产 | 路径 |
|------|------|
| 二进制 | `/root/CyberStrikeAI-1.7.9/tools/reasonix/reasonix` (9.7MB) |
| 全局链接 | `/usr/local/bin/reasonix` |
| 配置文件 | `~/.reasonix/config.toml` |
| 凭证文件 | `~/.reasonix/.env` |
| API Key | `sk-dufoojj***` (同 CyberStrikeAI DeepSeek Key) |
| Provider | `deepseek-pro` / `deepseek-flash` / `deepseek-reasoner` |

## 核心配置 (effort=MAX)

```toml
model = "deepseek-pro"
effort = "max"           # 最强推理: full tool calling + multi-round search
background_tasks = true   # 后台执行长时间任务
subagent_pool = 4         # 4 并发子代理
```

## 启动方式

```bash
# 方式1: 直接调用 (需先 export API Key)
export DEEPSEEK_API_KEY="sk-dufoojjrgkcvzszetdvmcikqbabveemhvrnucastdzebursy"
reasonix                           # 交互式会话
reasonix run "写一个SQL注入检测脚本"  # 一次性任务
reasonix -p "审计app.py的安全漏洞"   # 单轮问答

# 方式2: 一键启动脚本 (已封装)
/root/CyberStrikeAI-1.7.9/tools/reasonix/run.sh run "任务描述"

# 方式3: 全局命令
rx run "生成CVE-2024-xxxx的Python POC"
```

## 渗透测试代码生成场景

```bash
# POC/Exploit 生成
rx -p "Write a Python exploit for CVE-2022-0847 (DirtyPipe) targeting Linux kernel 5.8-5.16"

# 安全工具开发
rx run "Create a subdomain brute-force scanner in Go with DNS over HTTPS support"

# Shellcode 生成
rx -p "Generate x86_64 Linux reverse TCP shellcode in NASM format"

# 代码审计
rx run "Audit /path/to/webapp/ for SQL injection, XSS, and command injection vulnerabilities"

# WAF Bypass Payload
rx -p "Generate 20 SQL injection payloads that bypass ModSecurity CRS 3.x"

# 免杀 Loader
rx -p "Write a C++ Windows shellcode loader using indirect syscalls and API hashing"
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `reasonix` | 启动交互式会话 |
| `reasonix run "task"` | 执行一次性任务 |
| `reasonix -p "question"` | 单轮问答(不打工具) |
| `reasonix --model deepseek-pro` | 指定模型 |
| `reasonix --effort max` | 最强推理 |
| `reasonix review` | 代码审查 PR |
| `reasonix setup` | 重新配置 |
| `reasonix --help` | 完整帮助 |

## 在CyberStrikeAI攻击链中的定位

```
渗透测试发现漏洞
    │
    ├── DeepCode(deepcode_factory.py) → 快速代码生成
    │
    ├── Reasonix → 复杂多文件项目 + 代码审计 + 子代理并发
    │     (effort=max, 4 subagents)
    │
    └── Donut/VoidShell → 免杀打包
```

## 注意事项

1. `effort=max` 会触发多轮工具调用和子代理，适合复杂任务
2. `deepseek-pro` 适合代码生成，`deepseek-reasoner` 适合代码审计
3. Reasonix 的 `exec()` 环境受沙箱限制，需在真实 shell 中运行
4. API Key 与 CyberStrikeAI 共用，注意余额
