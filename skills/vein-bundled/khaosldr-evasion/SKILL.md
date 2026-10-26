---
name: khaosldr-evasion
description: KhaosLdr — Windows 高级 Shellcode 加载器与 EDR 规避框架。集成直接系统调用（Direct Syscalls）、硬件断点（HWBP）绕过、IPv4 混淆 Shellcode 解码、EVS XOR 字符串混淆、多层沙箱/VM 检测逃逸、PPID 父进程欺骗、Syscall 级休眠混淆、RC4 载荷加密、多模式进程注入 (Early Bird APC / NtCreateThreadEx)。触发词：KhaosLdr、shellcode loader、直接系统调用、HWBP绕过、EDR规避、Windows Loader、免杀加载器、syscall注入、PPID欺骗、沙箱逃逸、RC4 shellcode、IPv4混淆、EVS字符串加密、进程注入免杀、Sleep混淆、NtDelayExecution、NtAllocateVirtualMemory、NtProtectVirtualMemory、NtWriteVirtualMemory。
version: 1.0.0
source: KhaosLdr by 28Zaakypro | 信益安信息安全研究院 技能化适配
---

# KhaosLdr — Windows 高级 Shellcode 加载器与 EDR 规避框架

> 信益安信息安全研究院出品 | XinYiAn Security Research Institute
> 基于 KhaosLdr (by 28Zaakypro@proton.me) 深入分析并编写为可操作技能

## 概述

KhaosLdr 是一个模块化的 Windows Shellcode 加载器 / EDR 规避框架，专为红队行动设计。它通过**直接系统调用 (Direct Syscalls)** 完全绕过用户态 API Hook，并结合**多层规避策略**实现对现代 EDR/XDR/AV 的全面对抗。

### 核心能力一览

| 模块 | 能力 | OPSEC 评级 |
|------|------|-----------|
| `syscalls` | 直接内核系统调用（NtAllocateVirtualMemory / NtProtectVirtualMemory / NtWriteVirtualMemory / NtCreateThreadEx / NtDelayExecution 等） | ★★★★★ |
| `hwbp_bypass` | 硬件断点检测与清除 — 反 EDR Hook 检测 | ★★★★☆ |
| `evs` | XOR 字符串混淆引擎 — 100+ 个敏感字符串运行时解密，单函数 noinline 避免特征 | ★★★★★ |
| `sandbox_evasion` | 6 层沙箱/VM/调试器检测 — 评分机制 + 自动退出 | ★★★★☆ |
| `ppid_spoofing` | 父进程 PID 欺骗 — 通过 PROC_THREAD_ATTRIBUTE_PARENT_PROCESS | ★★★★☆ |
| `spoof_sleep` | NtDelayExecution syscall 替代 Sleep() — 阻止 EDR sleep hook | ★★★★☆ |
| `injection` | 多模式进程注入 — Early Bird APC / NtCreateThreadEx 远程线程 | ★★★★☆ |
| `crypto` | RC4 加密引擎 — 载荷加密与解密 | ★★★☆☆ |
| `ipv4` | IPv4 地址格式 Shellcode 混淆 — 非标准编码绕过静态特征 | ★★★★☆ |
| `obfuscation` | XOR 密钥混淆、随机休眠、自适应延迟 | ★★★☆☆ |

---

## 架构总览

