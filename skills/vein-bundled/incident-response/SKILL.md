---
name: incident-response
description: 安全事件响应深度专业技能：APT追踪与溯源、恶意样本分析、内存取证、日志关联分析、攻击链重建、从告警到溯源完整响应链
version: 2.0.0
---

# 安全事件响应深度技能

## 概述

安全事件响应是安全运营的核心能力。本技能系统化覆盖**告警分析→事件确认→现场取证→攻击链重建→溯源追踪→修复加固→复盘报告**完整响应链，涵盖APT对抗、内存取证、恶意样本分析等高级技术。

## 一、事件分级与优先级

### 1.1 事件分级矩阵

| 级别 | 场景 | 响应时效 |
|------|------|---------|
| P0-紧急 | 域控被控/核心数据泄露/勒索病毒 | 15分钟内响应 |
| P1-严重 | Webshell/权限提升/横向移动 | 1小时内响应 |
| P2-高 | 单主机入侵/凭据泄露 | 4小时内响应 |
| P3-中 | 弱口令/异常登录/可疑流量 | 24小时内响应 |
| P4-低 | 信息泄露/配置缺陷 | 72小时内响应 |

### 1.2 初步研判
```
1. 告警来源：WAF/IDS/HIDS/SIEM/蜜罐/用户报告
2. 影响范围：单主机/子网/全域/数据
3. 攻击阶段：侦察/利用/安装/C2/目标达成
4. 是否活跃：攻击者是否仍在系统中
5. 业务影响：业务中断风险/数据泄露规模
```

## 二、现场取证

### 2.1 Windows取证
```bash
# 易失性数据（按优先级采集）
# 1. 内存dump
winpmem /acquire RAMDump.raw
DumpIt.exe

# 2. 网络连接
netstat -ano > netstat.txt
Get-NetTCPConnection | Export-Csv connections.csv

# 3. 进程信息
tasklist /svc /v > processes.txt
wmic process get ProcessId,Name,ExecutablePath,CommandLine > wmic_process.txt

# 4. 网络连接+进程关联
netstat -anob > net_process.txt

# 5. 服务与计划任务
sc query type= service state= all > services.txt
schtasks /query /fo LIST /v > scheduled_tasks.txt

# 6. 注册表
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
reg query HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run

# 7. 用户与登录
net user > users.txt
net localgroup administrators > admins.txt
wevtutil qe Security /q:"*[System[EventID=4624]]" /c:100 /f:text > logins.txt

# 8. 文件时间线
# 最近修改的文件
forfiles /P C:\ /S /D +2026-06-27 /C "cmd /c echo @path @fdate @ftime" > recent_files.txt
```

### 2.2 Linux取证
```bash
# 易失性数据
# 1. 内存
cat /proc/meminfo
# LiME内核模块采集完整内存

# 2. 网络连接
ss -antup > connections.txt
netstat -antup > netstat.txt

# 3. 进程
ps auxef > processes.txt
ls -la /proc/*/exe 2>/dev/null > proc_exe.txt

# 4. 用户与登录
last -20 > last_login.txt
lastb -20 > failed_login.txt
cat /etc/passwd > passwd.txt
who > who.txt

# 5. 计划任务
crontab -l > crontab.txt
cat /etc/crontab >> crontab.txt
ls -la /etc/cron.* >> crontab.txt

# 6. 启动项
systemctl list-unit-files --type=service > services.txt
cat /etc/init.d/* > init_scripts.txt

# 7. 日志
cp /var/log/auth.log ./
cp /var/log/syslog ./
cp /var/log/nginx/access.log ./

# 8. 文件系统时间线
find / -mtime -2 -type f -ls > recent_files.txt 2>/dev/null

# 9. SUID/Capabilities
find / -perm -4000 -type f -ls > suid.txt 2>/dev/null
getcap -r / > capabilities.txt 2>/dev/null

# 10. Rootkit检测
rkhunter --check --skip-keypress
chkrootkit
```

### 2.3 内存分析（Volatility）
```bash
# 系统信息
vol -f memdump.raw windows.info

# 进程列表
vol -f memdump.raw windows.pslist
vol -f memdump.raw windows.pstree
vol -f memdump.raw windows.psscan  # 检测隐藏进程

# 网络连接
vol -f memdump.raw windows.netscan

# DLL注入检测
vol -f memdump.raw windows.dlllist
vol -f memdump.raw windows.malfind  # 内存注入代码段

# 命令历史
vol -f memdump.raw windows.cmdline

# 文件提取
vol -f memdump.raw windows.filescan --pattern "password"
vol -f memdump.raw windows.dumpfiles --pid PID
```

## 三、攻击链重建（MITRE ATT&CK映射）

