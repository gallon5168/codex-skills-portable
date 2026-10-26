---
name: "sandbox-detection"
description: "Sandbox detection techniques to identify automated analysis environments like Cuckoo Sandbox, VMRay, and Joe Sandbox"
version: "1.0.0"
---

# Sandbox Detection

> 沙箱检测技术用于恶意软件和红队操作员识别代码何时在自动化分析环境中运行。通过检测沙箱特征，恶意代码可以延迟执行或拒绝运行，避免静态和动态分析。

## 概述

自动化分析被恶意软件研究人员和AV/EDR广泛使用。沙箱分析行为、网络流量和文件操作。通过检测沙箱环境，恶意软件可以：
- **拒绝运行**（逃避分析）
- **延迟恶意行为**（逃避基于时间的分析）
- **执行看似良性的代码**（避免检测）

### 常见沙箱

- **Cuckoo Sandbox** - 开源沙箱
- **VMRay** - 商业恶意软件分析器
- **Joe Sandbox** - 商业分析平台
- **Hybrid Analysis** - 在线沙箱
- **ANY.RUN** - 交互式在线沙箱
- **VMware/VirtualBox工作站** - 常用于分析

## 基于CPU的检测

### CPUID指令检查

使用CPUID检测虚拟化（Intel VT-x、AMD-V）。

```cpp
#include <intrin.h>

bool IsCPUVirtualized() {
    int registers[4];
    __cpuid(registers, 1); // 查询功能标志

    // 检查VMX位（ECX的第31位）
    if (registers[2] & (1 << 31)) {
        return true;  // 正在运行虚拟机
    }

    return false;
}
```

### CPUID虚拟机检查

```cpp
bool IsHypervisorPresent() {
    int registers[4];
    __cpuid(registers, 0x40000000); // 查询虚拟机监控程序供应商ID

    // 如果支持此叶节点，则存在虚拟机监控程序
    if (registers[0] >= 0x40000000) {
        char vendor[13];
        memcpy(vendor, &registers[1], 4);
        memcpy(vendor + 4, &registers[2], 4);
        memcpy(vendor + 8, &registers[3], 4);
        vendor[12] = '\0';

        printf("Hypervisor Vendor: %s\n", vendor);
        return true;
    }

    return false;
}
```

## 内存和硬件检测

### 内存大小检查

沙箱虚拟机通常内存有限（< 4GB）。

```cpp
bool IsLowMemory() {
    MEMORYSTATUSEX memInfo = {0};
    memInfo.dwLength = sizeof(memInfo);
    GlobalMemoryStatusEx(&memInfo);

    // < 4GB可能表示沙箱虚拟机
    if (memInfo.ullTotalPhys < (4ull << 30)) {
        return true;
    }

    return false;
}
```

### CPU核心数检查

```cpp
bool IsLowCpuCores() {
    SYSTEM_INFO sysInfo = {0};
    GetSystemInfo(&sysInfo);

    // < 2核心可能是轻量级虚拟机或沙箱
    if (sysInfo.dwNumberOfProcessors < 2) {
        return true;
    }

    return false;
}
```

### 磁盘大小检查

```cpp
bool IsLowDiskSpace() {
    ULARGE_INTEGER freeBytes, totalBytes;
    GetDiskFreeSpaceExW(L"C:\\", &freeBytes, &totalBytes, NULL);

    // < 40 GB可能是小型虚拟机
    if (totalBytes.QuadPart < (40ull << 30)) {
        return true;
    }

    return false;
}
```

## MAC地址检测

虚拟机供应商具有特定的MAC地址OUI（组织唯一标识符）。