```
KhaosLdr-main/
├── build.ps1              # PowerShell 构建脚本（MinGW 交叉编译）
├── loader_v3.c            # 主入口：编排所有模块的执行流程
└── modules/
    ├── syscalls.h          # 系统调用号表 + 间接 syscall 存根声明
    ├── syscalls.c          # 间接 syscall 实现（FreshyCalls 风格）
    ├── dosyscall.S         # x64 syscall 汇编存根（直接 syscall 指令）
    ├── hwbp_bypass.h       # 硬件断点绕过头文件
    ├── hwbp_bypass.c       # HWBP 检测 → 修改 DR0-DR3 → 删除 VEH
    ├── evs.h               # 加密字符串常量（EVS_KEY + 宏定义）
    ├── evs.c               # 字符串 XOR 解密函数（noinline 单例）
    ├── evs_strings.h       # 预计算的 XOR 加密字符串数组（100+ 条）
    ├── sandbox_evasion.h   # 沙箱逃逸结构体与函数声明
    ├── sandbox_evasion.c   # 6 层检测：VM/调试器/资源/运行时间/用户活动/进程数
    ├── ppid_spoofing.h     # PPID 欺骗结构体
    ├── ppid_spoofing.c     # 查找目标进程 PID → 属性列表 → CreateProcess
    ├── spoof_sleep.h       # Sleep 混淆头文件
    ├── spoof_sleep.c       # NtDelayExecution syscall 替代 WinAPI Sleep
    ├── injection.h         # 注入模块头文件
    ├── injection.c         # 多模式进程注入实现
    ├── crypto.h            # RC4 加密头文件
    ├── crypto.c            # RC4 加解密实现
    ├── ipv4.h              # IPv4 混淆头文件
    ├── ipv4.c              # IPv4 格式 Shellcode 解码
    ├── obfuscation.h       # 混淆工具头文件（含日志宏）
    └── obfuscation.c       # XOR 密钥混淆、随机/自适应休眠、字符串解密
```

### 主流程（loader_v3.c）

```
main()
  ├── 1. 沙箱检测 → CheckSandboxEnvironment()
  │     ├── CheckVirtualMachine()     # VMware/VBox/Hyper-V 注册表 + 驱动文件
  │     ├── CheckDebugger()           # PEB.BeingDebugged + NtQueryInformationProcess(DebugPort)
  │     ├── CheckSystemResources()    # CPU < 2 / RAM < 4GB / Disk C: < 80GB
  │     ├── CheckUptime()             # 启动时间 < 10 分钟 → 沙箱标志
  │     ├── CheckUserActivity()       # 用户目录 + 最后输入时间
  │     └── CheckProcessCount()       # 进程数 < 50 → 沙箱标志
  │     └── 评分 ≥ 30 或调试器存在 → exit(0)
  │
  ├── 2. EVS 初始化 → evs_init() → 解密所有敏感字符串
  │
  ├── 3. 反沙箱二次检查 → IsRunningInSandbox() / IsDebuggerActive()
  │
  ├── 4. 解析加密载荷
  │     ├── [IPv4模式] → 从 .ipv4 节读取 → ipv4_decode() → 得到加密 shellcode
  │     └── [嵌入模式] → 直接使用嵌入的 enc_payload[]
  │
  ├── 5. RC4 解密 → rc4_crypt() → 得到明文 shellcode → 清零密钥材料
  │
  ├── 6. 进程注入
  │     ├── [有目标进程] → 远程进程注入
  │     │   ├── NtOpenProcess → NtAllocateVirtualMemory(remote)
  │     │   ├── NtWriteVirtualMemory(remote) → 写入 shellcode
  │     │   ├── NtProtectVirtualMemory(remote, PAGE_EXECUTE_READ)
  │     │   └── NtCreateThreadEx(remote) → 执行
  │     └── [自注入] → 本地分配 + HWBP 绕过 → 创建线程执行
  │
  └── 7. 资源清理 → 清零内存 → 退出
```

---

## 核心模块深度解析

### 1. 直接系统调用 (Direct Syscalls)

**文件**: `modules/syscalls.c`, `modules/syscalls.h`, `modules/dosyscall.S`

这是 KhaosLdr 最核心的能力，完全绕过用户态 API Hook。

#### 实现原理

KhaosLdr 采用 **间接 syscall (Indirect Syscall)** 模式：

1. **从 ntdll.dll 读取 syscall 号** — 不硬编码 SSN（Syscall Service Number），避免跨版本兼容性问题
2. **汇编存根执行 syscall 指令** — 不调用 ntdll.dll 中的函数，直接跳转到内核
3. **干净调用栈** — 调用栈中不出现 ntdll 函数帧

```
传统调用路径（被EDR Hook拦截）:
  kernel32!CreateThread → ntdll!NtCreateThreadEx → [EDR Hook] → syscall → 内核

KhaosLdr 调用路径（绕过EDR Hook）:
  Loader → syscall_stub (ASM) → syscall → 内核
                  ↑
         直接执行 syscall 指令
```

#### 关键代码