### 3.1 攻击阶段映射
```
初始访问(TA0001): 
  → 钓鱼邮件/漏洞利用/暴力破解/供应链

执行(TA0002):
  → PowerShell/CMD/WMI/脚本

持久化(TA0003):
  → 注册表/计划任务/服务/启动项/WMI事件

权限提升(TA0004):
  → 令牌操纵/CVE利用/Sudo滥用

防御规避(TA0005):
  → 进程注入/日志清除/AMSI绕过/Timestomping

凭据访问(TA0006):
  → LSASS转储/Kerberoast/密码喷洒

发现(TA0007):
  → 网络扫描/用户枚举/权限审计

横向移动(TA0008):
  → PTH/PTT/WMI/WinRM/RDP

收集(TA0009):
  → 文件收集/剪贴板/浏览器数据

数据外传(TA0010):
  → DNS/HTTP/ICMP隧道/云存储

影响(TA0040):
  → 数据加密/删除/篡改
```

## 四、恶意样本分析

### 4.1 静态分析
```bash
# 文件基础信息
file sample
strings sample | head -100
xxd sample | head -50
ssdeep sample  # 模糊Hash

# PE分析
pefile / pestudio
python -m pefile sample.exe

# 恶意文档
oletools（olevba/oleid）
python -m oletools.olevba sample.doc

# YARA规则匹配
yara -r rules/ sample
```

### 4.2 动态分析
```
沙箱环境：
- Cuckoo Sandbox（自动化）
- Any.Run（在线交互式）
- Joe Sandbox（在线）
- 本地VM（隔离网络）

监控项：
- 进程创建/注入
- 文件操作（创建/修改/删除）
- 注册表操作
- 网络通信（DNS/HTTP/TCP）
- 互斥量/管道
- 持久化机制
```

## 五、日志分析与关联

### 5.1 Windows日志关键EventID
| EventID | 事件 | 分析重点 |
|---------|------|---------|
| 4624 | 成功登录 | Logon Type 3/10（网络/远程） |
| 4625 | 失败登录 | 暴力破解检测 |
| 4672 | 特殊权限分配 | SeDebugPrivilege |
| 4688 | 进程创建 | 可疑命令行 |
| 4698 | 计划任务创建 | 持久化 |
| 7045 | 服务安装 | 后门服务 |
| 1102 | 日志清除 | 反取证 |
| 4776 | NTLM认证 | Pass The Hash |
| 4768/4769 | Kerberos票据 | 票据攻击 |

### 5.2 Linux日志分析
```bash
# 异常登录检测
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn

# 成功登录后源IP
grep "Accepted" /var/log/auth.log

# 权限提升
grep "sudo" /var/log/auth.log
grep "su:" /var/log/auth.log

# 命令历史
cat ~/.bash_history
cat ~/.zsh_history

# Web日志分析
# 异常请求检测
awk '$9 >= 400' access.log | head -100
# 可疑UA
awk -F'"' '{print $6}' access.log | sort | uniq -c | sort -rn
```

## 六、溯源追踪

### 6.1 IOC提取与共享
```
IOC类型：
- Hash（MD5/SHA256/SSDeep）
- IP/Domain/URL
- 文件名/路径
- 注册表键值
- 互斥量名称
- C2协议特征
- YARA规则
- 网络指纹（JA3/JA3S）

共享格式：STIX/TAXII、OpenIOC、MISP
```

### 6.2 攻击者画像
```
分析维度：
- 攻击时间规律（工作时区推断）
- 使用语言（代码注释/文件名/字符串）
- 工具特征（C2框架/工具链偏好）
- TTPs映射（MITRE ATT&CK Group匹配）
- 目标选择（行业/地域偏好）
```

## 七、工具链

```bash
# 取证
Autopsy/Sleuth Kit    # 磁盘取证
Volatility 3          # 内存分析
Bulk Extractor        # 批量数据提取
LogParser             # Windows日志分析

# 恶意样本
Cuckoo Sandbox        # 动态沙箱
Ghidra/IDA            # 逆向分析
YARA                  # 规则匹配
CyberChef             # 编解码分析

# 日志分析
ELK Stack             # 日志聚合
Splunk                # SIEM
Timesketch            # 时间线分析

# 响应编排
TheHive               # 事件管理平台
Cortex                # IOC分析
MISP                  # 威胁情报共享
GRR Rapid Response    # 远程取证
```

## 八、测试检查清单

- [ ] 事件确认与分级
- [ ] 易失性数据采集（内存→网络→进程→磁盘）
- [ ] 证据链完整性（Hash校验+时间戳+操作记录）
- [ ] 攻击链重建（MITRE ATT&CK映射）
- [ ] 恶意样本分析（静态+动态）
- [ ] 日志关联分析（多源日志交叉验证）
- [ ] IOC提取与威胁情报共享
- [ ] 根因分析与修复
- [ ] 复盘报告与改进措施