```cpp
#include <iphlpapi.h>
#pragma comment(lib, "iphlpapi.lib")

bool IsVirtualMac() {
    PIP_ADAPTER_INFO adapterInfo = (PIP_ADAPTER_INFO)malloc(sizeof(IP_ADAPTER_INFO));
    ULONG len = sizeof(IP_ADAPTER_INFO);

    if (GetAdaptersInfo(adapterInfo, &len) == ERROR_BUFFER_OVERFLOW) {
        free(adapterInfo);
        adapterInfo = (PIP_ADAPTER_INFO)malloc(len);
    }

    if (GetAdaptersInfo(adapterInfo, &len) == NO_ERROR) {
        PIP_ADAPTER_INFO adapter = adapterInfo;
        while (adapter) {
            BYTE* mac = adapter->Address;

            // VirtualBox: 08:00:27
            if (mac[0] == 0x08 && mac[1] == 0x00 && mac[2] == 0x27) {
                free(adapterInfo);
                return true;
            }

            // VMware: 00:05:69, 00:0C:29, 00:1C:14, 00:50:56
            if (mac[0] == 0x00 && (mac[1] == 0x05 || mac[1] == 0x0C || mac[1] == 0x1C || mac[1] == 0x50)) {
                free(adapterInfo);
                return true;
            }

            // Hyper-V: 00:15:5D
            if (mac[0] == 0x00 && mac[1] == 0x15 && mac[2] == 0x5D) {
                free(adapterInfo);
                return true;
            }

            adapter = adapter->Next;
        }
    }

    free(adapterInfo);
    return false;
}
```

## 基于注册表的检测

检查虚拟化相关的注册表项。

### VMware注册表项

```cpp
bool IsVMwareRegistry() {
    HKEY hKey;
    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE,
                      "SYSTEM\\CurrentControlSet\\Services\\Disk\\Enum",
                      0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        char data[256];
        DWORD size = sizeof(data);
        if (RegQueryValueExA(hKey, "0", NULL, NULL, (LPBYTE)data, &size) == ERROR_SUCCESS) {
            if (strstr(data, "VMware") != NULL) {
                RegCloseKey(hKey);
                return true;
            }
        }
        RegCloseKey(hKey);
    }

    return false;
}
```

### VirtualBox注册表项

```cpp
bool IsVirtualBoxRegistry() {
    HKEY hKey;
    if (RegOpenKeyExA(HKEY_LOCAL_MACHINE,
                      "SOFTWARE\\Oracle\\VirtualBox Guest Additions",
                      0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        RegCloseKey(hKey);
        return true;  // 已安装VirtualBox增强功能
    }

    return false;
}
```

## 基于文件系统的检测

检查沙箱特定文件。

### 常见沙箱文件

```cpp
bool IsSandboxFilePresent() {
    const char* sandboxFiles[] = {
        "C:\\Program Files\\VMware\\",
        "C:\\Program Files\\Oracle\\VirtualBox Guest Additions\\",
        "C:\\Program Files (x86)\\VMware\\",
        "C:\\vboxshared\\",
        "C:\\windows\\System32\\drivers\\VBoxMouse.sys",
        "C:\\windows\\System32\\drivers\\VBoxGuest.sys"
    };

    for (int i = 0; i < sizeof(sandboxFiles) / sizeof(sandboxFiles[0]); i++) {
        DWORD attrs = GetFileAttributesA(sandboxFiles[i]);
        if (attrs != INVALID_FILE_ATTRIBUTES) {
            return true;
        }
    }

    return false;
}
```

## 基于进程的检测

查找沙箱特定进程。

```cpp
bool IsSandboxProcessRunning() {
    const char* sandboxProcesses[] = {
        "vmwaretray.exe",
        "vmtoolsd.exe",
        "vboxtray.exe",
        "vboxservice.exe",
        "vmusrvc.exe",
        "vmount2.exe",
        "python.exe",       // Cuckoo Python通常使用此进程
        "cuckoomon.exe",    // Cuckoo沙箱
        "vmsrvc.exe"        // VMware快照
    };

    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    PROCESSENTRY32 pe32 = {0};
    pe32.dwSize = sizeof(PROCESSENTRY32);

    if (Process32First(hSnapshot, &pe32)) {
        do {
            char* processName = pe32.szExeFile;
            for (int i = 0; i < sizeof(sandboxProcesses) / sizeof(sandboxProcesses[0]); i++) {
                if (strcmp(processName, sandboxProcesses[i]) == 0) {
                    CloseHandle(hSnapshot);
                    return true;
                }
            }
        } while (Process32Next(hSnapshot, &pe32));
    }

    CloseHandle(hSnapshot);
    return false;
}
```