**dosyscall.S** — x64 汇编存根（直接 syscall 指令）：
```asm
; x64 syscall stub: 参数已在 r10/rdx/r8/r9 + stack 中就绪
; SSN 在 eax 中传输
.global SysNtAllocateVirtualMemory
SysNtAllocateVirtualMemory:
    mov  r10, rcx           ; 第一个参数 → r10（syscall 约定）
    mov  eax, SSN           ; syscall 号
    syscall                  ; 执行系统调用
    ret

; 类似定义其他 syscall 存根...
```

**syscalls.c** — 间接 syscall + SSN 动态解析：
```c
// 从 ntdll.dll 中动态提取 syscall 号
DWORD GetSyscallNumber(LPVOID pFunction) {
    // ntdll 中每个 syscall 函数都以固定模式开始:
    // 4C 8B D1    mov r10, rcx
    // B8 XX XX XX XX mov eax, <SSN>
    // 读取第 5 个字节得到 SSN
    if (*(BYTE*)pFunction == 0x4C && *(BYTE*)(pFunction + 1) == 0x8B && 
        *(BYTE*)(pFunction + 2) == 0xD1) {
        return *(DWORD*)((BYTE*)pFunction + 4);
    }
    return 0;
}
```

**现有 syscall 列表**:
- `NtAllocateVirtualMemory` — 内存分配
- `NtProtectVirtualMemory` — 内存保护修改
- `NtWriteVirtualMemory` — 内存写入
- `NtCreateThreadEx` — 远程线程创建
- `NtOpenProcess` — 进程打开
- `NtDelayExecution` — 延迟执行（替代 Sleep）
- `NtClose` — 句柄关闭
- `NtQueryInformationProcess` — 进程信息查询
- `NtQuerySystemInformation` — 系统信息查询

---

### 2. 硬件断点 (HWBP) 绕过

**文件**: `modules/hwbp_bypass.c`, `modules/hwbp_bypass.h`

EDR 常通过设置硬件断点 (DR0-DR3) 来监控关键 API 和 syscall 指令。KhaosLdr 通过以下方式绕过：

#### 检测逻辑
```
1. 注册 VEH (Vectored Exception Handler)
2. 触发硬件断点异常 (EXCEPTION_SINGLE_STEP)
3. 检查异常上下文中 DR6 寄存器
4. 如 DR6.BS=1 (硬件断点触发) → 确认 EDR 监控
```

#### 清除策略
```
1. 使用 SetThreadContext 清零 DR0-DR3 和 DR7
2. 移除 VEH 处理程序
3. 继续执行 — EDR 的硬件断点已被清除
```

#### OPSEC 备注
- 2026 年后的部分 EDR 已能检测 HWBP 清除行为
- 高风险环境建议结合 **间接 syscall + Stack Spoofing** 双保险

---

### 3. EVS 加密字符串引擎

**文件**: `modules/evs.c`, `modules/evs.h`, `modules/evs_strings.h`

KhaosLdr 的字符串混淆子系统 — 这是该项目最精致的工程特色之一。

#### 设计哲学

传统的 `DEFINE #XOR_STR("...")` 宏使用 `__attribute__((always_inline))` 强制内联，导致：
- 100+ 个相同模式的 XOR 解密循环散落在 `.text` 段
- ML-based AV 将此特征归类为 "shellcode packing" 签名

KhaosLdr 采用 **单函数 noinline** 策略：
```c
__attribute__((noinline))
void evs_dec(char *out, const unsigned char *enc, size_t n) {
    unsigned char k = EVS_KEY;
    for (size_t i = 0; i < n; i++)
        out[i] = (char)(enc[i] ^ k);
    out[n] = '\0';
}
```

- `.text` 段中**只有 1 个** XOR 循环副本
- 避免触发 "重复短循环 = shellcode 封装" 的启发式检测
- 所有字符串调用 `evs_dec()`，代码复用

#### 使用示例
```c
// 预加密字符串（编译时生成）
const unsigned char enc_ntdll[] = {0x2C, 0x36, 0x26, 0x2E, 0x2E, 0x6C, 0x26, 0x2E, 0x2E};

// 运行时解密
char ntdll[16];
evs_dec(ntdll, enc_ntdll, 9);  // → "ntdll.dll"
```

---
### 4. 沙箱与虚拟机逃逸

**文件**: `modules/sandbox_evasion.c`, `modules/sandbox_evasion.h`