## 用户交互检测

沙箱在分析过程中通常没有用户交互。

### 鼠标移动检测

```cpp
bool IsMouseMoving() {
    POINT pos1, pos2;
    GetCursorPos(&pos1);

    // 等待30秒
    Sleep(30000);

    GetCursorPos(&pos2);

    // 如果鼠标没有移动，可能没有用户交互
    if (pos1.x == pos2.x && pos1.y == pos2.y) {
        return false;  // 无鼠标移动
    }

    return true;  // 鼠标已移动
}
```

### 活动窗口检查

```cpp
int GetUserSessions() {
    DWORD sessions = 0;
    if (WTSGetActiveConsoleSessionId() != 0xFFFFFFFF) {
        sessions++;
    }

    return sessions;
}
```

## 基于时间的检测

### 时间加速检查

沙箱环境通常通过加速时间来加快执行速度。

```cpp
bool IsTimeAccelerated() {
    DWORD start = GetTickCount();

    // 睡眠5秒
    Sleep(5000);

    DWORD end = GetTickCount();

    // 差异应 >= 5000 ms
    if ((end - start) < 5000) {
        return true;  // 时间被加速
    }

    return false;
}
```

### 系统启动时间检查

```cpp
bool IsRecentlyBooted() {
    DWORD upTime = GetTickCount(); // 毫秒
    DWORD upTimeSeconds = upTime / 1000;
    DWORD upTimeMinutes = upTimeSeconds / 60;

    // 如果系统启动不到10分钟，可能是新虚拟机
    if (upTimeMinutes < 10) {
        return true;
    }

    return false;
}
```

## 高级检测

### CPU温度检查

物理CPU有温度传感器；虚拟机可能返回无效数据。

### BIOS检查

```cpp
bool IsVirtualBios() {
    // 通过WMI或注册表查询BIOS信息
    // 在BIOS字符串中查找"VMware"、"VirtualBox"
    return false;  // 此处未实现
}
```

## 综合检测示例

```cpp
bool IsInSandbox() {
    int sandboxScore = 0;

    // CPU检查
    if (IsCPUVirtualized()) sandboxScore += 2;
    if (IsHypervisorPresent()) sandboxScore += 2;

    // 硬件检查
    if (IsLowMemory()) sandboxScore += 1;
    if (IsLowCpuCores()) sandboxScore += 1;

    // 网络检查
    if (IsVirtualMac()) sandboxScore += 2;

    // 系统检查
    if (IsVMwareRegistry()) sandboxScore += 2;
    if (IsVirtualBoxRegistry()) sandboxScore += 2;
    if (IsSandboxFilePresent()) sandboxScore += 2;
    if (IsSandboxProcessRunning()) sandboxScore += 2;

    // 用户交互
    if (!IsMouseMoving()) sandboxScore += 1;

    // 时间
    if (IsTimeAccelerated()) sandboxScore += 2;
    if (IsRecentlyBooted()) sandboxScore += 1;

    // 阈值：如果分数 >= 5，可能在沙箱中
    return sandboxScore >= 5;
}
```

## 沙箱反检测对抗

现代沙箱实现：

- **用户交互模拟**：模拟鼠标移动和点击
- **时间保持**：不加速时间
- **硬件伪装**：隐藏虚拟化特征
- **注册表/文件隐藏**：隐藏沙箱特定文件和注册表项
- **随机化**：随机化MAC地址、系统属性等

### 最佳免杀实践

- 使用多种检测方法
- 结合时间延迟
- 优先使用环境独立检查（如用户交互）
- 考虑分析网络活动，而不仅仅是系统状态

## 参考资源

- [Al-Khaser](https://github.com/LordNoteworthy/al-khaser) - 全面的沙箱检测工具
- [Pafish](https://github.com/a0rtega/pafish) - 虚拟机检测工具
- [AntiVM](https://github.com/a0rtega/AntiVM) - 简单的虚拟机检测
- [PayloadsAllTheThings - Anti-Debugging](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Anti-Debugging.md)
- [Cuckoo Sandbox - Anti-VM Techniques](https://cuckoosandbox.org/)