6 层检测，金字塔式评分机制：

| 检查项 | 方法 | 检测阈值 | 评分权重 |
|--------|------|---------|---------|
| 虚拟机 | VMware/VBox/Hyper-V 注册表 + 驱动文件 (vmmouse.sys, vmhgfs.sys, VBoxMouse.sys, VBoxGuest.sys, vmci.sys) | 任一命中 | +30 |
| 调试器 | PEB.BeingDebugged + NtQueryInformationProcess(DebugPort=7) | 任一命中 | +40 |
| 系统资源 | CPU < 2 核 / RAM < 4GB / Disk C: < 80GB | 任一命中 | +20 |
| 系统运行时间 | GetTickCount64 < 10 分钟 | < 10min | +15 |
| 用户活动 | 无用户配置文件 / 无最后输入 | 0 用户 | +10 |
| 进程数量 | CreateToolhelp32Snapshot < 50 进程 | < 50 | +15 |

**退出判定**:
- `score >= 50` 或 `isDebugger == TRUE` → 立即退出
- `score >= 30` → 判定为疑似沙箱，继续执行但标记
- `score < 30` → 正常环境

#### 反制措施
- 所有注册表路径、驱动文件名、API 名称均使用 XOR 混淆
- 不使用 `IsDebuggerPresent()`（常见 IoC），直接读 PEB

---

### 5. PPID 父进程欺骗

**文件**: `modules/ppid_spoofing.c`, `modules/ppid_spoofing.h`

通常进程的父进程是启动它的进程。通过 `PROC_THREAD_ATTRIBUTE_PARENT_PROCESS` 可以将父 PID 伪造为任意进程（如 `explorer.exe`）。

#### 工作流程
```
1. FindProcessByName("explorer.exe") → 获取目标进程 PID
2. OpenProcess(PROCESS_CREATE_PROCESS) → 打开目标进程句柄
3. InitializeProcThreadAttributeList → 创建属性列表
4. UpdateProcThreadAttribute(PARENT_PROCESS, hParent) → 设置伪造父进程
5. CreateProcess(EXTENDED_STARTUPINFO_PRESENT | CREATE_NO_WINDOW) → 以伪造 PPID 启动
```

#### 应用场景
- 注入到 `explorer.exe` / `svchost.exe` 子进程，降低异常度
- 绕过基于父子进程关系异常的 EDR 检测规则

---

### 6. Spoof Sleep — Syscall 级休眠混淆

**文件**: `modules/spoof_sleep.c`, `modules/spoof_sleep.h`

EDR 常 Hook `kernel32!Sleep` 和 `ntdll!NtDelayExecution` 来检测恶意休眠模式（如 Ekko sleep obfuscation 的对策）。

KhaosLdr 直接通过 syscall 调用 `NtDelayExecution`：
```c
void SleepViaSyscall(DWORD milliseconds) {
    LARGE_INTEGER li;
    li.QuadPart = -(LONGLONG)milliseconds * 10000LL;
    SysNtDelayExecution(FALSE, &li);  // 直接 syscall
}
```

这样做的好处：
- **不经过任何用户态 API** — 完全绕过 Sleep Hook
- **调用栈干净** — 无 ntdll!NtDelayExecution 帧
- 可与 Ekko 等内存加密 sleep 技术组合

---

### 7. RC4 载荷加密

**文件**: `modules/crypto.c`, `modules/crypto.h`

使用 RC4 流密码加密/解密 Shellcode：

```c
void rc4_init(unsigned char *S, const unsigned char *key, size_t keylen);
void rc4_crypt(unsigned char *S, unsigned char *data, size_t len);
```

特点：
- 密钥材料使用后**立即清零**（`SecureZeroMemory` 或 `memset_s`）
- 配合 XOR 混淆的密钥，即使静态提取也无法直接解密
- 载荷嵌入在 `.ipv4` 节或 `enc_payload[]` 数组中

---

### 8. IPv4 Shellcode 混淆

**文件**: `modules/ipv4.c`, `modules/ipv4.h`

Shellcode 以 IPv4 地址列表形式存储：
```
.payload 节:
    192.168.1.1   →  [C0 A8 01 01] → 4 字节 shellcode
    10.0.0.1      →  [0A 00 00 01] → 4 字节 shellcode
    ...
```

运行时解码：
```c
// 解析 "192.168.1.1" → 4 个字节
// → x86: bswap 反转字节序 → 写入缓冲区
// → 循环直到解析完所有 IP
```

优点：
- Shellcode 以人类可读的 IP 地址形式存在，躲避基于二进制特征的静态检测
- 存放在独立 `.ipv4` 节中，PE 分析工具误判为配置数据

---

### 9. 进程注入引擎

**文件**: `modules/injection.c`, `modules/injection.h`

支持多种注入模式：

| 模式 | 描述 | OPSEC 等级 |
|------|------|-----------|
| **自注入** | 在当前进程中分配 RW → 写入 shellcode → RX → 创建线程 | ★★★☆☆ |
| **远程 NtCreateThreadEx** | 通过 syscall 在远程进程中分配/写入/保护/执行 | ★★★★☆ |
| **Early Bird APC** | 创建挂起进程 → 分配内存 → QueueUserAPC → ResumeThread | ★★★★★ |

所有操作均通过直接 syscall 完成，不调用 Win32 API。

---

## 构建系统

### build.ps1

PowerShell 构建脚本，使用 MinGW 交叉编译：

```powershell
# 编译配置
$CC = "x86_64-w64-mingw32-gcc"
$CFLAGS = "-O2 -s -ffunction-sections -fdata-sections -Wl,--gc-sections"
$DEFINES = "-DPRODUCTION"  # 生产模式（去除所有调试输出）

# 编译
& $CC $CFLAGS $DEFINES -o output.exe `
    loader_v3.c `
    modules/syscalls.c `
    modules/hwbp_bypass.c `
    modules/evs.c `
    modules/injection.c `
    modules/crypto.c `
    modules/ipv4.c `
    modules/obfuscation.c `
    modules/sandbox_evasion.c `
    modules/ppid_spoofing.c `
    modules/spoof_sleep.c `
    -lntdll -lws2_32
```

### 构建产物优化

- `-Os` 优化大小 → 减小特征面
- `-fno-asynchronous-unwind-tables` → 移除异常处理表
- `strip` → 移除符号表
- `PRODUCTION` 定义 → 移除所有 printf 调试输出

---

## 实战工作流

### 场景 1: C2 Beacon 投放（有 EDR 环境）

```
1. 生成原始 Shellcode
   └── msfvenom / CobaltStrike / Havoc 生成 raw shellcode

2. RC4 加密
   └── 生成随机 16 字节密钥 → RC4 加密 shellcode → 输出 enc_payload[]

3. 嵌入 KhaosLdr
   └── 将 enc_payload[] 和密钥写入 loader_v3.c
   └── 或生成 .ipv4 节（IPv4 混淆模式）

4. 构建
   └── build.ps1 -mode PRODUCTION -target svchost.exe

5. 投放执行
   └── 通过初始访问渠道投放 .exe
   └── KhaosLdr 自动完成：沙箱检测 → 解密 → PPID欺骗 → 注入 → 上线
```

### 场景 2: 自注入测试

```
1. 配置 loader_v3.c: 无目标进程 → 自注入模式
2. 启用 HWBP 绕过: cfg_hwbp_bypass = TRUE
3. 启用 Spoof Sleep: cfg_spoof_sleep = TRUE
4. 编译后运行 → shellcode 在当前进程中执行
```

### 场景 3: PPID 欺骗 + 远程注入

```
1. 目标进程: notepad.exe (有GUI，看起来更像正常进程)
2. 父进程伪装: explorer.exe (正常用户操作)
3. ppid_spoofing → 启动 notepad.exe (PPID=explorer.exe)
4. injection → NtCreateThreadEx 注入 shellcode
```

---

## OPSEC 注意事项

### 优势
- ✅ 全 syscall 调用链 — 无 Win32 API Hook 点
- ✅ HWBP 清除 — 对抗 EDR 硬件断点监控
- ✅ 100+ 字符串 XOR 混淆 — 单函数模式避免静态特征
- ✅ IPv4 格式混淆 — shellcode 伪装为 IP 地址列表
- ✅ 沙箱评分 > 30 → 退出 — 对抗自动分析环境
- ✅ PPID 欺骗 → 进程树看起来正常
- ✅ Spoof Sleep → 绕过 Sleep Hook 检测

### 弱点
- ⚠️ NtCreateThreadEx 远程线程注入（Kernel Callback 可检测）
- ⚠️ 直接 syscall 指令（高级 EDR 通过内核回调 + ETW 可关联）
- ⚠️ RW → RX 内存保护切换（Behavioral 检测点）
- ⚠️ 未实现 Stack Spoofing（调用栈可能溯源到 Loader）
- ⚠️ 未实现 NTDLL Unhooking（如果 EDR 修改了 ntdll.text 段）
- ⚠️ MinGW 编译产物有特定 PE 特征

### 强化建议
1. **Stack Spoofing**: 结合 `RetSpool` 或手工 `RopFrame` 伪造调用栈
2. **NTDLL Unhooking**: 从 `KnownDlls` 或磁盘重新映射干净的 ntdll.dll
3. **Threadless Injection**: 替换 `NtCreateThreadEx` → Work Item / Thread Pool 注入
4. **Sleep Obfuscation**: Spoof Sleep + Ekko (内存加密) 双保险
5. **ETW Bypass**: 结合 `EtwEventWrite` patch 或 `ntdll!EtwNotificationRegister`

---

## 快速参考：触发词映射

当用户提及以下关键词时，自动激活本技能：

| 关键词 | 对应模块 |
|--------|---------|
| KhaosLdr, shellcode loader, 免杀加载器 | 全局 |
| 直接系统调用, direct syscall, syscall注入 | syscalls |
| HWBP绕过, 硬件断点, hardware breakpoint | hwbp_bypass |
| EVS, XOR字符串加密, 字符串混淆 | evs |
| 沙箱逃逸, VM检测, 反沙箱, 反调试 | sandbox_evasion |
| PPID欺骗, 父进程伪造, parent PID spoof | ppid_spoofing |
| Sleep混淆, NtDelayExecution, spoof sleep | spoof_sleep |
| RC4 shellcode, 载荷加密 | crypto |
| IPv4混淆, IP地址shellcode | ipv4 |
| 进程注入免杀, APC注入, NtCreateThreadEx | injection |

---

## 文件路径参考

项目源代码位于服务器：
```
/root/CyberStrikeAI-1.7.1/chat_uploads/2026-07-15/e77c3fd2-c4dd-4a53-bad6-159c5055c1a0/KhaosLdr-main/KhaosLdr-main/
├── README.md
├── loader_v3.c
├── build.ps1
└── modules/
    ├── syscalls.h / syscalls.c / dosyscall.S
    ├── hwbp_bypass.h / hwbp_bypass.c
    ├── evs.h / evs.c / evs_strings.h
    ├── sandbox_evasion.h / sandbox_evasion.c
    ├── ppid_spoofing.h / ppid_spoofing.c
    ├── spoof_sleep.h / spoof_sleep.c
    ├── injection.h / injection.c
    ├── crypto.h / crypto.c
    ├── ipv4.h / ipv4.c
    └── obfuscation.h / obfuscation.c
```

## 技术组合模式（与 win-offensive-dev 配合）

### 模式 A: 隐蔽 C2 Beacon 投放
```
KhaosLdr + C2 Malleable Profile + CS Beacon
  ├── 使用 KhaosLdr 加载 C2 Shellcode
  ├── PPID Spoofing → explorer.exe 子进程
  ├── Direct Syscalls → 绕过 EDR Userland Hook
  ├── HWBP Bypass → 清除 EDR 硬件断点
  └── Spoof Sleep → 绕过 Sleep Hook
```

### 模式 B: 自注入 + 持久化
```
KhaosLdr (自注入) + win-offensive-dev/persistence
  ├── KhaosLdr 自注入模式执行 shellcode
  ├── shellcode 内实现持久化逻辑
  └── 使用 syscall 级别 API 操作注册表/计划任务
```

### 模式 C: 内网横向移动 Loader
```
KhaosLdr + Impacket/SMB 投放
  ├── 编译 KhaosLdr (目标: windows/amd64)
  ├── SMB/WMI 投放至目标主机
  ├── 远程执行 → 沙箱检测 → 注入 → 上线
  └── 每个节点使用不同 RC4 密钥 + 不同 PPID
```
